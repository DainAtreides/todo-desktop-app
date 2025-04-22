from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from gui.factories.widget_factory import WidgetFactory as factory
from database.db import TaskDatabase
from core.models import TaskManager


class ToDoAppGUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.db = TaskDatabase('todo')
        self.db.connect()
        self.task_manager = TaskManager(self.db)
        self.padding = [30, 30, 30, 30]
        # Главное окно
        self.task_box = factory(
            'gridlayout',
            cols=1,
            size_hint=(1, 1),
            spacing=10
        ).widget
        self.add_widget(self.task_box)
        """Контейнер для ввода"""
        input_layout = factory(
            'boxlayout',
            orientation='horizontal',
            size_hint=(1, None),
            height=40
        ).widget
        self.add_widget(input_layout)

        """Поле ввода"""
        self.input = factory(
            'textinput',
            hint_text='Enter new task...',
            size_hint=(0.85, None),
            height=40,
            font_name='Roboto',
            font_size='20',
            multiline=False
        ).widget
        self.input.bind(on_text_validate=self.add_task)
        input_layout.add_widget(self.input)

        """Кнопка Добавить"""
        add_button = factory(
            'button',
            text='Add',
            size_hint=(0.15, None),
            height=40,
            font_name='Roboto',
            font_size='20'
        ).widget
        add_button.bind(on_press=self.add_task)
        input_layout.add_widget(add_button)

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
                size_hint=(1, None),
                height=40,
                pos_hint={'x': 0}
            ).widget

            # Label for task with defined size and text wrapping
            label = factory(
                'label',
                text=f'{title} [{"Done" if status else "Pending"}]',
                size_hint=(1, None),
                height=40,
                font_name='Roboto',
                font_size='20',
                valign='middle'
            ).widget
            label.bind(size=lambda inst, val: setattr(label, 'text_size', val))
            task_layout.add_widget(label)

            # Чекбокс для переключения статуса
            checkbox = factory(
                'checkbox',
                # Состояние чекбокса зависит от статуса задачи
                active=bool(status),
                size_hint=(None, None),
                size=(80, 40),
            ).widget

            # Привязываем изменение состояния чекбокса к методу toggle_status
            checkbox.bind(active=lambda instance, value,
                          tid=task_id: self.toggle_status(tid, value))
            task_layout.add_widget(checkbox)

            # Delete button with defined size
            del_button = factory(
                'button',
                text='Delete',
                size_hint=(None, None),
                size=(80, 40),
                font_name='Roboto'
            ).widget
            del_button.bind(on_press=lambda _,
                            tid=task_id: self.delete_task(tid))
            task_layout.add_widget(del_button)

            self.task_box.add_widget(task_layout)

    def toggle_status(self, task_id, new_status):
        self.task_manager.update(task_id, new_status)
        self.refresh_tasks()

    def delete_task(self, task_id):
        self.task_manager.delete(task_id)
        self.refresh_tasks()


class ToDoApp(App):
    def build(self):
        Window.size = (600, 400)
        Window.minimum_width = 600
        Window.minimum_height = 400
        return ToDoAppGUI()


if __name__ == '__main__':
    ToDoApp().run()
