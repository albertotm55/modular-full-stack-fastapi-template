import re
from datetime import datetime
from typing import List, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    computed_field,
    field_validator,
    model_validator,
)


def validate_username(username: str) -> str:
    """
    Validate username according to Google Workspace guidelines.
    """
    if not username:
        raise ValueError("Username cannot be empty")

    # Convert to lowercase
    username = username.lower()

    # Check length (max 64 characters)
    if len(username) > 64:
        raise ValueError("Username cannot exceed 64 characters")

    # Check for reserved words
    reserved_words = ["abuse", "postmaster"]
    if username in reserved_words:
        raise ValueError(f"Username '{username}' is a reserved word and cannot be used")

    # Check allowed characters
    if not re.match(r"^[a-z0-9\-_'.]+$", username):
        raise ValueError(
            "Username can only contain letters (a-z), numbers (0-9),"
            " dashes (-), underscores (_), apostrophes ('), and periods (.)"
        )

    # Check for consecutive periods
    if ".." in username:
        raise ValueError("Username cannot contain consecutive periods")

    # Check first character (cannot be a period)
    if username.startswith("."):
        raise ValueError("Username cannot start with a period")

    # Check last character (cannot be a period)
    if username.endswith("."):
        raise ValueError("Username cannot end with a period")

    return username


class UserBase(BaseModel):
    username: Optional[str] = Field(
        None,
        min_length=1,
        max_length=64,
        description="Unique username following Google Workspace guidelines",
    )
    email: Optional[EmailStr] = Field(
        None, description="User's email address (optional)"
    )
    avatar_url: Optional[str] = Field(
        None, description="URL to the user's avatar image"
    )
    is_active: Optional[bool] = Field(
        True, description="Indicates if the user account is active"
    )
    is_superuser: Optional[bool] = Field(
        False, description="Indicates if the user has superuser privileges"
    )

    @field_validator("username")
    def validate_username_field(cls, v):
        if v is None:
            return v
        return validate_username(v)

    model_config = ConfigDict(extra="ignore")


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        description="Password for the user account, at least 8 characters",
    )

    @model_validator(mode="after")
    def set_username_from_email(self):
        if self.username is None and self.email is not None:
            self.username = validate_username(self.email.split("@", 1)[0])
        if self.username is None:
            raise ValueError("Username or email is required")
        return self


class UserRead(UserBase):
    username: str = Field(
        ...,
        min_length=1,
        max_length=64,
        description="Unique username following Google Workspace guidelines",
    )
    id: int = Field(..., description="Unique identifier for the user")
    is_superuser: bool = Field(
        ..., description="Indicates if the user has superuser privileges"
    )
    created_at: datetime = Field(
        ..., description="Timestamp when the user account was created"
    )

    @computed_field
    @property
    def full_name(self) -> str | None:
        return self.username

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(
        None,
        min_length=1,
        max_length=64,
        description="New username following Google Workspace guidelines",
    )
    avatar_url: Optional[str] = Field(
        None, description="New URL to the user's avatar image"
    )
    email: Optional[EmailStr] = Field(
        None, description="New email address for the user (optional)"
    )

    @field_validator("username")
    def validate_username_field(cls, v):
        if v is not None:
            return validate_username(v)
        return v

    is_active: Optional[bool] = Field(
        None, description="Indicates if the user account is active (optional)"
    )
    is_superuser: Optional[bool] = Field(
        None, description="Indicates if the user has superuser privileges (optional)"
    )
    password: Optional[str] = Field(None, min_length=8)

    model_config = ConfigDict(extra="ignore")


class UserPasswordUpdate(BaseModel):
    current_password: str = Field(..., description="Current password of the user")
    new_password: str = Field(
        ...,
        min_length=8,
        description="New password for the user account, at least 8 characters",
    )


class UserFilter(BaseModel):
    username: Optional[str] = Field(
        None, description="Filter by username (partial match)"
    )
    email: Optional[str] = Field(None, description="Filter by email (partial match)")
    is_active: Optional[bool] = Field(None, description="Filter by active status")
    created_at_from: Optional[datetime] = Field(
        None, description="Filter users created on or after this datetime"
    )
    created_at_to: Optional[datetime] = Field(
        None, description="Filter users created on or before this datetime"
    )


class UserSort(BaseModel):
    field: str = Field("id", description="Field to sort by")
    direction: str = Field("asc", description="Sort direction: asc or desc")


class UserListResponse(BaseModel):
    users: List[UserRead] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users")
    skip: int = Field(..., description="Number of users skipped")
    limit: int = Field(..., description="Maximum number of users returned")

    @computed_field
    @property
    def data(self) -> List[UserRead]:
        return self.users

    @computed_field
    @property
    def count(self) -> int:
        return self.total
