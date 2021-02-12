from django.urls import path
from paper import views
urlpatterns = [
    path("index", views.main_page, name="main_page"),
    path("detail", views.detail, name="detail"),
]