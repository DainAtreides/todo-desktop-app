import sqlite3
from db_utils import execute_query

# Функция для создания задачи
def create_task(cursor, title: str, status=False):
    if execute_query(cursor, 'SELECT * FROM tasks WHERE title = ?', (title,), fetchone=True):
        print(f'Задача с названием "{title}" уже существует.')
        return False
    query = 'INSERT INTO tasks (title, status) VALUES (?, ?)'
    return execute_query(cursor, query, (title, int(status)), commit=True) is not None

# Функция для получения всех задач
def get_tasks(cursor):
    tasks = execute_query(cursor, 'SELECT * FROM tasks', fetchall=True)
    if not tasks:
        print('Задач нет.')
    else:
        for task in tasks:
            task_id, title, status = task
            status_str = '✅ Выполнено' if status else '❌ Не выполнено'
            print(f'{task_id}. {title} {status_str}')
    return tasks

# Функция для обновления статуса задачи
def update_task(cursor, task_id: int):
    task = execute_query(cursor, 'SELECT status FROM tasks WHERE id = ?', (task_id,), fetchone=True)
    if task:
        new_status = 0 if task[0] else 1
        execute_query(cursor, 'UPDATE tasks SET status = ? WHERE id = ?', (new_status, task_id), commit=True)
        print(f'Задача с ID {task_id} обновлена.')
    else:
        print(f'Задача с ID {task_id} не найдена.')

# Функция для удаления задачи
def delete_task(cursor, task_id: int):
    if execute_query(cursor, 'SELECT * FROM tasks WHERE id = ?', (task_id,), fetchone=True):
        execute_query(cursor, 'DELETE FROM tasks WHERE id = ?', (task_id,), commit=True)
        print(f'Задача с ID {task_id} удалена.')
    else:
        print(f'Задача с ID {task_id} не найдена.')