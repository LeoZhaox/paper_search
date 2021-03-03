from django.shortcuts import render
import time
# Create your views here.
from rest_framework.decorators import api_view
from paper.models import Paper
from rest_framework.response import Response
from api.serializers import PaperSerializer
from tf_idf import TFIDF
from bm25 import BM25
from django.core.cache import cache


# from tf_idf import tf_idf
# from bm25 import bm_25c

@api_view(['GET'])
def detail(request, paper_id):
    paper = Paper.objects.get(id=paper_id)
    serializer = PaperSerializer(paper)
    return Response(serializer.data)


@api_view(['GET'])
def search(request):
    key = request.GET.get('key')
    algorithm_type = request.GET.get('algorithm_type', '1')
    key_name = '{}_{}'.format(key, algorithm_type)
    algorithm_type = int(algorithm_type)
    papers = cache.get(key_name)
    if papers is None:
        if algorithm_type == 2:
            papers = BM25(key)
        else:
            papers = TFIDF(key)
    # 127.0.0.1: 8000 / api / search?key = design & alogorithm = 1 & order = 1 & descend = 1

    # order: 1:year 2: citation
    # descend: 1 降序 2: 升序
    # 排序
    order_by_date = request.GET.get('order')
    descend = request.GET.get('descend')

    print(order_by_date, descend)
    if descend == '1':
        descend = True
    else:
        descend = False
    if order_by_date == '1':
        papers = sorted(papers, key=lambda x: x.year, reverse=descend)

    elif order_by_date == '2':
        papers = sorted(papers, key=lambda x: x.n_citation, reverse=descend)
    # History.objects.create();
    print(request.data)
    'localhost:8000/search?key=nlp&algorithm_type=1'
    'localhost:8000/search?key=nlp'
    # print('key', key)
    # print('algorithm', algorithm_type)
    serializer = PaperSerializer(papers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def test(request):
    papers = Paper.objects.order_by('?')[:100]
    serializer = PaperSerializer(papers, many=True)
    return Response(serializer.data)

# def list_history():
# redis.set(''
