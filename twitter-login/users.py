from fastapi import HTTPException
from models import UserCredentials, UserReq, TaskStatus

async def add_user(request: UserReq):

        username = await UserCredentials.find_one({"username":request.username})
        if username:
            raise HTTPException(status_code=400, detail="Username already exists")

        phone = await UserCredentials.find_one({"phone_number": request.phone_number})
        if phone:
            raise HTTPException(status_code=400, detail="phone number already exists")
        if request.email:
            email = await UserCredentials.find_one({"email": request.email})
            if email:
                raise HTTPException(status_code=400, detail="email already exists")

        new_user = UserCredentials(**request.dict())
        await new_user.insert()
        return {"message": "User created successfully"}


async def get_all_users():
    return await UserCredentials.find_all().to_list()

async def get_all_tasks():
    return await TaskStatus.find_all().to_list()
