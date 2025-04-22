import console_app
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to the system path for imports
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class TestConsoleApp(unittest.TestCase):

    @patch('console_app.TaskManager')
    @patch('console_app.input')
    @patch('console_app.print')
    def test_create_task(self, mock_print, mock_input, MockTaskManager):
        print('Starting test_create_task...')

        # Simulate user input: '1' to create task, 'Test Task' as task title, '5' to exit
        mock_input.side_effect = ['1', 'Test Task', '5']
        mock_task = MagicMock()
        MockTaskManager.return_value = mock_task

        # Patch sys.exit to prevent actual exit
        with patch('sys.exit') as mock_exit:
            print('Calling console_app.main()...')
            console_app.main()

            print('Checking if create was called...')
            mock_task.create.assert_called_with('Test Task')
            mock_print.assert_any_call('Task "Test Task" created.')
            mock_exit.assert_called_once()

    @patch('console_app.TaskManager')
    @patch('console_app.input')
    @patch('console_app.print')
    def test_invalid_choice(self, mock_print, mock_input, MockTaskManager):
        # Simulate invalid user input followed by exit command
        mock_input.side_effect = ['invalid', '5']
        mock_task = MagicMock()
        MockTaskManager.return_value = mock_task

        with patch('sys.exit') as mock_exit:
            console_app.main()

            mock_print.assert_any_call(
                'Wrong action choice. Please select a valid option.')
            mock_exit.assert_called_once()


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
