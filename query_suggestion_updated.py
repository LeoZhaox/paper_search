import json
import numpy as np
import re


def create_bi_word(tmp1, tmp2):
    tmp1 = str(tmp1)
    tmp2 = str(tmp2)
    return tmp1 + '_' + tmp2


dic1 = {}  # {first word : [second word]}
# second word list: not sorted, contain repeated terms
dic2 = {}  # {first word : [second word]}
# second word list: sorted, only unique terms
dic3 = {}  # {bigram: [third word]}
# third word list: not sorted, contain repeated terms
dic4 = {}  # {bigram : [third word]}
# third  word list: sorted, only unique terms

# open the file  
file = open("order_citation_5000.json", 'r', encoding='utf-8')

doc_list = []
# read line from the file
for line in file.readlines()[1:]:
    dic = json.loads(line)
    doc_list.append(dic)

for dic in doc_list:
    title = dic.get('title')
    # print(title)
    # pre-processing
    line = title.strip('\n').lower()

    r = '\W'
    line = re.sub(r, ' ', line)
    line = re.sub('_', ' ', line)
    items = list(filter(None, line.split(' ')))
    # print(items)

    # case 1: user input is a single word
    for i, item in enumerate(items[0:-1]):
        first_word = item
        second_word = items[i + 1]

        if first_word in dic1.keys():
            dic1[first_word].append(second_word)
        else:
            dic1.update({first_word: [second_word]})
            print(first_word)

    # case 2: user input is two words
    if len(items) >= 3:
        for i, item in enumerate(items[0:-2]):
            # print(item)
            first_word = item
            second_word = items[i + 1]
            third_word = items[i + 2]
            bi_gram = create_bi_word(first_word, second_word)
            # print(bi_gram)

            if bi_gram in dic3.keys():
                dic3[bi_gram].append(third_word)
            else:
                dic3.update({bi_gram: [third_word]})


def sort_the_second_word(list1):
    unique = np.unique(list1)
    dic_tmp = {}
    for item in unique:
        tmp = list1.count(item)
        dic_tmp.update({item: tmp})
    dic_tmp = sorted(dic_tmp.items(), key=lambda d: d[1], reverse=True)
    return dic_tmp


for item in dic3.items():
    # print(item)
    first_word = item[0]
    second_word_list = item[1]
    dic_tmp = sort_the_second_word(second_word_list)
    # print(dic_tmp)
    _list = []
    for tmp in dic_tmp:
        _list.append(tmp[0])
    dic2.update({first_word: _list})

for item in dic1.items():
    # print(item)
    first_word = item[0]
    second_word_list = item[1]
    dic_tmp = sort_the_second_word(second_word_list)
    # print(dic_tmp)
    _list = []
    for tmp in dic_tmp:
        _list.append(tmp[0])
    dic2.update({first_word: _list})

# import csv
#
# with open('query_suggestions_updated.csv', 'w', encoding='utf8', newline='') as f2:
#     writer = csv.writer(f2)
#     writer.writerow(["input", "suggested word"])
#
#     for key, vals in dic2.items():
#         _list = []
#         _list.append(key)
#
#         _str = ''
#         for i, tmp in enumerate(vals):
#             if i > 5: break
#
#             if i == 0:
#                 _str = _str + tmp
#             else:
#                 _str = _str + ';' + tmp
#
#         _list.append(_str)
#         writer.writerow(_list)
#