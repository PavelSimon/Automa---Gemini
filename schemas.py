from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str

class User(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

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
        from_attributes = True

class ScriptBase(BaseModel):
    name: str
    description: str
    content: str
    filename: str

class ScriptCreate(ScriptBase):
    pass

class Script(ScriptBase):
    id: int

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    name: str
    description: str
    script_id: int
    agent_id: int

class TaskCreate(TaskBase):
    scheduled_time: Optional[datetime] = None

class Task(TaskBase):
    id: int
    status: str
    scheduled_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    script_id: Optional[int] = None
    agent_id: Optional[int] = None
    status: Optional[str] = None
    scheduled_time: Optional[datetime] = None

class AuditLogBase(BaseModel):
    user_id: Optional[int]
    action: str
    resource_type: str
    resource_id: Optional[int]
    details: Optional[str]
    ip_address: Optional[str]

class AuditLogCreate(AuditLogBase):
    pass

class AuditLog(AuditLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
