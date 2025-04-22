from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup


WIDGETS = {
    "button": Button,
    "label": Label,
    "textinput": TextInput,
    "checkbox": CheckBox,
    "slider": Slider,
    "switch": Switch,
    "spinner": Spinner,
    "gridlayout": GridLayout,
    "boxlayout": BoxLayout,
    "stacklayout": StackLayout,
    "image": Image,
    "popup": Popup
}


class WidgetFactory:
    def __init__(self, widget_type: str, **kwargs):
        self.widget_type = widget_type
        self.params = kwargs
        widget_class = WIDGETS.get(self.widget_type)
        if not widget_class:
            raise ValueError(f'Unknown widget type: {self.widget_type}')
        self.widget = widget_class(**self.params)
