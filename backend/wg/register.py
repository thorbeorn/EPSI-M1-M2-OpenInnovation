import os
from fastapi import APIRouter, HTTPException, Header
from jose import jwt
from bdd.auth_bdd import get_access_token
from modules.wg_mod import generate_client_key, keys_match, generate_client_psk
from dotenv import load_dotenv

load_dotenv()
router = APIRouter(prefix="/wg", tags=["auth"])

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

@router.get("/register")
def register(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid Authorization header")
    token = authorization.split(" ")[1]
    username, device = verify_token(token)

    private_client_key, public_client_key = generate_client_key()
    if not keys_match(private_client_key, public_client_key):
        raise HTTPException(status_code=409, detail="Invalid generated client key")
    public_server_key = os.getenv('SRV_PUB_WG_KEY')
    if not public_server_key:
        raise HTTPException(status_code=409, detail="Cannot find server public key")
    psk_client_server = generate_client_psk()
    if not psk_client_server:
        raise HTTPException(status_code=409, detail="Cannot generate psk for client server peer")
    server_endpoint = f"{os.getenv('SRV_ENDPOINT_IP')}:{os.getenv('SRV_ENDPOINT_PORT')}"
    if not server_endpoint:
        raise HTTPException(status_code=409, detail="Cannot find server endpoint")
    
    return {"status": "valid", "username": username, "device": device}