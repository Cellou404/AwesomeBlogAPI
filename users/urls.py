from django.urls import path, include
from .views import UserProfileViewset, UserPostsViewset
from rest_framework.routers import DefaultRouter

# from rest_framework_nested import routers
from rest_framework_nested.routers import NestedDefaultRouter

router = DefaultRouter()
router.register("profiles", UserProfileViewset, basename="profiles")

users_router = NestedDefaultRouter(router, "profiles", lookup="profile")
users_router.register("posts", UserPostsViewset, basename="user-posts")
urlpatterns = [
    path("", include(router.urls)),
    path("", include(users_router.urls)),
]
