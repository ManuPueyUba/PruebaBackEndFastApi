import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: EmailStr
    age: int
