"""

Repository for user

All methods that interact with the database should be here
Only database models or nothing should be returned from this class

"""

import json
import random

from sqlalchemy.future import select
from snowflake import SnowflakeGenerator
from .shemas import UserBaseSchema, UserRegisterSchema
from .models import UserBaseModel

from database import DatabaseSession

snowflake = SnowflakeGenerator(42)


class UserRepository:
    def __init__(self, database: DatabaseSession) -> None:
        self.database: DatabaseSession = database

    async def _get_user_in_database(self, email: str) -> UserBaseModel | None:
        """ Get user from database """
        query = select(UserBaseModel).where(UserBaseModel.email == email)
        result = await self.database.execute(query)
        user = result.scalars().first()
        return user

    async def get_user_by_email(self, email: str) -> UserBaseModel | None:
        """ Get user by email """
        user = await self._get_user_in_database(email)

        return user

    async def create_user(self, user: UserRegisterSchema | UserBaseSchema) -> UserBaseModel:
        """ Create user """
        user = UserBaseModel(
            id=next(SnowflakeGenerator(42)),
            email=user.email,
            hash_password=user.hash_password,
        )
        self.database.add(user)
        await self.database.commit()

        return user

    async def get_or_create(self, user_input: UserRegisterSchema | UserBaseSchema) -> UserBaseModel:
        """ Get or create user """
        user = await self.get_user_by_email(user_input.email)

        if not user:
            user = await self.create_user(user_input)

        return user
