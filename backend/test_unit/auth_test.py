import os
from fastapi import APIRouter, HTTPException, Header, Depends
from jose import jwt, JWTError
from bdd.auth_bdd import get_access_token
from dotenv import load_dotenv

load_dotenv()
router = APIRouter(prefix="/test", tags=["auth"])

def verify_token(token: str):
    try:
        payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
        row = get_access_token(token)
        if not row:
            raise HTTPException(status_code=401, detail="Access token not found")
        return str(payload["sub"]).split(",")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/verify_token")
def verify_token_endpoint(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid Authorization header")
    
    token = authorization.split(" ")[1]
    username, device = verify_token(token)
    return {"status": "valid", "username": username, "device": device}