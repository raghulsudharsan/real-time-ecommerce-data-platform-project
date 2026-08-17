from pydantic import BaseModel
from uuid import UUID


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: UUID
    username: str
    role: str

    model_config = {
        "from_attributes": True
    }

from pydantic import BaseModel
from uuid import UUID


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: UUID
    username: str
    role: str

    model_config = {
        "from_attributes": True
    }

