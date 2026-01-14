# server.py
from fastapi import FastAPI

from auth import login, logout, refresh
from modules import auth_test
from bdd.jwt import init_refresh_token_db

app = FastAPI()

init_refresh_token_db()

# Include Routers
app.include_router(login.router)
app.include_router(logout.router)
app.include_router(refresh.router)
app.include_router(auth_test.router)