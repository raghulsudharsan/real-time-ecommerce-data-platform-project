from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(50),
        default="customer",
        nullable=False,
    )