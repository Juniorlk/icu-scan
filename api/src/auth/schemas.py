import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from src.projects.schemas import Project


class UserCreateModel(BaseModel):
    name: str = Field(max_length=25)
    username: str = Field(max_length=60)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "John Doe",
                "username": "johndoe",
                "email": "johndoe123@co.com",
                "password": "testpass123",
            }
        }
    }


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    update_at: datetime


class UserReadModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    name: str
    is_verified: bool
    created_at: datetime
    update_at: datetime

class UserProjectsModel(UserModel):
    projects : List[Project]


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)


class EmailModel(BaseModel):
    addresses : List[str]


class PasswordResetRequestModel(BaseModel):
    email: str


class PasswordResetConfirmModel(BaseModel):
    new_password: str
    confirm_new_password: str