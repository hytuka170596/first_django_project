from rest_framework import serializers
from django.contrib.auth.models import Group, User

from blogapp.models import Article, Tag
from myauth.models import Profile


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", "permissions", "pk")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "pk")


class TagSerializer(serializers.ModelSerializer):
    tag = serializers.ReadOnlyField(source="name_tag")

    class Meta:
        model = Tag
        fields = ("tag", "pk")


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for Article objects. Includes all fields from the Article model

    """

    author = serializers.ReadOnlyField(source="author.name_author")
    tags = TagSerializer(many=True)
    pub_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    category = serializers.ReadOnlyField(source="category.name_category")

    class Meta:
        model = Article
        fields = (
            "title",
            "content",
            "pub_date",
            "author",
            "pk",
            "tags",
            "author",
            "category",
            "archived",
        )


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["title", "content", "author", "category", "tags", "archived"]
        read_only_fields = ["author"]


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile objects. Includes all fields from the Profile model
    """

    user = UserSerializer()
    avatar = serializers.ReadOnlyField(source="user.avatar")

    class Meta:
        model = Profile
        fields = (
            "pk",
            "user",
            "bio",
            "agreement_accepted",
            "created_at",
            "avatar",
            "sex",
            "username",
            "email",
            "first_name",
            "last_name",
        )
