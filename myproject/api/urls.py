from django.urls import path

from .views import (
    books,
    authors,
    categories,
    book_details,
    author_details,
    books_by_year,
    books_by_author,
    books_by_author_year,
    add_category_to_book,
    books_by_category,
)

urlpatterns = [
    path("books/", books),
    path("books/<int:id>/", book_details),
    path("books/category/<int:book_id>/", add_category_to_book),
    path("books/by-category/<int:cat_id>/", books_by_category),
    path("books/year/<int:year>/", books_by_year),
    path("books/author/<str:author>/", books_by_author),
    path("books/author/year/<int:year>/", books_by_author_year),
    path("authors/", authors),
    path("categories/", categories),
    path("authors/<int:id>/", author_details),
]
