from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QListWidget, QListWidgetItem, QLineEdit, QLabel, 
                           QMessageBox, QDialog, QDialogButtonBox, QComboBox)
from PyQt5.QtCore import Qt, pyqtSignal
import ast

class ConstantEditDialog(QDialog):
    """Dialog for editing a constant's value and type"""
    
    def __init__(self, name="", value="", value_type="str", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Constant")
        self.resize(400, 150)
        
        # Main layout
        layout = QVBoxLayout(self)
        
        # Name field
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        self.name_edit = QLineEdit(name)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)
        
        # Type selection
        type_layout = QHBoxLayout()
        type_label = QLabel("Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["str", "int", "float", "bool", "list", "dict"])
        self.type_combo.setCurrentText(value_type)
        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)
        
        # Value field
        value_layout = QHBoxLayout()
        value_label = QLabel("Value:")
        self.value_edit = QLineEdit(str(value))
        value_layout.addWidget(value_label)
        value_layout.addWidget(self.value_edit)
        layout.addLayout(value_layout)
        
        # Button box
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def on_type_changed(self, type_text):
        """Show a placeholder appropriate for the selected type"""
        if type_text == "str":
            self.value_edit.setPlaceholderText("Enter a string value")
        elif type_text == "int":
            self.value_edit.setPlaceholderText("Enter an integer (e.g. 42)")
        elif type_text == "float":
            self.value_edit.setPlaceholderText("Enter a float (e.g. 3.14)")
        elif type_text == "bool":
            self.value_edit.setPlaceholderText("Enter True or False")
        elif type_text == "list":
            self.value_edit.setPlaceholderText("Enter a list (e.g. [1, 2, 3])")
        elif type_text == "dict":
            self.value_edit.setPlaceholderText("Enter a dict (e.g. {'a': 1, 'b': 2})")
    
    def get_name(self):
        return self.name_edit.text()
    
    def get_value(self):
        # Parse the value based on the selected type
        value_str = self.value_edit.text()
        value_type = self.type_combo.currentText()
        
        try:
            if value_type == "str":
                return value_str
            elif value_type == "int":
                return int(value_str)
            elif value_type == "float":
                return float(value_str)
            elif value_type == "bool":
                return value_str.lower() == "true"
            elif value_type == "list" or value_type == "dict":
                return ast.literal_eval(value_str)
            else:
                return value_str
        except Exception as e:
            QMessageBox.warning(self, "Invalid Value", f"Could not convert value to {value_type}: {str(e)}")
            return None
    
    def get_type(self):
        return self.type_combo.currentText()


class GlobalConstantsWidget(QWidget):
    """Widget for managing global constants"""
    
    constants_changed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        
        # Constants dictionary
        self.constants = {}
        self.constants_types = {}
        
        # Set up the UI
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Global Constants")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        layout.addWidget(title_label)
        
        # Constants list
        self.constants_list = QListWidget()
        self.constants_list.itemDoubleClicked.connect(self.edit_constant)
        layout.addWidget(self.constants_list)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        # Add button
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_constant)
        buttons_layout.addWidget(self.add_button)
        
        # Edit button
        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.edit_selected_constant)
        buttons_layout.addWidget(self.edit_button)
        
        # Remove button
        self.remove_button = QPushButton("Remove")
        self.remove_button.clicked.connect(self.remove_constant)
        buttons_layout.addWidget(self.remove_button)
        
        layout.addLayout(buttons_layout)
    
    def add_constant(self):
        """Add a new constant"""
        dialog = ConstantEditDialog(parent=self)
        if dialog.exec_():
            name = dialog.get_name()
            if not name:
                QMessageBox.warning(self, "Invalid Name", "Constant name cannot be empty.")
                return
                
            if name in self.constants:
                QMessageBox.warning(self, "Duplicate Name", "A constant with this name already exists.")
                return
            
            value = dialog.get_value()
            if value is None:  # Conversion error occurred
                return
                
            value_type = dialog.get_type()
            
            self.constants[name] = value
            self.constants_types[name] = value_type
            
            self.update_constants_list()
            self.constants_changed.emit(self.constants)
    
    def edit_constant(self, item):
        """Edit an existing constant"""
        name = item.text().split(":")[0].strip()
        current_value = self.constants.get(name, "")
        current_type = self.constants_types.get(name, "str")
        
        dialog = ConstantEditDialog(name, current_value, current_type, parent=self)
        if dialog.exec_():
            new_name = dialog.get_name()
            value = dialog.get_value()
            if value is None:  # Conversion error occurred
                return
                
            value_type = dialog.get_type()
            
            # If name changed, remove old constant
            if new_name != name:
                if new_name in self.constants:
                    QMessageBox.warning(self, "Duplicate Name", "A constant with this name already exists.")
                    return
                    
                del self.constants[name]
                del self.constants_types[name]
            
            # Update with new values
            self.constants[new_name] = value
            self.constants_types[new_name] = value_type
            
            self.update_constants_list()
            self.constants_changed.emit(self.constants)
    
    def edit_selected_constant(self):
        """Edit the currently selected constant"""
        selected_items = self.constants_list.selectedItems()
        if selected_items:
            self.edit_constant(selected_items[0])
    
    def remove_constant(self):
        """Remove the selected constant"""
        selected_items = self.constants_list.selectedItems()
        if not selected_items:
            return
            
        name = selected_items[0].text().split(":")[0].strip()
        
        # Confirm deletion
        reply = QMessageBox.question(
            self, "Confirm Deletion", 
            f"Are you sure you want to delete the constant '{name}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if name in self.constants:
                del self.constants[name]
                del self.constants_types[name]
                
            self.update_constants_list()
            self.constants_changed.emit(self.constants)
    
    def update_constants_list(self):
        """Update the displayed list of constants"""
        self.constants_list.clear()
        
        for name, value in self.constants.items():
            type_name = self.constants_types.get(name, "unknown")
            display_value = str(value)
            
            # Truncate long values
            if len(display_value) > 30:
                display_value = display_value[:27] + "..."
                
            item_text = f"{name}: {display_value} ({type_name})"
            item = QListWidgetItem(item_text)
            self.constants_list.addItem(item)
    
    def get_constants(self):
        """Get the current constants dictionary"""
        return self.constants
    
    def set_constants(self, constants_dict, types_dict=None):
        """Set the constants from a dictionary"""
        self.constants = constants_dict.copy()
        
        if types_dict:
            self.constants_types = types_dict.copy()
        else:
            # Infer types if not provided
            self.constants_types = {}
            for name, value in self.constants.items():
                value_type = type(value).__name__
                if value_type == "str":
                    self.constants_types[name] = "str"
                elif value_type == "int":
                    self.constants_types[name] = "int"
                elif value_type == "float":
                    self.constants_types[name] = "float"
                elif value_type == "bool":
                    self.constants_types[name] = "bool"
                elif value_type == "list":
                    self.constants_types[name] = "list"
                elif value_type == "dict":
                    self.constants_types[name] = "dict"
                else:
                    self.constants_types[name] = "str"
                    
        self.update_constants_list()
