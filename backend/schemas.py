from pydantic import BaseModel, Field

class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)

class TodoCreate(TodoBase):
    completed: bool = False

class TodoUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

class TodoRead(TodoBase):
    id: int
    completed: bool