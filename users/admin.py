from django.contrib import admin
from .models import User, Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    ]
    list_display_links = [
        "email",
    ]
    list_filter = ["is_active", "is_staff", "is_superuser"]
    search_fields = ["firs_name", "last_name", "email"]
    date_hierarchy = "date_joined"
    list_per_page = 25


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "email",
        "date_joined",
    ]
    list_display_links = [
        "email",
    ]
    search_fields = ["firs_name", "last_name", "email"]
    date_hierarchy = "date_joined"
    list_per_page = 25
