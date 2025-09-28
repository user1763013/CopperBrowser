from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QMessageBox, QInputDialog
)
from PyQt6.QtWebEngineCore import QWebEngineProfile

from .config import (
    Config, DEFAULT_USER_AGENT, CHROME_USER_AGENT, SEARCH_ENGINES
)
from .storage import app_root
from .bookmarks import save_bookmarks, load_bookmarks
from .history import save_history, load_history
from .browser_tab import BrowserTab
from .browser_toolbar import BrowserToolbar
from .browser_dialogs import BookmarksDialog, HistoryDialog


class MainWindow(QMainWindow):
    """Main application window with tabs, toolbar, UA toggle, SE switcher, bookmarks, and history."""

    def __init__(self, config: Config):
        super().__init__()
        self.setWindowTitle("CopperBrowser V1 (PyQt6)")
        self.resize(1100, 700)

        app_root()
        self.config = config
        self.history = load_history()
        self.bookmarks = load_bookmarks()

        # Web profile and UA
        self.current_ua = self.config.user_agent
        self.web_profile = QWebEngineProfile.defaultProfile()
        self.web_profile.setHttpUserAgent(self.current_ua)

        # Tabs
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # Toolbar
        self.toolbar = BrowserToolbar(self)
        self.addToolBar(self.toolbar.get_toolbar())
        actions = self.toolbar.get_actions()

        # Connect actions
        actions["back"].triggered.connect(self.on_back)
        actions["forward"].triggered.connect(self.on_forward)
        actions["reload"].triggered.connect(self.on_reload)
        actions["home"].triggered.connect(self.on_home)
        actions["new_tab"].triggered.connect(lambda: self.new_tab(self.config.homepage))
        actions["close_tab"].triggered.connect(self.close_tab_current)
        actions["bookmarks"].triggered.connect(self.on_bookmarks)
        actions["history"].triggered.connect(self.on_history)
        actions["toggle_ua"].triggered.connect(self.toggle_user_agent)
        actions["search_engine"].triggered.connect(self.toggle_search_engine)
        actions["address"].returnPressed.connect(self.on_go)

        self.address = actions["address"]
        self.act_toggle_ua = actions["toggle_ua"]
        self.act_search_engine = actions["search_engine"]

        # Initial tab
        self.new_tab(self.config.homepage)

    # --- Tab management ---
    def current_tab(self) -> BrowserTab:
        return self.tabs.currentWidget()

    def new_tab(self, url: str):
        tab = BrowserTab(self.web_profile, self)
        idx = self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentIndex(idx)
        tab.view.urlChanged.connect(lambda u, t=tab: self.update_address(u, t))
        tab.view.loadFinished.connect(lambda ok, t=tab: self.on_load_finished(ok, t))
        tab.load(url)

    def close_tab(self, index: int):
        if self.tabs.count() <= 1:
            QMessageBox.information(self, "CopperBrowser", "Cannot close the last tab.")
            return
        w = self.tabs.widget(index)
        self.tabs.removeTab(index)
        w.deleteLater()

    def close_tab_current(self):
        self.close_tab(self.tabs.currentIndex())

    def update_address(self, url: QUrl, tab: BrowserTab):
        if tab is self.current_tab():
            self.address.setText(url.toString())

    # --- Navigation ---
    def on_back(self): self.current_tab().view.back()
    def on_forward(self): self.current_tab().view.forward()
    def on_reload(self): self.current_tab().view.reload()
    def on_home(self): self.current_tab().load(self.config.homepage)

    def on_go(self):
        text = self.address.text().strip()
        if not text:
            return
        if "://" not in text and "." not in text:
            url = self.config.search_engine.replace("{query}", text)
        elif "://" not in text:
            url = "https://" + text
        else:
            url = text
        self.current_tab().load(url)

    def on_load_finished(self, ok: bool, tab: BrowserTab):
        if ok:
            url = tab.view.url().toString()
            title = tab.view.title()
            self.tabs.setTabText(self.tabs.indexOf(tab), title or "Tab")
            self.history.add(url, title)
            save_history(self.history)
        else:
            QMessageBox.warning(self, "Load failed", "The page failed to load.")

    # --- User Agent Toggle ---
    def toggle_user_agent(self):
        if self.current_ua == DEFAULT_USER_AGENT:
            self.current_ua = CHROME_USER_AGENT
            self.act_toggle_ua.setText("UA: Chrome")
        else:
            self.current_ua = DEFAULT_USER_AGENT
            self.act_toggle_ua.setText("UA: Copper")
        self.web_profile.setHttpUserAgent(self.current_ua)
        QMessageBox.information(self, "User Agent Switched",
                                f"Now using:\n{self.current_ua}")

    # --- Search Engine Toggle ---
    def toggle_search_engine(self):
        engines = list(SEARCH_ENGINES.items())
        current_idx = [name for name, url in engines].index(
            next(name for name, url in engines if url == self.config.search_engine)
        )
        next_idx = (current_idx + 1) % len(engines)
        name, url = engines[next_idx]
        self.config.search_engine = url
        self.act_search_engine.setText(f"SE: {name}")
        QMessageBox.information(self, "Search Engine Switched",
                                f"Now using {name}:\n{url}")

    # --- Bookmarks ---
    def on_bookmarks(self):
        dlg = BookmarksDialog(self, self.bookmarks)
        dlg.btn_open.clicked.connect(lambda: self._open_from_table(dlg.table, dlg))
        dlg.btn_add.clicked.connect(lambda: self._add_bookmark(dlg))
        dlg.btn_delete.clicked.connect(lambda: self._delete_bookmark(dlg))
        dlg.btn_close.clicked.connect(dlg.accept)
        dlg.exec()

    def _open_from_table(self, table, dlg):
        row = table.currentRow()
        if row < 0: return
        url = table.item(row, 2).text()
        self.current_tab().load(url)
        dlg.accept()

    def _add_bookmark(self, dlg):
        tab = self.current_tab()
        if not tab.view.url(): return
        name, ok = QInputDialog.getText(self, "Add Bookmark", "Name:",
                                        text=tab.title or tab.view.url().toString())
        if not ok or not name: return
        self.bookmarks.add(name, tab.view.url().toString())
        save_bookmarks(self.bookmarks)
        dlg.refresh()

    def _delete_bookmark(self, dlg):
        row = dlg.table.currentRow()
        if row < 0: return
        id_ = int(dlg.table.item(row, 0).text())
        if self.bookmarks.delete(id_):
            save_bookmarks(self.bookmarks)
            dlg.refresh()

    # --- History ---
    def on_history(self):
        dlg = HistoryDialog(self, self.history)
        dlg.btn_open.clicked.connect(lambda: self._open_from_table(dlg.table, dlg))
        dlg.btn_clear.clicked.connect(lambda: self._clear_history(dlg))
        dlg.btn_close.clicked.connect(dlg.accept)
        dlg.exec()

    def _clear_history(self, dlg):
        self.history.clear()           # <-- FIXED: actually clears entries
        save_history(self.history)     # overwrite file with empty list
        dlg.refresh()                  # refresh the dialog table
        QMessageBox.information(self, "History Cleared",
                                "All browsing history has been removed.")