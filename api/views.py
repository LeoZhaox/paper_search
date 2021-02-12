from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from paper.models import Paper
from rest_framework.response import Response
from api.serializers import PaperSerializer
from tf_idf import TFIDF
from bm25 import BM25


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
    algorithm_type = int(algorithm_type)
    print(request.data)
    'localhost:8000/search?key=nlp&algorithm_type=1'
    'localhost:8000/search?key=nlp'
    print('key', key)
    print('algorithm', algorithm_type)
    if algorithm_type == 2:
        papers = BM25(key)
    # elif algorithm_type==3:
    #     key
    #     Paper.objects.filter(abstract__icontains=['name','dfs']|title__icontains=[]).order_by('-years')
    else:
        papers = TFIDF(key)
    serializer = PaperSerializer(papers, many=True)
    return Response(serializer.data)
1--->stage---->commit