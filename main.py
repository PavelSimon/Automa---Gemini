from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from database import engine, get_db
from models import Base
from schemas import UserCreate, User, Token, Agent, AgentCreate, Script, ScriptCreate, Task, TaskCreate
import crud
import auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/me/", response_model=User)
def read_users_me(current_user: User = Depends(auth.get_current_user)):
    return current_user

# Agent endpoints
@app.get("/agents/", response_model=List[Agent])
def read_agents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    agents = crud.get_agents(db, skip=skip, limit=limit)
    return agents

@app.get("/agents/{agent_id}", response_model=Agent)
def read_agent(agent_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    db_agent = crud.get_agent(db, agent_id=agent_id)
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return db_agent

@app.post("/agents/", response_model=Agent)
def create_agent(agent: AgentCreate, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    return crud.create_agent(db=db, agent=agent)

@app.put("/agents/{agent_id}", response_model=Agent)
def update_agent(agent_id: int, agent: AgentCreate, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    db_agent = crud.update_agent(db, agent_id=agent_id, agent=agent)
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return db_agent

@app.delete("/agents/{agent_id}", response_model=Agent)
def delete_agent(agent_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    db_agent = crud.delete_agent(db, agent_id=agent_id)
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return db_agent

# Script endpoints
@app.get("/scripts/", response_model=List[Script])
def read_scripts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    scripts = crud.get_scripts(db, skip=skip, limit=limit)
    return scripts

@app.get("/scripts/{script_id}", response_model=Script)
def read_script(script_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    db_script = crud.get_script(db, script_id=script_id)
    if db_script is None:
        raise HTTPException(status_code=404, detail="Script not found")
    return db_script

@app.post("/scripts/", response_model=Script)
def create_script(script: ScriptCreate, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    return crud.create_script(db=db, script=script)

@app.put("/scripts/{script_id}", response_model=Script)
def update_script(script_id: int, script: ScriptCreate, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    db_script = crud.update_script(db, script_id=script_id, script=script)
    if db_script is None:
        raise HTTPException(status_code=404, detail="Script not found")
    return db_script

@app.delete("/scripts/{script_id}", response_model=Script)
def delete_script(script_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    db_script = crud.delete_script(db, script_id=script_id)
    if db_script is None:
        raise HTTPException(status_code=404, detail="Script not found")
    return db_script

# Task endpoints
@app.get("/tasks/", response_model=List[Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    return crud.create_task(db=db, task=task)

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    db_task = crud.update_task(db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    db_task = crud.delete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.get("/")
def read_root():
    return {"Hello": "World"}
