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



def preprocess_file(filename):
    created_num = 0

    with open(filename, 'r') as opener:
        contents = opener.readlines()
        # print(content)
        for content in contents:
            created_num += 1
            print(threading.current_thread().name, created_num)
            res = json.loads(content)
            authors = res.get('authors')
            n_citation = res.get('n_citation')
            references = res.get('references')
            id = res.get('id')
            title = res.get('title')
            year = res.get('year')
            # print(res['abstract'])
            abstract = res.get('abstract')
            venue = res.get('venue')
            date = datetime.datetime(year=year, month=1, day=1, tzinfo=pytz.UTC)
            try:
                p = Paper.objects.create(id=id, title=title, year=date, abstract=abstract, references=references, venue=venue, n_citation=n_citation)

                # p, created = Paper.objects.get_or_create(id=id,
                #                                          defaults={"title": title, 'year': date, 'abstract': abstract,
                #                                                    'references': references, 'n_citation': n_citation,
                #                                                    'venue': venue})

            except (IntegrityError, OperationalError) as e:
                print('error', e, id)
                continue
            for author_name in authors:
                author, _ = Author.objects.get_or_create(name=author_name)
                p.authors.add(author)


preprocess_file('dblp-ref-2.json')
