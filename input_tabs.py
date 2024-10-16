from PySide6.QtWidgets import QTextEdit, QTabWidget, QScrollArea, QTableWidget, QHeaderView
from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt

class KeyValueTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(1, 2, parent)
        self.setHorizontalHeaderLabels(["Key", "Value"])
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
                background-color: #f0f0f0;
                padding: 4px;
                border: 1px solid #d0d0d0;
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
            }
            QTabBar::tab {
                padding: 10px;
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background: #E6E6E6;
            }
        """)
        self.body_text = QTextEdit()
        self.body_text.setStyleSheet("""
            QTextEdit {
                font-family: Consolas, Monaco, monospace;
                font-size: 14px;
            }
        """)
        self.body_text.setPlaceholderText("Enter request body here (e.g., JSON)")
        self.addTab(self.body_text, "Body")
        
        params_scroll = QScrollArea()
        self.params_table = KeyValueTable()
        params_scroll.setWidget(self.params_table)
        params_scroll.setWidgetResizable(True)
        self.addTab(params_scroll, "Params")
        
        headers_scroll = QScrollArea()
        self.headers_table = KeyValueTable()
        headers_scroll.setWidget(self.headers_table)
        headers_scroll.setWidgetResizable(True)
        self.addTab(headers_scroll, "Headers")
        
        
    def get_body(self):
        return self.body_text.toPlainText()

    def get_params(self):
        return self.params_table.get_pairs()

    def get_headers(self):
        return self.headers_table.get_pairs()