from django.shortcuts import render
import time
# Create your views here.
from rest_framework.decorators import api_view
from paper.models import Paper, QuerySearch
from rest_framework.response import Response
from api.serializers import PaperSerializer, WordsSerializer
from tf_idf import TFIDF
from bm25_new import BM25
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
    if algorithm_type == 2:
        cache.delete('{}_{}'.format(key, 1))
    else:
        cache.delete('{}_{}'.format(key, 2))
    print(key_name)
    papers = cache.get(key_name)
    print(papers, 'cache')
    if papers is None:
        if algorithm_type == 2:
            papers = BM25(key)
        else:
            papers = TFIDF(key)
    # 127.0.0.1: 8000 / api / search?key = design & alogorithm = 1 & order = 1 & descend = 1&year=2015-2020&author=Zelalem Mekuria&venue=ccf
    # alogorithm 1 代表 tfidf， 2代表bm25，order 1 year，2citation；descend 1 降序，2 升序；后面就是按照输入过滤了
    # order: 1:year 2: citation
    # descend: 1 降序 2: 升序
    # 排序c
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
    print('this is year', year)
    if year is not None and year != '':
        begin, end = year.split('-')
        # if begin==end or begin=='0000':

        temp = []
        for paper in papers:
            # localhost:8000/api/test?key=design&alogorithm=1&order=1&descend=1&year=2013-2014
            # localhost:8000/api/test?key=design&alogorithm=1&order=1&descend=1
            try:
                begin_date = datetime(year=int(begin), month=1, day=1, tzinfo=pytz.utc)
                end_date = datetime(year=int(end), month=1, day=1, tzinfo=pytz.utc)
                if paper.year <= end_date and paper.year >= begin_date:
                    temp.append(paper)
            except Exception:
                temp = []
                break
        papers = temp
    author = request.GET.get('author')
    if author is not None and author != '':
        temp = []
        for paper in papers:
            exist = paper.authors.filter(name=author).exists()
            print('author', author)
            print('exist', exist)
            if exist:
                temp.append(paper)
        papers = temp
    venue = request.GET.get('venue')
    if venue is not None and venue != '':
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



@api_view(['GET'])
def auto_query_suggestion(request):
    # Get the input *
    _input = request.GET.get('key')
    # search the data base and get the recommended id list
    n_words = _query_search(_input)
    search_res = QuerySearch.objects.get(word=n_words)
    # print(search_res.words)
    return_list = []
    for i in range(len(search_res.words)):
        temp = {'value': _input +" "+ search_res.words[i]}
        return_list.append(temp)
    print(return_list)
    # serializer = WordsSerializer(return_list)
    return Response(return_list)


@api_view(['GET'])
def similarity_paper(request):
    paper_id = request.GET.get('id')
    paper = Paper.objects.get(id=paper_id)
    papers = find_similar(paper.title)
    serializer = PaperSerializer(papers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def author_paper(request):
    author_name = request.GET.get('name')
    papers = Paper.objects.filter(authors__name=author_name)
    serializer = PaperSerializer(papers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def check_grammar(request):
    sentence = request.GET.get('sentence')
    res = check_grammer(sentence)
    print(res)
    return JsonResponse({'sentence': res})
