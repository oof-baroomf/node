# Python Function Node Editor

A visual editor for creating Python function flows using QNodeEditor. This application allows you to create nodes that represent Python functions with dynamic inputs and outputs, and connect them together to create data processing pipelines.

## Features

- Create Python functions as nodes with customizable inputs and outputs
- Add and remove inputs dynamically
- Edit function bodies directly in the node
- Manage global constants via a sidebar
- Save and load flows to/from JSON files
- Modern, visually appealing UI

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
python python_node_editor.py
```

## Usage

### Creating Functions

1. Right-click in the editor area and select "Add > Python Function" to create a new node
2. Edit the function code in the code editor area of the node
3. Use the (+) button to add inputs and the (-) button to remove inputs
4. Use the (✎) button to cycle through output name options

### Managing Global Constants

Use the sidebar on the left to add, edit, and remove global constants that will be available to all function nodes.

### Running Flows

Click the "Run" button in the toolbar to execute the flow. Results will be displayed in a dialog.

### Saving and Loading

- Click "Save" to save your flow to a JSON file
- Click "Load" to load a previously saved flow

## Examples

### Simple Calculator

```python
# Node 1: Add two numbers
a + b

# Node 2: Multiply by 2
result * 2
```

### Text Processing

```python
# Node 1: Capitalize text
text.upper()

# Node 2: Count words
len(text.split())
```