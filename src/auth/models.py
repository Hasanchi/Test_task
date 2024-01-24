from sqlalchemy.orm import mapped_column, Mapped

from src.models import Base
from src.auth.schema import SelectUserSchema

from enum import Enum


class Role(Enum):
    meneger = 'Менеджер'
    developer = 'Разработчик'
    team_leader = 'Тимлид'
    test_engineer = 'Тест-инженер'


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    role: Mapped['Role'] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    def to_read_model(self) -> SelectUserSchema:
        return SelectUserSchema(
            id=self.id,
            role=self.role,
            username=self.username
        )
