import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer
import datetime
import json
import os
import django
import csv
import pandas as pd
from itertools import groupby

docList = []
file = open("dblp-ref-0.json", 'r', encoding='utf-8')
stop_file = open('stop.txt')
stop_words = stop_file.readlines()
stop_file.close()
stop_words = [w.strip() for w in stop_words]
def splite_sentence(title):
    doc_list = []
    if title is None:
        return []
    if title is not None:
        title_string = list(filter(str.isalnum, [''.join(list(g)) for k, g in
                                                 groupby(title, key=lambda x: x.isalpha() or x.isdigit())]))
        for index, word in enumerate(title_string):
            if word.isalnum():
                word = word.lower()
                title_string[index] = word
                if word not in stop_words:
                    doc_list.append(nltk.PorterStemmer().stem(word))
    return doc_list
count = 0
for line in file.readlines()[920000:1000000]:
    doc_list = []
    dic = json.loads(line)
    doc_list.append(dic.get('id'))
    title = dic.get('title')
    abstract = dic.get('abstract')
    doc_list.extend(splite_sentence(title))
    doc_list.extend(splite_sentence(abstract))
    docList.append(doc_list)
    count += 1
    print(count)
word_list = []
doc_id = []
docs_position = []
doc_idid = []
doc_length = []
from collections import defaultdict

for doc in docList:
    word_dict = defaultdict(list)
    doc_idid.append(doc[0])
    doc_length.append(len(doc) - 1)
    check = []
    for index, word in enumerate(doc[1:]):
        word_dict[word].append(str(index))
        #apple apple stem
        #check: apple, apple, stem
        #word_list: apple ,stem
        if word not in check:
            word_list.append(word)
            doc_id.append(doc[0])
        check.append(word)
    for value in word_dict.values():
        position_str = ','.join(value)
        docs_position.append(position_str)
csv_list2 = np.c_[np.array(word_list), np.array(doc_id), np.array(docs_position)]
with open('word_position92_100.csv', 'a', encoding='utf8', newline='') as f2:
    writer = csv.writer(f2)
    writer.writerows(csv_list2)
csv_list3 = np.c_[np.array(doc_idid), np.array(doc_length)]
with open('doc_length92_100.csv', 'a', encoding='utf8', newline='') as f3:
    writer = csv.writer(f3)
    writer.writerows(csv_list3)
print('Done!')
