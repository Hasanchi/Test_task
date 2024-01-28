from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.models import Base
from src.auth.schema import SelectUserSchema

from enum import Enum
from datetime import datetime
from typing import Annotated

str_50 = Annotated[str, 50]
str_150 = Annotated[str, 150]


class Type(Enum):
    bug = 'Bug'
    task = 'Task'


class Status(Enum):
    to_do = 'To do'
    in_progress = 'In progress'
    code_review = 'Code review'
    dev_test = 'Dev test'
    testing = 'Testing'
    done = 'Done'
    wontfix = 'Wontfix'


class Priority(Enum):
    critical = 'Critical'
    high = 'High'
    medium = 'Medium'
    low = 'Low'


class Role(Enum):
    meneger = 'Менеджер'
    developer = 'Разработчик'
    team_leader = 'Тимлид'
    test_engineer = 'Тест-инженер'


class Task(Base):
    __tablename__ = 'task'
    __table_args__ = {'extend_existing': True}
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    type: Mapped['Type']
    priority: Mapped['Priority']
    status: Mapped['Status']
    heading: Mapped[str_50]
    description: Mapped[str_150]
    executor_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            'user.id',
            ondelete='SET NULL'
        )
    )
    сreator_id: Mapped[int] = mapped_column(
        ForeignKey(
            'user.id',
            ondelete='SET NULL'
        )
    )
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now()
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey(
            'project.id',
            ondelete='SET NULL'
        )
    )
    project: Mapped['Project'] = relationship(
        back_populates='tasks'
    )

    blocking_by_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            'task.id',
            ondelete='CASCADE'
        )
    )
    blocking_by: Mapped[list['Task']] = relationship(
        remote_side=[id]
    )
    blocked_by: Mapped[list['Task']] = relationship(
        remote_side=[blocking_by_id]
    )


class Project(Base):
    __tablename__ = 'project'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    tasks: Mapped['Task'] = relationship(
        back_populates='project'
    )
    project_user: Mapped['ProjectUser'] = relationship(
        back_populates='project'
    )


class ProjectUser(Base):
    __tablename__ = 'project_user'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey(
            'project.id',
            ondelete='SET NULL'
        )
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            'user.id',
            ondelete='SET NULL'
        )
    )
    project: Mapped['Project'] = relationship(
        back_populates='project_user'
    )
    user: Mapped['User'] = relationship(
        back_populates='project_user'
    )
    role: Mapped['Role'] = mapped_column(nullable=True)


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    project_user: Mapped['ProjectUser'] = relationship(
        back_populates='user'
    )

    def to_read_model(self) -> SelectUserSchema:
        return SelectUserSchema(
            id=self.id,
            username=self.username
        )
