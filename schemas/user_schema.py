from pydantic import BaseModel
from typing import Optional


class UserSignUpSchema(BaseModel):
    username: str
    password: str
    balance: float


class UserSignInSchema(BaseModel):
    username: str
    password: str
    balance: Optional[float] = None


class UserDataViewSchema(BaseModel):
    username: str
    balance: float

