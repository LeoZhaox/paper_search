import django
import os
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paper_search.settings')
django.setup()
import pymysql
from nltk import PorterStemmer

from paper.models import Paper
import math
import pandas as pd

total_document_number = 10000
import re


def search_terms_with_position(term_list):
    combine_list_fixed = []
    r = '[’!"#$%&\'()*+,./;<=>?@[\\]^_`{|}~\t。！，]+'
    term_list = re.sub(r, ' ', term_list)

    with open('stop.txt') as stopwords:
        stopword = stopwords.read()
    stopwords_list = stopword.split()
    term_list = term_list.split()
    docno_dic = []
    docno_matrix = []
    df = pd.DataFrame(columns=('word_name', 'paper_id', 'position'))
    lower_list = [word.lower() for word in term_list]
    term_without_sw = [word for word in lower_list if word not in stopwords_list]
    stemmer_porter = PorterStemmer()
    query_list = [stemmer_porter.stem(word) for word in term_without_sw]
    print(query_list)
    con_engine = pymysql.connect(host='localhost', user='root', password='ed2021', database='paper', port=3306,
                                 charset='utf8')
    # select *
    # from paper_wordposition where
    # word_name in ('base', 'tool', 'includ', 'achiev', 'featur', 'featur', 'classifi', 'solv', 'utf-8', 'utf8');
    query_list = ["'{}'".format(q) for q in query_list]
    query_string = '(' + ','.join(query_list) + ')';
    print(query_string)
    sql_ = "select * from paper_wordposition where word_name in {};".format(query_string);
    print(sql_)
    # ['001c8744-73c4-4b04-9364-22d31a10dbf1']
    df_data = pd.read_sql(sql_, con_engine)
    print('after querying', query_list)
    # print(df_data.head())
    return df_data


def TFIDF(str, return_number=80):
    df = search_terms_with_position(str)
    docno_matrix = df.paper_id
    doc_list = []
    for list in docno_matrix:
        if not list in doc_list:
            doc_list.append(list)
    doc_list.sort()
    score_list = []
    for docno in doc_list:
        score = 0.
        data = df[df.paper_id == docno]
        docno_position = data.position.tolist()
        word_name = data.word_name.tolist()
        for i in range(len(docno_position)):
            position = docno_position[i].split(',')

            score = score + (1 + math.log(len(position), 10)) * math.log(
                total_document_number / len(df[df.word_name == word_name[i]]), 10)
            score = round(score, 4)
        score_list.append(score)
    score_dic = {key: value for key, value in zip(doc_list, score_list)}
    sorted_score_list = sorted(score_dic.items(), key=lambda x: x[1], reverse=True)
    paper_ids = [paper[0] for paper in sorted_score_list]
    # print(paper_ids)
    # print(len(paper_ids))
    paper_objects = Paper.objects.filter(id__in=paper_ids)[:return_number]
    print(len(paper_objects))
    print([p.id for p in paper_objects])
    return paper_objects


if __name__ == '__main__':
    start = time.time()
    TFIDF('structure, structures include achieve feature, features, classify solve utf-8 utf8')
    end = time.time()
    print('spend', end - start)
