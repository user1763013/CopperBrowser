from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile


class BrowserTab(QWidget):
    """A single browser tab wrapping a QWebEngineView."""

    def __init__(self, profile: QWebEngineProfile, parent=None):
        super().__init__(parent)
        self.view = QWebEngineView(self)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)

        self.url = ""
        self.title = ""
        self.view.titleChanged.connect(self._on_title_changed)

    def _on_title_changed(self, t: str):
        self.title = t

    def load(self, url: str):
        self.url = url
        self.view.setUrl(QUrl(url))