#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer
import datetime
import json
import os
import django
import csv

file = open("json_test.json", 'r', encoding='utf-8')
papers = []
for line in file.readlines():
    dic = json.loads(line)
    papers.append(dic)

papers_length = len(papers)

docList = [[] for i in range(papers_length)]

for i in range(papers_length):
    docList[i].append(papers[i].get('id'))  # 添加文件ID

    title = papers[i].get('title')
    if title != None:
        title_string = papers[i].get('title').split(' ')  # 添加title的token
        title_length = len(title_string)
        title_term = ''
        for a in range(title_length):
            if title_string[a] != '':
                term_length = len(title_string[a])
                title_term = ''
                # do the tokenization, stopping and stemming, appending terms into docList
                for b in range(term_length):
                    if title_string[a][b].isalpha() == True or title_string[a][b].isdigit() == True:
                        title_term = title_term + str(title_string[a][b].lower())
                    else:
                        if title_term != '':
                            file = open('stop.txt')
                            if title_term + '\n' not in list(file):
                                docList[i].append(nltk.PorterStemmer().stem(title_term))
                                file.close()
                            title_term = ''
                if title_term != '':
                    file = open('stop.txt')
                    if title_term + '\n' not in list(file):
                        docList[i].append(nltk.PorterStemmer().stem(title_term))
                        file.close()

    abstract = papers[i].get('abstract')
    if abstract != None:
        abstract_string = abstract.split(' ')  # 添加abstract的token
        abstract_length = len(abstract_string)
        abstract_term = ''
        for a in range(abstract_length):
            if abstract_string[a] != '':
                term_length = len(abstract_string[a])
                abstract_term = ''
                # do the tokenization, stopping and stemming, appending terms into docList
                for b in range(term_length):
                    if abstract_string[a][b].isalpha() == True or abstract_string[a][b].isdigit() == True:
                        abstract_term = abstract_term + str(abstract_string[a][b].lower())
                    else:
                        if abstract_term != '':
                            file = open('stop.txt')
                            if abstract_term + '\n' not in list(file):
                                docList[i].append(nltk.PorterStemmer().stem(abstract_term))
                                file.close()
                            abstract_term = ''
                if abstract_term != '':
                    file = open('stop.txt')
                    if abstract_term + '\n' not in list(file):
                        docList[i].append(nltk.PorterStemmer().stem(abstract_term))
                        file.close()

# Inverted index fuction    

# The first table
check = []
frequency = []

# The second table
word_list = []
doc_id = []
doc_position = []

index_file = open('index.txt', 'w', encoding='UTF-8')
for e in range(papers_length):
    list_length = len(docList[e])
    for f in range(1, list_length):
        # check whether it is a new term
        if str(docList[e][f]) not in check:
            token = str(docList[e][f])
            freq = 1
            check.append(token)
            index_file.write(str(token) + ':')

            # count each term frequency in documents
            for g in range(e + 1, papers_length):
                if token in docList[g]:
                    freq = freq + 1
            index_file.write(str(freq) + '\n')
            frequency.append(freq)

            # get the positions of term
            for h in range(e, papers_length):
                if token in docList[h]:
                    word_list.append(token)
                    doc_id.append(docList[h][0])
                    index_file.write('\t' + str(docList[h][0]) + ':')
                    length5 = len(docList[h])
                    times = docList[h].count(token)
                    times1 = 1
                    position_string = ''
                    for i in range(1, length5):
                        if str(docList[h][i]) == str(token):
                            index_file.write(str(i))
                            position_string = position_string + str(i)
                            if times1 != times:
                                index_file.write(',')
                                position_string = position_string + ','
                                times1 = times1 + 1
                    index_file.write('\n')
                    doc_position.append(position_string)

index_file.close()

csv_list1 = np.c_[np.array(check), np.array(frequency)]
csv_list2 = np.c_[np.array(word_list), np.array(doc_id), np.array(doc_position)]
headers1 = ['word_name', 'word_freq']
headers2 = ['word_name', 'doc_id', 'position']

with open('word_freq.csv', 'w', encoding='utf8', newline='') as f1:
    writer = csv.writer(f1)
    writer.writerow(headers1)
    writer.writerows(csv_list1)

with open('word_position.csv', 'w', encoding='utf8', newline='') as f2:
    writer = csv.writer(f2)
    writer.writerow(headers2)
    writer.writerows(csv_list2)

doc_idid = []
doc_length = []
for a in range(len(docList)):
    doc_idid.append(docList[a][0])
    doc_length.append(len(docList[a]) - 1)

csv_list3 = np.c_[np.array(doc_idid), np.array(doc_length)]
# headers3=['doc_id','doc_length']
with open('doc_length.csv', 'w', encoding='utf8', newline='') as f3:
    writer = csv.writer(f3)
    # writer.writerow(headers3)
    writer.writerows(csv_list3)

# print(word_list)
# print(doc_id)
# print(doc_position)


# In[ ]:


# In[ ]:


# In[ ]:
