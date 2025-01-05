import asyncio
from consumer import consume_messages
from fastapi import FastAPI
from producer import send_message
from db import init_db
from users import add_user, get_all_users, get_all_tasks
from models import UserReq
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app : FastAPI):
   print("Starting...")
   try:
      await init_db()
      # asyncio.create_task(consume_messages())

      print("Connected to the database")

      yield print("Shutting down...")
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
   return {"task_id": task_id}

@app.get("/get-tasks")
async def get_tasks_route():
   return await get_all_tasks()
