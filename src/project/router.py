from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.user.router import get_current_user
from src.database import get_async_session
from src.project.helper import get_user_username, get_role_id, TaskCheck, StatusCheck, check_blocked, search_user_in_project
from src.models import ProjectUser, Project, Task, Role
from src.project.schema import CreatedProject, CreatedTask, UpdateUserForManager, UpdateTask, SelectedProject

project_router = APIRouter(prefix='/project', tags=['Project'])


@project_router.get('/')
async def get_projects(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    decode_data = get_current_user(request)
    user_id = decode_data['id']
    query = (
        select(ProjectUser)
        .where(ProjectUser.user_id == user_id)
        .options(joinedload(ProjectUser.project))
    )
    resulst = await session.execute(query)
    return resulst.scalars().all()


@project_router.get('/tasks')
async def get_tasks(
        project_id: int,
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(Task)
        .where(Task.project_id == project_id)
        .order_by(Task.updated_at.desc())
    )
    resulst = await session.execute(query)
    return resulst.scalars().all()


@project_router.post('/add')
async def add_project(
        body: CreatedProject,
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    decode_data = get_current_user(request)
    user_id = decode_data['id']
    data = body.model_dump()
    project = Project(**data)
    project_user = ProjectUser(
        user_id=user_id,
        project=project,
        role=Role.meneger.name
    )
    session.add(project)
    session.add(project_user)
    await session.commit()
    return {
        'message': 'Проект успешно добавлена'
    }


@project_router.get('/task/{task_id}')
async def get_task(
        task_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(Task)
        .where(Task.id == task_id)
        .options(
            joinedload(Task.blocked_by),
            joinedload(Task.blocking_by)
        )
    )
    result = await session.execute(query)
    return [result.scalar()]


@project_router.post('/task/add')
async def add_task_in_project(
        project_id: int,
        body: CreatedTask,
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    decode_data = get_current_user(request)
    user_id = decode_data['id']
    data = body.model_dump()
    data['project_id'] = project_id
    data['сreator_id'] = user_id
    task = Task(**data)
    session.add(task)
    await session.commit()
    return {
        'message': 'Задача успешно добавлена'
    }


@project_router.put('/task/{task_id}')
async def update_task(
        project_id: int,
        task_id: int,
        body: UpdateTask,
        session: AsyncSession = Depends(get_async_session)
):
    if await check_blocked(session, task_id):
        return {
            'message': 'У данной задачи есть блокирующие задачи, вы не моежете изменить ее статус пока не закончите блокирующие'
        }

    data = body.model_dump()

    executor_id = data['executor_id']

    new_status = data['status']

    role = await get_role_id(session, executor_id, project_id)
    role = role[0]

    taskcheck = TaskCheck(status=new_status, executor=role)

    value = taskcheck.is_valid_status_executor_combination(
        taskcheck.status,
        taskcheck.executor
    )

    if not value:
        return {
            'message': f'Вы не можете назначить исполнителем {role.value} на задачу со статусом {new_status}'
        }
    query = select(Task.status).where(Task.id == task_id)
    current_status = await session.execute(query)
    current_status = current_status.scalar()

    status_check = StatusCheck(current_status, new_status)
    value = status_check.check_status()

    if not value:
        return {
            'message': f'Вы не можете поменять статус с {current_status} до {new_status}'
        }

    query = update(Task).where(Task.id == task_id).values(**data)
    await session.execute(query)
    await session.commit()
    return {
        'message': 'Задача успешно изменена'
    }


@project_router.delete('/task/{task_id}')
async def delete_task(
        task_id: int,
        project_id: int,
        request: Request,
        session: AsyncSession = Depends(get_async_session),
):
    current_user = await search_user_in_project(request, session, project_id)
    if current_user.role.value != Role.meneger.value:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Вы не менеджер в этом проекте'
        )
    if await check_blocked(session, task_id):
        return {
            'message': 'У данной задачи есть блокирующие задачи, вы не можеете удалить'
        }
    query = (
        delete(Task)
        .where(Task.id == task_id)
    )
    await session.execute(query)
    return {
        'message': 'Задача успешно удалена'
    }


@project_router.post('/user/add')
async def add_user_in_project(
        project_id: int,
        body: UpdateUserForManager,
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    user = await get_user_username(session, body.username)
    project_user = ProjectUser(
        project_id=project_id,
        user_id=user.id,
        role=body.role
    )
    session.add(project_user)
    await session.commit()
    return {
        'message': 'Пользователь успешно добавлен в проект'
    }


@project_router.put('/user/{username}')
async def update_user_in_project(
        project_id: int,
        body: UpdateUserForManager,
        username: str, request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    current_user = await search_user_in_project(request, session, project_id)
    if current_user.role.value != Role.meneger.value:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Вы не менеджер в этом проекте'
        )
    updete_user = await get_user_username(session, username)
    if updete_user is None:
        return {
            'message': 'Данный пользователь не найден в этом проекте'
        }
    updete_user.username = body.username
    await session.commit()
    qyery = (
        update(ProjectUser)
        .where(ProjectUser.user_id == updete_user.id)
        .where(ProjectUser.project_id == project_id)
        .values(role=body.role)
    )
    await session.execute(qyery)
    await session.commit()
    return {
        'message': 'Пользователь успешно изменён'
    }
