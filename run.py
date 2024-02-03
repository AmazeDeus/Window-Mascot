from PyQt5.QtCore import QFileSystemWatcher
from PyQt5.QtWidgets import QApplication
import sys
from transparent_window import TransparentWindow
from config_loader import load_config

def main():
    app = QApplication(sys.argv)
    config = load_config('config.yaml')
    transp_window = TransparentWindow(app, config)

    def config_changed(path):
        print(f"Configuration changed: {path}")
        new_config = load_config('config.yaml')
        transp_window.updateConfig(new_config)
    
    # Setup filesystem watcher
    config_watcher = QFileSystemWatcher(['config.yaml'])
    config_watcher.fileChanged.connect(config_changed)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()