import unittest
import os
from database.db import TaskDatabase
from core.models import TaskManager


class TestTaskManagerCRUD(unittest.TestCase):

    def setUp(self):
        # Create a temporary database file for testing
        self.db_file = 'test_todo.db'
        self.db = TaskDatabase(self.db_file)
        self.db.connect()
        self.task_manager = TaskManager(self.db)

    def tearDown(self):
        # Close the database connection and remove the test database file
        self.db.close()
        os.remove(self.db_file)

    def test_create_task(self):
        # Test that a task can be created and retrieved
        self.task_manager.create('Test task')
        tasks = self.task_manager.show()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][1], 'Test task')
        self.assertFalse(tasks[0][2])  # Task should not be marked as done

    def test_update_task_status(self):
        # Test that a task's status can be updated
        self.task_manager.create('Test task')
        task_id = self.task_manager.show()[0][0]
        self.task_manager.update(task_id, True)
        task = self.task_manager.show()[0]
        self.assertTrue(task[2])  # Task should be marked as done

    def test_delete_task(self):
        # Test that a task can be deleted
        self.task_manager.create('Task to delete')
        task_id = self.task_manager.show()[0][0]
        self.task_manager.delete(task_id)
        tasks = self.task_manager.show()
        self.assertEqual(len(tasks), 0)  # Task list should be empty


if __name__ == '__main__':
    unittest.main()
