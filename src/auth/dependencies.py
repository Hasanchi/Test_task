from src.repositories.user import UserRepositories

from src.services.user import UserServices

def user_service():
    return UserServices(UserRepositories)