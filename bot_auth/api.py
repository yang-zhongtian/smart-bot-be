import uuid
from typing import List

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from ninja import Router, UploadedFile, File
from ninja.security import django_auth

from bot.exception import BadRequestError
from bot_face.chroma import search_face, delete_face, save_face
from bot_face.face import FaceLib
from bot_face.models import UserFace
from .schema import PasswordLoginSchema, UserSchema, UserFaceSchema, UserFaceRecordSchema

router = Router()


@router.post('/csrf/')
@ensure_csrf_cookie
@csrf_exempt
def get_csrf_token(request):
    return HttpResponse()


@router.post('/login/', response=UserSchema)
def password_login(request, payload: PasswordLoginSchema):
    user = authenticate(request, **payload.dict())
    if user is None:
        raise BadRequestError('Invalid username or password')
    login(request, user)
    return user


@router.post('/login-face/', response=UserSchema)
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


@router.post('/register/', response=UserSchema)
def register(request, payload: PasswordLoginSchema):
    user = User.objects.create_user(**payload.dict())
    login(request, user)
    return user


@router.get('/user/', response=List[UserFaceSchema])
def user_list(request):
    users = User.objects.all()
    result = []
    for user in users:
        face = user.userface
        last_detected = user.facedetectionrecord_set.last()
        result.append(UserFaceSchema(
            id=user.id,
            username=user.username,
            face_image=face.face_image.url if face else None,
            last_detected=last_detected.created_at if last_detected else None,
            credit=user.facedetectionrecord_set.count()
        ))
    return result


@router.get('/user/{int:user_id}/', response=List[UserFaceRecordSchema])
def user_detail(request, user_id: int):
    user = User.objects.get(id=user_id)
    return user.facedetectionrecord_set.all().order_by('-created_at')


@router.get('/user/current/', response=UserFaceSchema, auth=django_auth)
def user_current(request):
    user = request.auth
    try:
        face = user.userface
    except UserFace.DoesNotExist:
        face = None
    last_detected = user.facedetectionrecord_set.last()
    return UserFaceSchema(
        id=user.id,
        username=user.username,
        face_image=face.face_image.url if face else None,
        last_detected=last_detected.created_at if last_detected else None,
        credit=user.facedetectionrecord_set.count()
    )


@router.post('/user/current/', auth=django_auth)
def upload_face(request, face: UploadedFile = File(...)):
    user = request.auth  # type: User

    UserFace.objects.update_or_create(defaults={
        'face_image': face,
    }, user=user)

    return {'status': 'success'}
