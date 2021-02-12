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
from paper.models import Paper, Author, WordPosition, PaperLength

number = 0
with open('doc_length.csv', 'r')as opener:
    reader = csv.reader(opener)
    for r in reader:
        paper_id, paper_length = r
        paper_len, _ = PaperLength.objects.get_or_create(paper_id=paper_id, defaults={'length': paper_length})
        number += 1
        print('created', number, paper_id)
