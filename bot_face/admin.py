from django.contrib import admin
from .models import UserFace


@admin.register(UserFace)
class UserFaceAdmin(admin.ModelAdmin):
    list_display = ('user', 'face_uuid', 'created_at')
    search_fields = ('user__username', 'face_uuid')
    readonly_fields = ('face_uuid', 'created_at')
