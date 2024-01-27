from fastapi import FastAPI
from src.auth.router import auth_rouret
from src.project.router import project_router

app = FastAPI(title='Этот проект является тестовым заданием')

app.include_router(auth_rouret)
app.include_router(project_router)


@app.get('/')
async def hello():
    return {'message': 'hello world'}
