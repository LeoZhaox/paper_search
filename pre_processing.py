import datetime
import json
import os

import django
from django.db import IntegrityError, OperationalError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paper_search.settings')
django.setup()
from paper.models import Paper, Author
import pytz
import threading


# saved = Paper.objects.all().count()
def preprocess_file(filename):
    created_num = 0
    with open(filename, 'r') as opener:
        contents = opener.readlines()
        print(threading.current_thread().name, created_num)
        # print(content)
        for content in contents:
            res = json.loads(content)
            authors = res.get('authors')
            n_citation = res.get('n_citation')
            references = res.get('references')
            id = res.get('id')
            title = res.get('title')
            year = res.get('year')
            abstract = res.get('abstract')
            # print(res['abstract'])
            venue = res.get('venue')
            date = datetime.datetime(year=year, month=1, day=1, tzinfo=pytz.UTC)
            try:
                created_num += 1
                if created_num < 100000:
                    p = Paper.objects.create(id=id, title=title, year=date, references=references, venue=venue, n_citation=n_citation, abstract=abstract)
                else:
                    p = Paper.objects.create(id=id, title=title, year=date, references=references, abstract='', venue=venue, n_citation=n_citation)
            except (IntegrityError, OperationalError) as e:
                print('error', e, id)
                continue
            for author_name in authors:
                author, _ = Author.objects.get_or_create(name=author_name)
                p.authors.add(author)


preprocess_file('dblp-ref-0.json')
