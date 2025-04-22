from kivy.app import App
from kivy.core.window import Window
from gui.kivy_gui import ToDoAppGUI


class ToDoApp(App):
    def build(self):
        # Set window size and minimum size
        Window.size = (500, 400)
        Window.minimum_width = 500
        Window.minimum_height = 400

        # Return the main GUI layout
        return ToDoAppGUI()


# Start the application when the script is run
if __name__ == '__main__':
    ToDoApp().run()
