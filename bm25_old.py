from django.shortcuts import render
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paper_search.settings')
django.setup()
# Create your views here.
import xml.dom.minidom
import re
from nltk.stem.porter import PorterStemmer
import math
import pandas as pd
import pymysql
import re

from paper.models import Paper

total_document_number = 10000

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
    print(query_list)
    con_engine = pymysql.connect(host='localhost', user='root', password='ed2021', database='paper', port=3306,
                                 charset='utf8')
    query_list = ["'{}'".format(q) for q in query_list]
    query_string = '(' + ','.join(query_list) + ')';
    sql_ = "select * from paper_wordposition where word_name in {};".format(query_string);
    # ['001c8744-73c4-4b04-9364-22d31a10dbf1']
    df_data = pd.read_sql(sql_, con_engine)
    print('after querying', query_list)
    return df_data


def BM25(str, return_number=80):
    df = search_terms_with_position(str)
    docno_matrix = df.paper_id
    doc_list = []
    for list in docno_matrix:
        if not list in doc_list:
            doc_list.append(list)
    doc_list.sort()
    score_list = []
    con_engine = pymysql.connect(host='localhost', user='root', password='ed2021', database='paper', port=3306,
                                 charset='utf8')

    sql_ = "select * from paper_paperlength;"
    df_data = pd.read_sql(sql_, con_engine)
    L_mean = df_data.mean(axis=0)[0]
    for docno in doc_list:
        score = 0.
        data = df[df.paper_id == docno]

        docno_position = data.position.tolist()
        word_name = data.word_name.tolist()
        L = df_data[df_data.paper_id == docno].length.iloc[0]
        for i in range(len(docno_position)):
            position = docno_position[i].split(',')
            score += math.log((total_document_number - len(df[df.word_name == word_name[i]]) + 0.5) / (
                    len(df[df.word_name == word_name[i]]) + 0.5), 10) * (
                             len(position) / (1.5 * (L / L_mean) + len(position) + 0.5))
            score = round(score, 4)
        score_list.append(score)
    score_dic = {key: value for key, value in zip(doc_list, score_list)}
    sorted_score_list = sorted(score_dic.items(), key=lambda x: x[1], reverse=True)
    # remove files ranked lower than 150
    sorted_score_list = sorted_score_list[:return_number]
    paper_ids = [paper[0] for paper in sorted_score_list]
    print(paper_ids)
    print(len(paper_ids))
    paper_objects = Paper.objects.filter(id__in=paper_ids)
    print([p.id for p in paper_objects])
    return paper_objects

if __name__ == '__main__':
    BM25('heterogen')
