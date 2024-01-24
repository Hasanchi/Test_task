from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.models import Base
from src.auth.models import User

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
