from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from .api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
