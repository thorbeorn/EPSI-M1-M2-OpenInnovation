# server.py
from fastapi import FastAPI

from auth import login, logout, refresh
from test_unit import auth_test
from wg import register
from bdd.auth_bdd import init_refresh_token_table
from bdd.wg_bdd import init_IPs_table

app = FastAPI()

init_refresh_token_table()
init_IPs_table()

# Include Routers
app.include_router(login.router)
app.include_router(logout.router)
app.include_router(refresh.router)
app.include_router(register.router)

app.include_router(auth_test.router)