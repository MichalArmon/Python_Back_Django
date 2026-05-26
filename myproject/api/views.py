from django.shortcuts import render, get_object_or_404
from .models import Book, Author, Category
from .serializers import (
    Book_serializer,
    Author_serializer,
    Book_with_author_serializer,
    Category_serializer,
)
from rest_framework.response import Response
from rest_framework import status


from rest_framework.decorators import api_view


@api_view(["GET", "POST"])
def categories(request):
    if request.method == "GET":
        categories = Category.objects.all()
        serializer = Category_serializer(categories, many=True)

        return Response(serializer.data)
    if request.method == "POST":
        serializer = Category_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET", "POST"])
def books(request):
    if request.method == "GET":
        books = Book.objects.all()
        serializer = Book_with_author_serializer(books, many=True)

        return Response(serializer.data)
    if request.method == "POST":
        serializer = Book_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET", "POST"])
def authors(request):
    if request.method == "GET":
        authors = Author.objects.all()
        serializer = Author_serializer(authors, many=True)

        return Response(serializer.data)
    if request.method == "POST":
        serializer = Author_serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET", "PUT", "DELETE"])
def book_details(request, id):
    try:
        book = Book.objects.get(pk=id)
        if request.method == "GET":
            serializer = Book_with_author_serializer(book)
            return Response(serializer.data)
        if request.method == "DELETE":
            book.delete()
            return Response({"message": "book deleted successfully!"})
        if request.method == "PUT":
            serializer = Book_serializer(book)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Book.DoesNotExist:
        return Response({"detail": "not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def add_category_to_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    cat_id = request.data.get("category_id")
    category = get_object_or_404(Category, pk=cat_id)
    if book.categories.filter(pk=cat_id).exists():
        book.categories.remove(category)
        message = "category removed from book"
    else:
        book.categories.add(category)
        message = "category added to book"
    serializer = Book_serializer(book)

    return Response({"message": message, "book": serializer.data})


@api_view(["GET"])
def books_by_year(request, year):

    books = Book.objects.filter(year=year)
    serializer = Book_with_author_serializer(books, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def books_by_author(request, author):

    books = Book.objects.filter(author__name=author)
    serializer = Book_with_author_serializer(books, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def books_by_author_year(request, year):

    books = Book.objects.filter(author__birth_year__gt=year)
    serializer = Book_with_author_serializer(books, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def author_details(request, id):

    author = get_object_or_404(Author, pk=id)
    serializer = Author_serializer(author)
    return Response(serializer.data, status=status.HTTP_200_OK)
