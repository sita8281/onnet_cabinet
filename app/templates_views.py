from .main import app, templates
from fastapi import Request, Response, Form
from fastapi.responses import RedirectResponse
from .auth import auth_protect, auth_protect_redirect, auth_login, logout_response
from typing import Dict, Annotated
from app.deil_api.deil_async_api import BaseAPI
from app.deil_api.exceptions import AuthFailed


@app.get('/')
@auth_protect_redirect
async def main(request: Request, deil_account: dict = {}):
    print(deil_account)
    return templates.TemplateResponse(request=request, name='index.html')


@app.get('/login')
@auth_login
async def login(request: Request, login_failed: str = ''):
    return templates.TemplateResponse(request=request, name='login.html', context={'login_failed': login_failed})


@app.post('/login')
@auth_login
async def login_form(request: Request, login: Annotated[str, Form()], passw: Annotated[str, Form()]):
    return {'user': login, 'passw': passw}


@app.get('/logout')
async def logout(request: Request):
    return logout_response



