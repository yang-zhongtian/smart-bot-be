import logging
from io import BytesIO

from PIL import Image, ImageDraw
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.utils import timezone

from bot_face.chroma import search_face
from bot_face.face import FaceLib
from bot_face.models import UserFace
from bot_host.models import Host
from bot_mall.models import FaceDetectionRecord


def analyze_face(bot_id: str, face_buf: bytes):
    face_lib = FaceLib()
    pic = face_lib.load_from_file(face_buf)
    faces = face_lib.detect(pic)
    if len(faces) > 0:
        face_pic = Image.frombytes("RGB", (pic.shape[1], pic.shape[0]), pic)
        draw = ImageDraw.Draw(face_pic)
        embedding = face_lib.normalize(faces[0].embedding).tolist()
        face_uuid = search_face(embedding, 0.5)
        try:
            user_face = UserFace.objects.get(face_uuid=face_uuid)
            draw.rectangle(faces[0].bbox, outline="green")
            draw.text((faces[0].bbox[0], faces[0].bbox[1]), user_face.user.username, fill="green")
            temp_img = BytesIO()
            face_pic.save(temp_img, format="JPEG", quality=100, optimize=False)
            image_file = ContentFile(temp_img.getvalue(), name=f"{str(int(timezone.now().timestamp()))}.jpg")
            bot = Host.objects.get(id=bot_id)
            FaceDetectionRecord.objects.create(user=user_face.user, face_image=image_file, bot=bot)
            return True
        except ObjectDoesNotExist:
            logging.warning("Face not found")
    return False
