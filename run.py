from PyQt5.QtWidgets import QApplication
import sys
from transparent_window import TransparentWindow
from config_loader import load_config

if __name__ == '__main__':
    config = load_config('config.yaml')
    app = QApplication(sys.argv)
    transp_window = TransparentWindow(config)
    sys.exit(app.exec_())