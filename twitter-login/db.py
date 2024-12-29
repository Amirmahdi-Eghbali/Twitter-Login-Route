from decouple import config
from motor.motor_asyncio import AsyncIOMotorClient
from models import UserCredentials, TaskStatus
from beanie import init_beanie

async def init_db():
    db_uri = config("MONGO_URI")
    db_name = config("DB_NAME")

    client = AsyncIOMotorClient(db_uri)
    await init_beanie(
        database = client[db_name],
        document_models = [UserCredentials, TaskStatus]
    )
