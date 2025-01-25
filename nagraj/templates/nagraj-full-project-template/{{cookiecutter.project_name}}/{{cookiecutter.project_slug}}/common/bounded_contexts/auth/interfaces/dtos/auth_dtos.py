from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ValidationInfo, field_validator


class RegisterUserRequest(BaseModel):
    """Request model for user registration."""

    email: EmailStr = Field(description="User's email address")
    password: str = Field(description="User's password", min_length=8)


class LoginRequest(BaseModel):
    """Request model for user login."""

    email: EmailStr = Field(description="User's email address")
    password: str = Field(description="User's password")


class ChangePasswordRequest(BaseModel):
    """Request model for password change."""

    current_password: str = Field(description="Current password")
    new_password: str = Field(description="New password", min_length=8)

    @field_validator("new_password")
    def validate_new_password(cls, value: str, info: ValidationInfo) -> str:
        """Validate that new password is different from current."""
        current_password = info.data.get("current_password")
        if current_password and value == current_password:
            raise ValueError("New password must be different from current password")
        return value


class UserResponse(BaseModel):
    """Response model for user data."""

    id: str = Field(description="User's unique identifier")
    email: EmailStr = Field(description="User's email address")
    is_active: bool = Field(description="Whether the user account is active")
    created_at: datetime = Field(description="When the user was created")
    updated_at: datetime = Field(description="When the user was last updated")
    last_login: Optional[datetime] = Field(
        None, description="When the user last logged in"
    )


class TokenResponse(BaseModel):
    """Response model for authentication token."""

    access_token: str = Field(description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(description="Token expiration time in seconds")
