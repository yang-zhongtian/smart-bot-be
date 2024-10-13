import uuid

from django.db import models


class Host(models.Model):
    id = models.UUIDField('host UUID', primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField('host name', max_length=255, unique=True)
    status_cam = models.BooleanField('cam status', default=False)
    status_command = models.BooleanField('command status', default=False)
    status_analyze = models.BooleanField('analyze status', default=False)
    created_at = models.DateTimeField('create time', auto_now_add=True)

    class Meta:
        verbose_name = 'host'
        verbose_name_plural = 'hosts'

    def __str__(self):
        return self.name
