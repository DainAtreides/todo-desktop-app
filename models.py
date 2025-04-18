from abc import ABC, abstractmethod
from database import Database

class Task(ABC):
    """Абстракция для задачи"""
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

class TaskManager(Task):
    def __init__(self, db: Database):
        self.db = db
    def create(self, title: str):
        """Создаёт задачу в базе данных"""
        query = 'INSERT INTO tasks (title) VALUES (?)'
        params = (title,)
        self.db.execute_query(query, params, commit=True)
    def update(self, task_id: int):
        """Обновляет статус задачи"""
        task = self.db.execute_query(query, (task_id,), fetchone=True)
        if task:
            current_status = task[-1]
            new_status = int(not current_status)
            query = 'UPDATE tasks SET status = ? WHERE id = ?'
            self.db.execute_query(query, (new_status, task_id), commit=True)
        else:
            print(f"Task {task_id} doesn't exist.")
    def delete(self, task_id: int):
        """Удаляет задачу"""
        query = 'SELECT * FROM tasks WHERE id = ?'
        if self.db.execute_query(query, (task_id,), fetchone=True):
            query = 'DELETE FROM tasks WHERE id = ?'
            self.db.execute_query(query, (task_id,), commit=True)
    def show(self):
        """Показывает все задачи"""
        query = 'SELECT * FROM tasks'
        return self.db.execute_query(query, fetchall=True)