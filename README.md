
# Window Mascot

## Description
This project creates a transparent, always on top, frameless window overlay that can continously capture and display content from a specified, target window. It's particularly useful for applications like VTube Studio, where users might want to overlay certain window contents onto another screen, while keeping certain parts transparent by configuring the chroma_key_settings inside config.yaml (such as a bright green background). The application uses PyQt5 for the windowing system, OpenCV for image processing, and the Win32 API for window capture.

Note:
- This code relies heavily on the Win32 API for window capture functionality, which is specific to Windows operating systems. As a result, this code will not be directly usable on other operating systems like macOS or Linux in its current form.
- This code works for target windows that might also be covered by other windows, but due to how the WIN32 API is currently capturing the window, it will still throw an error if the target window is minimized.

## Example
- Raw Target Window:
  
![Raw Target Window](https://i.gyazo.com/50e5a75873a066b5bc06c8d369d06f65.png)

- Captured result:
  
![Captured Window Result](https://i.gyazo.com/2a40f07bf2739399043640ffecd5e777.png)

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
   git clone https://github.com/AmazeDeus/Window-Mascot.git
   ```
2. Navigate to the project directory:
   ```
   cd Window-Mascot
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
