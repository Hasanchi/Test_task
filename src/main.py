from fastapi import FastAPI
from src.auth.router import auth_rouret

app = FastAPI(title='Этот проект является тестовым заданием')

app.include_router(auth_rouret)


@app.get('/')
async def hello():
    return {'message': 'hello world'}
