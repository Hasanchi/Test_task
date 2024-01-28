from pydantic import BaseModel
from datetime import datetime

from src.project.models import Type, Status, Priority, Role


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
    blocked_by_id: int | None = None

    class Config:
        json_schema_extra = {
            'example': {
                'type': 'Bug/Task',
                'priority': 'Critical/High/Medium/Low',
                'status': 'To do/In progress/Code review/Dev test/Testing/Done/Wontfix',
                'heading': 'Функция по добавлению пользовотеля',
                'description': 'Нужно добавить функцию по добавлению пользователя',
                'blocked_by_id': 5
            }
        }


class SelectTask(CreatedTask):
    id: int
    сreator_id: int
    executor_id: int | None
    created_at: datetime
    updated_at: datetime
    project_id: int

    class Cofig:
        json_schema_extra = None
        from_attributes = True


class DetailTask(SelectTask):

    blocking_by: list[SelectTask] | None
    blocked_by: list[SelectTask] | None


class SelectedProject(CreatedProject):
    tasks: list[CreatedTask]
