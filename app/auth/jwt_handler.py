import os
import sys
from dotenv import load_dotenv
import time
from datetime import datetime
from fastapi import HTTPException, status
from jose import jwt, JWTError


env_path = os.path.join(sys.path[0], ".env")
load_dotenv(env_path)
SECRET_KEY = os.getenv("SECRET_KEY")


def create_access_token(user: str) -> str:
    payload = {"user": user, "expires": time.time() + 3600}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def verify_access_token(token: str) -> dict:
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        expire = data.get("expires")
        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied",
            )
        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Token expired!"
            )
        return data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )
