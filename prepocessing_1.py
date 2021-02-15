import datetime
import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paper_search.settings')
django.setup()
from paper.models import Paper, Author
import pytz


def preprocess_file(filename):
    created_num = 0
    with open(filename, 'r') as opener:
        contents = opener.readlines()

        # print(content)

        for content in contents:
            created_num += 1
            res = json.loads(content)
            # paper=a.get('authors')
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
                p, created = Paper.objects.get_or_create(id=id,
                                                         defaults={"title": title, 'year': date, 'abstract': abstract,
                                                                   'references': references, 'n_citation': n_citation,
                                                                   'venue': venue})

            except Exception as e:
                print('error',e,id)
                pass
            for author_name in authors:
                author, _ = Author.objects.get_or_create(name=author_name)
                p.authors
            print(created_num)

# preprocess_file('dblp-ref-0.json')
# preprocess_file('dblp-ref-1.json')
# preprocess_file('dblp-ref-2.json')
# preprocess_file('dblp-ref-3.json')

# print(content)
# paper = json.load(opener)
# print(type(paper))

# print(paper)
# paper=a.get('authors')
# authors = paper.get('authors')
# n_citation = paper.get('n_citation')
# references = paper.get('n_citation')
# id = paper.get('id')
# title = paper.get('title')
# year = paper.get('year')
# abstract = paper.get('abstract')
# venue = paper.get('venue')
#
# # print(type(abstract),type(year),type(title),type(venue),type(references),type(authors),type(d))
# authors = str(authors)
