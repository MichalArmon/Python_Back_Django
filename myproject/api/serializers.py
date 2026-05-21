from rest_framework import serializers
from .models import Book, Author, Category

invalidated_words = ["test", "temp", "check", "admin", "null"]


class Category_serializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class Book_serializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "id", "pages", "year", "author"]

    def validate_pages(self, value):
        if value < 10:
            raise serializers.ValidationError(
                "Can't save book with less then 10 pages!"
            )
        return value

    def validate_title(self, value):
        for word in invalidated_words:
            if word in value:
                raise serializers.ValidationError(f"Title can't include {word}")
            return value

    def validate(self, data):
        title = data.get("title")
        if len(title) < 2:
            raise serializers.ValidationError("Book title must be more then 1 char!")
        pages = data.get("pages")
        if title[0] == "a" or title[0] == "A" and pages < 25:
            raise serializers.ValidationError("Stupid rule, bu what can you do!")
        return data


class Author_serializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class Book_with_author_serializer(serializers.ModelSerializer):
    author = Author_serializer()

    class Meta:
        model = Book
        fields = ["title", "id", "pages", "year", "author"]
