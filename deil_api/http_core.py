from aiohttp import request
from functools import wraps


class HttpCore:
    def __init__(self, carbon_ip, carbon_port):
        self.carbon_ip = carbon_ip
        self.carbon_port = carbon_port

    async def authenticate():



