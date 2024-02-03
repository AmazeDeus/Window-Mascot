from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer
from utils import capture_and_process_target_window, updateConfigurationFile
from config_editor import ConfigEditor

class TransparentWindow(QWidget):
    """
    A transparent overlay window that can display an image and be interacted with through mouse events and hotkeys.

    Attributes:
        config (dict): Configuration settings for the window, including size, position, and update interval.
    """
    def __init__(self, app, config):
        """
        Initialize the class with the given app and config.
        
        Parameters:
            app: The QApplication app instance
            config (dict): The configuration settings for the window.
        
        Returns:
            None
        """
        super().__init__()
        self.config = config
        self.app = app
        self.initUI()
        self.postInit(app)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateImage)
        self.timer.start(self.config['update_interval'])

    def initUI(self):
        """
        Initializes the user interface of the transparent window based on the provided configuration.
        """
        self.label = QLabel(self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.label.setStyleSheet('background-color: transparent;')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # Set initial size
        window_settings = self.config['window_settings']
        self.resize(window_settings['size']['width'], window_settings['size']['height'])

        self.show()
        self.label.setGeometry(0, 0, self.width(), self.height())

        # Immediately adjust position according to selected screen
        self.adjustPositionToNewScreen()

    def postInit(self, app):
        """
        Initializes the instance after it has been created. It connects the screenRemoved signal of the app to the handleScreenRemoved method of the instance.
        """
        app.screenRemoved.connect(self.handleScreenRemoved)

    def launchConfigEditor(self):
        """
        Launches the configuration editor window to allow users to modify settings.
        """
        self.editor = ConfigEditor(self, self.app)
        self.editor.show()

    def adjustPositionToNewScreen(self):
        """Adjusts the window's initial position based on the selected screen in the config."""
        # Fetch the identifier of the selected screen from the configuration
        selected_screen_name = self.config.get('selected_screen', self.app.primaryScreen().name())
            
        # Find the target screen based on the selected identifier, default to primary if not found
        target_screen = next((screen for screen in self.app.screens() if screen.name() == selected_screen_name), self.app.primaryScreen())
            
        # Directly use the position from the configuration as relative to the target screen
        window_settings = self.config['window_settings']

        # Calculate new position by adding the screen's top-left corner position
        new_x = target_screen.geometry().x() + window_settings['position']['x']
        new_y = target_screen.geometry().y() + window_settings['position']['y']

        # Apply the calculated position
        self.move(int(new_x), int(new_y))

    def updateConfig(self, new_config):
        """
        Updates the window's configuration and adjusts the window accordingly.

        Args:
            new_config (dict): The new configuration settings to apply.
        """
        self.config = new_config

        # Update the window geometry based on new configuration
        window_settings = self.config['window_settings']
        self.resize(window_settings['size']['width'], window_settings['size']['height'])

        # Recalculate and apply the new position relative to the possibly updated selected screen
        self.adjustPositionToNewScreen()

        # Restart the timer with the new update interval
        self.timer.stop()
        self.timer.start(self.config['update_interval'])

        # Update QLabel geometry to match the new window size
        self.label.setGeometry(0, 0, window_settings['size']['width'], window_settings['size']['height'])

        # Force the window and its contents to update
        self.update()

    def updateImage(self):
        """
        Captures and processes an image according to the current configuration, then updates the window's display.
        """
        image = capture_and_process_target_window(self.config)
        if image is not None:
            height, width, channel = image.shape
            bytesPerLine = 4 * width
            qImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qImg)
            
            # Scale the pixmap to maintain aspect ratio
            self.scalePixmapToLabel(pixmap)

            self.label.setAlignment(Qt.AlignCenter) # Center the label within the window

    def resizeEvent(self, event):
        """
        Handle the resize event for the widget.

        Args:
            event: The resize event object.

        Returns:
            None
        """
        super().resizeEvent(event)  # Call the superclass method
        if self.label.pixmap() is not None:
            self.scalePixmapToLabel(self.label.pixmap())  # Scale current pixmap to new window size

    def scalePixmapToLabel(self, pixmap):
        """
        Scale the given pixmap to fit the dimensions of the QLabel, while maintaining the aspect ratio. 

        Args:
            pixmap: The pixmap to be scaled

        Returns:
            None
        """
        if pixmap:
            # Calculate the aspect ratio of the pixmap
            aspect_ratio = pixmap.width() / pixmap.height()
            new_width = self.width()
            new_height = int(new_width / aspect_ratio)
            if new_height > self.height():
                new_height = self.height()
                new_width = int(new_height * aspect_ratio)
            
            # Scale the pixmap to fill the new dimensions. Might crop parts of the image but will avoid black bars while keeping the aspect ratio.
            scaled_pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            
            # Update the QLabel with the resized pixmap
            self.label.setPixmap(scaled_pixmap)
            self.label.resize(new_width, new_height)  # Adjust QLabel size to fit the scaled pixmap

    def handleScreenRemoved(self, removed_screen):
        """
        Handle the removal of a screen.

        Args:
            removed_screen: The screen that has been removed.

        Returns:
            None
        """
        self.editor = ConfigEditor(self)

        if self.config.get('selected_screen', '') == removed_screen.name():
            QMessageBox.warning(self, "Screen Removed", "The selected screen has been removed. Adjusting position.")
            primary_screen = self.app.primaryScreen()
            self.config['selected_screen'] = primary_screen.name()
            
            # Save the updated configuration
            self.editor.save_config()

    def keyPressEvent(self, event):
        """
        Handles hotkey presses for launching the configuration editor.

        Args:
            event (QKeyEvent): The key press event.
        """
        if event.key() == Qt.Key_Q and (event.modifiers() & Qt.ControlModifier):
            self.launchConfigEditor()
        else:
            super().keyPressEvent(event)

    def mousePressEvent(self, event):
        """
        Initiates window drag on mouse press.

        Args:
            event (QMouseEvent): The mouse press event.
        """
        if event.button() == Qt.LeftButton:
            self.moving = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        """
        Handles window dragging.

        Args:
            event (QMouseEvent): The mouse move event.
        """
        if self.moving:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        """
        Stops window dragging on mouse release and updates the configuration
        with the new window position relative to the selected screen.

        Args:
            event (QMouseEvent): The mouse release event.
        """
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton and self.moving:
            self.moving = False  # Assuming you have a self.moving attribute set in mousePressEvent and mouseMoveEvent

            # Determine the center of the window for identifying the current screen
            window_center = self.geometry().center()
            current_screen = self.app.screenAt(window_center)

            # Find the index or identifier of the current screen
            current_screen_name = current_screen.name()
            self.config['selected_screen'] = current_screen_name  # Update the selected_screen configuration

            # Calculate the new position relative to the current screen's top-left corner
            new_x_relative = self.x() - current_screen.geometry().x()
            new_y_relative = self.y() - current_screen.geometry().y()

            # Update the position in the configuration
            self.config['window_settings']['position']['x'] = new_x_relative
            self.config['window_settings']['position']['y'] = new_y_relative

            # Save the updated configuration
            updateConfigurationFile(self)