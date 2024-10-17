from PySide6.QtWidgets import QTextEdit
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