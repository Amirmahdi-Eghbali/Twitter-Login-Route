from fastapi import HTTPException
from models import UserCredentials

async def add_user(user: dict):

        username = await UserCredentials.find_one({"username":user["username"]})
        if username:
            raise HTTPException(status_code=400, detail="Username already exists")

        phone = await UserCredentials.find_one({"phone_number": user["phone_number"]})
        if phone:
            raise HTTPException(status_code=400, detail="phone number already exists")
        if user.get("email"):
            email = await UserCredentials.find_one({"email": user["email"]})
            if email:
                raise HTTPException(status_code=400, detail="email already exists")

        new_user = UserCredentials(**user)
        await new_user.insert()
        return {"message": "User created successfully"}


async def get_all_users():
    return await UserCredentials.find_all().to_list()
