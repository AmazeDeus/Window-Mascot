import cv2
import numpy as np
import yaml
from PyQt5.QtWidgets import QMessageBox
from capture_image import capture_image

def capture_target_window(window_title):
    """
    Capture the specified window and return its image.

    Args:
        window_title (str): The title of the window to capture.

    Returns:
        ndarray: The captured image as an OpenCV image (BGR format).
    """
    try:
        image = capture_image(window_title)
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    except Exception as e:
        print(f"Error capturing window: {e}")
        return None

def apply_chroma_key(image, hsv_lower, hsv_upper):
    """
    Apply a chroma key effect to an image.

    This function converts an image to the RGBA color space and applies a mask to the alpha channel
    to make a specific color range transparent. Typically used for green screen effects.

    Args:
        image (ndarray): The original image in BGR format.
        hsv_lower (ndarray): The lower bound of the HSV values to be made transparent.
        hsv_upper (ndarray): The upper bound of the HSV values to be made transparent.

    Returns:
        ndarray: The modified image with the specified color range made transparent.
    """
    # Convert BGR to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create a mask for the target color
    mask = cv2.inRange(hsv_image, hsv_lower, hsv_upper)

    # Invert the mask to get everything but the target color
    mask_inv = cv2.bitwise_not(mask)

    # Convert the image to RGBA and apply the mask to the alpha channel
    image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    image[:, :, 3] = mask_inv

    return image

def capture_and_process_target_window(config):
    """
    Capture and process an image from a specified window.

    This function captures an image from a specified window, then applies a chroma key effect to it
    using predefined HSV bounds for the target color.

    The global variables `window_title`, `hsv_lower_hue`, `hsv_lower_saturation`, `hsv_lower_value`,
    `hsv_upper_hue`, `hsv_upper_saturation`, and `hsv_upper_value` are used for configuration.

    Returns:
        ndarray or None: The processed image if successful, or None if the window cannot be captured.
    """
    window_title = config['window_settings']['title']

    # Capture the window with the $window_title title
    captured_image = capture_target_window(window_title)

    if captured_image is not None:
        # Define the lower and upper bounds of the target color in HSV
        hsv_lower = np.array([config['chroma_key_settings']['hsv_lower']['h'], 
                          config['chroma_key_settings']['hsv_lower']['s'], 
                          config['chroma_key_settings']['hsv_lower']['v']], dtype=np.uint8)
        hsv_upper = np.array([config['chroma_key_settings']['hsv_upper']['h'], 
                          config['chroma_key_settings']['hsv_upper']['s'], 
                          config['chroma_key_settings']['hsv_upper']['v']], dtype=np.uint8)

        # Apply chroma key effect
        return apply_chroma_key(captured_image, hsv_lower, hsv_upper)
    return None

def updateConfigurationFile(self):
        """Directly update the configuration file with the current config."""
        with open('config.yaml', 'w') as file:
            yaml.dump(self.config, file, sort_keys=False)

def is_valid_update_interval(self, interval_str):
    """
    Validates the update interval input to ensure it's an integer within a reasonable range.

    Args:
        interval_str (str): The input string to validate.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    try:
        interval = int(interval_str)
        # Define the acceptable range for your update interval here
        # For example, between 10 ms and 5000 ms (5 seconds)
        if 10 <= interval <= 5000:
            return True
        else:
            QMessageBox.warning(self, "Invalid Input", "Update interval must be between 10 and 5000 milliseconds.")
            return False
    except ValueError:
        QMessageBox.warning(self, "Invalid Input", "Update interval must be a valid integer.")
        return False
    
def is_valid_position(self, x, y, selected_screen_name=None):
    """
    Check if the given position is valid, and adjust it if necessary to fit within the screen's bounds.

    Parameters:
        x (int): The x-coordinate of the position.
        y (int): The y-coordinate of the position.
        selected_screen_name (str, optional): The name of the selected screen. Defaults to None.

    Returns:
        tuple: The adjusted x and y coordinates if they fall outside the selected screen's bounds; otherwise, the original x and y coordinates.
    """
    try:
        x = int(x)
        y = int(y)
    except ValueError:
        QMessageBox.warning(self, "Invalid Input", "Position coordinates must be valid integers.")
        return False
    
    # Fallback to primary screen if not specified
    if selected_screen_name is None: selected_screen_name = self.app.primaryScreen().name()

    # Find the selected screen's geometry
    selected_screen = None
    for screen in self.app.screens():
        if screen.name() == selected_screen_name:
            selected_screen = screen
            break

    if selected_screen:
        screen_geometry = selected_screen.geometry()
        # Ensure x, y falls within the selected screen's bounds; if not, adjust
        adjusted_x = max(screen_geometry.x(), min(x, screen_geometry.x() + screen_geometry.width() - 1))
        adjusted_y = max(screen_geometry.y(), min(y, screen_geometry.y() + screen_geometry.height() - 1))
        return adjusted_x, adjusted_y
    
    return x, y  # Return original coordinates if the screen is not found

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