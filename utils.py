import cv2
import numpy as np
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