from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtGui import  QPainter, QColor
from PySide6.QtCore import Qt

class LoadingOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        self.spinner = QProgressBar()
        self.spinner.setRange(0, 0)
        self.spinner.setTextVisible(False)
        self.spinner.setFixedSize(50, 50)
        self.spinner.setStyleSheet("""
            QProgressBar {
                border: 2px solid #FFF4E2;
                border-radius: 25px;
                background-color: transparent;
            }
            QProgressBar::chunk {
                background-color: transparent;
            }
        """)
        
        layout.addWidget(self.spinner)
        
        self.label = QLabel("Loading...")
        self.label.setStyleSheet("color: #FFF4E2; font-weight: bold;")
        layout.addWidget(self.label)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 128))