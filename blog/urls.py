from django.urls import path, include
from .views import PostViewSet, CommentViewSet, CategoryViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from rest_framework_nested.routers import NestedDefaultRouter

router = DefaultRouter()
router.register("posts", PostViewSet, basename="posts")
router.register("categories", CategoryViewSet)

blog_router = NestedDefaultRouter(router, 'posts', lookup='post')
blog_router.register('comments', CommentViewSet, basename='post-comments')

urlpatterns = [
    path("", include(router.urls)),
    path("", include(blog_router.urls))
]
