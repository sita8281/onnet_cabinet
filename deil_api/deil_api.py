import pickle
from bs4 import BeautifulSoup
import requests
import urllib.parse
import time
import socket


class SessionStorageDeilAPI:
    _storage = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SessionStorageDeilAPI, cls).__new__(cls)
        return cls.instance

    def get_session(self, login):
        if login in self._storage:
            return self._storage[login]
        return

    def set_session(self, login, iid):
        self._storage[login] = iid

    def del_session(self, login):
        if login in self._storage:
            del self._storage[login]


class DeilAPI:
    def __init__(self, login, passw, ip, port):
        super().__init__()

        self.session = requests.Session()
        self.user_login = login
        self.user_passw = passw
        self.static_url = f'http://{ip}:{port}'
        self.storage = SessionStorageDeilAPI()

    @staticmethod
    def auth_fixer(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception:
                self.storage.del_session(self.user_login)
                self.authenticate()
                return func(self, *args, **kwargs)
        return wrapper

    def authenticate(self):
        """авторизоваться на сайте"""
        _session = self.storage.get_session(self.user_login)
        if _session:
            self.session = _session
            return
        response = self.session.post(f'{self.static_url}/cabinet/login', {
            'cab_login': self.user_login,
            'cab_hash': 'C8373A1586FE2EB2BADEEAA98E363D67',
            'cab_password': self.user_passw,
            'cab_random_word': '712947',
            'cab_user_login': '%C2%EE%E9%F2%E8+%E2+%EA%E0%E1%E8%ED%E5%F2'

        })
        self.storage.set_session(self.user_login, self.session)
        # проверка на успешность авторизации
        if not self._unathorized_detect(response):
            return 401

    def dump_all_tree(self):
        """Сохранить dump-файл общего древа пользователей"""
        with open(file='web/all_tree.pickle', mode='wb') as file:
            try:
                pickle.dump(self.get_tree_users(), file)
                return True
            except Exception:
                return

    def get_dump_tree(self):
        """Получить dump-файл общего древа папок"""
        with open(file='web/all_tree.pickle', mode='rb') as file:
            return pickle.load(file)

    @auth_fixer
    def get_tree_users(self):
        all_tree = []
        folders, bs = self.get_folders(return_all=True)
        admins = self.parse_admins(bs)
        servers = self.parse_servers(bs)
        for fname, fiid in folders:
            folder = {
                'iid': fiid,
                'name': fname,
                'type': 'folder',
                'child': [],
            }
            users = self.get_users(fiid)
            for login, uname, uiid in users:
                user = {
                    'iid': uiid,
                    'name': uname,
                    'type': 'user',
                    'login': login,
                }
                folder['child'].append(user)
            all_tree.append(folder)

        for login, uname, uiid in admins:
            user = {
                'iid': uiid,
                'name': uname,
                'type': 'user',
                'login': login,
            }
            all_tree.append(user)

        for login, sname, siid in servers:
            user = {
                'iid': siid,
                'name': sname,
                'type': 'server',
                'login': login,
            }
            all_tree.append(user)
        return all_tree

    @auth_fixer
    def get_folders(self, return_all=None):
        """Получить список папок клиентов"""
        bs = self._get_bs('/cabinet/userinfo', 'html.parser')
        divs_folders = bs.find_all('div', {'class': 'tree_folder_closed tree_node_folder'})

        folder_list = []
        for div in divs_folders:
            a = div.find('a', {'class': ''})
            text = a.text.strip()
            url = a['href'].split('/')[-1]
            folder_list.append((text, url.split('/')[-1]))

        if return_all:
            return folder_list, bs
        else:
            return folder_list

    def parse_servers(self, bs):
        divs_users = bs.find_all('div', {'class': 'tree_server tree_node_user'})

        user_list = []
        for div in divs_users:
            a = div.find('a', {'class': ''})
            name, login = a.text.split('<')
            url_user = a['href'].split('/')[-1]
            user_list.append((login.replace('>', ''), name, url_user))

        return user_list

    def parse_admins(self, bs):
        divs_users = bs.find_all('div', {'class': 'tree_admin tree_node_user'})

        user_list = []
        for div in divs_users:
            a = div.find('a', {'class': ''})
            name, login = a.text.split('<')
            url_user = a['href'].split('/')[-1]
            user_list.append((login.replace('>', ''), name, url_user))

        return user_list

    @auth_fixer
    def get_users(self, iid, search_class='tree_user tree_node_user'):
        """получить список клиентов из папки
        :param iid: ссылка папки
        :param search_class html класс элемента
        """
        bs = self._get_bs(f'/cabinet/userinfo/{iid}', 'html.parser')
        divs_users = bs.find_all('div', {'class': search_class})

        user_list = []
        for div in divs_users:
            a = div.find('a', {'class': ''})
            name, login = a.text.split('<')
            url_user = a['href'].split('/')[-1]
            user_list.append((login.replace('>', ''), name, url_user))

        return user_list

    @auth_fixer
    def get_info_user(self, iid):
        """получить информацию клиента

        :param iid: ссылка на клиента
        """
        bs = self._get_bs(f'/cabinet/userinfo/{iid}', 'html.parser')
        table = bs.find('table', {'id': 'ideco_user_info'})
        tr_lst = table.find_all('tr')

        info_list = []
        for tr in tr_lst:
            label = tr.find('td', {'class': 'label'}).text.strip()
            if label.endswith(':'):
                label = label[:-1]
            value = tr.find('td', {'class': 'value'}).text
            info_list.append([label, value])

        tables = bs.find_all('table', {'id': 'ideco_user_addons'})
        for table in tables:
            try:
                if table:
                    tr_lst = table.find_all('tr')
                    for tr in tr_lst:
                        try:
                            label, value = tr.find_all('td')
                            info_list.append([label.text, value.text])
                        except ValueError:
                            if info_list[-1] != ['Выделенный IP:', 'вкл']:
                                info_list.append(['Выделенный IP:', 'вкл'])
            except Exception:
                pass

        return info_list

    @auth_fixer
    def get_sessions_user(self, iid, start_date, end_date):
        """Получить сессии клиента
        :param iid: ссылка на клиента
        :param start_date: от числа 01.05.2023
        :param end_date: до числа 03.05.2023
        """
        pages_url = []
        client_sessions = []
        tr_elements = []

        def parse_tr(html):
            table = html.find('table', {'id': 'stat_table'})
            trs = table.find_all('tr')
            for tr in trs:
                tr_elements.append(tr)

        self.session.get(f'{self.static_url}/cabinet/userinfo/{iid}', timeout=15)
        response = self.session.post(f'{self.static_url}/cabinet/stat', timeout=15, data={
            'module': 'stat',
            'date_start': start_date,
            'date_end': end_date,
            'resolution': '0'
        })

        response.encoding = 'windows-1251'
        bs = BeautifulSoup(response.text, 'html.parser')

        # div_pages = bs.find('div', {'class': 'stat_pages'})
        # span_lst = div_pages.find_all('span', {'class': 'page_num'})
        span_lst = bs.find_all('span', {'class': 'page_num'})

        for span in span_lst:
            a = span.find('a')
            if not a:
                continue
            pages_url.append(a['href'])

        parse_tr(bs)
        for url in pages_url:
            parse_tr(self._get_bs(url, 'html.parser'))

        for tr_element in tr_elements:
            tds = tr_element.find_all('td')
            lst = []
            for td in tds:
                lst.append(td.text)
            if lst:
                client_sessions.append(lst)
        return client_sessions

    @auth_fixer
    def get_helpdesk_list(self):
        """получить список открытых заявок"""
        tickets = {}
        bs = self._get_bs('/cabinet/helpdesk', 'lxml')
        table = bs.find('table', {'id': 'stat_table'})
        tbody_lst = table.find_all('tbody')
        for tbody in tbody_lst:
            td1, td2, td3, td4, td5 = tbody.find_all('td')
            iid = td2.find('a').text
            name = td3.find('a').text
            date = td1.text
            status = td5.text
            tickets[iid] = [name, date, status]
        return tickets

    @auth_fixer
    def get_helpdesk_info(self, iid):
        """получить содержимое заявки
        :param iid: номер заявки
        """
        bs = self._get_bs(f'/cabinet/helpdesk?id={iid}', 'lxml')
        info_block = bs.find('div', {'class', 'hdsk_main'})
        name = info_block.find('h1').text.strip()
        mini_chat = []
        lst_li = info_block.find_all('li')
        for li in lst_li:
            val = li.find('div').text.strip().split('\n')
            if len(val) > 2:
                div_elements = val[:-1]
                small_element = val[-1]
                div = ' '.join(div_elements)
                small = small_element
            else:
                div, small = val
            mini_chat.append([div, small])
        result = {'name': name, 'chat': mini_chat}

        return result

    @auth_fixer
    def close_helpdesk(self, *args):
        """закрыть заявки
        :param iids: номера заявок
        """
        for c, iid in enumerate([*args]):
            self.session.get(f'{self.static_url}/cabinet/helpdesk?id={iid}')
            try:
                self.session.post(f'{self.static_url}/cabinet/helpdesk?id={iid}', {'status': '10'})
            except Exception:
                pass
        return ['success']

    def raw_sock_post(self, url, data):
        """сырой http post"""
        cookie, val = self.session.cookies.items()[0]
        url = urllib.parse.urlparse(url)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(15)
        sock.connect((url.netloc.split(':')[0], 80))
        if url.path and url.query:
            method = f'POST {url.path}?{url.query} HTTP/1.1'
        elif url.path:
            method = f'POST {url.path} HTTP/1.1'
        else:
            method = f'POST / HTTP/1.1'
        headers = {
            'Host': url.netloc,
            'Cookie': f'{cookie}={val}',
            'User-Agent': 'raw-tcp-socket-request',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Content-Length': f'{len(data)}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        buff = b''
        buff += method.encode()
        buff += b'\r\n'
        for item, val in headers.items():
            b = f'{item}: {val}\r\n'.encode()
            buff += b
        buff += b'\r\n'
        buff += data
        sock.sendall(buff)
        time.sleep(1)

    @auth_fixer
    def create_helpdesk(self, iid, theme, info):
        """Создать новую заявку"""
        try:
            subj = urllib.parse.quote_plus(theme, encoding='cp1251')
            text = urllib.parse.quote_plus(info, encoding='cp1251')
            self.session.get(f'{self.static_url}/cabinet/helpdesk?filter_id={iid}')
            post_data = f'subj={subj}&text={text}'.encode()
            self.raw_sock_post(f'{self.static_url}/cabinet/helpdesk', post_data)
        finally:
            return ['success']

    @auth_fixer
    def send_helpdesk(self, iid, text):
        a = 'none'
        try:
            text = urllib.parse.quote_plus(text, encoding='cp1251')
            a = self._get_bs(f'/cabinet/helpdesk?id={iid}', 'lxml').text
            self.raw_sock_post(f'{self.static_url}/cabinet/helpdesk?id={iid}', b'text=' + text.encode())
        finally:
            return [a]

    def _get_bs(self, url, parser):
        response = self.session.get(f'{self.static_url}{url}')
        response.encoding = 'windows-1251'
        bs = BeautifulSoup(response.text, parser)
        return bs

    @staticmethod
    def _unathorized_detect(response):
        if response.status_code != 200:
            return
        bs = BeautifulSoup(response.text, 'html.parser')
        div_auth_err = bs.find_all('div', {'class': 'ideco_error'})
        if div_auth_err:
            return
        return True

