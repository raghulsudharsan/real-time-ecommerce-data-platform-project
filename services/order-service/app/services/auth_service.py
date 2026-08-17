from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,create_refresh_token,
    hash_password,
    verify_password,
)
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class AuthService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register_user(
        self,
        db: Session,
        request: UserCreate,
    ):
        existing_user = self.repository.get_user_by_username(
            db=db,
            username=request.username,
        )

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Username already exists",
            )

        password_hash = hash_password(
            request.password
        )

        user = self.repository.create_user(
            db=db,
            username=request.username,
            password_hash=password_hash,
        )

        return user

    def login_user(
        self,
        db: Session,
        username: str,
        password: str,
    ):
        # 1. Find user
        user = self.repository.get_user_by_username(
            db=db,
            username=username,
        )

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password",
            )

        # 2. Verify password
        if not verify_password(
            password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password",
            )

        # 3. Create JWT access token
        access_token = create_access_token({
            "sub": str(user.id),
            "role": user.role,
})

        refresh_token = create_refresh_token({
            "sub": str(user.id),
})

        # 4. Return token
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }