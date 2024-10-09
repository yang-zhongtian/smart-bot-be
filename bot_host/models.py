from django.db import models


class Host(models.Model):
    id = models.UUIDField('host UUID', primary_key=True, editable=False)
    name = models.CharField('host name', max_length=255, unique=True)
    created_at = models.DateTimeField('create time', auto_now_add=True)

    class Meta:
        verbose_name = 'host'
        verbose_name_plural = 'hosts'

    def __str__(self):
        return self.name
