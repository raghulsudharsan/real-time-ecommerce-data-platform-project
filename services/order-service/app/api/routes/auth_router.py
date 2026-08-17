from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.schemas.auth import LoginRequest, TokenResponse
from jose import JWTError, jwt

from app.core.security import (
    SECRET_KEY,
    ALGORITHM,
    create_access_token,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


def get_auth_service() -> AuthService:
    return AuthService(UserRepository())


@router.post("/register", response_model=UserResponse)
def register(
    request: UserCreate,
    db: Session = Depends(get_db),
    service: AuthService = Depends(get_auth_service),
):
    return service.register_user(
        db=db,
        request=request,
    )

@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    service: AuthService = Depends(get_auth_service),
):
    return service.login_user(
        db=db,
        username=form_data.username,
        password=form_data.password,
    )

@router.post("/refresh")
def refresh_access_token(refresh_token: str):

    try:
        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token",
            )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token",
            )

        access_token = create_access_token({
            "sub": user_id,
        })

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token",
        )