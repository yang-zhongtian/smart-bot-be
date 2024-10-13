from datetime import datetime
from typing import Optional
from uuid import UUID

from ninja import Schema


class UserSchema(Schema):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str


class PasswordLoginSchema(Schema):
    username: str
    password: str


class UserFaceSchema(Schema):
    id: int
    username: str
    face_image: Optional[str]
    last_detected: Optional[datetime]
    credit: int


class HostSchema(Schema):
    id: UUID
    name: str


class UserFaceRecordSchema(Schema):
    id: int
    bot: HostSchema
    face_image: str
    created_at: datetime
