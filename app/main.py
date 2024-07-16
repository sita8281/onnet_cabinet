from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .api_views import api_router


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
app.include_router(router=api_router)
templates = Jinja2Templates(directory='templates')


from . import templates_views



