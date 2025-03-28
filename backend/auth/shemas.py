from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    id: int
    email: str
    hash_password: str


class UserRegisterSchema(BaseModel):
    email: str
    hash_password: str


class UserLoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
