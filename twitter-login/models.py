from beanie import Document, Indexed
from typing import Optional

from pydantic.v1 import BaseModel, validator


class UserCredentials(Document):
    username : str = Indexed(unique=True)
    password : str
    phone_number : str = Indexed(unique=True)
    email : Optional[str] = Indexed(unique=True)

    class Settings:
        collections = "User_credentials"

class TaskStatus(Document):
    task_id : str = Indexed(unique=True)
    status : str

    class Settings:
        collections = "task_statuses"
#
class UserReq(BaseModel):
   username : str
   password : str
   phone_number : str
   email : str | None = None


   @validator("username")
   def validate_username(cls, value):
      if not (3 <= len(value)):
         raise ValueError("Username must be at least 3characters.")
      return value

   @validator("password")
   def validate_password(cls, value):
      if len(value) < 6:
         raise ValueError("Password must be at least 6 characters.")
      return value

   @validator("phone_number")
   def validate_phone_number(cls, value):
      if not value.startswith("+") or not value[1:].isdigit():
         raise ValueError("Phone number must start with '+' and contain only digits.")
      return value
