from django.contrib import admin

from django.contrib import admin
from quiz_management_app.models import Quiz, Question


@admin.register(Quiz)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin configuration for Quiz instances."""

    list_display = ('id', "owner", "title", "description",
                    "video_url", "created_at", "updated_at")


@admin.register(Question)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin configuration for OfferDetails instances."""

    list_display = ("id", "question_title", "question_options", "answer",
                    "created_at", "updated_at")
