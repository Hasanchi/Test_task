from src.utils.repository import SQLAlchemyRepository

from src.auth.models import User


class UserRepositories(SQLAlchemyRepository):
    model = User
