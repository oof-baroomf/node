from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QTextCursor

class TerminalWidget(QWidget):
    """Terminal widget for displaying command execution output"""
    
    def __init__(self):
        super().__init__()
        
        # Set up the UI
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the terminal UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header_layout = QHBoxLayout()
        header_label = QLabel("Terminal")
        header_label.setStyleSheet("font-weight: bold; font-size: 12px; padding: 5px;")
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Terminal output area
        self.terminal = QPlainTextEdit()
        self.terminal.setReadOnly(True)
        
        # Set monospace font
        font = QFont("Menlo", 10)  # Just use Menlo which is available on macOS
        if not font.exactMatch():
            # Fall back to a more common monospace font if Menlo isn't available
            font = QFont("Courier New", 10)
        self.terminal.setFont(font)
        
        # Set colors
        self.terminal.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e2e;
                color: #d9e0ee;
                border: none;
                border-radius: 4px;
            }
        """)
        
        # Initialize text formats for different message types
        self.format_standard = QTextCharFormat()
        self.format_standard.setForeground(QColor("#d9e0ee"))
        
        self.format_error = QTextCharFormat()
        self.format_error.setForeground(QColor("#f38ba8"))
        
        self.format_success = QTextCharFormat()
        self.format_success.setForeground(QColor("#a6e3a1"))
        
        self.format_info = QTextCharFormat()
        self.format_info.setForeground(QColor("#89dceb"))
        
        layout.addWidget(self.terminal)
        
    def clear(self):
        """Clear the terminal"""
        self.terminal.clear()
        
    def append_message(self, message, message_type="standard"):
        """Append a message to the terminal"""
        cursor = self.terminal.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        # Choose format based on message type
        if message_type == "error":
            text_format = self.format_error
        elif message_type == "success":
            text_format = self.format_success
        elif message_type == "info":
            text_format = self.format_info
        else:
            text_format = self.format_standard
            
        # Insert text with the specified format
        cursor.setCharFormat(text_format)
        cursor.insertText(message)
        
        # Add a newline if the message doesn't end with one
        if not message.endswith('\n'):
            cursor.insertText('\n')
            
        # Scroll to the new content
        self.terminal.setTextCursor(cursor)
        self.terminal.ensureCursorVisible()
