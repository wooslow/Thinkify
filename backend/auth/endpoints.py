import logging

from fastapi import APIRouter, Depends, Response

from .service import AuthService
from .shemas import UserBaseSchema, UserRegisterSchema, UserLoginResponseSchema
from database import DatabaseSession

log = logging.getLogger(__name__)

auth_router = APIRouter(tags=["auth"])


@auth_router.post("/register", response_model=UserBaseSchema)
async def register(user: UserRegisterSchema, database: DatabaseSession):
    auth_service = AuthService(database)
    return await auth_service.register_user(user)


@auth_router.post("/login", response_model=UserLoginResponseSchema)
async def login(
    response: Response,
    user: UserRegisterSchema,
    database: DatabaseSession
):
    auth_service = AuthService(database)
    result = await auth_service.login_user(user)
    response.set_cookie(key="Authorization", value=result['access_token'], httponly=True)

    return result

