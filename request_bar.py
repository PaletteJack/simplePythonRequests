from PySide6.QtWidgets import QWidget, QHBoxLayout, QComboBox, QLineEdit, QPushButton
from PySide6.QtCore import Signal

class UrlInput(QWidget):
    returnPressed = Signal()  # Custom signal to emulate QLineEdit's returnPressed

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.protocol = QComboBox()
        self.protocol.addItems(["https://", "http://"])
        self.protocol.setStyleSheet("""
            QComboBox {
                border-top-left-radius: 5px;
                border-bottom-left-radius: 5px;
                padding: 5px;
                background: #FFF4E2;
                font-size: 16px;
            }
        """)
        self.protocol.setFixedWidth(90)

        self.url = QLineEdit()
        self.url.setPlaceholderText("google.com")
        self.url.setStyleSheet("""
            QLineEdit {
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
                border-left: none;
                padding: 5px;
                font-size: 16px;
            }
        """)
        self.url.returnPressed.connect(self.returnPressed.emit)

        layout.addWidget(self.protocol)
        layout.addWidget(self.url)

    def text(self):
        return self.protocol.currentText() + self.url.text()

    def setText(self, text):
        if text.startswith("https://"):
            self.protocol.setCurrentIndex(0)
            self.url.setText(text[8:])
        elif text.startswith("http://"):
            self.protocol.setCurrentIndex(1)
            self.url.setText(text[7:])
        else:
            self.url.setText(text)

class RequestBar(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.http_verb = QComboBox()
        self.http_verb.addItems(["GET", "POST", "PUT", "PATCH", "DELETE"])
        self.http_verb.setStyleSheet("""
            QComboBox {
                background-color: #FFF4E2;
                border-radius: 5px;
                padding: 5px;
                font-size: 16px;
            }
        """)
        self.addWidget(self.http_verb)

        self.url_input = UrlInput()  # Using our custom UrlInput widget
        self.addWidget(self.url_input, 1)  # 1 is the stretch factor

        self.send_button = QPushButton("SEND")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #FFF4E2;
                border-radius: 5px;
                padding: 5px 15px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #FFE0B0;
            }
        """)
        self.addWidget(self.send_button)