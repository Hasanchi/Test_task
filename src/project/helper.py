from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User, ProjectUser, Role, Status, Task
from src.user.router import get_current_user


class StatusCheck:
    def __init__(self, current_status, new_status) -> None:
        self.current_status = current_status
        self.new_status = new_status

    def check_status(self):
        if self.new_status in [Status.to_do, Status.wontfix]:
            return True
        elif self.current_status == Status.to_do and self.new_status == Status.in_progress:
            return True
        elif self.current_status == Status.in_progress and self.new_status == Status.code_review:
            return True
        elif self.current_status == Status.code_review and self.new_status == Status.dev_test:
            return True
        elif self.current_status == Status.dev_test and self.new_status == Status.testing:
            return True
        elif self.current_status == Status.testing and self.new_status == Status.done:
            return True
        else:
            return False


class TaskCheck:
    def __init__(self, status, executor):
        self.status = status
        self.executor = executor

    def is_valid_executor(self, executor):
        if self.status in [Status.in_progress, Status.code_review, Status.dev_test]:
            return executor != Role.test_engineer
        elif self.status == Status.testing:
            return executor != Role.developer
        else:
            return True

    def is_valid_status_executor_combination(self, status, executor):
        if executor == Role.meneger:
            return False
        if executor == Role.team_leader:
            return True
        if executor is None and status != Status.in_progress:
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


async def check_blocked(session: AsyncSession, task_id):
    query = select(Task).where(Task.blocking_by_id == task_id)
    results = await session.execute(query)
    print(results)
    if results.scalars().first():
        return True
    return False


async def search_user_in_project(request, session: AsyncSession, project_id: int) -> User:
    decode_data = get_current_user(request)
    user_id = decode_data['id']
    query = (
        select(ProjectUser)
        .where(ProjectUser.user_id == user_id)
        .where(ProjectUser.project_id == project_id)
    )
    user = await session.scalar(query)
    return user
