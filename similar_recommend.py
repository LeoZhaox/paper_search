import json
import django
import os
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paper_search.settings')
django.setup()
from scipy.linalg import norm
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from paper.models import Paper
from django.db.models import Q


def find_similar(Input):
    def tfidf_similarity(s1, s2):
        # 转化为TF矩阵
        cv = CountVectorizer(tokenizer=lambda s: s.split())
        corpus = [s1, s2]
        vectors = cv.fit_transform(corpus).toarray()
        # 计算TF系数
        return np.dot(vectors[0], vectors[1]) / (norm(vectors[0]) * norm(vectors[1]))

    doc_list = Paper.objects.filter(~Q(abstract=""), abstract__isnull=False).order_by('-n_citation')[:5000]
    match_list = []
    for paper in doc_list:
        title = paper.title
        abstract = paper.abstract
        match = title + abstract
        matchdic = {'match': tfidf_similarity(Input, match), 'paper': paper}
        match_list.append(matchdic)
    res = sorted(match_list, key=lambda a: a['match'], reverse=True)[:10]
    papers = [r['paper'] for r in res]
    return papers


if __name__ == '__main__':
    res = find_similar(
        "EFL learners' use of online reading strategies and comprehension of texts: An exploratory study")
    print(res)
