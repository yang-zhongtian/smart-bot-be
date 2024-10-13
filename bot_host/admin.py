from django.contrib import admin

from .models import Host


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status_cam', 'status_command', 'status_analyze', 'created_at')
