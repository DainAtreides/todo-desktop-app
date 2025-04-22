from database.db import TaskDatabase
from core.models import TaskManager

db = TaskDatabase('todo')
task = TaskManager(db)
db.connect()
<<<<<<< HEAD

=======
>>>>>>> f30da920894dae1b401b0e965012c48ddc3f3487

def main():
    """Главная функция"""
    while True:
        print('\nMain menu:',
              '1. Create task',
              '2. Show all tasks',
              '3. Change task status',
              '4. Delete task',
              '5. Exit', sep='\n')

        choice = input('Select action: ')
        match choice:
            case '1':
                """Создаёт задачу"""
                title = input('Enter task title: ').strip()
                if not title:
                    print('Title cannot be empty. Please try again.')
                    continue
                task.create(title)
                print(f'Task "{title}" created.')
            case '2':
                """Показывает все задачи"""
                tasks = task.show()
                if tasks:
                    print('All tasks:')
                    for t in tasks:
                        print(
                            f"{t[0]}. {t[1]} - Status: {('Done' if t[-1] else 'Pending')}")
                else:
                    print('No tasks found.')
            case '3':
                """Изменяет статус задачи"""
                try:
                    task_id = int(input('Enter task ID to change status: '))
                    if task_id <= 0:
                        print('Invalid task ID. It must be a positive integer.')
                        continue
                    task.update(task_id)
                    print(f'Task {task_id} status updated.')
                except ValueError:
                    print('Invalid input. Please enter a valid task ID.')
            case '4':
                """Удаляет задачу"""
                try:
                    task_id = int(input('Enter task ID to delete: '))
                    if task_id <= 0:
                        print('Invalid task ID. It must be a positive integer.')
                        continue
                    task.delete(task_id)
                    print(f'Task {task_id} deleted.')
                except ValueError:
                    print('Invalid input. Please enter a valid task ID.')
            case '5':
                """Завершает программу"""
                db.close()
                print('Program ended.')
                break
            case _:
                print('Wrong action choice.')
                continue


if __name__ == '__main__':
    main()
