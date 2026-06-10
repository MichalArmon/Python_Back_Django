from django.shortcuts import render, get_object_or_404
from .models import Book, Author, Category, UserProfile
from .serializers import (
    Book_serializer,
    Author_serializer,
    Book_with_author_serializer,
    Category_serializer,
    UserProfile_serializer,
)
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.db.models import Sum, Count
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


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
@permission_classes([IsAuthenticated])
def books(request):

    year = request.query_params.get("year")
    pages = request.query_params.get("pages")
    q = request.query_params.get("q")

    if request.method == "GET":
        books = Book.objects.all()
        query = Q(year__gt=year) | Q(pages__gt=pages)
        serializer = Book_with_author_serializer(books, many=True)
        return Response(serializer.data)
    if request.method == "GET" and year and pages:
        books = Book.objects.filter(query)
        serializer = Book_with_author_serializer(books, many=True)

    if request.method == "GET" and q:
        query = Q(title__icontains=q) | Q(author__name__icontains=q)
        books = Book.objects.filter(query)
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


@api_view(["GET"])
def books_by_category(request, cat_id):
    books = Book.objects.filter(categories__id=cat_id)
    serializer = Book_with_author_serializer(books, many=True)
    return Response(serializer.data)


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


@api_view(["GET"])
def books_by_pages_year(request, year, pages):

    books = Book.objects.filter(year__gt=year, pages__gt=pages)
    serializer = Book_with_author_serializer(books, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_total_pages(request):
    sum_pages = Book.objects.aggregate(total_pages=Sum("pages"))
    return Response(sum_pages)


@api_view(["GET"])
def author_books(request):
    authors = Author.objects.annotate(num_book=Count("books"))
    data = []
    for author in authors:
        data.append({"author": author.name, "books": author.num_book})

    return Response(data)


def train_book_price_model():
    books_df = pd.read_json("api/model_data/books.json")

    X = books_df[["pages", "is_best_seller"]]
    y = books_df[["price"]]

    x_scaler = MinMaxScaler()
    y_scaler = MinMaxScaler()

    X_scaled = x_scaler.fit_transform(X)
    y_scaled = y_scaler.fit_transform(y)

    model = LinearRegression()
    model.fit(X_scaled, y_scaled)

    return model, x_scaler, y_scaler


model, x_scaler, y_scaler = train_book_price_model()


@api_view(["GET"])
def predict_book_price(request):
    pages = request.GET.get("pages")
    is_best_seller = request.GET.get("is_best_seller")

    if pages is None or is_best_seller is None:
        return Response(
            {"error": "Please provide pages and is_best_seller"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        pages = float(pages)
        is_best_seller = int(is_best_seller)
    except ValueError:
        return Response(
            {"error": "pages must be a number and is_best_seller must be 0 or 1"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    new_book = pd.DataFrame([{"pages": pages, "is_best_seller": is_best_seller}])

    new_book_scaled = x_scaler.transform(new_book)

    predicted_price_scaled = model.predict(new_book_scaled)

    predicted_price = y_scaler.inverse_transform(predicted_price_scaled)

    return Response(
        {
            "pages": pages,
            "is_best_seller": is_best_seller,
            "predicted_price": round(float(predicted_price[0][0]), 2),
        }
    )


@api_view(["GET", "POST"])
def create_user(request):
    if request.method == "GET":
        users = UserProfile.objects.all()
        serializer = UserProfile_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "POST":
        serializer = UserProfile_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
