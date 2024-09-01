from django.utils import timezone
from rest_framework import serializers
from blog.models import Post, Comment


class BasicPostSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = [
            "id", "slug", "title", 
            "category", "date_created"
        ]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    related_posts = serializers.SerializerMethodField(method_name="get_related_posts")
    comments_count = serializers.SerializerMethodField(method_name="get_comments_count")

    class Meta:
        model = Post
        fields = [
            "id", "slug", "author",
            "category", "title", "overview",
            "thumbnail", "body", "is_active",
            "comments_count", "date_created",
            "date_updated", "related_posts",
        ]

    def get_related_posts(self, post) -> list:
        category = post.category
        posts = Post.objects.filter(category=category).exclude(id=post.id)
        serializer = BasicPostSerializer(posts, many=True)
        return serializer.data

    def get_comments_count(self, post) -> int:
        comments = Comment.objects.filter(post=post).count()
        return comments

    def create(self, validated_data):
        author = self.context["author"]
        post = Post.objects.create(author=author, **validated_data)
        return post
