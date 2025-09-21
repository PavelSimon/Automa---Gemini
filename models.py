from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    status = Column(String)

    tasks = relationship("Task", back_populates="agent")

class Script(Base):
    __tablename__ = "scripts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    content = Column(String)  # The actual Python script content
    filename = Column(String)

    tasks = relationship("Task", back_populates="script")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    script_id = Column(Integer, ForeignKey("scripts.id"), index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), index=True)
    status = Column(String, default="pending")  # pending, running, completed, failed
    scheduled_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    script = relationship("Script", back_populates="tasks")
    agent = relationship("Agent", back_populates="tasks")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String)  # create, update, delete, execute, login, etc.
    resource_type = Column(String)  # agent, script, task, user
    resource_id = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(String, nullable=True)  # JSON string with additional info
    ip_address = Column(String, nullable=True)

    user = relationship("User")
