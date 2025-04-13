import sqlite3

# Функция для создания и подключения к базе данных
def connect_db():
    db = sqlite3.connect('todo.db')
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL,
                      status BOOLEAN DEFAULT 0)''')
    db.commit()
    return db, cursor

# Универсальная функция для выполнения SQL-запросов
def execute_query(cursor, query: str, params: tuple = (), fetchone=False, fetchall=False, commit=False):
    try:
        cursor.execute(query, params)
        if commit:
            cursor.connection.commit()
        if fetchone:
            return cursor.fetchone()
        if fetchall:
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f'Ошибка при выполнении запроса: {e}')
        return None
