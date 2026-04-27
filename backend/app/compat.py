from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import schemas as common_schemas
from .auth import schemas as auth_schemas
from .auth import security
from .auth.service import auth_service
from .database.core import get_db
from .dependencies import get_current_active_user
from .users import schemas as user_schemas
from .users.models import User

router = APIRouter()

CurrentUser = Annotated[User, Depends(get_current_active_user)]


class NewPassword(BaseModel):
    token: str
    new_password: str


@router.post("/login/access-token", response_model=auth_schemas.Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = auth_service.authenticate_user(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user is inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return auth_schemas.Token(
        access_token=security.create_access_token(subject=user.id),
        refresh_token=security.create_refresh_token(subject=user.id),
    )


@router.post("/login/test-token", response_model=user_schemas.UserRead)
def test_token(current_user: CurrentUser):
    return current_user


@router.post("/password-recovery/{email}", response_model=common_schemas.Message)
def recover_password(email: str):
    return common_schemas.Message(
        message=f"If {email} exists, a password recovery email will be sent."
    )


@router.post("/reset-password/", response_model=common_schemas.Message)
def reset_password(password_data: NewPassword):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Password recovery tokens are not implemented in this backend.",
    )


@router.post("/password-recovery-html-content/{email}", response_model=str)
def recover_password_html_content(email: str):
    return f"Password recovery preview is not implemented for {email}."


@router.post("/utils/test-email/", response_model=common_schemas.Message)
def test_email(email_to: str):
    return common_schemas.Message(message=f"Test email endpoint called for {email_to}")


@router.get("/utils/health-check/", response_model=bool)
def health_check():
    return True
