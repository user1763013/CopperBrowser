from PyQt6.QtWidgets import QToolBar, QLineEdit
from PyQt6.QtGui import QAction


class BrowserToolbar:
    """
    Encapsulates the navigation toolbar and its actions.
    The MainWindow can access actions and the address bar via this class.
    """

    def __init__(self, parent=None):
        self.toolbar = QToolBar("Navigation", parent)

        # Actions
        self.act_back = QAction("←", parent)
        self.act_forward = QAction("→", parent)
        self.act_reload = QAction("⟳", parent)
        self.act_home = QAction("🏠", parent)
        self.act_new_tab = QAction("New Tab", parent)
        self.act_close_tab = QAction("Close Tab", parent)
        self.act_bookmarks = QAction("Bookmarks", parent)
        self.act_history = QAction("History", parent)

        # Toggles
        self.act_toggle_ua = QAction("UA: Copper", parent)       # User Agent toggle
        self.act_search_engine = QAction("SE: DuckDuckGo", parent)  # Search Engine toggle

        # Address bar
        self.address = QLineEdit(parent)
        self.address.setPlaceholderText("Enter URL or search…")

        # Assemble toolbar
        self.toolbar.addAction(self.act_back)
        self.toolbar.addAction(self.act_forward)
        self.toolbar.addAction(self.act_reload)
        self.toolbar.addAction(self.act_home)
        self.toolbar.addWidget(self.address)
        self.toolbar.addAction(self.act_new_tab)
        self.toolbar.addAction(self.act_close_tab)
        self.toolbar.addAction(self.act_bookmarks)
        self.toolbar.addAction(self.act_history)
        self.toolbar.addAction(self.act_toggle_ua)
        self.toolbar.addAction(self.act_search_engine)

    def get_toolbar(self) -> QToolBar:
        """Return the actual QToolBar widget."""
        return self.toolbar

    def get_actions(self):
        """Return all actions and the address bar for MainWindow wiring."""
        return {
            "back": self.act_back,
            "forward": self.act_forward,
            "reload": self.act_reload,
            "home": self.act_home,
            "new_tab": self.act_new_tab,
            "close_tab": self.act_close_tab,
            "bookmarks": self.act_bookmarks,
            "history": self.act_history,
            "toggle_ua": self.act_toggle_ua,
            "search_engine": self.act_search_engine,
            "address": self.address,
        }