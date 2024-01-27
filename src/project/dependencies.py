from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_maker
from src.project.models import User, ProjectUser, Role


class TaskCom:
    def __init__(self, status, executor):
        self.status = status
        self.executor = executor

    def is_valid_executor(self, executor):
        if self.status in ["In progress", "Code review", "Dev test"]:
            return executor != "Тест-инженер"
        elif self.status == "Testing":
            return executor != "Разработчик"
        else:
            return True

    def is_valid_status_executor_combination(self, status, executor):
        if executor == Role.meneger.name:
            return False
        if executor == "Тимлид":
            return True
        if executor is None and status != "In progress":
            return True
        return self.is_valid_executor(executor)

async def get_role_id(session: AsyncSession, id: int, project_id: int):
    query = select(ProjectUser.role).where(ProjectUser.user_id == id).where(ProjectUser.project_id == project_id)
    result = await session.execute(query)
    return [result.scalar()]


async def get_user_id(session: AsyncSession, id: int) -> User:
    query = select(User).where(User.id == id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_user_username(session: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    resulst = await session.execute(query)
    return resulst.scalar_one_or_none()