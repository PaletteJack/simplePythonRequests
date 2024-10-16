from PySide6.QtWidgets import QTextEdit, QTabWidget

class OutputTabs(QTabWidget):
    def __init__(self):
        super().__init__()
        # Tab widget for Response, Headers, Body
        self.setStyleSheet("""
            QTabWidget::pane {
                border-radius: 0px;
                background: #FFE0B0;
            }
            QTabBar::tab {
                background: #FFF4E2;
                padding: 10px;
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background: #FFE0B0;
            }
        """)

        # Response tab
        self.response_text = QTextEdit()
        self.response_text.setReadOnly(True)
        self.response_text.setStyleSheet("""
            QTextEdit {
                border-radius: 5px;
                padding: 10px;
                font-family: Consolas, Monaco, monospace;
                font-size: 14px;
            }
        """)
        self.addTab(self.response_text, "Response")

        # Headers tab
        self.headers_text = QTextEdit()
        self.headers_text.setReadOnly(True)
        self.headers_text.setStyleSheet("""
            QTextEdit {
                border-radius: 5px;
                padding: 10px;
                font-family: Consolas, Monaco, monospace;
                font-size: 14px;
            }
        """)
        self.addTab(self.headers_text, "Response Headers")