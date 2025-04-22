import logging
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


# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Dictionary to map widget names to widget classes
WIDGETS = {
    'button': Button,
    'label': Label,
    'textinput': TextInput,
    'checkbox': CheckBox,
    'slider': Slider,
    'switch': Switch,
    'spinner': Spinner,
    'gridlayout': GridLayout,
    'boxlayout': BoxLayout,
    'stacklayout': StackLayout,
    'image': Image,
    'popup': Popup
}


class WidgetFactory:
    def __init__(self, widget_type: str, **kwargs):
        '''Initializes a widget based on the given type and parameters.'''
        self.widget_type = widget_type
        self.params = kwargs

        # Log widget creation attempt
        logger.info(
            f'Attempting to create widget of type: {self.widget_type} with parameters: {self.params}')

        # Get the corresponding widget class from the WIDGETS dictionary
        widget_class = WIDGETS.get(self.widget_type)

        # If the widget type is invalid, log an error and raise a ValueError
        if not widget_class:
            logger.error(f'Unknown widget type: {self.widget_type}')
            raise ValueError(f'Unknown widget type: {self.widget_type}')

        # Create the widget with the specified parameters
        self.widget = widget_class(**self.params)

        # Log successful widget creation
        logger.info(f'Successfully created widget: {self.widget_type}')
