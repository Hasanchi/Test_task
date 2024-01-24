from pydantic import BaseModel


class SelectUserSchema(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True


class InsertUserSchema(SelectUserSchema):
    hashed_password: str
