#!/usr/bin/env python
# coding: utf-8

# In[32]:


import json
import numpy as np

# Load the file
# import csv
#
# dic1 = {}
# list_file = []
# with open('query_suggestions.csv', 'r', encoding="utf-8") as csv_file:
#     all_lines = csv.reader(csv_file)
#     for i, line in enumerate(all_lines):
#
#         if i != 0:
#             # print(line)
#             dic1.update({line[0]: line[1]})
#

# Take the input
import re


def convert_to_N_gram(tmp):
    # input: tmp a list of word
    # output (string): word1_word2_word3
    _str = tmp[0]
    for item in tmp[1:]:
        _str = _str + '_' + item

    return _str


def _query_search(_input):
    # preprocessing
    line = re.sub('_', ' ', _input.lower())
    line = re.sub('-', ' ', line)

    # Split on space
    items = list(filter(None, line.split(' ')))

    # check Length of the input
    l = len(items)
    paper_id_list = []
    if l < 5:
        # Convert to N-gram word
        print('items', items)
        N_gram_word = convert_to_N_gram(items)
        print('this is ngram word', N_gram_word)

        # Search from the database *

        if N_gram_word in dic1.keys():
            paper_id_list = dic1[N_gram_word].split(';')
            # print(paper_id_list)
            # for paper_id in paper_id_list:
            # print(paper_id)
    return paper_id_list


def auto_query_suggestion(_input):
    # Get the input *
    print(_input)
    paper_id_list = _query_search(_input)
    print(paper_id_list)

    # return


# Take the input
# import re

# ********import the data base model *******
# from app01.models import query_suggest
# from app01.models import paper_id_and_title


# _input = 'active'
# auto_query_suggestion(_input)
#
# _query_search('active apple')
#

def _query_search(_input):
    # preprocessing
    line = re.sub('_', ' ', _input.lower())
    line = re.sub('-', ' ', line)

    # Split on space
    items = list(filter(None, line.split(' ')))

    # check Length of the input
    l = len(items)
    paper_id_list = []
    if l < 5:
        # Convert to N-gram word
        N_gram_word = convert_to_N_gram(items)
    return N_gram_word

# res = convert_to_N_gram(['active','apple'])
# print(res)
