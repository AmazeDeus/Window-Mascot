### WORKS BEST WITH TEST5!!!

import win32gui
import win32ui
from ctypes import windll
from PIL import Image

def capture_image(window_name):
    """
    Captures the image of a specified window.

    This function captures the current view of a window given its name. It works by 
    obtaining the window handle, creating a device context, and copying the window's 
    content into a bitmap, which is then converted into a PIL Image.

    Note: 
    - Uncomment the SetProcessDPIAware line if using a high DPI display or scaling > 100%.
    - Use GetClientRect instead of GetWindowRect to capture just the client area.

    Args:
        window_name (str): The title of the window to capture.

    Returns:
        Image: A PIL Image object of the captured window.

    Raises:
        ValueError: If the window cannot be captured.
    """
    hwnd = win32gui.FindWindow(None, window_name)

    # Uncomment the following line if you use a high DPI display or >100% scaling size
    # windll.user32.SetProcessDPIAware()

    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer('RGBA', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'RGBA', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        # Success
        return im
    
    raise ValueError("Failure to capture window image.")