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
- Task scheduling with APScheduler
- Script execution with basic sandboxing
- Comprehensive audit logging system
- RESTful API with OpenAPI documentation
- Environment-based configuration
- SQLite database with SQLAlchemy ORM

### Planned
- Web dashboard
- Advanced security features (Docker sandboxing, role-based access)
- Real-time monitoring
- Plugin architecture

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
- `POST /tasks/` - Create new task (supports scheduled_time for scheduling)
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task
- `POST /tasks/{id}/execute` - Execute task immediately

### Audit Logs
- `GET /audit/` - List audit logs (filterable by user_id, resource_type)

## Running the Application

To run the application, use the following command:

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

The API documentation will be available at `http://localhost:8000/docs`

The web dashboard will be available at `http://localhost:8000/dashboard`

## Dashboard Features

The Automa-Gemini dashboard provides a complete web interface for managing your Python scripts and agents:

### Authentication
- **User Registration**: Create new accounts with email and password
- **Email/Password Login**: Standard authentication with JWT tokens
- **Token-based login**: Direct API token entry for advanced users
- **Persistent sessions**: Authentication tokens stored locally
- **Secure logout**: Properly clears session data and local storage

### Dashboard Overview
- **Real-time statistics**: Live counts of agents, scripts, tasks, and running processes
- **Recent activity**: Latest task executions with status indicators
- **Auto-refresh**: Configurable automatic data updates

### Management Sections
- **Agents**: Create and manage execution agents
- **Scripts**: Upload and manage Python scripts with validation
- **Tasks**: Schedule and execute tasks with real-time monitoring
- **Audit Logs**: Comprehensive activity logging and monitoring

### Advanced Features
- **Settings**: Configurable refresh intervals and preferences
- **Data Export**: Download all system data as JSON
- **Connection Testing**: Verify API connectivity
- **User Profile**: View current user information

## Environment Configuration

Create a `.env` file in the project root with:

```
SECRET_KEY=your-secret-key-change-this-in-production
DATABASE_URL=sqlite:///./automa.db
```
