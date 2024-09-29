from django.contrib.auth import authenticate, login
from ninja import Router, UploadedFile, File

from bot.exception import BadRequestError
from bot_face.chroma import search_face
from bot_face.face import FaceLib
from bot_face.models import UserFace
from .schema import PasswordLoginSchema, UserSchema

router = Router()


@router.post('/login', response=UserSchema)
def password_login(request, payload: PasswordLoginSchema):
    user = authenticate(request, **payload.dict())
    if user is None:
        raise BadRequestError('Invalid username or password')
    login(request, user)
    return user


@router.post('/login-face', response=UserSchema)
def face_login(request, face: UploadedFile = File(...)):
    face_lib = FaceLib()
    pic = face_lib.load_from_file(face.read())
    faces = face_lib.detect(pic)
    if len(faces) == 0:
        raise BadRequestError('Face detection failed')
    embedding = face_lib.normalize(faces[0].embedding).tolist()
    face_uuid = search_face(embedding, 0.65)
    if not face_uuid:
        raise BadRequestError('Face not found')
    user_face = UserFace.objects.get(face_uuid=face_uuid)
    login(request, user_face.user)
    return user_face.user
