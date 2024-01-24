from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class Project(Base):
    __tablename__ = 'project'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            'user.id',
            ondelete='SET NULL'
        )
    )
