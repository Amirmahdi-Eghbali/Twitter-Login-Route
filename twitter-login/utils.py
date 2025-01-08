import bcrypt
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException

def hash_password(password: str) -> str:

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


SECRET_KEY = "Who-knows?"

def create_jwt(data: dict):

    temp = data.copy()
    expire = datetime.now() + timedelta(minutes=30)
    temp.update({"exp": expire})
    return jwt.encode(temp, SECRET_KEY, algorithm="HS256")

def verify(token: str):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="token is Invalid")

