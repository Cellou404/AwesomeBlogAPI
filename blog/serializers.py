from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Category, Post, Comment


# Basic Serializer for Post Model
class BasicPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "slug", "title", "thumbnail", "category", "date_created"]


# Serializer for Category Model
class CategorySerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField(method_name="get_posts")

    class Meta:
        model = Category
        fields = ["id", "name", "description", "is_active", "date_created", "posts"]

    # Custom Method to return related posts in category
    def get_posts(self, cat_name):
        category = Category.objects.get(name=cat_name)
        posts = Post.objects.filter(category=category)
        serializer = BasicPostSerializer(posts, many=True)
        return serializer.data


# Serializer for Post Model
class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    related_posts = serializers.SerializerMethodField(method_name="get_related_posts")
    comments_count = serializers.SerializerMethodField(method_name="get_comments_count")

    class Meta:
        model = Post
        fields = [
            "id",
            "slug",
            "author",
            "category",
            "title",
            "overview",
            "thumbnail",
            "body",
            "is_active",
            "comments_count",
            "date_created",
            "date_updated",
            "related_posts",
        ]

    """ Get related posts to each post
    1. Get the current post's id
    2. Query all other posts that have a similar category to current post
    3. Remove the current post from the list
    """

    def get_related_posts(self, post):
        category = post.category
        posts = Post.objects.filter(category=category).exclude(id=post.id)
        serializer = BasicPostSerializer(posts, many=True)
        return serializer.data

    # Get comments count for each post
    def get_comments_count(self, post):
        comments = Comment.objects.filter(post=post).count()
        return comments

    # Overrinding default create method
    def create(self, validated_data):
        author = self.context[
            "author"
        ]  # the current  logged-in user is the author while creatind a post
        post = Post.objects.create(author=author, **validated_data)
        return post


# Serializing Comment Model
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "body", "date_created"]

    def create(self, validated_data):
        post = self.context["post"]
        user = self.context["user"]
        comment = Comment.objects.create(user=user, post=post, **validated_data)

        return comment
