from functools import wraps
from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
import app.deil_api.exceptions as deil_api_exc
from app.deil_api.deil_async_api import BaseAPI
from cryptography.fernet import Fernet
from app import config
from base64 import urlsafe_b64encode

logout_response = RedirectResponse(url='/login', status_code=302)
logout_response.set_cookie('deil_token', value='false', max_age=0, expires=0)


def token_decoder(token: str) -> dict[str: str]:
    crypto = Fernet(key=urlsafe_b64encode(config['secret_key'].encode()))
    l, p = crypto.decrypt(token=token).decode().split('\n')
    return {'login': l, 'passw': p}


def token_encoder(login: str, passw: str) -> str:
    crypto = Fernet(key=urlsafe_b64encode(config['secret_key'].encode()))
    token = crypto.encrypt(f'{login}\n{passw}'.encode())
    return token.decode()


def auth_login(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs['request']
        token = request.cookies.get('deil_token')
        if token:
            return RedirectResponse(url='/', status_code=302)
        if request.method == 'GET':
            result = await func(*args, **kwargs)
            return result
        else:
            login = kwargs['login']
            passw = kwargs['passw']
            api = BaseAPI(config=config, login=login, passw=passw)
            try:
                await api.get_user_info()
                token = token_encoder(login, passw)
                response = RedirectResponse(url='/', status_code=302)
                response.set_cookie(key='deil_token', value=token)
                return response
            except deil_api_exc.AuthFailed:
                return RedirectResponse(url='/login?login_failed=1', status_code=302)

    return wrapper


def auth_protect(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs['request']
        token = request.cookies.get('deil_token')
        if not token:
            raise HTTPException(status_code=401)
        kwargs['deil_account'] = token_decoder(token)
        try:
            result = await func(*args, **kwargs)
        except deil_api_exc.AuthFailed:
            raise HTTPException(status_code=401)
        return result
    return wrapper


def auth_protect_redirect(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs['request']
        token = request.cookies.get('deil_token')
        if token:
            try:
                kwargs['deil_account'] = token_decoder(token)
                return await func(*args, **kwargs)
            except deil_api_exc.AuthFailed:
                pass
        return logout_response
    return wrapper


def auth_logout(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        response = RedirectResponse(url='/login', status_code=302)
        response.set_cookie('deil_token', value='false', max_age=0, expires=0)
        return response
    return wrapper




