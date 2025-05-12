from typing import Optional
from pydantic import BaseModel, EmailStr
from fastapi import HTTPException, status, APIRouter
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, user_list_schema
from bson import ObjectId

# http://127.0.0.1:8000

# Documentación de la API
# http://127.0.1:8000/docs
# http://127.0.1:8000/redoc

# http://127.0.1:8000/static/images/Black-Hole Nasa.png

ID = "_id"
EMAIL = "email"
USERNAME = "username"
AGE = "age"


router = APIRouter(prefix="/user_db",
                   tags=["user_db"],
                   responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}})



def get_user(field: str, value):
    """
    Get a user by a field.
    """
    if field not in ["email", "username", "age", "_id"]:
        raise HTTPException(status.HTTP_428_PRECONDITION_REQUIRED,
                            detail="Field must be email, username or age")
    try:
        user = user_schema(db_client.local.users.find_one({field: value}))
        return User(**user)
    except:
        return {"error": "User not found"}



# http://127.0.0.1:8000/users
# Devueve una lista de todos los usuarios
@router.get("/all", response_model=list[User], status_code=200)
async def users():
    """
    Devuelve una lista de todos los usuarios en la base de datos.
    """
    return user_list_schema(list(db_client.local.users.find({})))


# http://127.0.0.1:8000/user/
# Devuelve un mensaje de bienvenida
@router.get("/")
async def root():
    return "Hola Usuario!"

# Devuelve un usuario por id en caso de que exista, si no existe devuelve None
# Query parameter
@router.get("/byquery", response_model=User, status_code=200)
async def get_user_by_query(id: str):
    user = get_user(ID,ObjectId(id))
    if user is not None:
        return user
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail = "User not found")

# Devuelve un usuario por id en caso de que exista, si no existe devuelve None
@router.get("/{user_id}",  response_model=User, status_code=200)
async def user_id(user_id: str):
    return get_user(ID, ObjectId(user_id))

### Post ###

@router.post("/", response_model = User, status_code=201)
async def create_user(user: User):
    """
    Crea un nuevo usuario en la base de datos.
    """
    # Verifica si el usuario ya existe en la base de datos
    # Si existe, devuelve un mensaje de error
    if type(get_user(EMAIL,user.email)) == User:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="email already exists")

    user_dict = dict(user)
    del user_dict["id"]
    # Genera un nuevo id para el usuario
    id = db_client.local.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.local.users.find_one({"_id": id}))
    return User(**new_user)

### Put ###

# http://127.0.0.1:8000/user/{user_id}
# Actualiza un usuario por id en caso de que exista, si no existe devuelve un mensaje de error
@router.put("/{user_id}", response_model=User, status_code=200)
async def update_user(user_id: str, user: User):

    user_dict = dict(user)
    del user_dict["id"]

    db_client.local.users.find_one_and_replace(
        {ID: ObjectId(user_id)}, user_dict
    )
    return get_user(ID, ObjectId(user_id))
    

### Delete ###

### http://127.0.0.1:8000/user/{user_id} ###
# Elimina un usuario por id en caso de que exista, si no existe devuelve un mensaje de error
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    user = get_user(ID,ObjectId(user_id))
    if user:
        # Elimina el usuario de la base de datos
        db_client.local.users.delete_one({ID: ObjectId(user_id)})
        return user
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

