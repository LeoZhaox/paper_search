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
from paper.models import Paper, Author, WordPosition

null_number = 0
with open('word_position.csv', 'r')as opener:
    reader = csv.reader(opener)
    for r in reader:

        word_name, paper_id, word_position = r
        word_position_list = word_position.split(',')
        word_position_list = [int(w) for w in word_position_list]
        # print(paper_id)
        print(word_name)
        try:
            WordPosition.objects.get_or_create(word_name=word_name, paper_id=paper_id,
                                               defaults={'position': word_position_list})
        except IntegrityError:
            null_number += 1
            print('null:', paper_id, null_number)
