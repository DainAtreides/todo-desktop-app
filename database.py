import sqlite3

# Функция для создания/подключения базы данных
def connect_db():
    db = sqlite3.connect('todo.db')
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS 
                      tasks (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL,
                      status BOOLEAN DEFAULT 0)''')
    db.commit()
    return db, cursor

# Универсальная функция для выполнения SQL-запросов
def execute_query(query: str, params: tuple = ()):
    db, cursor = connect_db()
    try:
        cursor.execute(query, params)
        db.commit()
        return cursor
    except sqlite3.Error as e:
        print(f'Ошибка при выполнении запроса: {e}')
        return None
    finally:
        db.close()

# CRUD (Create Read Update Delete) функционал
# Функция для создания новой задачи
def create_task(title: str, status=False) -> bool:
    query = 'INSERT INTO tasks (title, status) VALUES (?, ?)'
    result = execute_query(query, (title, int(status)))
    return result is not None
            
# Функция для вывода списка всех задач
def get_tasks() -> list[tuple]:
    query = 'SELECT * FROM tasks'
    cursor = execute_query(query)
    if cursor is None:
        return []             
    tasks = cursor.fetchall()
    if not tasks:
        print('Задач нет.')
        return [] 
    for task in tasks:
        task_id, title, status = task
        status_str = '✅Выполнено' if status else '❌Не выполнено'
        print(f'{task_id}. {title} {status_str}')
    return tasks

# Функция для изменения статуса задачи
def update_task(task_id: int) -> bool:
    query = 'SELECT status FROM tasks WHERE id = ?'
    result = execute_query(query, (task_id,), fetchone=True)
    if result is None:
        print(f'Задача с ID {task_id} не найдена.')
        return False
    current_status = result[0]
    new_status = 0 if current_status else 1
    update_query = 'UPDATE tasks SET status = ? WHERE id = ?'
    result = execute_query(update_query, (new_status, task_id))
    return result is not None

# Функция для удаления задачи
def delete_task(task_id: int) -> bool:
    query = 'DELETE FROM tasks WHERE id = ?'
    result = execute_query(query, (task_id,))
    if result is None:
        print(f'Ошибка при удалении задачи с ID {task_id}')
        return False
    if result.rowcount == 0:
        print(f'Задача с ID {task_id} не найдена.')
        return False
    return True