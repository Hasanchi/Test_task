from pydantic import BaseModel
from datetime import datetime

from src.project.models import Type, Status, Priority, Role

class UpdateUserForManager(BaseModel):
    username: str
    role: Role

class CreatedProject(BaseModel):
    name: str


class CreatedTask(BaseModel):
    type: Type
    priority: Priority
    status: Status
    heading: str
    description: str

class UpdateTask(BaseModel):
    status: Status
    executor_id: int



class SelectedProject(CreatedProject):
    tasks: list[CreatedTask]




    
    
