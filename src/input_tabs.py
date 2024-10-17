from PySide6.QtWidgets import (QTabWidget, QVBoxLayout, QHBoxLayout, QWidget,
                               QRadioButton, QButtonGroup, QLabel, QScrollArea)
from PySide6.QtGui import QKeyEvent, QTextCursor
from PySide6.QtCore import Signal
from auto_closing_text import AutoClosingTextEdit
from key_value_table import KeyValueTable

class InputTabs(QTabWidget):
    contentTypeChanged = Signal(str)
    
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
        
        body_widget = QWidget()
        body_widget.setStyleSheet("""
            QWidget {
                border-radius: 0px;
                border: 2px solid #000;
            }
        """)
        body_layout = QVBoxLayout(body_widget)
        
        content_type_layout = QHBoxLayout()
        
        self.content_type_group = QButtonGroup(self)
        content_types = [
            ("none", "none"),
            ("x-www-form-urlencoded","x-www-form-urlencoded"),
            ("raw", "raw (json)")
        ]
        
        for value, text in content_types:
            radio_button = QRadioButton(text)
            radio_button.setStyleSheet("""
                QRadioButton {
                    border: none;
                    font-weight: bold;
                    font-family: Consolas, Monaco, monospace;
                }
            """)
            self.content_type_group.addButton(radio_button)
            content_type_layout.addWidget(radio_button)
            if value == "none":
                radio_button.setChecked(True)
                
        self.content_type_group.buttonClicked.connect(self.on_content_type_changed)
        content_type_layout.addStretch()
        
        self.body_text = AutoClosingTextEdit()
        self.body_text.setStyleSheet("""
            QTextEdit {
                font-family: Consolas, Monaco, monospace;
                font-size: 14px;
                border: none;
            }
        """)
        self.body_text.setPlaceholderText("Enter request body here (e.g., JSON)")
        body_layout.addLayout(content_type_layout)
        body_layout.addWidget(self.body_text)

        self.addTab(body_widget, "BODY")
        
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
        
    def on_content_type_changed(self, button):
        content_type = self.get_content_type()
        self.contentTypeChanged.emit(content_type)
        if content_type is None:
            self.body_text.setPlaceholderText("This request does not have a body")
            self.body_text.setReadOnly(True)
        else:
            self.body_text.setPlaceholderText("Enter request body here")
            self.body_text.setReadOnly(False)
    
    def get_content_type(self):
        selected_button = self.content_type_group.checkedButton()
        content_type = selected_button.text()
        match content_type:
            case "raw (json)":
                return "application/json"
            case "x-www-form-urlencoded":
                return "application/x-www-form-urlencoded"
            case _:
                return None
    
    def get_body(self):
        return self.body_text.toPlainText() if not self.body_text.isReadOnly() else None

    def get_params(self):
        return self.params_table.get_pairs()

    def get_headers(self):
        return self.headers_table.get_pairs()