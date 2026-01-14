from pydantic import BaseModel
from fastapi import APIRouter
from bdd.auth_bdd import remove_refresh_token, remove_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

class LogoutRequest(BaseModel):
    refresh_token: str

@router.post("/logout")
def logout(logout_request: LogoutRequest):
    remove_refresh_token(logout_request.refresh_token)
    remove_access_token(logout_request.refresh_token)
    return {"message": "Successfully logged out"}
