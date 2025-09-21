## Project Overview

This project is a web application for managing, monitoring, scheduling, and auditing Python scripts and agents. The application provides a web-based interface for managing the entire lifecycle of these scripts, from execution to logging. The backend is built with FastAPI, and the frontend will be a simple HTML/CSS/JS dashboard. The application also features a REST API for remote management and integration.

**Key Technologies:**

*   **Backend:** FastAPI
*   **Database:** SQLite
*   **Task Scheduling:** APScheduler (planned)
*   **Sandboxing:** Docker, VM, or chroot jail (planned)
*   **Frontend:** HTML/CSS/JavaScript (planned)

## Features

### Implemented
- User authentication with JWT tokens
- Full CRUD operations for Agents, Scripts, and Tasks
- RESTful API with OpenAPI documentation
- Environment-based configuration
- SQLite database with SQLAlchemy ORM

### Planned
- Task scheduling with APScheduler
- Script execution sandboxing
- Audit logging system
- Web dashboard
- Advanced security features

## API Endpoints

### Authentication
- `POST /token` - Login and get access token
- `POST /users/` - Create new user
- `GET /users/me/` - Get current user info

### Agents
- `GET /agents/` - List all agents
- `GET /agents/{id}` - Get agent by ID
- `POST /agents/` - Create new agent
- `PUT /agents/{id}` - Update agent
- `DELETE /agents/{id}` - Delete agent

### Scripts
- `GET /scripts/` - List all scripts
- `GET /scripts/{id}` - Get script by ID
- `POST /scripts/` - Create new script
- `PUT /scripts/{id}` - Update script
- `DELETE /scripts/{id}` - Delete script

### Tasks
- `GET /tasks/` - List all tasks
- `GET /tasks/{id}` - Get task by ID
- `POST /tasks/` - Create new task
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task

## Running the Application

To run the application, use the following command:

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

The API documentation will be available at `http://localhost:8000/docs`

## Environment Configuration

Create a `.env` file in the project root with:

```
SECRET_KEY=your-secret-key-change-this-in-production
DATABASE_URL=sqlite:///./automa.db
```
