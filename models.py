from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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
    filename = Column(String)

    tasks = relationship("Task", back_populates="script")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    script_id = Column(Integer, ForeignKey("scripts.id"), index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), index=True)

    script = relationship("Script", back_populates="tasks")
    agent = relationship("Agent", back_populates="tasks")
