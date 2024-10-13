from datetime import datetime
from uuid import UUID

from ninja import Schema, UploadedFile

from bot_auth.schema import UserSchema


class StatusSchema(Schema):
    cam: bool
    command: bool
    analyze: bool


class HostSchema(Schema):
    id: UUID
    name: str
    status: StatusSchema


class FaceRecordSchema(Schema):
    id: int
    user: UserSchema
    face_image: str
    created_at: datetime
