import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from jose import jwt, JWTError

from .repository import UserRepository
from .models import UserBaseModel
from .shemas import UserRegisterSchema, UserBaseSchema

from database import DatabaseSession

load_dotenv()
security = HTTPBearer(scheme_name="Authorization")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, database: DatabaseSession) -> None:
        self.user_repository = UserRepository(database)

    async def register_user(self, user: UserRegisterSchema) -> UserBaseSchema:
        """ Function to register a new user """
        user.hash_password = self.hash_password(user.hash_password)
        action = await self.user_repository.get_or_create(user)

        return UserBaseSchema(**action.model_dump())

    async def login_user(self, user: UserRegisterSchema) -> dict:
        """ Authenticate user and return JWT tokens """
        db_user = await self.user_repository.get_user_by_email(email=user.email)
        if db_user is None or not self.check_password(user.hash_password, db_user.hash_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        access_token = self.create_access_token({"email": db_user.email})
        refresh_token = self.create_refresh_token({"email": db_user.email})

        return {"access_token": access_token, "refresh_token": refresh_token}

    @staticmethod
    def create_access_token(data: dict) -> str:
        """ Generate an access token """
        to_encode = data.copy()
        to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=40)})
        return jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm="HS256")

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        """ Generate a refresh token """
        to_encode = data.copy()
        to_encode.update({"exp": datetime.utcnow() + timedelta(days=7)})
        return jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm="HS256")

    async def refresh_access_token(self, refresh_token: str) -> dict:
        """ Refresh access token using a refresh token """
        try:
            payload = jwt.decode(refresh_token, os.getenv("SECRET_KEY"), algorithms="HS256")
            email: str = payload.get("email")
            if email is None:
                raise HTTPException(status_code=401, detail="Invalid refresh token")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        new_access_token = self.create_access_token({"email": email})
        return {"access_token": new_access_token}

    @staticmethod
    def hash_password(password: str) -> str:
        """ Hash a password using bcrypt """
        return pwd_context.hash(password)

    @staticmethod
    def check_password(plain_password: str, hashed_password: str) -> bool:
        """ Verify a password against its hash """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Security(security),
        db: DatabaseSession = DatabaseSession,
    ) -> UserBaseModel:
        """ Function to get current user from token """
        token = credentials.credentials
        secret_key = os.getenv("SECRET_KEY")

        try:
            payload = jwt.decode(token, secret_key, algorithms="HS256")
            email: str = payload.get("email")

            if email is None:
                raise HTTPException(status_code=401, detail="Invalid token")

        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user = await UserRepository(db).get_user_by_email(email=email)

        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    @staticmethod
    async def get_currect_user_by_cookie(
        auth: HTTPAuthorizationCredentials = Security(security),
        db: DatabaseSession = DatabaseSession,
    ):
        secret_key = os.getenv("SECRET_KEY")

        try:
            payload = jwt.decode(auth.credentials, secret_key, algorithms="HS256")
            email: str = payload.get("email")

            if email is None:
                raise HTTPException(status_code=401, detail="Invalid token")

        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user = await UserRepository(db).get_user_by_email(email=email)

        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user
