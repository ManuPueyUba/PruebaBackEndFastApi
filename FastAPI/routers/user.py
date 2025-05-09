import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr
from fastapi import HTTPException, status, APIRouter

# http://127.0.0.1:8000

# Documentación de la API
# http://127.0.1:8000/docs
# http://127.0.1:8000/redoc

# http://127.0.1:8000/static/images/Black-Hole Nasa.png


router = APIRouter(prefix="/user", tags=["user"])

class User(BaseModel):
    id: Optional[uuid.UUID] = None
    name: str
    surname: str
    email: EmailStr
    age: int

user_list = [
    User(id=uuid.uuid4(), name="Jane", surname = "Doe", email="janedoe@gmail.com", age=25),
    User(id=uuid.uuid4(), name="John", surname= "Doe", email="johndoe@gmail.com", age=30),
    User(id=uuid.uuid4(), name="Alice", surname= "Smith", email="alicesmith@gmail.com", age=28),
        ]

print("IDs generados:")
for user in user_list:
    print(user.id)

def get_user_by_id(user_id: uuid.UUID):
    if not isinstance(user_id, uuid.UUID):
        raise HTTPException(status.HTTP_428_PRECONDITION_REQUIRED, detail="Id must be a uuid")

    return next((user for user in user_list if user.id == user_id), None)


# http://127.0.0.1:8000/users
# Devueve una lista de todos los usuarios
@router.get("/all")
async def users():
    return user_list

# http://127.0.0.1:8000/user/
# Devuelve un mensaje de bienvenida
@router.get("/")
async def root():
    return "Hola Usuario!"

# Devuelve un usuario por id en caso de que exista, si no existe devuelve None
# Query parameter
@router.get("/byquery", response_model=User, status_code=200)
async def get_user_by_query(id: uuid.UUID):
    user = get_user_by_id(id)
    if user is not None:
        return user
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail = "User not found")

# Devuelve un usuario por id en caso de que exista, si no existe devuelve None
@router.get("/{user_id}",  response_model=User, status_code=200)
async def user_id(user_id: uuid.UUID):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail = "User not found")
    return user

### Post ###

@router.post("/", response_model = User, status_code=201)
async def create_user(user: User):
    user.id = uuid.uuid4()
    user_list.append(user)
    return user

### Put ###

# http://127.0.0.1:8000/user/{user_id}
# Actualiza un usuario por id en caso de que exista, si no existe devuelve un mensaje de error
@router.put("/{user_id}", response_model=User, status_code=200)
async def update_user(user_id: uuid.UUID, user: User):

    existing_user = get_user_by_id(user_id)
    if existing_user:
        existing_user.name = user.name
        existing_user.surname = user.surname
        existing_user.email = user.email
        existing_user.age = user.age
        return existing_user
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

### Delete ###

### http://127.0.0.1:8000/user/{user_id} ###
# Elimina un usuario por id en caso de que exista, si no existe devuelve un mensaje de error
@router.delete("/{user_id}", status_code=200)
async def delete_user(user_id: uuid.UUID):
    user = get_user_by_id(user_id)
    if user:
        user_list.remove(user)
        return user
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

