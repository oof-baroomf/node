import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QPushButton, QSplitter, QFileDialog, 
                            QListWidget, QLineEdit, QLabel, QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QFont, QPalette

from QNodeEditor import NodeEditorDialog, Node, NodeEditor
from QNodeEditor.themes import Theme

from python_node import PythonFunctionNode
from global_constants import GlobalConstantsWidget
from custom_theme import ModernTheme

class PythonNodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Function Node Editor")
        self.resize(1200, 800)
        
        # Set application style
        self.apply_styles()
        
        # Create central widget and layout
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        self.setCentralWidget(central_widget)
        
        # Create splitter for sidebar and editor
        self.splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.splitter)
        
        # Create global constants sidebar
        self.constants_widget = GlobalConstantsWidget()
        self.splitter.addWidget(self.constants_widget)
        
        # Create node editor container
        self.editor_container = QWidget()
        self.editor_layout = QVBoxLayout(self.editor_container)
        self.splitter.addWidget(self.editor_container)
        
        # Create editor
        self.create_editor()
        
        # Create toolbar
        self.create_toolbar()
        
        # Set splitter sizes
        self.splitter.setSizes([300, 900])
        
    def apply_styles(self):
        # Set the application palette
        palette = QPalette()
        background_color = QColor(20, 20, 30)
        text_color = QColor(240, 240, 250)
        
        palette.setColor(QPalette.Window, background_color)
        palette.setColor(QPalette.WindowText, text_color)
        palette.setColor(QPalette.Base, QColor(30, 30, 40))
        palette.setColor(QPalette.AlternateBase, QColor(35, 35, 45))
        palette.setColor(QPalette.Text, text_color)
        palette.setColor(QPalette.Button, QColor(45, 45, 55))
        palette.setColor(QPalette.ButtonText, text_color)
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        
        QApplication.setPalette(palette)
        
        # Set default font
        font = QFont("Inter", 10)
        QApplication.setFont(font)
        
        # Apply stylesheet
        stylesheet = """
        QMainWindow, QDialog {
            background-color: #14141e;
        }
        
        QPushButton {
            background-color: #3a3a4a;
            color: #f0f0fa;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: 500;
        }
        
        QPushButton:hover {
            background-color: #4a4a5a;
        }
        
        QPushButton:pressed {
            background-color: #2a2a3a;
        }
        
        QLineEdit, QTextEdit {
            background-color: #2a2a3a;
            color: #f0f0fa;
            border: 1px solid #3a3a4a;
            border-radius: 4px;
            padding: 6px;
        }
        
        QListWidget {
            background-color: #232330;
            color: #f0f0fa;
            border: 1px solid #3a3a4a;
            border-radius: 4px;
        }
        
        QListWidget::item {
            padding: 8px;
        }
        
        QListWidget::item:selected {
            background-color: #3a3a6a;
        }
        
        QSplitter::handle {
            background-color: #3a3a4a;
        }
        
        QLabel {
            color: #f0f0fa;
        }
        """
        self.setStyleSheet(stylesheet)
        
    def create_editor(self):
        # Create node editor instance
        self.editor = NodeEditor()
        self.editor.available_nodes = {"Python Function": PythonFunctionNode}
        self.editor.theme = ModernTheme
        self.editor_layout.addWidget(self.editor)
        
    def create_toolbar(self):
        toolbar_widget = QWidget()
        toolbar_layout = QHBoxLayout(toolbar_widget)
        toolbar_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create toolbar buttons
        run_button = QPushButton("Run")
        run_button.setIcon(self.style().standardIcon(self.style().SP_MediaPlay))
        run_button.clicked.connect(self.run_flow)
        
        save_button = QPushButton("Save")
        save_button.setIcon(self.style().standardIcon(self.style().SP_DialogSaveButton))
        save_button.clicked.connect(self.save_flow)
        
        load_button = QPushButton("Load")
        load_button.setIcon(self.style().standardIcon(self.style().SP_DialogOpenButton))
        load_button.clicked.connect(self.load_flow)
        
        # Add buttons to toolbar
        toolbar_layout.addWidget(run_button)
        toolbar_layout.addWidget(save_button)
        toolbar_layout.addWidget(load_button)
        toolbar_layout.addStretch()
        
        self.editor_layout.insertWidget(0, toolbar_widget)
        
    def run_flow(self):
        """Execute the node graph"""
        try:
            # Add global constants to environment
            globals_env = self.constants_widget.get_constants()
            
            # Pass globals to the scene through a special property
            for node in self.editor.scene.nodes:
                node.globals_env = globals_env
            
            # Evaluate the scene
            result = self.editor.scene.evaluate()
            
            if result:
                QMessageBox.information(self, "Flow Result", f"Flow executed successfully: {result}")
            else:
                QMessageBox.information(self, "Flow Result", "Flow executed successfully")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error executing flow: {str(e)}")
    
    def save_flow(self):
        """Save the current node graph to a file"""
        try:
            # Get file path
            filepath, _ = QFileDialog.getSaveFileName(
                self, "Save Flow", "", "JSON Files (*.json)"
            )
            
            if not filepath:
                return
                
            # Save node editor state
            editor_state = self.editor.scene.get_state()
            
            # Save global constants
            global_constants = self.constants_widget.get_constants()
            
            # Combine both states
            save_data = {
                "editor_state": editor_state,
                "global_constants": global_constants
            }
            
            # Save to file
            with open(filepath, 'w') as f:
                json.dump(save_data, f, indent=2)
                
            QMessageBox.information(self, "Success", f"Flow saved to {filepath}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving flow: {str(e)}")
    
    def load_flow(self):
        """Load a node graph from a file"""
        try:
            # Get file path
            filepath, _ = QFileDialog.getOpenFileName(
                self, "Load Flow", "", "JSON Files (*.json)"
            )
            
            if not filepath:
                return
                
            # Load file
            with open(filepath, 'r') as f:
                save_data = json.load(f)
                
            # Clear current scene
            self.editor.scene.clear()
            
            # Restore node editor state
            editor_state = save_data.get("editor_state", {})
            self.editor.scene.set_state(editor_state)
            
            # Restore global constants
            global_constants = save_data.get("global_constants", {})
            self.constants_widget.set_constants(global_constants)
            
            QMessageBox.information(self, "Success", f"Flow loaded from {filepath}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading flow: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PythonNodeEditor()
    window.show()
    sys.exit(app.exec_())
