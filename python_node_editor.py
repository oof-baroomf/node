import sys
import os
import json
import io
import contextlib
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QPushButton, QSplitter, QFileDialog, 
                            QListWidget, QLineEdit, QLabel, QMessageBox, QTabWidget)
from PyQt5.QtCore import Qt, QSize, pyqtSlot
from PyQt5.QtGui import QColor, QFont, QPalette

from QNodeEditor import NodeEditorDialog, Node, NodeEditor
from QNodeEditor.themes import theme as Theme

from python_node import PythonFunctionNode
from global_constants import GlobalConstantsWidget
from function_sidebar import FunctionSidebar
from terminal_widget import TerminalWidget
from custom_theme import ModernTheme

class PythonNodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Function Node Editor")
        self.resize(1400, 900)
        
        # Set application style
        self.apply_styles()
        
        # Create central widget and layout
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(central_widget)
        
        # Create main horizontal splitter
        self.main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.main_splitter)
        
        # Create sidebar splitter (for functions and constants)
        self.sidebar_splitter = QSplitter(Qt.Vertical)
        
        # Create function sidebar
        self.function_sidebar = FunctionSidebar()
        self.function_sidebar.function_dragged.connect(self.create_function_node)
        self.sidebar_splitter.addWidget(self.function_sidebar)
        
        # Create global constants sidebar
        self.constants_widget = GlobalConstantsWidget()
        self.sidebar_splitter.addWidget(self.constants_widget)
        
        # Add sidebar splitter to main splitter
        self.main_splitter.addWidget(self.sidebar_splitter)
        
        # Create editor and terminal splitter
        self.editor_terminal_splitter = QSplitter(Qt.Vertical)
        
        # Create node editor container
        self.editor_container = QWidget()
        self.editor_layout = QVBoxLayout(self.editor_container)
        self.editor_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create editor
        self.create_editor()
        
        # Create toolbar
        self.create_toolbar()
        
        # Add editor container to splitter
        self.editor_terminal_splitter.addWidget(self.editor_container)
        
        # Create terminal
        self.terminal = TerminalWidget()
        self.editor_terminal_splitter.addWidget(self.terminal)
        
        # Add editor/terminal splitter to main splitter
        self.main_splitter.addWidget(self.editor_terminal_splitter)
        
        # Set splitter sizes
        self.main_splitter.setSizes([250, 1150])
        self.sidebar_splitter.setSizes([500, 400])
        self.editor_terminal_splitter.setSizes([700, 200])
        
        # Initialize with welcome message
        self.terminal.append_message("Python Function Node Editor started\n", "info")
        self.terminal.append_message("Drag functions from the sidebar to the editor to create nodes\n")
        
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
        palette.setColor(QPalette.Highlight, QColor(99, 102, 241))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        
        QApplication.setPalette(palette)
        
        # Set default font - use system font instead of "Inter"
        font = QFont()  # Use default system font
        font.setPointSize(10)
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
            padding: 6px;
        }
        
        QTreeWidget, QListWidget {
            background-color: #232330;
            color: #f0f0fa;
            border: none;
        }
        
        QTreeWidget::item, QListWidget::item {
            padding: 6px;
        }
        
        QTreeWidget::item:selected, QListWidget::item:selected {
            background-color: #3a3a6a;
        }
        
        QSplitter::handle {
            background-color: #2a2a3a;
            height: 1px;
            width: 1px;
        }
        
        QLabel {
            color: #f0f0fa;
        }
        
        QTabWidget::pane {
            border: none;
        }
        
        QTabBar::tab {
            background-color: #232330;
            color: #f0f0fa;
            padding: 8px 16px;
            border: none;
        }
        
        QTabBar::tab:selected {
            background-color: #3a3a6a;
        }
        """
        self.setStyleSheet(stylesheet)
        
    def create_editor(self):
        # Create node editor instance
        self.editor = NodeEditor()
        self.editor.available_nodes = {"Python Function": PythonFunctionNode}
        # Remove custom theme
        self.editor_layout.addWidget(self.editor)
        
    def create_toolbar(self):
        toolbar_widget = QWidget()
        toolbar_layout = QHBoxLayout(toolbar_widget)
        toolbar_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create toolbar buttons with modern styling
        run_button = QPushButton("Run Flow")
        run_button.setStyleSheet("""
            QPushButton { 
                background-color: #6366f1; 
                font-weight: 600;
            }
            QPushButton:hover { 
                background-color: #818cf8; 
            }
        """)
        run_button.clicked.connect(self.run_flow)
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_flow)
        
        load_button = QPushButton("Load")
        load_button.clicked.connect(self.load_flow)
        
        clear_button = QPushButton("New")
        clear_button.clicked.connect(self.clear_flow)
        
        # Add buttons to toolbar
        toolbar_layout.addWidget(run_button)
        toolbar_layout.addWidget(save_button)
        toolbar_layout.addWidget(load_button)
        toolbar_layout.addWidget(clear_button)
        toolbar_layout.addStretch()
        
        self.editor_layout.insertWidget(0, toolbar_widget)
    
    @pyqtSlot(str, dict)
    def create_function_node(self, node_type, function_data):
        """Create a new function node from the dragged function data"""
        if node_type == "Python Function" and function_data:
            try:
                # Get node class
                node_class = self.editor.available_nodes.get(node_type)
                if not node_class:
                    self.terminal.append_message(f"Unknown node type: {node_type}", "error")
                    return
                
                # Use the view's add_node method to place a node
                # This properly creates and positions the node in the editor
                pos = self.editor.view.mapToScene(self.editor.view.rect().center())
                node = self.editor.view.add_node(node_class)
                
                if node:
                    # Set node properties from function data
                    node.function_body = function_data.get("code", "")
                    node.title = function_data.get("name", "Function")
                    
                    # Get inputs
                    inputs = function_data.get("inputs", ["input1"])
                    
                    # Clear existing inputs
                    existing_inputs = node.inputs.copy()
                    for input_name in existing_inputs:
                        node.remove_input(input_name)
                    
                    # Add new inputs
                    for input_name in inputs:
                        node.add_input(input_name)
                    
                    # Set output name
                    output_name = function_data.get("output", "result")
                    node.output_name = output_name
                    
                    # Update the node
                    node.update_entries()
                    
                    # Set the code in the code editor
                    for entry_name in node.entry_names():
                        entry = node.get_entry(entry_name)
                        if entry_name == "code_editor" and hasattr(entry, 'set_text'):
                            entry.set_text(node.function_body)
                    
                    # Log to terminal
                    self.terminal.append_message(f"Created {node.title} node", "info")
                
            except Exception as e:
                import traceback
                self.terminal.append_message(f"Error creating node: {str(e)}", "error")
                self.terminal.append_message(traceback.format_exc(), "error")
        
    def run_flow(self):
        """Execute the node graph"""
        try:
            self.terminal.append_message("\n--- Running Flow ---\n", "info")
            
            # Capture stdout to display in terminal
            stdout_capture = io.StringIO()
            
            # Add global constants to environment
            globals_env = self.constants_widget.get_constants()
            
            # Log constants
            if globals_env:
                self.terminal.append_message("Using global constants:\n")
                for name, value in globals_env.items():
                    self.terminal.append_message(f"  {name} = {repr(value)}\n")
                self.terminal.append_message("\n")
            
            # Pass globals to the scene through a special property
            for node in self.editor.scene.nodes:
                node.globals_env = globals_env
            
            # Evaluate the scene and capture stdout
            with contextlib.redirect_stdout(stdout_capture):
                result = self.editor.scene.evaluate()
            
            # Get captured output
            output = stdout_capture.getvalue()
            if output:
                self.terminal.append_message("Output:\n")
                self.terminal.append_message(output)
            
            # Display result
            if result:
                self.terminal.append_message(f"Result: {result}\n", "success")
            
            self.terminal.append_message("Flow executed successfully\n", "success")
                
        except Exception as e:
            self.terminal.append_message(f"Error executing flow: {str(e)}\n", "error")
    
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
                
            self.terminal.append_message(f"Flow saved to {filepath}\n", "success")
            
        except Exception as e:
            self.terminal.append_message(f"Error saving flow: {str(e)}\n", "error")
    
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
            
            self.terminal.append_message(f"Flow loaded from {filepath}\n", "success")
            
        except Exception as e:
            self.terminal.append_message(f"Error loading flow: {str(e)}\n", "error")
    
    def clear_flow(self):
        """Create a new empty flow"""
        # Ask for confirmation
        reply = QMessageBox.question(
            self, "New Flow", 
            "Create a new flow? Any unsaved changes will be lost.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Clear the editor
            self.editor.scene.clear()
            # Clear the constants
            self.constants_widget.set_constants({})
            # Log
            self.terminal.append_message("Created new flow\n", "info")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PythonNodeEditor()
    window.show()
    sys.exit(app.exec_())
