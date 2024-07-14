from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/')
async def index():
    return {'hello': 'world'}
