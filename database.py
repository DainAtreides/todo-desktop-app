import sqlite3

# Функция для создания/подключения базы данных
def connect_db():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    pass

# CRUD
def create_task():
    pass

def get_tasks():
    pass

def update_task():
    pass

def delete_task():
    pass