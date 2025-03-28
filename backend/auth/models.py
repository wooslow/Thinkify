from sqlalchemy import String, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from database import CustomBase


class UserBaseModel(CustomBase):
    __tablename__ = "users_base"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hash_password: Mapped[str] = mapped_column(String)
