from django.shortcuts import render

# Create your views here.
import xml.dom.minidom
import re
from nltk.stem.porter import PorterStemmer
import math
import pandas as pd
import pymysql

total_document_number = 10000

def search_terms_with_position(term_list):
    with open('C:\\englishST.txt') as stopwords:
        stopword = stopwords.read()
    stopwords_list = stopword.split()
    term_list = term_list.split()
    docno_dic = []
    docno_matrix = []
    df = pd.DataFrame(columns=('word_name', 'doc_id', 'position'))
    lower_list = [word.lower() for word in term_list]
    term_without_sw = [word for word in lower_list if word not in stopwords_list]
    stemmer_porter = PorterStemmer()
    query_list = [stemmer_porter.stem(word) for word in term_without_sw]
    con_engine = pymysql.connect(host='localhost', user='root', password='111111', database='test', port=3306,
                                 charset='utf8')

    sql_ = "select * from word_position;"
    df_data = pd.read_sql(sql_, con_engine)
    # print(df_data)
    for query in query_list:
        df1 = df_data[df_data.word_name == query]
        df = df.append(df1)
    return df

def BM25(str):
    df = search_terms_with_position(str)
    docno_matrix = df.doc_id
    doc_list = []
    for list in docno_matrix:
        if not list in doc_list:
            doc_list.append(list)
    doc_list.sort()
    score_list = []
    con_engine = pymysql.connect(host='localhost', user='root', password='111111', database='test', port=3306,
                                 charset='utf8')

    sql_ = "select * from doc_length;"
    df_data = pd.read_sql(sql_, con_engine)
    L_mean = df_data.mean(axis=0)[0]
    for docno in doc_list:
        score = 0.
        data = df[df.doc_id == docno]
        docno_position = data.position.tolist()
        word_name = data.word_name.tolist()
        L = df_data[df_data.doc_id == docno].doc_length.iloc[0]

        for i in range(len(docno_position)):
            position = docno_position[i].split(',')

            score = score + (1 + math.log(len(position), 10)) * math.log(
                total_document_number / len(df[df.word_name == word_name[i]]), 10)
            score = score + math.log((total_document_number - len(df[df.word_name == word_name[i]]) + 0.5) / (
                        len(df[df.word_name == word_name[i]]) + 0.5), 10) * (
                                len(position) / (1.5 * (L / L_mean) + len(position) + 0.5))
            score = round(score, 4)
        score_list.append(score)
    score_dic = {key: value for key, value in zip(doc_list, score_list)}
    sorted_score_list = sorted(score_dic.items(), key=lambda x: x[1], reverse=True)
    # remove files ranked lower than 150
    if len(sorted_score_list) > 150:
        sorted_score_list = sorted_score_list[:150]
    print(sorted_score_list)


BM25('heterogen')
