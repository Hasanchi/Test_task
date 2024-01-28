from fastapi import FastAPI
from src.user.router import user_router
from src.project.router import project_router

app = FastAPI(title='Этот проект является тестовым заданием')

app.include_router(user_router)
app.include_router(project_router)


@app.get('/')
async def hello():
    return {'message': 'hello world'}
