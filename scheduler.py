from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
from sqlalchemy.orm import Session
import asyncio
import logging

from database import get_db
from crud import get_task, update_task, log_action, get_script
from executor import execute_python_script
from config import settings

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

async def execute_task(task_id: int):
    """Execute a scheduled task"""
    db = next(get_db())
    task = None
    try:
        task = get_task(db, task_id)
        if not task:
            logger.error(f"Task {task_id} not found")
            return

        # Update task status to running
        update_task(db, task_id, {"status": "running"})

        logger.info(f"Executing task {task_id}: {task.name}")

        # Get the script content
        script = get_script(db, task.script_id)
        if not script:
            raise Exception(f"Script {task.script_id} not found")

        # Execute the script
        from executor import execute_python_script
        result = await asyncio.get_event_loop().run_in_executor(
            None, execute_python_script, script.content, f"task_{task_id}.py"
        )

        # Update task status based on execution result
        if result["success"]:
            update_task(db, task_id, {"status": "completed"})
            logger.info(f"Task {task_id} completed successfully")
        else:
            update_task(db, task_id, {"status": "failed"})
            logger.error(f"Task {task_id} failed: {result['error']}")

        # Log the execution
        log_action(
            db,
            action="execute",
            resource_type="task",
            resource_id=task_id,
            details={
                "status": "completed" if result["success"] else "failed",
                "script_id": task.script_id,
                "execution_time": result["execution_time"],
                "output": result["output"][:500] if result["output"] else None,  # Truncate output
                "error": result["error"][:500] if result["error"] else None
            }
        )

    except Exception as e:
        logger.error(f"Error executing task {task_id}: {str(e)}")
        if task:
            update_task(db, task_id, {"status": "failed"})

        log_action(
            db,
            action="execute",
            resource_type="task",
            resource_id=task_id,
            details={"status": "failed", "error": str(e)}
        )
    finally:
        db.close()

def schedule_task(task_id: int, scheduled_time: datetime):
    """Schedule a task for execution"""
    if scheduled_time > datetime.utcnow():
        scheduler.add_job(
            execute_task,
            trigger=DateTrigger(run_date=scheduled_time),
            args=[task_id],
            id=f"task_{task_id}",
            replace_existing=True
        )
        logger.info(f"Scheduled task {task_id} for {scheduled_time}")

def cancel_task_schedule(task_id: int):
    """Cancel a scheduled task"""
    try:
        scheduler.remove_job(f"task_{task_id}")
        logger.info(f"Cancelled schedule for task {task_id}")
    except Exception as e:
        logger.warning(f"Could not cancel schedule for task {task_id}: {str(e)}")

def load_scheduled_tasks():
    """Load all pending scheduled tasks from database"""
    db = next(get_db())
    try:
        # Get all tasks with scheduled_time in the future and status pending
        from models import Task
        pending_tasks = db.query(Task).filter(
            Task.scheduled_time.isnot(None),
            Task.scheduled_time > datetime.utcnow(),
            Task.status == "pending"
        ).all()

        for task in pending_tasks:
            schedule_task(task.id, task.scheduled_time)

        logger.info(f"Loaded {len(pending_tasks)} scheduled tasks")
    finally:
        db.close()

def start_scheduler():
    """Start the APScheduler"""
    load_scheduled_tasks()
    scheduler.start()
    logger.info("Scheduler started")

def stop_scheduler():
    """Stop the APScheduler"""
    scheduler.shutdown()
    logger.info("Scheduler stopped")
