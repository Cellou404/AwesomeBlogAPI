from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .models import Category, Post, Comment
from .serializers import (
    CategorySerializer,
    PostSerializer,
    CommentSerializer,
)


# ============================== Category ViewSet ============================ #
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]


# ============================== Post ViewSet ============================ #
class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"

    @extend_schema(
        description="Retrieve a list of posts", responses=PostSerializer(many=True)
    )
    def get_queryset(self):
        queryset = Post.objects.all()
        category = self.request.query_params.get("category")
        author = self.request.query_params.get("author")
        if category is not None:
            queryset = Post.objects.filter(category__name__iexact=category)
        if author is not None:
            queryset = Post.objects.filter(author__profile__username=author)

        return queryset

    # Get serializer context, (to perform create)
    def get_serializer_context(self):
        if self.request.user:
            author = self.request.user
            return {"author": author}

    @extend_schema(
        description="Update a post. Only the Author of the post can perform this action",
        responses=PostSerializer,
    )
    def update(self, request, *args, **kwargs):
        post = self.get_object()

        if request.user != post.author:
            return Response(
                {"error": "You are not authorized to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )

        super().update(request, *args, **kwargs)
        return Response(
            {"success": "The post has been updated"}, status=status.HTTP_200_OK
        )

    @extend_schema(
        description="Delete a post. Only the Author of the post can perform this action",
        request=PostSerializer,
    )
    def destroy(self, request, *args, **kwargs):
        post = self.get_object()

        if request.user != post.author:
            return Response(
                {"error": "You are not authorized to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )

        super().destroy(request, *args, **kwargs)
        return Response(
            {"success": "The post has been deleted"}, status=status.HTTP_204_NO_CONTENT
        )


# ============================== Comment ViewSet ============================ #
class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(description="Retrieve a list of comments", responses=CommentSerializer)
    def get_queryset(self):
        post_slug = self.kwargs.get(
            "post_slug"
        )  # The lookup_field of the post is slug instead of id. So we'll refer to the slugfield to work with comments
        comments = Comment.objects.filter(post__slug=post_slug)
        return comments
    
    
    @extend_schema(
        description="Update a comment",
        request=CommentSerializer,
        responses=CommentSerializer,
    )
    def update(self, request, *args, **kwargs):
        #
        comment = self.get_object()
        # Check if the user is the author of the comment
        if request.user != comment.user:
            return Response(
                {"error": "You are not authorized to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        description="Delete a comment",
        responses=CommentSerializer,
    )
    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        # Check if the user is the author of the comment
        if request.user != comment.user:
            return Response(
                {"error": "You are not authorized to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)

    def get_serializer_context(self):
        post_id = self.kwargs.get("post_slug")
        post = Post.objects.get(slug=post_id)  # comment.post
        user = self.request.user  # comment.user
        return {"post": post, "user": user}
