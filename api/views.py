from django.shortcuts import render
import time
# Create your views here.
from rest_framework.decorators import api_view
from paper.models import Paper, QuerySearch
from rest_framework.response import Response
from api.serializers import PaperSerializer
from tf_idf import TFIDF
from bm25 import BM25
from django.core.cache import cache
from Search_function import _query_search
from datetime import datetime
import pytz
from similar_recommend import find_similar
from grammer import check_grammer
from django.http import JsonResponse


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
    # 127.0.0.1: 8000 / api / search?key = design & alogorithm = 1 & order = 1 & descend = 1&year=2015-2020&author=abc&venue=ccf
    # alogorithm 1 代表 tfidf， 2代表bm25，order 1 year，2citation；descend 1 降序，2 升序；后面就是按照输入过滤了
    # order: 1:year 2: citation
    # descend: 1 降序 2: 升序
    # 排序
    order_by_date = request.GET.get('order')
    descend = request.GET.get('descend')
    if descend == '1':
        descend = True
    else:
        descend = False
    if order_by_date == '1':
        papers = sorted(papers, key=lambda x: x.year, reverse=descend)

    elif order_by_date == '2':
        papers = sorted(papers, key=lambda x: x.n_citation, reverse=descend)
    # filter
    year = request.GET.get('year')
    if year is not None:
        begin, end = year.split('-')
        temp = []

        for paper in papers:
            # localhost:8000/api/test?key=design&alogorithm=1&order=1&descend=1&year=2013-2014
            # localhost:8000/api/test?key=design&alogorithm=1&order=1&descend=1
            begin_date = datetime(year=int(begin), month=1, day=1, tzinfo=pytz.utc)
            end_date = datetime(year=int(end), month=1, day=1, tzinfo=pytz.utc)
            if paper.year <= end_date and paper.year >= begin_date:
                temp.append(paper)
        papers = temp
    author = request.GET.get('author')
    if author is not None:
        temp = []
        for paper in papers:
            exist = paper.authors.filter(name=author).exists()
            print('author', author)
            print('exist', exist)
            if exist:
                temp.append(paper)
        papers = temp
    venue = request.GET.get('venue')
    if venue is not None:
        temp = []
        for paper in papers:
            if paper.venue == venue:
                temp.append(paper)
        papers = temp
    #
    # History.objects.create();

    'localhost:8000/search?key=nlp&algorithm_type=1'
    'localhost:8000/search?key=nlp'
    # print('key', key)
    # print('algorithm', algorithm_type)
    serializer = PaperSerializer(papers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def test(request):
    papers = Paper.objects.all()[:100]
    order_by_date = request.GET.get('order')
    descend = request.GET.get('descend')
    if descend == '1':
        descend = True
    else:
        descend = False
    if order_by_date == '1':
        papers = sorted(papers, key=lambda x: x.year, reverse=descend)

    elif order_by_date == '2':
        papers = sorted(papers, key=lambda x: x.n_citation, reverse=descend)
    # filter
    year = request.GET.get('year')
    if year is not None:
        begin, end = year.split('-')
        temp = []

        for paper in papers:
            # localhost:8000/api/test?key=design&alogorithm=1&order=1&descend=1&year=2013-2014
            # localhost:8000/api/test?key=design&alogorithm=1&order=1&descend=1
            begin_date = datetime(year=int(begin), month=1, day=1, tzinfo=pytz.utc)
            end_date = datetime(year=int(end), month=1, day=1, tzinfo=pytz.utc)
            if paper.year <= end_date and paper.year >= begin_date:
                temp.append(paper)
        papers = temp
    author = request.GET.get('author')
    if author is not None:
        temp = []
        for paper in papers:
            exist = paper.authors.filter(name=author).exists()
            print('author', author)
            print('exist', exist)
            if exist:
                temp.append(paper)
        papers = temp
    venue = request.GET.get('venue')
    if venue is not None:
        temp = []
        for paper in papers:
            if paper.venue == venue:
                temp.append(paper)
        papers = temp
    # History.objects.create();
    serializer = PaperSerializer(papers, many=True)
    return Response(serializer.data)


# def list_history():
# redis.set(''
@api_view(['GET'])
def auto_query_suggestion(request):
    # Get the input *
    _input = request.GET.get('key')
    # search the data base and get the recommended id list
    n_words = _query_search(_input)
    print('n_words', n_words)
    search_res = QuerySearch.objects.get(word=n_words)
    paper_ids = search_res.papers
    print('paper ids', paper_ids)
    'apple_tree'
    papers = Paper.objects.filter(id__in=paper_ids)
    serializer = PaperSerializer(papers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def similarity_paper(request):
    paper_id = request.GET.get('id')
    paper = Paper.objects.get(id=paper_id)
    papers = find_similar(paper.title)
    serializer = PaperSerializer(papers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def check_grammar(request):
    sentence = request.GET.get('sentence')
    res = check_grammer(sentence)
    print(res)
    return JsonResponse({'sentence': res})
