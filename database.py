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

# CRUD (Create Read Update Delete)

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

#
def get_tasks():
    pass

#
def update_task():
    pass

#
def delete_task():
    pass