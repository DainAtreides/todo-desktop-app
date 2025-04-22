import sqlite3
import logging
from abc import ABC, abstractmethod

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


# Abstract base class for a database
class Database(ABC):
    @abstractmethod
    def connect(self):
        # Establish a database connection
        pass

    @abstractmethod
    def execute_query(self):
        # Execute an SQL query
        pass

    @abstractmethod
    def close(self):
        # Close the database connection
        pass


# Concrete implementation of the Database for task management
class TaskDatabase(Database):
    def __init__(self, db_name: str):
        # Initialize with database name
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        # Connect to SQLite database and create tasks table if needed
        if self.db_name:
            if self.connection:
                logger.warning('Connection already established.')
                return
            logger.info('Connecting to the database...')
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   title TEXT NOT NULL,
                                   status BOOLEAN DEFAULT 0)''')
            self.connection.commit()
            logger.info('Connection established.')
        else:
            raise ValueError('Database name is missing.')

    def execute_query(self, query: str, params: tuple = (), fetchone=False, fetchall=False, commit=False):
        # Run an SQL query with optional fetching and committing
        if self.connection is None:
            logger.error('No connection established.')
            return None
        try:
            logger.debug(f'Executing query: {query} | Params: {params}')
            self.cursor.execute(query, params)
            if commit:
                self.connection.commit()
            if fetchone:
                return self.cursor.fetchone()
            if fetchall:
                return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f'Query execution error: {e}')
            return None

    def close(self):
        # Close the connection to the database
        if self.connection:
            logger.info('Closing database connection...')
            self.connection.close()
            self.connection = None
            self.cursor = None
            logger.info('Connection closed.')
        else:
            logger.warning('No connection to close.')
