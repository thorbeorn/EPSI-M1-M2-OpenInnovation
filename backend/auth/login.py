# auth/login.py
from fastapi import APIRouter, HTTPException
from datetime import timedelta
from modules.auth import authenticate_user, create_token, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from pydantic import BaseModel
from bdd.jwt import add_refresh_token_db, add_access_token_db

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    username: str
    password: str
    device: str

@router.post("/login")
def login(login_request: LoginRequest):
    user = authenticate_user(login_request.username, login_request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_token(
        {"sub": f"{user["username"]},{login_request.device}"},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    refresh_token = create_token(
        {"sub": user["username"], "type": "refresh"},
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    add_refresh_token_db(refresh_token, user["username"], REFRESH_TOKEN_EXPIRE_DAYS)
    add_access_token_db(refresh_token, access_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
