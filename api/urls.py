from django.urls import path
# from paper import views
from api import views

urlpatterns = [
    # path("index", views.main_page, name="main_page"),
    path("detail/<str:paper_id>", views.detail, name="detail"),
    path("search", views.search, name="search"),
    path("test", views.test, name="test"),
    path("query_suggestion", views.auto_query_suggestion, name="query_suggestion")
]

'1. localhost:8000/api/detail/<paper_id>'
'2. localhost:8000/api/search?key=<search_content>'
