from django.db import models
from django.contrib.auth.models import User

from bot_host.models import Host


class FaceDetectionRecord(models.Model):
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    bot = models.ForeignKey(Host, verbose_name='Bot', on_delete=models.CASCADE)
    face_image = models.ImageField(verbose_name='Face Image', upload_to='face_detection_record')
    created_at = models.DateTimeField(verbose_name='Created At', auto_now_add=True)

    class Meta:
        verbose_name = 'Face Detection Record'
        verbose_name_plural = 'Face Detection Records'
        get_latest_by = 'created_at'
