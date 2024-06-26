from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from .models import *
from .serializers import UserProfileSerializer, UserPostSerializer

from blog.models import Post
from blog.permissions import IsAuthor

# Create your views here.


class UserProfileViewset(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    pagination_class = PageNumberPagination
    # permission_classes = (IsAdminUser, IsAuthenticatedOrReadOnly)
    lookup_field = "username"

    def get_queryset(self):
        queryset = Profile.objects.order_by("-date_joined")
        return queryset

    def get_serializer_context(self):
        """add request to the serializer context"""
        if self.request.user:
            user = self.request.user
            return {"user": user}

    extend_schema(
        description="Update a profile. Only the according user can perform this action",
        responses=UserProfileSerializer,
    )

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        if request.user != profile.user:
            return Response(
                {"error": "You do not have permission to edit this profile"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super(UserProfileViewset, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs) -> Response:
        profile = self.get_object()
        # check that we are deleting our own account and there are no associated posts or followers
        if request.user != profile.user:
            return Response(
                {"error": "Your do not have permission to delete this profile"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super(UserProfileViewset, self).destroy(request, *args, **kwargs)


# User Post Viewset

class UserPostsViewset(viewsets.ModelViewSet):
    serializer_class = UserPostSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthor | IsAuthenticatedOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        author_id = self.kwargs.get("profile_username")
        print(author_id)
        queryset = Post.objects.filter(author__profile__username=author_id)
        return queryset

    # Get serializer context, (to perform create)

    def get_serializer_context(self):
        if self.request.user:
            author = self.kwargs.get("profile_username")
            return {"author": author}
    
    @extend_schema(
        description="Update a post. Only the Author of the post can perform this action",
        responses=UserPostSerializer,
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
        request=UserPostSerializer,
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