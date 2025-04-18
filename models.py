from database import Database

class Task:
    def __init__(self, title: str):
        self.title = title
        self.status = False
    '''CRUD-функционал'''
    def create_task(self, db: Database):
        '''Создаёт задачу'''
        query = 'INSERT INTO tasks (title, status) VALUES (?, ?)'
        params = (self.title, self.status)
        db.execute_query(query, params, commit=True)
        
    @staticmethod    
    def read_task(db: Database):
        '''Показывает все задачи'''
        query = 'SELECT * FROM tasks'
        return db.execute_query(query, fetchall=True)

    @staticmethod  
    def update_task(db: Database, task_id: int):
        '''Изменяет статус задачи'''
        query = 'SELECT status FROM tasks WHERE id = ?'
        task = db.execute_query(query, (task_id,), fetchone=True)
        if task:
            new_status = 0 if task[0] else 1
            query = 'UPDATE tasks SET status = ? WHERE id = ?'
            db.execute_query(query, (new_status, task_id), commit=True)
        else:
            print(f"Task {task_id} doesn't exist.")

    @staticmethod  
    def delete_task(db: Database, task_id: int):
        '''Удаляет задачу'''
        query = 'SELECT * FROM tasks WHERE id = ?'
        if db.execute_query(query, (task_id,), fetchone=True):
            query = 'DELETE FROM tasks WHERE id = ?'
            db.execute_query(query, (task_id,), commit=True)