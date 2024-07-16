from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from .api_views import api_router
from .static_files_no_cache import StaticNoCache


app = FastAPI()
app.mount('/static', StaticNoCache(directory='static'), name='static')
app.include_router(router=api_router)
templates = Jinja2Templates(directory='templates')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from . import templates_views



