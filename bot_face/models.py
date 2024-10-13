import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User

from .chroma import delete_face, save_face
from .face import FaceLib


class UserFace(models.Model):
    user = models.OneToOneField(User, verbose_name='user', on_delete=models.CASCADE, related_name='userface')
    face_image = models.ImageField('face image', upload_to='face_images')
    face_uuid = models.UUIDField('face UUID', blank=True, null=True, unique=True, db_index=True)
    created_at = models.DateTimeField('create time', auto_now_add=True)

    class Meta:
        verbose_name = 'user face'
        verbose_name_plural = 'user faces'

    def save(self, *args, **kwargs):
        previous_uuid = None

        if self.pk:
            try:
                previous_instance = self.__class__.objects.get(pk=self.pk)
                previous_uuid = previous_instance.face_uuid
            except ObjectDoesNotExist:
                pass

        if self.face_image:
            face_lib = FaceLib()
            pic = face_lib.load_from_file(self.face_image.read())
            faces = face_lib.detect(pic)
            if len(faces) != 1:
                raise ValueError('Face detection failed')
            embedding = face_lib.normalize(faces[0].embedding).tolist()

            if previous_uuid:
                delete_face(previous_uuid)

            self.face_uuid = uuid.uuid4()
            save_face(self.face_uuid, embedding)
        super().save(*args, **kwargs)
