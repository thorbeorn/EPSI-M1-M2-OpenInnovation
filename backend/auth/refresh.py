import os
from fastapi import APIRouter, HTTPException
from datetime import timedelta, datetime
from jose import jwt, JWTError
from modules.auth_mod import create_token
from pydantic import BaseModel
from bdd.auth_bdd import get_refresh_token, remove_access_token, add_access_token_db
from dotenv import load_dotenv

load_dotenv()
router = APIRouter(prefix="/auth", tags=["auth"])

class refreshRequest(BaseModel):
    refresh_token: str

@router.post("/refresh")
def refresh_token(refresh_token: refreshRequest):
    try:
        payload = jwt.decode(refresh_token.refresh_token, os.getenv('JWT_SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    row = get_refresh_token(refresh_token.refresh_token)
    if not row:
        raise HTTPException(status_code=401, detail="Refresh token not found")
    
    expires_at_str = row[0]
    expires_at = datetime.fromisoformat(expires_at_str)
    
    if expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token expired")

    new_access_token = create_token(
        {"sub": payload["sub"]},
        timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    )
    remove_access_token(refresh_token.refresh_token)
    add_access_token_db(refresh_token.refresh_token, new_access_token)

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }
