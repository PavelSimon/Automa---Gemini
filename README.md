## Project Overview

This project is a web application for managing, monitoring, scheduling, and auditing Python scripts and agents. The application will provide a web-based interface for managing the entire lifecycle of these scripts, from execution to logging. The backend will be built with FastAPI, and the frontend will be a simple HTML/CSS/JS dashboard. The application will also feature a REST API for remote management and integration.

**Key Technologies:**

*   **Backend:** FastAPI
*   **Database:** SQLite
*   **Task Scheduling:** Celery or APScheduler
*   **Sandboxing:** Docker, VM, or chroot jail
*   **Frontend:** HTML/CSS/JavaScript

## Running the Application

To run the application, use the following command:

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```