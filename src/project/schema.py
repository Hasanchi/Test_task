from pydantic import BaseModel
from datetime import datetime

from src.models import Type, Status, Priority, Role


class UpdateUserForManager(BaseModel):
    username: str
    role: Role


class CreatedProject(BaseModel):
    name: str


class UpdateTask(BaseModel):
    type: Type
    priority: Priority
    status: Status
    executor_id: int

    class Config:
        json_schema_extra = {
            'example': {
                'type': 'Bug/Task',
                'priority': 'Critical/High/Medium/Low',
                'status': 'To do/In progress/Code review/Dev test/Testing/Done/Wontfix',
                'executor_id': 2
            }
        }


class CreatedTask(BaseModel):
    type: Type
    priority: Priority
    status: Status
    heading: str
    description: str
    blocking_by_id: int | None = None

    class Config:
        json_schema_extra = {
            'example': {
                'type': 'Bug/Task',
                'priority': 'Critical/High/Medium/Low',
                'status': 'To do/In progress/Code review/Dev test/Testing/Done/Wontfix',
                'heading': 'Функция по добавлению пользовотеля',
                'description': 'Нужно добавить функцию по добавлению пользователя',
                'blocking_by_id': "id или убрать строку"
            }
        }


class SelectedProject(CreatedProject):
    tasks: list[CreatedTask]
