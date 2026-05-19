from django.shortcuts import render
from .models import Book, Author
from .serializers import Book_serializer, Author_serializer, Book_with_author_serializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


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
