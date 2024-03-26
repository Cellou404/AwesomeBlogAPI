from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import Profile
from blog.models import Post

User = get_user_model()


class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "email", "first_name", "last_name", "password"]


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = Profile
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "username",
            "profile_picture",
            "designation",
            "bio",
            "website",
            "github_link",
            "facebook_link",
            "linkedin_link",
            "tweeter_link",
            "phone",
            "date_joined",
            "date_updated",
        ]
        lookup_field = "username"

    def create(self, validated_data):
        # Use the custom method in the Profile model to handle creating users with profiles
        user = self.context["user"]
        profile = Profile.objects.create(user=user, **validated_data)
        return profile


class BasicUserProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Profile
        fields = [
            "id",
            "email",
            "username",
        ]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

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
            "date_created",
            "date_updated",
        ]
