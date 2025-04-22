from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from gui.factories.widget_factory import WidgetFactory as factory
from database.db import TaskDatabase
from core.models import TaskManager


class ToDoAppGUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.db = TaskDatabase('todo')
        self.db.connect()
        self.task_manager = TaskManager(self.db)

        # Box layout to hold task items
        self.task_box = factory(
            'boxlayout',
            orientation='vertical',
            size_hint=(1, 1)
        ).widget
        self.add_widget(self.task_box)

        # Text input field with defined height and width
        self.input = factory(
            'textinput',
            hint_text='Enter new task title',
            size_hint=(1, None),
            height=40
        ).widget
        self.add_widget(self.input)

        # Add Task button with defined height
        add_button = factory(
            'button',
            text='Add Task',
            size_hint=(1, None),
            height=40
        ).widget
        add_button.bind(on_press=self.add_task)
        self.add_widget(add_button)

        self.refresh_tasks()

    def add_task(self, instance):
        title = self.input.text.strip()
        if title:
            self.task_manager.create(title)
            self.input.text = ''
            self.refresh_tasks()

    def refresh_tasks(self):
        self.task_box.clear_widgets()
        tasks = self.task_manager.show()
        for task in tasks:
            task_id, title, status = task

            # Box layout for each task with defined height
            task_layout = factory(
                'boxlayout',
                orientation='horizontal',
                size_hint_y=None,
                height=40,
                padding=5,
                spacing=5
            ).widget

            # Label for task with defined size and text wrapping
            label = factory(
                'label',
                text=f'{title} [{"Done" if status else "Pending"}]',
                size_hint=(1, None),
                height=40,
                valign='middle'
            ).widget
            label.bind(size=lambda inst, val: setattr(label, 'text_size', val))
            task_layout.add_widget(label)

            # Toggle button with defined size
            toggle_btn = factory(
                'button',
                text='Toggle',
                size_hint=(None, None),
                size=(80, 40)
            ).widget
            toggle_btn.bind(on_press=lambda _,
                            tid=task_id: self.toggle_status(tid))
            task_layout.add_widget(toggle_btn)

            # Delete button with defined size
            del_btn = factory(
                'button',
                text='Delete',
                size_hint=(None, None),
                size=(80, 40)
            ).widget
            del_btn.bind(on_press=lambda _, tid=task_id: self.delete_task(tid))
            task_layout.add_widget(del_btn)

            self.task_box.add_widget(task_layout)

    def toggle_status(self, task_id):
        self.task_manager.update(task_id)
        self.refresh_tasks()

    def delete_task(self, task_id):
        self.task_manager.delete(task_id)
        self.refresh_tasks()


class ToDoApp(App):
    def build(self):
        return ToDoAppGUI()


if __name__ == '__main__':
    ToDoApp().run()
