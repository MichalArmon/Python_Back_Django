from rest_framework import serializers
from .models import Book, Author


class Book_serializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "pages", "year"]


class Author_serializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class Book_with_author_serializer(serializers.ModelSerializer):
    author = Author_serializer()

    class Meta:
        model = Book
        fields = ["id", "pages", "year", "author"]
