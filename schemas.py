from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str

class User(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class AgentBase(BaseModel):
    name: str
    description: str
    status: str

class AgentCreate(AgentBase):
    pass

class Agent(AgentBase):
    id: int

    class Config:
        orm_mode = True

class ScriptBase(BaseModel):
    name: str
    description: str
    filename: str

class ScriptCreate(ScriptBase):
    pass

class Script(ScriptBase):
    id: int

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    name: str
    description: str
    script_id: int
    agent_id: int

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True
