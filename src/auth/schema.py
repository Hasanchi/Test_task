from pydantic import BaseModel


class UpdateUserSchema(BaseModel):
    username: str
    role: str


class SelectUserSchema(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class InsertUserSchema(SelectUserSchema):
    hashed_password: str
