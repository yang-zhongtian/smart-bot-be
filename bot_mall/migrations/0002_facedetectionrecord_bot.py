# Generated by Django 5.1.1 on 2024-10-12 11:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_host', '0005_host_status_analyze_host_status_cam_and_more'),
        ('bot_mall', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='facedetectionrecord',
            name='bot',
            field=models.ForeignKey(default='bbd3bebc2c614ae1a9cebc4de8bf38d2', on_delete=django.db.models.deletion.CASCADE, to='bot_host.host', verbose_name='Bot'),
            preserve_default=False,
        ),
    ]
