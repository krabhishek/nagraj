"""Authentication API routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from {{cookiecutter.project_slug}}.common.bounded_contexts.auth.application.dtos.user_dto import (
    UserDTO,
)
from {{cookiecutter.project_slug}}.common.bounded_contexts.auth.application.services.auth_service import (
    AuthService,
)
from {{cookiecutter.project_slug}}.common.core.config import settings
from {{cookiecutter.project_slug}}.common.core.logging import LoggerService

from ....dtos.auth_dtos import ChangePasswordRequest, RegisterUserRequest, TokenResponse
from ...dependencies.auth import get_auth_service, get_current_user
from ...security.jwt import JWTService

router = APIRouter(tags=["auth"])
logger = LoggerService().get_logger({"module": "auth_routes"})


@router.post(
    "/register",
    response_model=UserDTO,
    status_code=status.HTTP_201_CREATED,
    description="Register a new user",
)
async def register_user(
    request: RegisterUserRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserDTO:
    """Register a new user."""
    try:
        return await auth_service.register_user(request.email, request.password)
    except ValueError as e:
        logger.error(f"Registration failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


@router.post(
    "/login",
    response_model=TokenResponse,
    description="Authenticate user and return access token",
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    jwt_service: Annotated[JWTService, Depends()],
) -> TokenResponse:
    """Authenticate user and return access token."""
    try:
        user = await auth_service.authenticate_user(
            email=form_data.username,
            password=form_data.password,
        )
        access_token = jwt_service.create_access_token({"sub": str(user.id)})
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.jwt_access_token_expire_minutes * 60,
        )
    except ValueError as e:
        logger.error(f"Authentication failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to authenticate user",
        )


@router.post(
    "/change-password",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Change user password",
)
async def change_password(
    request: ChangePasswordRequest,
    current_user: Annotated[UserDTO, Depends(get_current_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> None:
    """Change user password."""
    try:
        await auth_service.change_password(
            user_id=current_user.id,
            current_password=request.current_password,
            new_password=request.new_password,
        )
    except ValueError as e:
        logger.warning(f"Password change failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Unexpected error during password change: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password",
        )
