from fastapi import FastAPI
from routers import user, basic_auth_users, user_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(user.router)
app.include_router(basic_auth_users.router)
app.include_router(user_db.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return "Hola Mundo!"
