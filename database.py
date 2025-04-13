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
def create_task(title: str, status=False) -> bool:
    try:
        db, cursor = connect_db()
        cursor.execute(
            '''
            INSERT INTO tasks (title, status) VALUES (?, ?)
            ''', (title, int(status))
        )
        db.commit()
        return True
    except sqlite3.Error as e:
        print(f'Ошибка при создании задачи: {e}')
    finally:
        db.close()

# Функция для вывода списка всех задач
def get_tasks() -> list[tuple]:
    db, cursor = connect_db()
    try:
        cursor.execute(
            '''
            SELECT * FROM tasks
            '''
        )
        tasks = cursor.fetchall()
        if not tasks:
            print('Задач нет.')
            return []
        else:
            for task in tasks:
                task_id, title, status = task
                status_str = '✅Выполнено' if status else '❌Не выполнено'
                print(f'{task_id}. {title} {status_str}')
        return tasks
    except sqlite3.Error as e:
        print(f'Ошибка при выводе списка задач: {e}')
        return []
    finally:
        db.close()

# Функция для изменения статуса задачи
def update_task(task_id: int) -> bool:
    db, cursor = connect_db()
    try:
        cursor.execute(
            '''
            SELECT status FROM tasks WHERE id = ?
            ''', (task_id,)
        )
        result = cursor.fetchone()
        if result is None:
            print(f'Задача с ID {task_id} не найдена.')
            return False
        current_status = result[0]
        new_status = 0 if current_status else 1
        cursor.execute(
            '''
            UPDATE tasks SET status = ? WHERE id = ?
            ''', (new_status, task_id)
        )
        db.commit()
        return True
    except sqlite3.Error as e:
        print(f'Ошибка при изминении задачи: {e}')
        return False
    finally:
        db.close()

# Функция для удаления задачи
def delete_task(task_id: int):
    db, cursor = connect_db()
    try:
        cursor.execute(
            '''
            DELETE FROM tasks WHERE id = ?
            ''', (task_id,)
        )
        db.commit()
        if cursor.rowcount == 0:
            print(f"Задача с ID {task_id} не найдена.")
            return False
        return True
    except sqlite3.Error as e:
        print(f'Ошибка при удалении задачи: {e}')
        return False
    finally:    
        db.close()  