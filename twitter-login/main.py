from fastapi import FastAPI
from db import init_db
from users import add_user, get_all_users
from models import UserCredentials
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app : FastAPI):
   print("Starting...")
   try:
      await init_db()
      print("Connected to the database")
      yield print("Shutting down...")
   except Exception as e:
      print(f"Couldn't connect to the database: {e}")

app = FastAPI(lifespan=lifespan)


@app.post("/add-user")
async def add_user_route(user: UserCredentials):
   return await add_user(user.model_dump())

@app.get("/get-users")
async def get_users_route():
   return await get_all_users()