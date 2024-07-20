from fastapi import APIRouter, Request
from app.deil_api.deil_async_api import BaseAPI
from .auth import auth_protect
from app import config


api_router = APIRouter(prefix='/api')


@api_router.get('/user')
@auth_protect
async def user_info(request: Request, deil_account: dict = {}):
    api = BaseAPI(config=config, **deil_account)
    return await api.get_user_info()


@api_router.get('/operations')
@auth_protect
async def user_info(request: Request, deil_account: dict = {}):
    api = BaseAPI(config=config, **deil_account)
    return await api.get_operations_info()


@api_router.get('/tarif')
@auth_protect
async def user_info(request: Request, deil_account: dict = {}):
    api = BaseAPI(config=config, **deil_account)
    return await api.get_tarif_info()


@api_router.get('/payment')
@auth_protect
async def user_info(request: Request, deil_account: dict = {}):
    api = BaseAPI(config=config, **deil_account)
    return await api.get_payment_info()


@api_router.get('/phone')
@auth_protect
async def user_info(request: Request, deil_account: dict = {}):
    api = BaseAPI(config=config, **deil_account)
    return await api.get_sms_phone()


@api_router.get('/set_tarif')
@auth_protect
async def change_tarif(request: Request, tarif_plane: str, deil_account: dict = {}, ):
    api = BaseAPI(config=config, **deil_account)
    return await api.set_tarif(tarif=tarif_plane)


@api_router.get('/set_phone')
@auth_protect
async def change_tarif(request: Request, number: str, deil_account: dict = {}, ):
    api = BaseAPI(config=config, **deil_account)
    return await api.set_number_phone(phone=number)



