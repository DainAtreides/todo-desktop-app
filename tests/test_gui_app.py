import unittest
from unittest.mock import MagicMock, patch
from gui.kivy_gui import ToDoAppGUI


class TestToDoAppGUI(unittest.TestCase):

    @patch('gui.kivy_gui.TaskDatabase')
    @patch('gui.kivy_gui.TaskManager')
    def test_add_task(self, MockTaskManager, MockTaskDatabase):
        # Create a mock for the task manager
        mock_manager = MagicMock()
        MockTaskManager.return_value = mock_manager

        # Initialize the app and simulate adding a task
        app = ToDoAppGUI()
        app.input.text = 'New task'
        app.add_task(None)

        # Check that the task creation method was called with the correct title
        mock_manager.create.assert_called_with('New task')

    @patch('gui.kivy_gui.TaskDatabase')
    @patch('gui.kivy_gui.TaskManager')
    def test_refresh_tasks(self, MockTaskManager, MockTaskDatabase):
        # Mock task manager to return a predefined list of tasks
        mock_manager = MagicMock()
        mock_manager.show.return_value = [
            (1, 'Task A', False), (2, 'Task B', True)]
        MockTaskManager.return_value = mock_manager

        # Initialize the app and refresh the task list
        app = ToDoAppGUI()
        app.refresh_tasks()

        # Expect two widgets to be added to the task list, one for each task
        self.assertEqual(len(app.task_box.children), 2)


if __name__ == '__main__':
    unittest.main()
