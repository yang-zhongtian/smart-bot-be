# Generated by Django 5.1.1 on 2024-09-25 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_face', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userface',
            name='face_image',
            field=models.ImageField(default='', upload_to='face_images', verbose_name='face image'),
            preserve_default=False,
        ),
    ]
