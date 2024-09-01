from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from blog.models import Category, Post, Comment

from .serializers.posts import PostSerializer
from .serializers.categories import CategorySerializer
from .serializers.comments import CommentSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    @extend_schema(
        description="Retrieve a list of posts", responses=PostSerializer(many=True)
    )
    def get_queryset(self):
        queryset = Post.objects.all()
        category = self.request.query_params.get("category")
        author = self.request.query_params.get("author")
        if category is not None:
            queryset = queryset.filter(category__name__iexact=category)
        if author is not None:
            queryset = queryset.filter(author__profile__username=author)
        return queryset
 
    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), id=self.kwargs["id"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.user:
            context["author"] = self.request.user
        return context

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


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    @extend_schema(description="Retrieve a list of comments", responses=CommentSerializer)
    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        comments = Comment.objects.filter(post__id=post_id)
        return comments
    
    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), id=self.kwargs["id"])
        self.check_object_permissions(self.request, obj)
        return obj

    @extend_schema(
        description="Update a comment",
        request=CommentSerializer,
        responses=CommentSerializer,
    )
    def update(self, request, *args, **kwargs):
        comment = self.get_object()
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
        if request.user != comment.user:
            return Response(
                {"error": "You are not authorized to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        post_id = self.kwargs.get("post_id")
        try:
            post = get_object_or_404(Post, id=post_id)
        except Post.DoesNotExist:
            post = None
        context["post"] = post
        context["user"] = self.request.user
        return context