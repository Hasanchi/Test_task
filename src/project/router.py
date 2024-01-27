from fastapi import APIRouter, Request, Depends, HTTPException, status

from sqlalchemy import select, insert, update, Delete
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession


from src.auth.router import get_current_user
from src.database import get_async_session
from src.project.dependencies import get_user_username, get_role_id, get_user_id, TaskCom
from src.project.models import ProjectUser, Project, Task, User, Role
from src.project.schema import CreatedProject, CreatedTask, SelectedProject, UpdateUserForManager, UpdateTask

import logging

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")

project_router = APIRouter(prefix='/project', tags=['Project'])


@project_router.get('/')
async def get_projects(request: Request, session: AsyncSession = Depends(get_async_session)):
    decode_data = get_current_user(request)
    user_id = decode_data['id']

    # user = await get_user_username(session, username)
    query = select(ProjectUser).where(ProjectUser.user_id == user_id).options(joinedload(ProjectUser.user)).options(joinedload(ProjectUser.project))
    resulst = await session.execute(query)
    return resulst.scalars().all()


@project_router.get('/{project_id}/task')
async def get_tasks(project_id: int, request: Request, session: AsyncSession = Depends(get_async_session)):
    query = select(Task).where(Task.project_id==project_id)
    resulst = await session.execute(query)
    return [resulst.scalars().all()]

@project_router.get('/{project_id}')
async def get_users(project_id: int, request: Request, session: AsyncSession = Depends(get_async_session)):
    query = select(ProjectUser.user)
    resulst = await session.execute(query)    
    return [resulst.scalars().all()]


@project_router.post('/add')
async def add_project(body: CreatedProject, request: Request, session: AsyncSession = Depends(get_async_session)):
    decode_data = get_current_user(request)
    user_id = decode_data['id']
    data = body.model_dump()
    try:
        project = Project(**data)
        project_user = ProjectUser(user_id=user_id, project=project, role=Role.meneger.name)
        session.add(project)
        session.add(project_user)
        await session.commit()
        return {
            'message': 'Проект успешно добавлена'
        }
    except:
        HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Необработанный ответ'
        )

@project_router.get('/task/{task_id}')
async def get_task(task_id: int, requset: Request, session: AsyncSession = Depends(get_async_session)):
    query = select(Task).where(Task.id==task_id)
    result = await session.execute(query)
    return [result.scalar()]


@project_router.post('/{project_id}/task/add')
async def add_task_in_project(project_id: int, body: CreatedTask, request: Request, session: AsyncSession = Depends(get_async_session)):
    decode_data = get_current_user(request)
    user_id = decode_data['id']
    data = body.model_dump()
    data['project_id'] = project_id
    data['сreator_id'] = user_id
    print(data)
    try:
        task = Task(**data)
        session.add(task)
        await session.commit()
        return {
            'message': 'Задача успешно добавлена'
        }
    except Exception as e:
        await session.rollback()
        HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )

@project_router.put('/{project_id}/task/{task_id}')
async def update_task(project_id: int, task_id: int, body: UpdateTask, request: Request, session: AsyncSession = Depends(get_async_session)):
    data = body.model_dump()

    executor_id = data['executor_id']

    status = data['status']
    # To do
    # "Testing"
    # Разработчик

    role = await get_role_id(session, executor_id, project_id)
    taskcom = TaskCom(status=status, executor=role)
    

    value = taskcom.is_valid_status_executor_combination(taskcom.status, taskcom.executor[0])
    
    return {
        'message': value
    }
    

    query = update(Task).where(Task.id == task_id).values(**data)
    await session.execute(query)
    await session.commit()
    return {
        'message': 'Задача успешно изменена'
    }


@project_router.post('/{project_id}/user/add')
async def add_user_in_project(project_id: int, body: UpdateUserForManager, request: Request, session: AsyncSession = Depends(get_async_session)):
    user = await get_user_username(session, body.username)
    try:
        project_user = ProjectUser(project_id=project_id, user_id=user.id, role=body.role)
        session.add(project_user)
        await session.commit()
        return {
            'message': 'Пользователь успешно добавлен в проект'
        }
    except Exception as e:
        await session.rollback()
        HTTPException(
            status_code=status.HTTP_100_CONTINUE,
            detail=str(e)
        )


@project_router.put('/{project_id}/user/{username}')
async def update_user_in_project(project_id: int, body: UpdateUserForManager, username: str, request: Request, session: AsyncSession = Depends(get_async_session)):
    decode_data = get_current_user(request)
    meneger_id = decode_data['id']
    query = select(ProjectUser).where(ProjectUser.user_id==meneger_id).where(ProjectUser.project_id==project_id)
    meneger = await session.scalar(query)

    if meneger.role.value != Role.meneger.value:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Вы не менеджер в этом проекте'
        )
    user = await get_user_username(session, username)
    if user is None:
        return {
            'message': 'Данный пользователь не найден в этом проекте'
        }
    user.username = body.username
    await session.commit()
    try:
        qyery = update(ProjectUser).where(ProjectUser.user_id==user.id).where(ProjectUser.project_id==project_id).values(role=body.role)
        await session.execute(qyery)
        await session.commit()
        return {
            'message': 'Пользователь успешно изменён'
        }
    except Exception as e:
        await session.rollback()
        HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )












