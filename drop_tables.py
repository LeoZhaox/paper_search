# coding=utf-8
"""
@time: 2/15/21 12:45 PM
@author: colaplusice
@contact: fjl2401@163.com vx:18392358995
"""
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paper_search.settings')
django.setup()
from paper.models import Paper, WordPosition, PaperLength

WordPosition.objects.all().delete()
PaperLength.objects.all().delete()
Paper.objects.all().delete()
