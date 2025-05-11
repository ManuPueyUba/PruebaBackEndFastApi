from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid

router = APIRouter(prefix="/basic_auth", tags=["basic_auth"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/basic_auth/login")

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
        "username":"johndoe",
        "name":"John",
        "surname":"Doe",
        "email":"JohnDoe@gmail.com",
        "age":30,
        "disabled":False,
        "password":"secret1234",
        },
    "alice": {
        "username":"alice",
        "name":"Alice",
        "surname":"Smith",
        "email":"aliceSmith@gmail.com",
        "age":28,
        "disabled":True,
        "password":"unaPassword1234",
    }
    
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    return None

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    return None

async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=400,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me", response_model=User)
async def me(user: User = Depends(current_user)):
    return user