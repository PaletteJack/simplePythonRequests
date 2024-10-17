from PySide6.QtWidgets import QTextEdit, QTabWidget
from PySide6.QtGui import QTextOption, QFontDatabase
from PySide6.QtCore import Qt, QSize

class WrappingTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWordWrapMode(QTextOption.WrapMode.WrapAnywhere)
        self.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.setStyleSheet("""
            QTextEdit {
                border-radius: 0px;
                font-family: Consolas, Monaco, monospace;
                font-size: 14px;
                border: 2px solid #000;
                background: #FFF4E2;
            }
        """)
        
        # Set a monospace font
        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        font.setPointSize(10)  # Adjust size as needed
        self.setFont(font)
        
    def sizeHint(self):
        return QSize(600, 400)  # Adjust as needed

class OutputTabs(QTabWidget):
    def __init__(self):
        super().__init__()
        # Tab widget for Response, Headers, Body
        self.setStyleSheet("""
            QTabWidget::pane {
                border-radius: 0px;
                top: -2px;
            }
            QTabBar::tab {
                background: #FFF4E2;
                padding: 10px;
                border-radius: 0px;
                font-size: 14px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: #FFE0B0;
                border: 2px solid #000;
                margin-bottom: -2px;
            }
            QTabBar::tab:!selected {
                top: -2px;
            }
        """)

        # Response tab
        self.response_text = WrappingTextEdit()
        self.response_text.setReadOnly(True)
        self.addTab(self.response_text, "RESPONSE")

        # Headers tab
        self.headers_text = WrappingTextEdit()
        self.headers_text.setReadOnly(True)
        self.addTab(self.headers_text, "HEADERS")