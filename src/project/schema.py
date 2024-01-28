from pydantic import BaseModel
from datetime import datetime

from src.project.models import Type, Status, Priority, Role


class UpdateUserForManager(BaseModel):
    username: str
    role: Role


class CreatedProject(BaseModel):
    name: str


class UpdateTask(BaseModel):
    status: Status
    executor_id: int


class CreatedTask(BaseModel):
    id: int
    type: Type
    priority: Priority
    status: Status
    heading: str
    description: str

    class Config:
        json_schema_extra = {
            'example': {
                'type': 'Bug/Task',
                'priority': 'Critical/High/Medium/Low',
                'status': 'To do/In progress/Code review/Dev test/Testing/Done/Wontfix',
                'heading': 'Функция по добавлению пользовотеля',
                'description': 'Нужно добавить функцию по добавлению пользователя'
            }
        }


class SelectTask(CreatedTask):
    сreator_id: int
    executor_id: int | None
    created_at: datetime
    updated_at: datetime
    project_id: int

    class Cofig:
        json_schema_extra = None
        from_attributes = True


class SelectedProject(CreatedProject):
    tasks: list[CreatedTask]
