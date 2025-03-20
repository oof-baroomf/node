from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                            QLabel, QTextEdit, QMenu, QAction, QLineEdit)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from QNodeEditor import Node
from QNodeEditor.entry import Entry
from QNodeEditor.entries.text_box import TextBoxEntry
import inspect
import ast
import textwrap

class PythonFunctionNode(Node):
    # Use a counter to ensure each node has a unique code
    _node_counter = 0
    
    @classmethod
    def get_next_code(cls):
        code = cls._node_counter
        cls._node_counter += 1
        return code
    
    # This is how we'll handle the code property
    @property
    def code(self):
        return self._code
    
    def __init__(self):
        # Generate unique code for this node instance
        self._code = PythonFunctionNode.get_next_code()
        self.globals_env = {}  # Will be set from outside
        self.inputs = []  # Track input names
        self.input_types = {}  # Track input types
        self.output_name = "result"  # Default output name
        self.function_body = ""  # The Python code for the function body
        self.function_name = f"function_{self._code}"  # Default function name
        
        # Initialize first, then create components
        super().__init__()
        
        # Ensure entries are properly built
        self.update_entries()
    
    def create(self):
        """Initialize the node with default settings"""
        self.title = "Python Function"
        
        # Add output for the result
        self.add_label_output(self.output_name)
        
        # Add one default input
        self.add_input("input1")
        
        # Add code editing area as a text entry
        self.add_code_editor()

    def add_input(self, name, input_type="any"):
        """Add a new input to the node"""
        self.add_value_input(name)
        self.inputs.append(name)
        self.input_types[name] = input_type

    def remove_input(self, name):
        """Remove an input from the node"""
        if name in self.inputs:
            self.remove_entry(name)
            self.inputs.remove(name)
            if name in self.input_types:
                del self.input_types[name]
    
    def add_code_editor(self):
        """Add a code editor to the node"""
        # Custom text entry for code editing
        code_entry = CodeEntry(self.function_body)
        code_entry.name = "code_editor"
        code_entry.text_changed.connect(self.update_function_body)
        
        # Add our custom code entry to the node
        self.add_entry(code_entry)
        
        # Add buttons for managing inputs
        self.add_input_buttons()
    
    def add_input_buttons(self):
        """Add buttons for adding and removing inputs"""
        button_entry = InputButtonsEntry()
        button_entry.name = "input_buttons"
        button_entry.add_clicked.connect(self.on_add_input)
        button_entry.remove_clicked.connect(self.on_remove_input)
        button_entry.rename_clicked.connect(self.on_rename_output)
        
        self.add_entry(button_entry)
    
    def update_function_body(self, code):
        """Update the function body when code changes"""
        self.function_body = code
    
    def on_add_input(self):
        """Add a new input field"""
        # Find a unique name
        i = len(self.inputs) + 1
        while f"input{i}" in self.inputs:
            i += 1
            
        new_input = f"input{i}"
        
        # Add the new input
        self.add_input(new_input)
        
        # Force update of the node layout
        self.update_entries()
    
    def on_remove_input(self):
        """Remove the last input field"""
        if len(self.inputs) > 1:  # Always keep at least one input
            last_input = self.inputs[-1]
            self.remove_input(last_input)
            
            # Force update of the node layout
        self.update_entries()
    
    def on_rename_output(self):
        """Rename the output of the node"""
        # This would typically show a dialog, but for simplicity we'll just cycle through options
        outputs = ["result", "output", "return_value", "value"]
        current_index = outputs.index(self.output_name) if self.output_name in outputs else 0
        next_index = (current_index + 1) % len(outputs)
        self.output_name = outputs[next_index]
        
        # Update the output label
        for entry_name in self.entry_names():
            entry = self.get_entry(entry_name)
            if hasattr(entry, 'socket') and entry.socket and entry.socket.is_output:
                # Found our output entry
                entry.name = self.output_name
                # Force update of the node layout
                self.update_entries()
                break
    
    def evaluate(self, values):
        """Execute the Python function and return the result"""
        try:
            # Create local environment for execution
            local_env = {}
            
            # Add input values
            for input_name in self.inputs:
                if input_name in values:
                    local_env[input_name] = values[input_name]
                else:
                    local_env[input_name] = None
            
            # Prepare the full function code
            params = ", ".join(self.inputs)
            function_code = f"def {self.function_name}({params}):\n"
            
            # Handle empty function body
            if not self.function_body.strip():
                function_code += "    return None"
            else:
                # Indent the function body
                indented_body = textwrap.indent(self.function_body, '    ')
                function_code += indented_body
            
            # Execute the function in the context of both globals and locals
            exec_globals = self.globals_env.copy()
            
            # Execute the function definition
            exec(function_code, exec_globals, local_env)
            
            # Call the function with the inputs
            function_args = [local_env[input_name] if input_name in local_env else None 
                            for input_name in self.inputs]
            
            result = local_env[self.function_name](*function_args)
            
            # Set the output
            self.set_output_value(self.output_name, result)
            
        except Exception as e:
            raise RuntimeError(f"Error in Python function node: {str(e)}")
    
    def get_state(self):
        """Save the node state"""
        state = super().get_state()
        
        # Add custom properties
        state.update({
            "inputs": self.inputs,
            "input_types": self.input_types,
            "output_name": self.output_name,
            "function_body": self.function_body,
            "function_name": self.function_name
        })
        
        return state
    
    def set_state(self, state):
        """Restore the node state"""
        # Extract our custom properties
        if "inputs" in state:
            self.inputs = state["inputs"]
        
        if "input_types" in state:
            self.input_types = state["input_types"]
            
        if "output_name" in state:
            self.output_name = state["output_name"]
            
        if "function_body" in state:
            self.function_body = state["function_body"]
            
        if "function_name" in state:
            self.function_name = state["function_name"]
        
        # Call parent implementation
        super().set_state(state)
        
        # Ensure code editor has the latest function body
        for entry_name in self.entry_names():
            entry = self.get_entry(entry_name)
            if entry_name == "code_editor" and hasattr(entry, 'set_text'):
                entry.set_text(self.function_body)


class CodeEntry(Entry):
    """A custom entry for editing Python code"""
    text_changed = pyqtSignal(str)
    
    def __init__(self, initial_text=""):
        # Entry requires a name parameter
        super().__init__(name="code_editor")
        self.text = initial_text
        # Pre-create widget to avoid None issues during node creation
        self._widget = self.create_widget()
        
    def calculate_value(self):
        return self.text
        
    def create_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create code editor
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Enter Python code here...")
        self.editor.setText(self.text)
        
        # Set monospace font for code
        font = QFont("Courier New", 10)
        self.editor.setFont(font)
        
        # Connect change signal
        self.editor.textChanged.connect(self.on_text_changed)
        
        # Add editor to layout
        layout.addWidget(self.editor)
        
        # Set minimum size
        widget.setMinimumHeight(120)
        widget.setMinimumWidth(200)
        
        return widget
    
    def on_text_changed(self):
        self.text = self.editor.toPlainText()
        self.text_changed.emit(self.text)
        
    def set_text(self, text):
        """Set the text in the editor"""
        self.text = text
        if hasattr(self, 'editor'):
            self.editor.setText(text)
            
    def get_widget(self):
        """Override to ensure widget is always available"""
        return self._widget


class InputButtonsEntry(Entry):
    """A custom entry for adding input management buttons"""
    add_clicked = pyqtSignal()
    remove_clicked = pyqtSignal()
    rename_clicked = pyqtSignal()
    
    def __init__(self):
        # Entry requires a name parameter
        super().__init__(name="input_buttons")
    
    def calculate_value(self):
        return None
    
    def create_widget(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Add input button
        add_btn = QPushButton("+")
        add_btn.setToolTip("Add input")
        add_btn.setFixedWidth(30)
        add_btn.clicked.connect(self.add_clicked.emit)
        
        # Remove input button
        remove_btn = QPushButton("-")
        remove_btn.setToolTip("Remove input")
        remove_btn.setFixedWidth(30)
        remove_btn.clicked.connect(self.remove_clicked.emit)
        
        # Rename output button
        rename_btn = QPushButton("✎")
        rename_btn.setToolTip("Rename output")
        rename_btn.setFixedWidth(30)
        rename_btn.clicked.connect(self.rename_clicked.emit)
        
        # Add buttons to layout
        layout.addWidget(add_btn)
        layout.addWidget(remove_btn)
        layout.addWidget(rename_btn)
        layout.addStretch()
        
        return widget
