#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import numpy as np
import re


def convert_bi_gram(title):
    items = title.split(' ')
    bi_item_list = []
    previous_item = items[0]
    for item in items[1:]:
        bi_item = previous_item + '_' + item
        previous_item = item
        bi_item_list.append(bi_item)

    return bi_item_list


def create_bi_word(tmp1, tmp2):
    tmp1 = str(tmp1)
    tmp2 = str(tmp2)
    return tmp1 + '_' + tmp2


def create_tri_word(tmp1, tmp2, tmp3):
    tmp1 = str(tmp1)
    tmp2 = str(tmp2)
    tmp3 = str(tmp3)
    return tmp1 + '_' + tmp2 + '_' + tmp3


def create_qua_word(tmp):
    l = len(tmp)
    _str = tmp[0]
    for _tmp in tmp[1:]:
        _str = _str + '_' + _tmp

    return _str


dic1 = {}  # paper ID and paper title
dic2 = {}  # bi-gram word and paper ID
dic3 = {}  # First word : [second word]
dic4 = {}  # sorted version of dic 4

dic5 = {}  # tri-gram word and paper ID
dic6 = {}  # First_second_word : [third word]

dic7 = {}  # penta gram word and paper ID
dic8 = {}  # first_second_third_word :[fourth word]

dic9 = {}  # penta gram word and paper ID
dic10 = {}  # first_second_third_word :[fourth word]

# sort dic 3 and dic 6 , dic 8 put them in dic 4


file = open("order_citation_5000.json", 'r', encoding='utf-8')

doc_list = [];

for line in file.readlines()[1:]:
    dic = json.loads(line)
    doc_list.append(dic)
i = 1
for dic in doc_list:
    title = dic.get('title')
    id = dic.get('id')
    # print(title)
    # print(id)

    line = title.strip('\n').lower()
    # print(line)
    # form dic 1 : paper ID and paper title 
    dic1.update({id: line})

    r = '\W'
    line = re.sub(r, ' ', line)
    line = re.sub('_', ' ', line)
    items = list(filter(None, line.split(' ')))

    bi1 = create_bi_word(items[0], items[1])
    # print(bi1)

    if bi1 in dic2.keys():

        # if the bi-word already exists, append the list
        dic2[bi1].append(id)
    else:
        # if the bi-word is new, update it and add the title ID 
        dic2.update({bi1: [id]})

    first_word, second_word = bi1.split('_')
    # print(first_word)
    if first_word in dic3.keys():
        # first word already exist in keys, update the second word dic
        dic3[first_word].append(second_word)
    else:
        dic3.update({first_word: [second_word]})

    # bi2=create_tri_word(items[0],items[1], items[2])
    if len(items) > 2:
        bi2 = create_tri_word(items[0], items[1], items[2])
        # print(bi2)

        if bi2 in dic5.keys():
            # if the bi-word already exists, append the list
            dic5[bi2].append(id)
        else:
            # if the bi-word is new, update it and add the title ID 
            dic5.update({bi2: [id]})

        first_word, second_word, third_word = bi2.split('_')
        # print(first_word)
        if bi1 in dic6.keys():
            # first word already exist in keys, update the second word dic
            dic6[bi1].append(third_word)
        else:
            dic6.update({bi1: [third_word]})

    if len(items) > 3:
        bi3 = create_qua_word(items[:4])
        if bi3 in dic7.keys():
            # if the bi-word already exists, append the list
            dic7[bi3].append(id)
        else:
            # if the bi-word is new, update it and add the title ID 
            dic7.update({bi3: [id]})

        last_word = items[3]
        bi2 = create_tri_word(items[0], items[1], items[2])
        if bi2 in dic8.keys():
            # first word already exist in keys, update the second word dic
            dic8[bi2].append(last_word)
        else:
            dic8.update({bi2: [last_word]})

    if len(items) > 4:
        bi4 = create_qua_word(items[:5])
        if bi4 in dic9.keys():
            # if the bi-word already exists, append the list
            dic9[bi4].append(id)
        else:
            # if the bi-word is new, update it and add the title ID 
            dic9.update({bi4: [id]})

        last_word = items[4]
        bi3 = create_qua_word(items[:4])
        if bi3 in dic10.keys():
            # first word already exist in keys, update the second word dic
            dic10[bi3].append(last_word)
        else:
            dic10.update({bi3: [last_word]})


def sort_the_second_word(list1):
    unique = np.unique(list1)
    dic_tmp = {}
    for item in unique:
        tmp = list1.count(item)
        dic_tmp.update({item: tmp})
    dic_tmp = sorted(dic_tmp.items(), key=lambda d: d[1], reverse=True)
    return dic_tmp


dic4 = {}
for item in dic3.items():
    first_word = item[0]
    second_word_list = item[1]
    dic_tmp = sort_the_second_word(second_word_list)
    _list = []
    for tmp in dic_tmp:
        _list.append(tmp[0])
    dic4.update({first_word: _list})

for item in dic6.items():
    first_word = item[0]
    second_word_list = item[1]
    dic_tmp = sort_the_second_word(second_word_list)
    _list = []
    for tmp in dic_tmp:
        _list.append(tmp[0])
    dic4.update({first_word: _list})

for item in dic8.items():
    first_word = item[0]
    second_word_list = item[1]
    dic_tmp = sort_the_second_word(second_word_list)
    _list = []
    for tmp in dic_tmp:
        _list.append(tmp[0])
    dic4.update({first_word: _list})

for item in dic10.items():
    first_word = item[0]
    second_word_list = item[1]
    dic_tmp = sort_the_second_word(second_word_list)
    _list = []
    for tmp in dic_tmp:
        _list.append(tmp[0])
    dic4.update({first_word: _list})

if __name__ == '__main__':

    import csv

    with open('query_suggestions.csv', 'w', encoding='utf8', newline='') as f2:
        writer = csv.writer(f2)
        writer.writerow(["input", "ID"])

        for key, vals in dic4.items():
            # print(key)
            # print(vals)
            last_word_list = vals
            id_list = []

            write_tmp = []
            items = key.split('_')
            for last_word in last_word_list:
                if len(items) == 2:
                    bi_tmp = create_bi_word(key, last_word)
                    id_list_tmp = dic5[bi_tmp]
                    id_list.extend(id_list_tmp)
                elif len(items) == 3:
                    bi_tmp = create_bi_word(key, last_word)
                    id_list_tmp = dic7[bi_tmp]
                    id_list.extend(id_list_tmp)
                elif len(items) == 4:
                    bi_tmp = create_bi_word(key, last_word)
                    id_list_tmp = dic9[bi_tmp]
                    id_list.extend(id_list_tmp)
                else:
                    bi_tmp = create_bi_word(key, last_word)
                    id_list_tmp = dic2[bi_tmp]
                    id_list.extend(id_list_tmp)
            # print( key )
            # print(id_list[0:6])

            list1 = []
            _str = ''

            for i, item in enumerate(id_list[0:6]):

                if len(id_list[0:6]) == 1:
                    _str = _str + item
                else:
                    if i == 0:
                        _str = _str + item
                    else:
                        _str = _str + ';' + item
            # write_tmp.append(str(item))
            list1.append(key)
            list1.append(_str)
            writer.writerow(list1)

    # In[ ]:
