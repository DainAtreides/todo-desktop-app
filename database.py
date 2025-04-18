import sqlite3

class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
    
    def connect(self):
        '''Подключает существующую или создаёт новую базу данных'''
        if self.db_name:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   title TEXT NOT NULL,
                                   status BOOLEAN DEFAULT 0)''')
            self.connection.commit()
        else:
            raise ValueError("Name doesn't exist.")
            
    def close(self):
        '''Закрывает соединение с базой данных'''
        if self.connection:
            self.connection.close()
        
    def execute_query(
        self, query: str, params: tuple = (), fetchone=False, fetchall=False, commit=False):
        '''Выполняет SQL-запросы'''
        connection = self.connection
        cursor = self.cursor
        try:
            cursor.execute(query, params)
            if commit:
                connection.commit()
            if fetchone:
                return cursor.fetchone()
            if fetchall:
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f'Query execution error: {e}')
            return None