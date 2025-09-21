from sqlalchemy.orm import Session
from passlib.context import CryptContext

from models import User, Agent, Script, Task
from schemas import UserCreate, AgentCreate, ScriptCreate, TaskCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# User CRUD
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Agent CRUD
def get_agents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Agent).offset(skip).limit(limit).all()

def get_agent(db: Session, agent_id: int):
    return db.query(Agent).filter(Agent.id == agent_id).first()

def create_agent(db: Session, agent: AgentCreate):
    db_agent = Agent(**agent.dict())
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

def update_agent(db: Session, agent_id: int, agent: AgentCreate):
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if db_agent:
        for key, value in agent.dict().items():
            setattr(db_agent, key, value)
        db.commit()
        db.refresh(db_agent)
    return db_agent

def delete_agent(db: Session, agent_id: int):
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if db_agent:
        db.delete(db_agent)
        db.commit()
    return db_agent

# Script CRUD
def get_scripts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Script).offset(skip).limit(limit).all()

def get_script(db: Session, script_id: int):
    return db.query(Script).filter(Script.id == script_id).first()

def create_script(db: Session, script: ScriptCreate):
    db_script = Script(**script.dict())
    db.add(db_script)
    db.commit()
    db.refresh(db_script)
    return db_script

def update_script(db: Session, script_id: int, script: ScriptCreate):
    db_script = db.query(Script).filter(Script.id == script_id).first()
    if db_script:
        for key, value in script.dict().items():
            setattr(db_script, key, value)
        db.commit()
        db.refresh(db_script)
    return db_script

def delete_script(db: Session, script_id: int):
    db_script = db.query(Script).filter(Script.id == script_id).first()
    if db_script:
        db.delete(db_script)
        db.commit()
    return db_script

# Task CRUD
def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Task).offset(skip).limit(limit).all()

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def create_task(db: Session, task: TaskCreate):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: TaskCreate):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        for key, value in task.dict().items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task
