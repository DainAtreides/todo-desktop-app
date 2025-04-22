from kivy.uix.boxlayout import BoxLayout
from gui.factories.widget_factory import WidgetFactory as factory
from database.db import TaskDatabase
from core.models import TaskManager


class ToDoAppGUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # Initialize database connection
        self.db = TaskDatabase('todo')
        self.db.connect()

        # Initialize task manager with database
        self.task_manager = TaskManager(self.db)

        # Set padding for the main layout
        self.padding = [30, 30, 30, 30]  # top, right, bottom, left

        # Create a grid layout for tasks
        self.task_box = factory(
            'gridlayout',
            cols=1,
            size_hint=(1, 1),
            spacing=10
        ).widget
        self.add_widget(self.task_box)

        # Create input layout (horizontal box layout)
        input_layout = factory(
            'boxlayout',
            orientation='horizontal',
            size_hint=(1, None),
            height=40
        ).widget
        self.add_widget(input_layout)

        # Input field for new task
        self.input = factory(
            'textinput',
            hint_text='Type a new task here',
            size_hint=(0.8, None),
            height=40,
            font_name='Arial',
            font_size='20',
            multiline=False
        ).widget

        # Bind event to add task when the user presses Enter
        self.input.bind(on_text_validate=self.add_task)
        input_layout.add_widget(self.input)

        # Create Add button
        add_button = factory(
            'button',
            text='Add Task',
            size_hint=(0.2, None),
            height=40,
            font_name='Arial',
            font_size='20',
            background_normal='',
            background_color=(1, 0.5, 0, 1),
            color=(0, 0, 0, 1),
            bold=True
        ).widget
        # Bind event to add task when the button is pressed
        add_button.bind(on_press=self.add_task)
        input_layout.add_widget(add_button)

        # Refresh the list of tasks
        self.refresh_tasks()

    # Method to add a new task
    def add_task(self, instance):
        title = self.input.text.strip()

        # Only add task if title is not empty
        if title:
            self.task_manager.create(title)
            self.input.focus = True  # Set focus back to input
            self.input.text = ''  # Clear the input field
            self.refresh_tasks()  # Refresh task list

    # Method to refresh the task list display
    def refresh_tasks(self):
        self.task_box.clear_widgets()  # Clear existing widgets
        tasks = self.task_manager.show()  # Retrieve all tasks

        # Sort tasks by status (Pending first, Done last)
        tasks.sort(key=lambda task: task[2])

        # For each task, create a layout with task details
        for task in tasks:
            task_id, title, status = task

            # Create BoxLayout for the task with horizontal orientation
            task_layout = factory(
                'boxlayout',
                orientation='horizontal',
                size_hint=(1, None),
                height=40,
                pos_hint={'x': 0}
            ).widget

            # Create label for the task with its status (Done or Pending)
            label = factory(
                'label',
                text=f'{title}',
                size_hint=(1, None),
                height=40,
                font_name='Arial',
                font_size='28',
                valign='top',
                halign='center',
                strikethrough=status,  # Apply strikethrough if task is done
                color=(1, 0.5, 0, 1),  # Orange text color (RGBA)
                bold=True
            ).widget
            # Bind event to adjust text size dynamically
            label.bind(size=lambda inst, val: setattr(label, 'text_size', val))
            task_layout.add_widget(label)

            # Create checkbox to toggle task status
            checkbox = factory(
                'checkbox',
                active=bool(status),
                size_hint=(None, None),
                size=(80, 40),
                color=(1, 0.5, 0, 1)
            ).widget
            checkbox.bind(active=lambda instance, value, tid=task_id: self.toggle_status(
                tid, value))  # Bind event to toggle status
            task_layout.add_widget(checkbox)

            # Create Delete button to remove the task
            del_button = factory(
                'button',
                text='Delete',
                size_hint=(None, None),
                size=(80, 40),
                font_name='Arial',
                font_size='20',
                background_normal='',
                background_color=(1, 0.5, 0, 1),
                color=(0, 0, 0, 1),
                bold=True
            ).widget
            # Bind event to delete task
            del_button.bind(on_press=lambda _,
                            tid=task_id: self.delete_task(tid))
            task_layout.add_widget(del_button)

            # Add task layout to the main task box layout
            self.task_box.add_widget(task_layout)

    # Method to toggle task status between Done and Pending
    def toggle_status(self, task_id, new_status):
        # Update task status in the database
        self.task_manager.update(task_id, new_status)
        self.refresh_tasks()  # Refresh the task list

    # Method to delete a task
    def delete_task(self, task_id):
        self.task_manager.delete(task_id)  # Delete task from the database
        self.refresh_tasks()  # Refresh the task list
