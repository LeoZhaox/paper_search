# coding=utf-8
"""
@time: 3/9/21 1:14 PM
@author: colaplusice
@contact: fjl2401@163.com vx:18392358995
"""
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paper_search.settings')
django.setup()
from paper.models import QuerySearch, Paper

qs = QuerySearch.objects.all()

for q in qs:
    papers = q.papers
    for p in papers:
        ex=Paper.objects.filter(id=p)
        if ex:
            print('exitst', q.word,q.papers)
            break