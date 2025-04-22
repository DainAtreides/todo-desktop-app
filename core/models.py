from abc import ABC, abstractmethod
import logging
from database.db import Database

# Configure logger for this module
logger = logging.getLogger(__name__)


# Abstract base class for task operations
class Task(ABC):
    @abstractmethod
    def create(self, title: str):
        pass

    @abstractmethod
    def update(self, task_id: int):
        pass

    @abstractmethod
    def delete(self, task_id: int):
        pass

    @abstractmethod
    def show(self):
        pass


# Concrete implementation of the Task for CRUD operations
class TaskManager(Task):
    def __init__(self, db: Database):
        # Initialize with a database instance
        self.db = db

    def create(self, title: str):
        # Create a new task with the provided title
        if not title:
            logger.warning('Attempted to create a task with empty title.')
            return
        query = 'INSERT INTO tasks (title) VALUES (?)'
        params = (title,)
        logger.info(f'Creating task with title: "{title}"')
        self.db.execute_query(query, params, commit=True)

    def update(self, task_id: int, new_status: bool):
        # Update the status of a task
        query = 'SELECT status FROM tasks WHERE id = ?'
        task = self.db.execute_query(query, (task_id,), fetchone=True)
        if not task:
            logger.warning(f'Task with ID {task_id} does not exist.')
            return
        new_status_int = int(new_status)
        query = 'UPDATE tasks SET status = ? WHERE id = ?'
        logger.info(f'Updating task ID {task_id} to status: {new_status}')
        self.db.execute_query(query, (new_status_int, task_id), commit=True)

    def delete(self, task_id: str):
        # Delete a task by its ID
        query = 'SELECT * FROM tasks WHERE id = ?'
        task = self.db.execute_query(query, (task_id,), fetchone=True)
        if not task:
            logger.warning(
                f'Attempted to delete non-existent task ID {task_id}.')
            return
        query = 'DELETE FROM tasks WHERE id = ?'
        logger.info(f'Deleting task ID {task_id}')
        self.db.execute_query(query, (task_id,), commit=True)

    def show(self):
        # Retrieve all tasks from the database
        logger.info('Fetching all tasks.')
        query = 'SELECT * FROM tasks'
        return self.db.execute_query(query, fetchall=True)
