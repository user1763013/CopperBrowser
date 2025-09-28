from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem
)


class BookmarksDialog(QDialog):
    """Dialog for managing bookmarks."""

    def __init__(self, parent, bookmarks):
        super().__init__(parent)
        self.setWindowTitle("Bookmarks")
        self.bookmarks = bookmarks

        layout = QVBoxLayout(self)
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "URL"])
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        layout.addWidget(self.table)

        # Buttons
        btns = QHBoxLayout()
        self.btn_open = QPushButton("Open")
        self.btn_add = QPushButton("Add current")
        self.btn_delete = QPushButton("Delete")
        self.btn_close = QPushButton("Close")
        for b in (self.btn_open, self.btn_add, self.btn_delete, self.btn_close):
            btns.addWidget(b)
        layout.addLayout(btns)

        self.refresh()

    def refresh(self):
        items = self.bookmarks.list()
        self.table.setRowCount(len(items))
        for r, b in enumerate(items):
            self.table.setItem(r, 0, QTableWidgetItem(str(b.id)))
            self.table.setItem(r, 1, QTableWidgetItem(b.name))
            self.table.setItem(r, 2, QTableWidgetItem(b.url))


class HistoryDialog(QDialog):
    """Dialog for browsing history."""

    def __init__(self, parent, history):
        super().__init__(parent)
        self.setWindowTitle("History")
        self.history = history

        layout = QVBoxLayout(self)
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["#", "Title", "URL"])
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        layout.addWidget(self.table)

        # Buttons
        btns = QHBoxLayout()
        self.btn_open = QPushButton("Open")
        self.btn_clear = QPushButton("Clear")
        self.btn_close = QPushButton("Close")
        for b in (self.btn_open, self.btn_clear, self.btn_close):
            btns.addWidget(b)
        layout.addLayout(btns)

        self.refresh()

    def refresh(self):
        entries = self.history.list()
        self.table.setRowCount(len(entries))
        for i, e in enumerate(entries, start=1):
            self.table.setItem(i-1, 0, QTableWidgetItem(str(i)))
            self.table.setItem(i-1, 1, QTableWidgetItem(e.title or e.url))
            self.table.setItem(i-1, 2, QTableWidgetItem(e.url))