import sys
from PyQt6.QtWidgets import QApplication

from copper_browser.config import Config
from copper_browser.browser_window import MainWindow


def main():
    """
    Entry point for CopperBrowser.
    Creates the QApplication, loads config, and launches the main window.
    """
    app = QApplication(sys.argv)

    # Load configuration (homepage, user agent, search engine, etc.)
    config = Config()

    # Create and show the main browser window
    window = MainWindow(config)
    window.show()

    # Run the Qt event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()