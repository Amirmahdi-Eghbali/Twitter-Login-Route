from fastapi import FastAPI
from pydantic.v1 import BaseModel, validator
from producer import send_message
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

class TwitterLoginRequest(BaseModel):
   username : str
   password : str
   phone_number : str
   email : str | None = None


   @validator("username")
   def validate_username(self, value):
      if not (3 <= len(value)):
         raise ValueError("Username must be at least 3characters.")
      return value

   @validator("password")
   def validate_password(self, value):
      if len(value) < 6:
         raise ValueError("Password must be at least 6 characters.")
      return value

   @validator("phone_number")
   def validate_phone_number(self, value):
      if not value.startswith("+") or not value[1:].isdigit():
         raise ValueError("Phone number must start with '+' and contain only digits.")
      return value


@app.post("/add-user")
async def add_user_route(user: UserCredentials):
   return await add_user(user.model_dump())

@app.get("/get-users")
async def get_users_route():
   return await get_all_users()

@app.post("twitter-login")
async def login(request: TwitterLoginRequest):

   task_id = send_message(request)
   return {"task_id": task_id}

