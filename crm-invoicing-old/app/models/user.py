from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastkit_core.database import BaseWithTimestamps

class User(BaseWithTimestamps, SQLAlchemyBaseUserTableUUID):
    __tablename__ = "users"

    first_name: Mapped[str | None] = mapped_column(String(100))
    last_name: Mapped[str | None] = mapped_column(String(100))
    locale: Mapped[str] = mapped_column(String(5), default="en")
