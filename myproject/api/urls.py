from django.urls import path
from .views import books
from .views import authors

urlpatterns = [
    path("books/", books),
    path("authors/", authors),
]
