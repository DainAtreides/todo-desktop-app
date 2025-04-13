import sqlite3

# Функция для создания/подключения базы данных
def connect_db():
    db = sqlite3.connect('todo.db')
    cursor = db.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS 
            tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status BOOLEAN DEFAULT 0
            )
        '''
    )
    db.commit()
    return db, cursor

# CRUD (Create Read Update Delete) функционал
# Функция для создания новой задачи
def create_task(title: str, status=False):
    db, cursor = connect_db()
    cursor.execute(
        '''
        INSERT INTO tasks (title, status) VALUES (?, ?)
        ''', (title, int(status))
    )
    db.commit()
    db.close()

# Функция для вывода списка всех задач
def get_tasks():
    db, cursor = connect_db()
    cursor.execute(
        '''
        SELECT * FROM tasks
        '''
    )
    tasks = cursor.fetchall()
    db.close()
    if not tasks:
        print('Задач нет.')
    else:
        for task in tasks:
            task_id, title, status = task
            status_str = '✅Выполнено' if status else '❌Не выполнено'
            print(f'{task_id}. {title} {status_str}')

#
def update_task():
    db, cursor = connect_db()
    pass

#
def delete_task():
    pass