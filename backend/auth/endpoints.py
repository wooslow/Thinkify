import logging

from fastapi import APIRouter, Depends

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
async def login(user: UserRegisterSchema, database: DatabaseSession):
    auth_service = AuthService(database)
    return await auth_service.login_user(user)


@auth_router.get("/me")
async def get_me(user: UserBaseSchema = Depends(AuthService.get_current_user)):
    return user
