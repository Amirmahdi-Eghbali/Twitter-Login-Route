from beanie import Document, Indexed
from typing import Optional

class UserCredentials(Document):
    username : str = Indexed(str, unique=True)
    password : str
    phone_number : str = Indexed(str, unique=True)
    email : Optional[str] = Indexed(str, unique=True)

    class Settings:
        collections = "User_credentials"

class TaskStatus(Document):
    task_id : str = Indexed(unique=True)
    status : str

    class Settings:
        collections = "task_statuses"