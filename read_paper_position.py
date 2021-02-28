import csv
import datetime
import json
import os

import django
from django.db.utils import IntegrityError
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paper_search.settings')
django.setup()
from paper.models import WordPosition


def read_word_position(filename):
    with open(filename, 'r')as opener:
        reader = csv.reader(opener)
        for r in reader:
            word_name, paper_id, word_position = r
            word_position_list = word_position.split(',')
            word_position_list = [int(w) for w in word_position_list]
            try:
                WordPosition.objects.create(word_name=word_name, paper_id=paper_id, position=word_position_list)
            except IntegrityError:
                continue


import os

files = os.listdir('.')
for file in files:
    if file.startswith('word_position'):
        print('write file', file)
        read_word_position(file)
