from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
from jose import jwt, JWTError
from modules.auth import SECRET_KEY, ALGORITHM
from bdd.jwt import get_access_token, get_refresh_token

router = APIRouter(prefix="/test", tags=["auth"])

class TokenRequest(BaseModel):
    username: str

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        row = get_access_token(token)
        if not row:
            raise HTTPException(status_code=401, detail="Access token not found")
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/verify_token")
def verify_token_endpoint(authorization: str = Header(...)):
    """
    Passer le token dans le header Authorization: Bearer <token>
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid Authorization header")
    
    token = authorization.split(" ")[1]
    username = verify_token(token)
    return {"status": "valid", "username": str(username).split(",")[0], "device": str(username).split(",")[1]}