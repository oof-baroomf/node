from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTreeWidget, 
                           QTreeWidgetItem, QSizePolicy, QDialog, QLineEdit,
                           QTextEdit, QPushButton, QHBoxLayout, QFormLayout,
                           QListWidget, QListWidgetItem, QDialogButtonBox,
                           QMenu, QAction, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QIcon

class FunctionSidebar(QWidget):
    """Widget for displaying available functions in a sidebar"""
    
    # Signal emitted when a function is dragged
    function_dragged = pyqtSignal(str, dict)
    
    def __init__(self):
        super().__init__()
        
        # Set up the UI
        self.setup_ui()
        
        # Add default functions
        self.populate_default_functions()
        
    def setup_ui(self):
        """Set up the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title_label = QLabel("Function Library")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 10px;")
        layout.addWidget(title_label)
        
        # Tree widget to display functions
        self.function_tree = DraggableTreeWidget()
        self.function_tree.setHeaderHidden(True)
        self.function_tree.setIndentation(15)
        self.function_tree.setDragEnabled(True)
        self.function_tree.setAnimated(True)
        self.function_tree.item_dragged.connect(self.on_item_dragged)
        self.function_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.function_tree.customContextMenuRequested.connect(self.show_context_menu)
        
        layout.addWidget(self.function_tree)
        
        # Add New Function button
        add_btn = QPushButton("Add Custom Function")
        add_btn.clicked.connect(self.create_custom_function)
        layout.addWidget(add_btn)
        
        # Set size policies
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
    def populate_default_functions(self):
        """Add default function categories and functions"""
        # File Operations - Only include the three default functions
        file_category = self.add_category("File Operations")
        
        self.add_function(file_category, "Read File", 
                         "with open(filename, 'r') as f:\n    content = f.read()\nreturn content",
                         ["filename"], "content")
        
        self.add_function(file_category, "Write File",
                         "with open(filename, 'w') as f:\n    f.write(content)\nreturn True",
                         ["filename", "content"], "success")
        
        # System Operations
        system_category = self.add_category("System Operations")
        
        self.add_function(system_category, "Run Command",
                         "import subprocess\nresult = subprocess.run(command, shell=True, text=True, capture_output=True)\nreturn result.stdout",
                         ["command"], "output")
        
        # Custom Functions category (initially empty)
        self.add_category("Custom Functions")
        
        # Expand all categories by default
        self.function_tree.expandAll()
        
    def add_category(self, name):
        """Add a category to the function tree"""
        category = QTreeWidgetItem(self.function_tree)
        category.setText(0, name)
        category.setFlags(category.flags() & ~Qt.ItemIsDragEnabled)
        font = category.font(0)
        font.setBold(True)
        category.setFont(0, font)
        return category
        
    def add_function(self, parent, name, code, inputs, output):
        """Add a function to a category"""
        function_item = QTreeWidgetItem(parent)
        function_item.setText(0, name)
        function_item.setData(0, Qt.UserRole, {
            "name": name,
            "code": code,
            "inputs": inputs,
            "output": output
        })
        return function_item
        
    def on_item_dragged(self, item_data):
        """Emit signal when a function is dragged"""
        if item_data:
            self.function_dragged.emit("Python Function", item_data)
            
    def eventFilter(self, obj, event):
        """Filter events to prevent hover issues with NodeEditor"""
        return super().eventFilter(obj, event)
        
    def add_custom_function(self, category_name, name, code, inputs=None, output="result"):
        """Add a custom function to a specified category"""
        if inputs is None:
            inputs = ["input1"]
            
        # Find or create category
        category = None
        for i in range(self.function_tree.topLevelItemCount()):
            if self.function_tree.topLevelItem(i).text(0) == category_name:
                category = self.function_tree.topLevelItem(i)
                break
                
        if category is None:
            category = self.add_category(category_name)
            
        # Add function
        self.add_function(category, name, code, inputs, output)
        
        # Expand the category
        category.setExpanded(True)
    
    def create_custom_function(self):
        """Open dialog to create a new custom function"""
        dialog = CustomFunctionDialog(self)
        if dialog.exec_():
            # Get function data from dialog
            function_data = dialog.get_function_data()
            
            # Add to Custom Functions category
            self.add_custom_function("Custom Functions", 
                                   function_data["name"], 
                                   function_data["code"],
                                   function_data["inputs"],
                                   function_data["output"])
    
    def show_context_menu(self, position):
        """Show context menu for function tree items"""
        item = self.function_tree.itemAt(position)
        if not item:
            return
            
        # Only show context menu for function items (not categories)
        parent = item.parent()
        if not parent:
            return
            
        # Create context menu
        menu = QMenu()
        
        edit_action = None
        delete_action = None
        
        # Check if this is a custom function (in Custom Functions category)
        if parent.text(0) == "Custom Functions":
            edit_action = menu.addAction("Edit Function")
            delete_action = menu.addAction("Delete Function")
        
        # Show menu and handle actions
        action = menu.exec_(self.function_tree.mapToGlobal(position))
        
        if action == delete_action:
            # Remove the function
            parent.removeChild(item)
        elif action == edit_action:
            # Edit the function
            function_data = item.data(0, Qt.UserRole)
            dialog = CustomFunctionDialog(self, function_data)
            if dialog.exec_():
                # Update function data
                new_data = dialog.get_function_data()
                item.setText(0, new_data["name"])
                item.setData(0, Qt.UserRole, new_data)


class CustomFunctionDialog(QDialog):
    """Dialog for creating or editing a custom function"""
    
    def __init__(self, parent=None, function_data=None):
        super().__init__(parent)
        
        self.setWindowTitle("Create Custom Function")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        
        self.function_data = function_data or {
            "name": "",
            "code": "",
            "inputs": ["input1"],
            "output": "result"
        }
        
        self.setup_ui()
        
        # Populate fields if editing an existing function
        if function_data:
            self.setWindowTitle("Edit Function")
            self.name_edit.setText(function_data["name"])
            self.code_edit.setPlainText(function_data["code"])
            self.output_edit.setText(function_data["output"])
            
            # Clear and repopulate inputs list
            self.inputs_list.clear()
            for input_name in function_data["inputs"]:
                self.inputs_list.addItem(input_name)
    
    def setup_ui(self):
        """Set up the dialog UI"""
        layout = QVBoxLayout(self)
        
        # Function name
        form_layout = QFormLayout()
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter function name...")
        form_layout.addRow("Function Name:", self.name_edit)
        
        # Output name
        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText("Enter output name...")
        self.output_edit.setText(self.function_data["output"])
        form_layout.addRow("Output Name:", self.output_edit)
        
        layout.addLayout(form_layout)
        
        # Inputs list
        inputs_layout = QHBoxLayout()
        
        inputs_container = QWidget()
        inputs_vlayout = QVBoxLayout(inputs_container)
        
        label = QLabel("Inputs:")
        inputs_vlayout.addWidget(label)
        
        self.inputs_list = QListWidget()
        for input_name in self.function_data["inputs"]:
            self.inputs_list.addItem(input_name)
        inputs_vlayout.addWidget(self.inputs_list)
        
        # Input buttons
        input_buttons = QWidget()
        input_btn_layout = QVBoxLayout(input_buttons)
        
        add_input_btn = QPushButton("Add")
        add_input_btn.clicked.connect(self.add_input)
        input_btn_layout.addWidget(add_input_btn)
        
        edit_input_btn = QPushButton("Edit")
        edit_input_btn.clicked.connect(self.edit_input)
        input_btn_layout.addWidget(edit_input_btn)
        
        remove_input_btn = QPushButton("Remove")
        remove_input_btn.clicked.connect(self.remove_input)
        input_btn_layout.addWidget(remove_input_btn)
        
        input_btn_layout.addStretch()
        
        inputs_layout.addWidget(inputs_container)
        inputs_layout.addWidget(input_buttons)
        
        layout.addLayout(inputs_layout)
        
        # Code editor
        label = QLabel("Function Code:")
        layout.addWidget(label)
        
        self.code_edit = QTextEdit()
        self.code_edit.setFont(QFont("Courier New", 10))
        self.code_edit.setPlaceholderText("# Enter your Python code here...\n# Access inputs by name\n# Use 'return' to set the output value")
        if self.function_data["code"]:
            self.code_edit.setPlainText(self.function_data["code"])
        layout.addWidget(self.code_edit)
        
        # Buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.validate_and_accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
    
    def add_input(self):
        """Add a new input parameter"""
        # Create a default name
        base_name = "input"
        counter = 1
        name = f"{base_name}{counter}"
        
        # Find an unused name
        existing_inputs = [self.inputs_list.item(i).text() for i in range(self.inputs_list.count())]
        while name in existing_inputs:
            counter += 1
            name = f"{base_name}{counter}"
        
        # Create dialog to get the name
        input_name, ok = QLineEdit.getText(self, "Add Input", 
                                           "Enter input parameter name:", text=name)
        
        if ok and input_name:
            # Check if name already exists
            if input_name in existing_inputs:
                QMessageBox.warning(self, "Duplicate Input", 
                                    "An input with this name already exists.")
                return
                
            self.inputs_list.addItem(input_name)
    
    def edit_input(self):
        """Edit the selected input parameter"""
        current_item = self.inputs_list.currentItem()
        if not current_item:
            return
            
        current_name = current_item.text()
        existing_inputs = [self.inputs_list.item(i).text() for i in range(self.inputs_list.count())]
        existing_inputs.remove(current_name)
        
        input_name, ok = QLineEdit.getText(self, "Edit Input", 
                                           "Enter new input parameter name:", 
                                           text=current_name)
        
        if ok and input_name:
            # Check if name already exists
            if input_name in existing_inputs:
                QMessageBox.warning(self, "Duplicate Input", 
                                    "An input with this name already exists.")
                return
                
            current_item.setText(input_name)
    
    def remove_input(self):
        """Remove the selected input parameter"""
        current_row = self.inputs_list.currentRow()
        if current_row >= 0:
            self.inputs_list.takeItem(current_row)
    
    def validate_and_accept(self):
        """Validate the form before accepting"""
        # Check if name is provided
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Missing Name", 
                               "Please enter a function name.")
            return
            
        # Check if output name is provided
        if not self.output_edit.text().strip():
            QMessageBox.warning(self, "Missing Output", 
                               "Please enter an output name.")
            return
        
        # Check if at least one input is provided
        if self.inputs_list.count() == 0:
            QMessageBox.warning(self, "No Inputs", 
                               "Please add at least one input parameter.")
            return
            
        # Validate code - at minimum, check for a return statement
        code = self.code_edit.toPlainText().strip()
        if not code:
            QMessageBox.warning(self, "Empty Code", 
                               "Please enter function code.")
            return
            
        if "return" not in code:
            result = QMessageBox.question(self, "Missing Return", 
                                        "Your code doesn't contain a return statement. "
                                        "The function may not work as expected. Continue?",
                                        QMessageBox.Yes | QMessageBox.No)
            if result != QMessageBox.Yes:
                return
        
        # All checks passed, accept the dialog
        self.accept()
    
    def get_function_data(self):
        """Get the function data from the dialog"""
        inputs = []
        for i in range(self.inputs_list.count()):
            inputs.append(self.inputs_list.item(i).text())
            
        return {
            "name": self.name_edit.text().strip(),
            "code": self.code_edit.toPlainText().strip(),
            "inputs": inputs,
            "output": self.output_edit.text().strip()
        }


class DraggableTreeWidget(QTreeWidget):
    """Tree widget that supports custom drag operations"""
    
    item_dragged = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True)
        
    def startDrag(self, actions):
        """Override to emit a signal with the dragged item's data"""
        item = self.currentItem()
        if not item:
            return
            
        # Get the user data
        function_data = item.data(0, Qt.UserRole)
        if function_data:
            self.item_dragged.emit(function_data)
            
        # Call the parent implementation to handle the actual drag
        super().startDrag(actions)
