from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer
from utils import capture_and_process_target_window

class TransparentWindow(QWidget):
    def __init__(self, config):
		"""
        Initialize the TransparentWindow class.

        This class creates a transparent, frameless window that stays on top of other windows.
        It periodically updates its display with an image captured and processed from another window.
        """
        super().__init__()

        # Store the configuration
        self.config = config

        self.initUI()
        self.timer = QTimer(self)
		# Connect the timer to the updateImage method to refresh the window
        self.timer.timeout.connect(self.updateImage)
		# Set the timer interval for updating the window's image
        self.timer.start(self.config['update_interval']) # Update every $update_interval ms

    def initUI(self):
		"""
        Initialize the user interface of the transparent window.

        This method sets up the window's appearance and geometry.
        """
        self.label = QLabel(self) # QLabel to display the captured image
        self.setAttribute(Qt.WA_TranslucentBackground) # Set the background as translucent
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint) # Frameless and always on top

        window_settings = self.config['window_settings']
		# Set geometry of the window with the given position and size
        self.setGeometry(window_settings['position']['x'], 
                         window_settings['position']['y'], 
                         window_settings['size']['width'], 
                         window_settings['size']['height'])
        self.show() # Show the window
        self.label.setGeometry(0, 0, self.width(), self.height()) # Set the geometry of the label

    def updateImage(self):
        """
        Update the image displayed in the window.

        This method captures and processes an image from the target window and updates the QLabel with it.
        """
        image = capture_and_process_target_window(self.config)  # Capture and process the image

        if image is not None:
            # If an image is captured, convert it to QPixmap and display it in the label
            height, width, channel = image.shape
            bytesPerLine = 4 * width  # Calculate the number of bytes per line
            qImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qImg)
            self.label.setPixmap(pixmap)
            self.resize(pixmap.size())  # Resize the window to fit the image

    def mousePressEvent(self, event):
        """
        Handle mouse press events.

        Enables dragging of the window when pressing the left mouse button.
        """
        if event.button() == Qt.LeftButton:
            self.moving = True  # Flag to indicate the window is being moved
            self.offset = event.pos()  # Store the position where the mouse was pressed

    def mouseMoveEvent(self, event):
        """
        Handle mouse move events.

        Allows the window to be dragged around.
        """
        if self.moving:
            # Move the window's position based on mouse movement
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        """
        Handle mouse release events.

        Stops dragging the window when the left mouse button is released.
        """
        if event.button() == Qt.LeftButton:
            self.moving = False  # Stop moving the window