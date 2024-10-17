from PySide6.QtWidgets import QTextEdit, QTabWidget, QScrollArea, QTableWidget, QHeaderView
from PySide6.QtGui import QKeyEvent, QTextCursor
from PySide6.QtCore import Qt, QEvent

class AutoClosingTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.auto_close_pairs = {
            '"': '"',
            "'": "'",
            '(': ')',
            '[': ']',
            '{': '}',
            '<': '>'
        }

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.handleEnterKey(event)
        elif event.text() in self.auto_close_pairs:
            self.handleAutoClose(event.text())
        elif event.key() == Qt.Key_Backspace:
            self.handleBackspace()
        else:
            super().keyPressEvent(event)

    def handleAutoClose(self, opening_char):
        cursor = self.textCursor()
        closing_char = self.auto_close_pairs[opening_char]
        cursor.insertText(opening_char + closing_char)
        cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, 1)
        self.setTextCursor(cursor)

    def handleEnterKey(self, event):
        cursor = self.textCursor()
        current_line = cursor.block().text()
        indent = len(current_line) - len(current_line.lstrip())
        
        super().keyPressEvent(event)  # Default Enter key behavior
        
        cursor = self.textCursor()
        cursor.insertText(' ' * indent)
        self.setTextCursor(cursor)

    def handleBackspace(self):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 1)
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 1)
            selected_text = cursor.selectedText()
            if selected_text in self.auto_close_pairs.items():
                cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, 1)
                cursor.deleteChar()
                cursor.deleteChar()
                self.setTextCursor(cursor)
                return
        super().keyPressEvent(QKeyEvent(QEvent.KeyPress, Qt.Key_Backspace, Qt.NoModifier))

class KeyValueTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(1, 2, parent)
        self.setHorizontalHeaderLabels(["KEY", "VALUE"])
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setVisible(False)
        self.setStyleSheet("""
            QTableWidget {
                border: none;
                font-family: Consolas, Monaco, monospace;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #E6E6E6;
                padding: 4px;
                font-weight: bold;
            }
        """)
        self.cellChanged.connect(self.on_cell_changed)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.add_row()
        elif event.key() == Qt.Key_Backspace:
            current_row = self.currentRow()
            if current_row > 0 and self.is_row_empty(current_row):
                self.removeRow(current_row)
                self.setCurrentCell(current_row - 1, self.currentColumn())
        super().keyPressEvent(event)

    def add_row(self):
        if self.is_last_row_empty():
            return
        self.setRowCount(self.rowCount() + 1)

    def is_row_empty(self, row):
        return (self.item(row, 0) is None or self.item(row, 0).text() == "") and \
               (self.item(row, 1) is None or self.item(row, 1).text() == "")

    def is_last_row_empty(self):
        return self.is_row_empty(self.rowCount() - 1)

    def on_cell_changed(self, row, column):
        if row == self.rowCount() - 1 and not self.is_row_empty(row):
            self.add_row()

    def get_pairs(self):
        pairs = {}
        for row in range(self.rowCount()):
            key_item = self.item(row, 0)
            value_item = self.item(row, 1)
            if key_item and value_item and key_item.text():
                pairs[key_item.text()] = value_item.text()
        return pairs

class InputTabs(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QTabWidget::pane {
                border-radius: 0px;
                background: white;
                top: -2px;
            }
            QTabBar::tab {
                padding: 10px;
                border-radius: 0px;
                font-size: 14px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: #E6E6E6;
                border: 2px solid #000;
                border-bottom: none;
                margin-bottom: -2px;
            }
            QTabBar::tab:!selected {
                top: -2px;
            }
        """)
        self.body_text = AutoClosingTextEdit()
        self.body_text.setStyleSheet("""
            QTextEdit {
                font-family: Consolas, Monaco, monospace;
                font-size: 14px;
                border: 2px solid #000;
            }
        """)
        self.body_text.setPlaceholderText("Enter request body here (e.g., JSON)")
        self.addTab(self.body_text, "BODY")
        
        params_scroll = QScrollArea()
        self.params_table = KeyValueTable()
        params_scroll.setWidget(self.params_table)
        params_scroll.setWidgetResizable(True)
        params_scroll.setStyleSheet("""
            QScrollArea {
                font-family: Consolas, Monaco, monospace;
                font-size: 14px;
                border: 2px solid #000;
            }
        """)
        self.addTab(params_scroll, "PARAMS")
        
        headers_scroll = QScrollArea()
        self.headers_table = KeyValueTable()
        headers_scroll.setWidget(self.headers_table)
        headers_scroll.setWidgetResizable(True)
        headers_scroll.setStyleSheet("""
            QScrollArea {
                font-family: Consolas, Monaco, monospace;
                font-size: 14px;
                border: 2px solid #000;
            }
        """)
        self.addTab(headers_scroll, "HEADERS")
        
        
    def get_body(self):
        return self.body_text.toPlainText()

    def get_params(self):
        return self.params_table.get_pairs()

    def get_headers(self):
        return self.headers_table.get_pairs()