from src.utils.repository import AbstractRepository 

from src.auth.schema import InsertUserSchema


class UserServices:
    def __init__(self, user_repo: AbstractRepository) -> None:
        self.user_repo = user_repo()

    async def get_users(self):
        users = await self.user_repo.select_all()
        return users
    
    async def add_user(self, user: InsertUserSchema):
        user_dict = user.model_dump()
        user_id = await self.user_repo.add_one(user_dict)
        return user_id
