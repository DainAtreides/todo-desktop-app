import sqlite3
from abc import ABC, abstractmethod

class Database(ABC):
    """Абстракция для базы данных"""
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def execute_query(self):
        pass

    @abstractmethod    
    def close(self):
        pass    

class TaskDatabase(Database):
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None
        self.cursor = None   

    def connect(self):
        """Подключает существующую или создаёт новую базу данных"""
        if self.db_name:
            if self.connection:
                print("Connection already established.")
                return  # Уже есть соединение
            print("Connecting to the database...")
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   title TEXT NOT NULL,
                                   status BOOLEAN DEFAULT 0)''')
            self.connection.commit()
            print("Connection established.")
        else:
            raise ValueError("Name doesn't exist.")   

    def execute_query(
    self, query: str, params: tuple = (), fetchone=False, fetchall=False, commit=False):
        """Выполняет SQL-запросы"""
        if self.connection is None:
            print("Error: No connection established.")
            return None
        
        connection = self.connection
        cursor = self.cursor
        try:
            print(f"Executing query: {query} with params {params}")
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

    def close(self):
        """Закрывает соединение с базой данных"""
        if self.connection:
            print("Closing connection...")
            self.connection.close()
            self.connection = None
            self.cursor = None
            print("Connection closed.")
        else:
            print("No connection to close.")
