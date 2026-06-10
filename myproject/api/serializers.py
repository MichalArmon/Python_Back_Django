from rest_framework import serializers
from .models import Book, Author, Category, UserProfile
from django.contrib.auth.models import User
from django.db import transaction

invalidated_words = ["test", "temp", "check", "admin", "null"]


class Category_serializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class Book_serializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = fields = "__all__"

    # def validate_pages(self, value):
    #     if value < 10:
    #         raise serializers.ValidationError(
    #             "Can't save book with less then 10 pages!"
    #         )
    #     return value

    # def validate_title(self, value):
    #     for word in invalidated_words:
    #         if word in value:
    #             raise serializers.ValidationError(f"Title can't include {word}")
    #         return value

    # def validate(self, data):
    #     title = data.get("title")
    #     if len(title) < 2:
    #         raise serializers.ValidationError("Book title must be more then 1 char!")
    #     pages = data.get("pages")
    #     if title[0] == "a" or title[0] == "A" and pages < 25:
    #         raise serializers.ValidationError("Stupid rule, bu what can you do!")
    #     return data


class Author_serializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class Book_with_author_serializer(serializers.ModelSerializer):
    author = Author_serializer()

    class Meta:
        model = Book
        fields = "__all__"


class UserProfile_serializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            "user_id",
            "user_username",
            "username",
            "password",
            "primary_phone",
            "secondary_phone",
            "city",
            "street",
            "birth_date",
        )

    def create(self, validated_data):
        with transaction.atomic():

            user = User.objects.create_user(
                username=validated_data.pop("username"),
                password=validated_data.pop("password"),
            )
            profile = UserProfile.objects.create(user=user, **validated_data)
        return profile
