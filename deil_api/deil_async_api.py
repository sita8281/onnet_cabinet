from bs4 import BeautifulSoup
from httpx import AsyncClient, HTTPError
import asyncio
import exceptions


class BaseAPI:
    def __init__(self, config):
        self.host = config['host']
        self.port = config['port']
        self.client = AsyncClient()

    async def _get_bs(self, url):
        session_cookie = await self._auth('artem8281', '20012001')
        response = await self.client.get(f'http://{self.host}:{self.port}{url}', cookies={'PHPSESSID': session_cookie})
        response.encoding = 'cp1251'
        return BeautifulSoup(response.text, 'lxml')

    async def _auth(self, login, passw):
        response = await self.client.post(f'http://{self.host}:{self.port}/cabinet/login', data={
            'cab_login': login,
            'cab_hash': 'C8373A1586FE2EB2BADEEAA98E363D67',
            'cab_password': passw,
            'cab_random_word': '712947',
            'cab_user_login': '%C2%EE%E9%F2%E8+%E2+%EA%E0%E1%E8%ED%E5%F2'
        })
        location = response.headers.get('Location')
        cookie = response.cookies.get('PHPSESSID')
        if not location:
            raise exceptions.AuthFailed()
        if 'userinfo' in location:
            return cookie
        response = await self.client.get(location, cookies={'PHPSESSID': cookie})
        location = response.headers.get('Location')
        if not location:
            raise exceptions.AuthFailed()
        return cookie

    async def get_user_info(self):
        bs = await self._get_bs(url='/cabinet/userinfo')
        print(bs)

    async def get_payment_info(self):
        bs = await self._get_bs(url='/cabinet/payment')
        print(bs)

    async def get_operations_info(self):
        bs = await self._get_bs(url='/cabinet/operations')
        print(bs)

    async def get_control_info(self):
        bs = await self._get_bs(url='/cabinet/control')
        print(bs)

    async def get_tarif_info(self):
        bs = await self._get_bs(url='/cabinet/tarif')
        print(bs)


loop = asyncio.get_event_loop()
api = BaseAPI(config={'host': '192.168.255.100', 'port': '80'})
loop.run_until_complete(api.get_control_info())
