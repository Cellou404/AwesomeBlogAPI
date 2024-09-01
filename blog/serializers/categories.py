from rest_framework import serializers
from blog.models import Category, Post


# Basic Serializer for Post Model
class BasicPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id", "slug", "title", 
            "thumbnail", "category", "date_created"
        ]


class CategorySerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField(method_name="get_posts")

    class Meta:
        model = Category
        fields = [
            "id", "name", "description", 
            "is_active", "date_created", "posts"
        ]

    def get_posts(self, cat_name):
        category = Category.objects.get(name=cat_name)
        posts = Post.objects.filter(category=category)
        serializer = BasicPostSerializer(posts, many=True)
        return serializer.data
