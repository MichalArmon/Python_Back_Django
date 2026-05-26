from django.urls import path
from .views import books
from .views import authors, categories
from .views import (
    book_details,
    author_details,
    books_by_year,
    books_by_author,
    books_by_author_year,
    add_category_to_book,
)

urlpatterns = [
    path("books/", books),
    path("books/<int:id>/", book_details),
    path("books/category/<int:book_id>/", add_category_to_book),
    path("books/year/<int:year>/", books_by_year),
    path("books/author/<str:author>/", books_by_author),
    path("books/author/year/<int:year>/", books_by_author_year),
    path("authors/", authors),
    path("categories/", categories),
    path("authors/<int:id>/", author_details),
]
