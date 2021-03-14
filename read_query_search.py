import csv
import os

import django
from django.db import IntegrityError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paper_search.settings')
django.setup()
from paper.models import PaperLength, QuerySearch


def read_csv(filename):
    with open(filename, 'r')as opener:
        number = 0
        reader = csv.reader(opener)
        next(reader)
        for r in reader:
            word_input, ids = r
            ids = ids.split(';')
            try:
                paper_len = QuerySearch.objects.create(word=word_input, words=ids)
                number += 1
                print('created', number)
            except IntegrityError:
                pass



QuerySearch.objects.all().delete()
read_csv('query_suggestions_updated.csv')
