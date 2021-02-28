#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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

for line in file.readlines()[:10]:
    doc_list = []
    dic = json.loads(line)
    doc_list.append(dic.get('id'))
    title = dic.get('title')
    if title!=None:
        title_string = list(filter(str.isalnum, [''.join(list(g)) for k, g in groupby(title, key=lambda x: x.isalpha() or x.isdigit())]))
        for a in range(len(title_string)):
            if title_string[a].isalnum()==True:
                title_string[a] = title_string[a].lower()
                file = open('stop.txt')
                if title_string[a]+'\n' not in list(file):
                    doc_list.append(nltk.PorterStemmer().stem(title_string[a]))
                    file.close()
                    
    abstract = dic.get('abstract')
    if abstract!=None:
        abstract_string = list(filter(str.isalnum,[''.join(list(g)) for k, g in groupby(abstract, key=lambda x: x.isalpha() or x.isdigit())]))
        for a in range(len(abstract_string)):
            if abstract_string[a].isalnum()==True:
                abstract_string[a] = abstract_string[a].lower()
                file = open('stop.txt')
                if abstract_string[a]+'\n' not in list(file):
                    doc_list.append(nltk.PorterStemmer().stem(abstract_string[a]))
                    file.close()
    
    print('current ',len(doc_list))
    docList.append(doc_list)

lengths=[len(d) for d in docList]
print('final',sum(lengths))

papers_length = len(docList)

print('Total papers length is:',papers_length)
                    
#print(docList)

# The first table
word_list = []
doc_id = []
doc_position = []

# The second table
doc_idid = []
doc_length = []

for e in range(papers_length):
    doc_idid.append(docList[e][0])
    doc_length.append(len(docList[e])-1)
    
    list_length = len(docList[e])
    check = []
    for f in range(1,list_length):
        token = str(docList[e][f])
        if token not in check:
            token_index = docList[e].index(token)
            check.append(token)
            times = docList[e].count(token)
            times1=1
            position_string = ''
            for i in range(token_index,list_length):
                if str(docList[e][i])==str(token):
                    position_string = position_string + str(i)
                    if times1 != times:
                        position_string = position_string + ','
                        times1=times1+1
            word_list.append(token)
            doc_id.append(docList[e][0])
            doc_position.append(position_string)
            
            
csv_list2 = np.c_[np.array(word_list), np.array(doc_id),np.array(doc_position)]
with open('word_position.csv','w',encoding='utf8',newline='') as f2:
        writer = csv.writer(f2)
        writer.writerows(csv_list2)
            
csv_list3 = np.c_[np.array(doc_idid), np.array(doc_length)]
with open('doc_length.csv','w',encoding='utf8',newline='') as f3:
        writer = csv.writer(f3)
        writer.writerows(csv_list3)
        
print('Done!')

