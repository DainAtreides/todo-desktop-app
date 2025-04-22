import sys
import logging
from database.db import TaskDatabase
from core.models import TaskManager

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


# Main function to run the command line interface
def main():
    # Initialize the database and task manager
    db = TaskDatabase('todo')

    # Attempt to connect to the database
    try:
        db.connect()
        logger.info('Successfully connected to the database.')
    except Exception as e:
        # If connection fails, log an error and exit the program
        logger.error(f'Error connecting to the database: {e}')
        exit()

    task = TaskManager(db)

    while True:
        # Display the main menu options
        print('\nMain menu:',
              '1. Create task',
              '2. Show all tasks',
              '3. Change task status',
              '4. Delete task',
              '5. Exit', sep='\n')

        # Get user input for action
        choice = input('Select action: ')

        # Process the selected action
        match choice:
            case '1':
                # Create a new task
                # Get the title for the new task
                title = input('Enter task title: ').strip()

                # Validate that the title is not empty
                if not title:
                    print('Title cannot be empty. Please try again.')
                    continue

                # Create the task and confirm
                task.create(title)
                logger.info(f'Task "{title}" created.')
                print(f'Task "{title}" created.')

            case '2':
                # Show all tasks
                # Retrieve all tasks
                tasks = task.show()

                # Check if tasks exist
                if tasks:
                    print('All tasks:')
                    # Print each task with its ID, title, and status
                    for t in tasks:
                        print(
                            f'{t[0]}. {t[1]} - Status: {("Done" if t[-1] else "Pending")}')
                else:
                    logger.info('No tasks found.')
                    print('No tasks found.')

            case '3':
                # Change task status
                try:
                    # Get task ID to update its status
                    task_id = int(input('Enter task ID to change status: '))

                    # Validate the task ID
                    if task_id <= 0:
                        print('Invalid task ID. It must be a positive integer.')
                        continue

                    # Request the new status for the task
                    status = input(
                        'Enter status (Done/Pending): ').strip().lower()

                    # Validate the status input
                    if status not in ['done', 'pending']:
                        print('Invalid status. Please enter "Done" or "Pending".')
                        continue

                    # Convert the status string to a boolean value
                    new_status = True if status == 'done' else False

                    # Update the task status and confirm
                    task.update(task_id, new_status)
                    logger.info(
                        f'Task {task_id} status updated to {status.capitalize()}.')
                    print(
                        f'Task {task_id} status updated to {status.capitalize()}.')
                except ValueError:
                    # Handle invalid input for task ID
                    logger.warning('Invalid input for task ID.')
                    print('Invalid input. Please enter a valid task ID.')

            case '4':
                # Delete a task
                try:
                    # Get task ID to delete
                    task_id = int(input('Enter task ID to delete: '))

                    # Validate the task ID
                    if task_id <= 0:
                        print('Invalid task ID. It must be a positive integer.')
                        continue

                    # Delete the task and confirm
                    task.delete(task_id)
                    logger.info(f'Task {task_id} deleted.')
                    print(f'Task {task_id} deleted.')
                except ValueError:
                    # Handle invalid input for task ID
                    logger.warning('Invalid input for task ID.')
                    print('Invalid input. Please enter a valid task ID.')

            case '5':
                # Close the database connection and end the program
                db.close()
                logger.info('Program ended.')
                print('Program ended.')
                sys.exit()
                break

            case _:
                # Handle invalid menu choices
                logger.warning('Invalid action choice.')
                print('Wrong action choice. Please select a valid option.')
                continue


# Entry point of the program
if __name__ == '__main__':
    main()
