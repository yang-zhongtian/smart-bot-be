from django.contrib import admin

from .models import FaceDetectionRecord


@admin.register(FaceDetectionRecord)
class FaceDetectionRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bot', 'face_image', 'created_at')
    list_filter = ('user',)
