from bs4 import BeautifulSoup
from httpx import AsyncClient, HTTPError
import asyncio
import exceptions


class BaseAPI:
    def __init__(self, config):
        self.host = config['host']
        self.port = config['port']
        self.login = 'artem8281'
        self.passw = '20012001'
        self.client = AsyncClient()
        self.cookie = ''

    async def _get_bs(self, url):
        if not self.cookie:
            self.cookie = await self._auth(self.login, self.passw)
        response = await self.client.get(f'http://{self.host}:{self.port}{url}', cookies={'PHPSESSID': self.cookie})
        response.encoding = 'cp1251'
        return BeautifulSoup(response.text, 'lxml')

    async def _post_bs(self, url: str, data: dict):
        if not self.cookie:
            self.cookie = await self._auth(self.login, self.passw)
        response = await self.client.post(
            f'http://{self.host}:{self.port}{url}',
            cookies={'PHPSESSID': self.cookie},
            data=data
        )
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

    async def get_user_info(self) -> list:
        info_list = []
        bs = await self._get_bs(url='/cabinet/userinfo')
        table_info = bs.find('table', {'id': 'ideco_user_info'})
        if table_info:
            for tr in table_info.find_all('tr'):
                key = tr.find('td', {'class': 'label'}).get_text().strip()
                val = tr.find('td', {'class': 'value'}).get_text().strip()
                info_list.append((key, val))
        return info_list

    async def get_payment_info(self) -> int | None:
        bs = await self._get_bs(url='/cabinet/payment')
        try:
            summ = int(bs.find('input', {'id': 'amount-sample-3'})['value'])
        except ValueError:
            return
        return summ

    async def get_operations_info(self):
        bs = await self._get_bs(url='/cabinet/operations')
        stat_table = bs.find('table', {'id': 'stat_table'})
        stat_list = [tuple([td.get_text() for td in tr.find_all('td')]) for tr in stat_table.find_all('tr')]
        return list(filter(lambda x: x, stat_list))

    async def get_sms_phone(self):
        bs = await self._get_bs(url='/cabinet/control')
        phone = bs.find('input', {'name': 'new_sms'})['value']
        print(phone)

    async def get_tarif_info(self) -> dict[str: list[tuple[str, str]], str: tuple]:
        """
        Получить список доступных тарифов, и текущий подключённый
        :return:
        """
        tarif_list = []
        current_tarif = ()
        bs = await self._get_bs(url='/cabinet/tarif')
        tarifs = bs.find('select', {'name': 'new_plan_id'})
        if not tarifs:
            return
        for option in tarifs.find_all('option'):
            name = option.get_text()
            val = option['value']
            tarif_list.append((name.strip(), val))
        current_tarif = bs.find('tr', {'class': 'odd'})
        if current_tarif:
            tds = current_tarif.find_all('td')
            name = tds[0].get_text().strip()
            price = tds[1].get_text().strip()
            current_tarif = (name, price)
        return {'tarifs': tarif_list, 'current': current_tarif}

    async def set_number_phone(self, phone: str) -> bool:
        """Установить номер телефона для SMS"""
        bs = await self._post_bs('/cabinet/control', {'new_sms': phone, 'change_info': 'info'})
        if str(bs).find('alert'):
            return True





loop = asyncio.get_event_loop()
api = BaseAPI(config={'host': '192.168.255.100', 'port': '80'})
loop.run_until_complete(api.set_number_phone(phone='9998887722'))
