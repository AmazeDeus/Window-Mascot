from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QHBoxLayout, QComboBox
from utils import is_valid_update_interval, is_valid_position
import yaml

class HSVInputWidget(QWidget):
    """
    A custom widget for inputting HSV values.

    Attributes:
        hInput (QLineEdit): Input field for the Hue value.
        sInput (QLineEdit): Input field for the Saturation value.
        vInput (QLineEdit): Input field for the Value (brightness) value.
    """
    def __init__(self, label, initial_h, initial_s, initial_v):
        """
        Initializes the HSV input widget with specified initial values.

        Args:
            label (str): The label for the HSV input group.
            initial_h (int): Initial Hue value.
            initial_s (int): Initial Saturation value.
            initial_v (int): Initial Value (brightness) value.
        """
        super().__init__()
        layout = QHBoxLayout()
        
        layout.addWidget(QLabel(f'{label} H:'))
        self.hInput = QLineEdit(str(initial_h))
        layout.addWidget(self.hInput)
        
        layout.addWidget(QLabel('S:'))
        self.sInput = QLineEdit(str(initial_s))
        layout.addWidget(self.sInput)
        
        layout.addWidget(QLabel('V:'))
        self.vInput = QLineEdit(str(initial_v))
        layout.addWidget(self.vInput)
        
        self.setLayout(layout)

class ConfigEditor(QWidget):
    """
    A GUI editor for the application's configuration file.

    This editor allows users to modify settings such as window size,
    position, and chroma key settings without directly editing the YAML file.
    """
    def __init__(self, transparent_window=None, app=None):
        """
        Initializes the configuration editor window.

        Args:
            transparent_window (TransparentWindow, optional): Reference to the main application window.
            app (QApplication): Reference to the main application.
        """
        super().__init__()
        self.transparent_window = transparent_window
        self.app = app
        self.initUI()

    def initUI(self):
        """
        Initialize the user interface by setting up layout, screen selector, config loading, input fields for window settings, screen selection, window size and position, update interval settings, chroma key settings, and save button.
        """        
        self.layout = QVBoxLayout()
        self.screenSelector = QComboBox()
        self.config = self.load_config('config.yaml')

        # Create input fields for window settings
        self.titleInput = QLineEdit(self.config['window_settings']['title'])

        # Create input fields for window size and position
        self.widthInput = QLineEdit(str(self.config['window_settings']['size']['width']))
        self.heightInput = QLineEdit(str(self.config['window_settings']['size']['height']))
        self.xPositionInput = QLineEdit(str(self.config['window_settings']['position']['x']))
        self.yPositionInput = QLineEdit(str(self.config['window_settings']['position']['y']))

        # Add screen selector
        for i, screen in enumerate(self.app.screens()):
            self.screenSelector.addItem(f"Screen {i+1}", screen.name())
        
        # Try to select the previously chosen screen, if any
        selected_screen_name = self.config.get('selected_screen', self.app.primaryScreen().name())
        index = self.screenSelector.findData(selected_screen_name)
        if index >= 0:
            self.screenSelector.setCurrentIndex(index)

        # Add widgets to layout
        self.layout.addWidget(QLabel('Window Title'))
        self.layout.addWidget(self.titleInput)
        self.layout.addWidget(QLabel("Select Screen:"))
        self.layout.addWidget(self.screenSelector)
        self.layout.addWidget(QLabel('Window Width'))
        self.layout.addWidget(self.widthInput)
        self.layout.addWidget(QLabel('Window Height'))
        self.layout.addWidget(self.heightInput)
        self.layout.addWidget(QLabel('Window Position (x)'))
        self.layout.addWidget(self.xPositionInput)
        self.layout.addWidget(QLabel('Window Position (y)'))
        self.layout.addWidget(self.yPositionInput)

        # Update Interval Settings
        self.layout.addWidget(QLabel('Update Interval (ms)'))
        self.updateIntervalInput = QLineEdit(str(self.config['update_interval']))
        self.layout.addWidget(self.updateIntervalInput)

        # Chroma Key Settings section
        self.layout.addWidget(QLabel('Chroma Key Settings'))

        # HSV Lower
        hsv_lower = self.config['chroma_key_settings']['hsv_lower']
        self.hsvLowerWidget = HSVInputWidget('HSV Lower', hsv_lower['h'], hsv_lower['s'], hsv_lower['v'])
        self.layout.addWidget(self.hsvLowerWidget)

        # HSV Upper
        hsv_upper = self.config['chroma_key_settings']['hsv_upper']
        self.hsvUpperWidget = HSVInputWidget('HSV Upper', hsv_upper['h'], hsv_upper['s'], hsv_upper['v'])
        self.layout.addWidget(self.hsvUpperWidget)

        # Save button
        self.saveBtn = QPushButton('Save Configuration')
        self.saveBtn.clicked.connect(self.save_config)
        self.layout.addWidget(self.saveBtn)

        self.setLayout(self.layout)

    def load_config(self, filepath):
        """
        Loads the configuration from a YAML file.

        Args:
            filepath (str): Path to the YAML configuration file.

        Returns:
            dict: The loaded configuration dictionary.
        """
        with open(filepath, 'r') as file:
            return yaml.safe_load(file)

    def save_config(self):
        """
        Saves the modified configuration back to the YAML file and closes the editor.

        Updates the application's configuration if the main window is referenced.
        """
        # Save window settings
        self.config['window_settings']['title'] = self.titleInput.text()
        self.config['window_settings']['size']['width'] = int(self.widthInput.text())
        self.config['window_settings']['size']['height'] = int(self.heightInput.text())

        # Save chroma key settings
        self.config['chroma_key_settings']['hsv_lower'] = {
            'h': int(self.hsvLowerWidget.hInput.text()),
            's': int(self.hsvLowerWidget.sInput.text()),
            'v': int(self.hsvLowerWidget.vInput.text())
        }
        self.config['chroma_key_settings']['hsv_upper'] = {
            'h': int(self.hsvUpperWidget.hInput.text()),
            's': int(self.hsvUpperWidget.sInput.text()),
            'v': int(self.hsvUpperWidget.vInput.text())
        }

        # Preliminary update to selected screen to ensure it's considered in position validation
        selected_screen_name = self.screenSelector.currentData()
        self.config['selected_screen'] = selected_screen_name

        # Proceed with fetching and validating the window position
        x_position = self.xPositionInput.text()
        y_position = self.yPositionInput.text()

        if not is_valid_position(self, x_position, y_position, selected_screen_name):
            return  # Stop if validation fails

        # Validate the update interval input before saving
        if not is_valid_update_interval(self, self.updateIntervalInput.text()):
            return  # Do not save if the input is invalid

        # Proceed with saving if the input is valid
        self.config['window_settings']['position']['x'] = int(x_position)
        self.config['window_settings']['position']['y'] = int(y_position)
        self.config['update_interval'] = int(self.updateIntervalInput.text())

        # Write the updated configuration back to the YAML file
        with open('config.yaml', 'w') as file:
            yaml.dump(self.config, file, sort_keys=False)

        self.close() # Close the editor window
        if self.transparent_window:
            self.transparent_window.updateConfig(self.config) # Update the main window with the new config