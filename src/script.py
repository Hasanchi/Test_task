from src.database import async_session_maker
from src.models import User, ProjectUser, Project, Role

from passlib.context import CryptContext
import asyncio

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

first_user = {
    'username': 'Meneger',
    'hashed_password': pwd_context.hash(secret='testpass', scheme="bcrypt")
}

second_user = {
    'username': 'Developer',
    'hashed_password': pwd_context.hash(secret='testpass', scheme="bcrypt")
}

third_user = {
    'username': 'TeamLeader',
    'hashed_password': pwd_context.hash(secret='testpass', scheme="bcrypt")
}

fourth_user = {
    'username': 'TestEngineer',
    'hashed_password': pwd_context.hash(secret='testpass', scheme="bcrypt")
}

projects = {
    'name': 'Тестовый проект'
}


async def filling_db():
    async with async_session_maker() as session:
        user1 = User(**first_user)
        user2 = User(**second_user)
        user3 = User(**third_user)
        user4 = User(**fourth_user)
        project = Project(**projects)
        project_user1 = ProjectUser(
            project=project,
            user=user1,
            role=Role.meneger.name
        )
        project_user2 = ProjectUser(
            project=project,
            user=user2,
            role=Role.developer.name
        )
        project_user3 = ProjectUser(
            project=project,
            user=user3,
            role=Role.team_leader.name
        )
        project_user4 = ProjectUser(
            project=project,
            user=user4,
            role=Role.test_engineer.name
        )

        session.add_all(
            [
                user1, user2,
                user3, user4,
                project,
                project_user1,
                project_user2,
                project_user3,
                project_user4,
            ]
        )
        await session.commit()

asyncio.run(filling_db())
