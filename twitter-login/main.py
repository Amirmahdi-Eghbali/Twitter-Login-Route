import asyncio
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils import create_jwt, verify
from consumer import consume_messages
from fastapi import FastAPI, Depends
from producer import send_message
from db import init_db
from users import add_user, get_all_users, get_all_tasks, get_by_id
from models import UserReq
from contextlib import asynccontextmanager


auth_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    token = credentials.credentials
    return verify(token)

@asynccontextmanager
async def lifespan(app : FastAPI):
   print("Starting...")
   try:
      await init_db()
      asyncio.create_task(consume_messages())

      print("Connected to the database")

      yield
   except Exception as e:
      print(f"Couldn't connect to the database: {e}")

app = FastAPI(lifespan=lifespan)


@app.post("/add-user")
async def add_user_route(request: UserReq):
   return await add_user(request)

@app.get("/get-users")
async def get_users_route():
   return await get_all_users()

@app.post("/twitter-login")
async def login(request: UserReq):
   task_id = send_message(request)
   token = create_jwt({"username": request.username, "phone_number" : request.phone_number, "email" : request.email})

   return {"token": token, "task_id": task_id}

@app.get("/get-tasks")
async def get_tasks_route(user: dict = Depends(get_current_user)):
   return await get_all_tasks()

@app.get("/get-by-id")
async def gbi_route(task_id, user: dict = Depends(get_current_user)):
   return await get_by_id(task_id)

@app.get("/current-user")
async def current_user_route(user: dict = Depends(get_current_user)):
   return user
