import csv
import os

import django
from django.db.utils import IntegrityError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paper_search.settings')
django.setup()
from paper.models import WordPosition


def read_word_position(filename):
    created = 0
    with open(filename, 'r', encoding='latin1')as opener:
        reader = csv.reader(opener)
        for r in reader:
            word_name, frequency, tf_idf = r
            try:
                WordPosition.objects.create(word_name=word_name, frequency=frequency, tf_idf=tf_idf)
                created += 1
                print('create number', created)
            except IntegrityError:
                continue


WordPosition.objects.all().delete()
read_word_position('/Users/fjl2401/Downloads/word_position_10w.csv')
# files = os.listdir('.')
# for file in files:
#     if file.startswith('word_position'):
#         print('write file', file)
#         read_word_position(file)
