from database import TaskDatabase
from models import TaskManager 

db = TaskDatabase('todo')
task = TaskManager

def main():
    """Главная функция"""
    while True:
        print('\nMain menu:', 
              '1. Create task', 
              '2. Show all tasks', 
              "3. Change task status", 
              '4. Delete task',
              '5. Exit', sep='\n')
        
        choice = input('Select action: ')
        match choice:
            case '1':
                """Создаёт задачу"""
                title = input('Enter task title: ')
                task = Task(title)
                task.create_task(db)
            case '2':
                """Показывает все задачи"""
                tasks = db.read_tasks()
                print(tasks)
            case '3':
                """Изменяет статус задачи"""
                pass
            case '4':
                """Удаляет задачу"""
                pass
            case '5':
                """Завершает программу"""
                db.close()
                break
            case _:
                print('Wrong action choice.')
                continue

if __name__ == '__main__':
    main()
