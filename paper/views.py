from django.shortcuts import render

# Create your views here.前端
from paper.models import Paper


def main_page(request):
    # request.
    # paper=Paper.objects.get(paper_title='name')
    return render(request, 'paper/MainPage.html')


def detail(request):
    paper = Paper.objects.get(id='013ea675-bb58-42f8-a423-f5534546b2b1')
    return render(request, 'paper/Detail.html',{"paper":paper})


def ResultPage(request):
    return render(request, 'paper/Detail.html')
