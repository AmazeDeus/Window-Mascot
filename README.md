
# Transparent Window Overlay

## Description
This project creates a transparent, frameless window overlay that can continously capture and display content from a specified window. It's particularly useful for applications like VTube Studio, where users might want to overlay certain window contents onto another screen, while keeping certain parts transparent by configuring the chroma_key_settings inside config.yaml (such as a bright green background). The application uses PyQt5 for the windowing system, OpenCV for image processing, and the Win32 API for window capture.

Note: This also works for windows that might be covered by other windows, but due to how the WIN32 API is currently capturing the window, it will still throw an error if the target window is minimized.

## Installation

### Prerequisites
- Python 3.10.9 (Recommended)
- Virtual Environment (Recommended)
- numpy
- PyQt5
- OpenCV (cv2)
- PyWin32
- PIL

### Steps
1. Clone the repository:
   ```
   git clone https://github.com/AmazeDeus/transparent-window-overlay.git
   ```
2. Navigate to the project directory:
   ```
   cd transparent-window-overlay
   ```
3. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   .\venv\Scripts\activate # On Windows
   source venv/bin/activate # On Unix or MacOS
   ```
4. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Update the `config.yaml` file with the desired settings (window title, size, position, etc.).
2. Run the application:
   ```
   python run.py
   ```

## Configuration
Edit `config.yaml` to change the window settings and chroma key values. The available configurations are:
- `window_settings`: Configure the title, size, and position of the window to capture.
- `update_interval`: Set the refresh rate of the window capture.
- `chroma_key_settings`: Adjust the HSV values for the chroma key effect.

## Contributing
Contributions to this project are welcome! Feel free to fork the repository and submit pull requests.

## License
[MIT](https://choosealicense.com/licenses/mit/)