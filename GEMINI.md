## Project Overview

This project is a web application for managing, monitoring, scheduling, and auditing Python scripts and agents. The application will provide a web-based interface for managing the entire lifecycle of these scripts, from execution to logging. The backend will be built with FastAPI, and the frontend will be a simple HTML/CSS/JS dashboard. The application will also feature a REST API for remote management and integration.

**Key Technologies:**

*   **Backend:** FastAPI
*   **Database:** SQLite
*   **Task Scheduling:** Celery or APScheduler
*   **Sandboxing:** Docker, VM, or chroot jail
*   **Frontend:** HTML/CSS/JavaScript

## Building and Running

**TODO:** Add build and run commands here once they are defined.

## Development Conventions

*   Use `uv` for managing Python dependencies, not `pip`.
*   All scripts must run in a sandboxed environment.
*   All actions must be audited and logged.
*   The backend should be designed with a modular and extensible architecture, allowing for the addition of new features through plugins or modules.
*   The API should follow RESTful principles.
*   Authentication will be based on email and password, with role-based access control (admin, user).
