from contextlib import closing
from db_utils import connect_db
from db_functions import create_task, get_tasks, update_task, delete_task

# Главная функция
def main():
    with closing(connect_db()) as (db, cursor):
        while True:
            print("\nМеню:")
            print("1. Создать задачу")
            print("2. Показать все задачи")
            print("3. Обновить статус задачи")
            print("4. Удалить задачу")
            print("5. Выйти")
            
            choice = input("Выберите действие: ")
            
            if choice == '1':
                title = input("Введите название задачи: ")
                create_task(cursor, title)
            elif choice == '2':
                get_tasks(cursor)
            elif choice == '3':
                task_id = input("Введите ID задачи для обновления: ")
                update_task(cursor, int(task_id) if task_id.isdigit() else None)
            elif choice == '4':
                task_id = input("Введите ID задачи для удаления: ")
                delete_task(cursor, int(task_id) if task_id.isdigit() else None)
            elif choice == '5':
                break
            else:
                print("Неверный выбор.")

if __name__ == '__main__':
    main()
