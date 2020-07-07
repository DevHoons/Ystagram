from django.contrib import admin
from .models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at", "updated_at"]
    raw_id_fields = ["name"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["name__username", "text", "created_at"]
    ordering = ["-updated_at", "-created_at"]
