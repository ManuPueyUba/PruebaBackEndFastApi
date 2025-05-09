import uuid
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from fastapi import HTTPException, status, APIRouter

class User(BaseModel):
    username: str
    name: str
    surname: str
    email: EmailStr
    age: int
    disabled: bool


class UserDB(User):
    password: str


users_db = {

    "johndoe": {
        "username": "johndoe",
        "name": "John",
        "surname": "Doe",
        "email": "JohnDoe@gmail.com",
        "age": 30,
        "disabled": False,
        "password": "secret1234",
    },
    "alice": {
        "username": "alice",
        "name": "Alice",
        "surname": "Smith",
        "email": "aliceSmith@gmail.com",
        "age": 28,
        "disabled": True,
        "password": "unaPassword1234",
    }

}