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
