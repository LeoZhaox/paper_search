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

total_document_number = 100000
import re


def search_terms_with_position(term_list):
    combine_list_fixed = []
    r = '[’!"#$%&\'()*+,./;<=>?@[\\]^_`{|}~\t。！，]+'
    term_list = re.sub(r, ' ', term_list)

    with open('stop.txt') as stopwords:
        stopword = stopwords.read()
    stopwords_list = stopword.split()
    term_list = term_list.split()
    df = pd.DataFrame(columns=('word_name', 'paper_id', 'position'))
    lower_list = [word.lower() for word in term_list]
    term_without_sw = [word for word in lower_list if word not in stopwords_list]
    stemmer_porter = PorterStemmer()
    query_list = [stemmer_porter.stem(word) for word in term_without_sw]
    # print(query_list)
    con_engine = pymysql.connect(host='localhost', user='root', password='ed2021', database='paper', port=3306,
                                 charset='utf8')
    query_list = ["'{}'".format(q) for q in query_list]
    query_string = '(' + ','.join(query_list) + ')';
    sql_ = "select * from paper_wordposition where word_name in {};".format(query_string);
    # ['001c8744-73c4-4b04-9364-22d31a10dbf1']
    df_data = pd.read_sql(sql_, con_engine)
    # print('after querying', query_list)
    return df_data


def TFIDF(str, return_number=100):
    df = search_terms_with_position(str)
    # print(df)
    score_dic = {}
    for index, row in df.iterrows():
        # print(row)
        # print(row['token'])
        df = int(row['frequency'])
        documents = row['tf_idf'].split(';')
        documents = documents[:-1]
        # print(documents)
        for doc in documents:
            # print(doc)
            id_len_tf_position = doc.split(':')
            # print(id_len_tf_position)
            id = id_len_tf_position[0][1:]
            tf = int(id_len_tf_position[2])

            if id not in score_dic.keys():
                score_dic[id] = (1 + math.log(tf, 10)) * math.log(total_document_number / df, 10)
            else:
                score_dic[id] = score_dic[id] + (1 + math.log(tf, 10)) * math.log(total_document_number / df, 10)
    sorted_score_list = sorted(score_dic.items(), key=lambda x: x[1], reverse=True)
    if len(sorted_score_list) > return_number:
        sorted_score_list = sorted_score_list[:return_number]
    paper_ids = [paper[0] for paper in sorted_score_list]
    # print(paper_ids)
    # print(len(paper_ids))
    paper_objects = Paper.objects.filter(id__in=paper_ids)[:return_number]
    # print(len(paper_objects))
    # print([p.id for p in paper_objects])
    return paper_objects
    # print(sorted_score_list)


if __name__ == '__main__':
    start = time.time()
    TFIDF('structure')
    end = time.time()
    print('BM25 spends', end - start)
