from QNodeEditor.themes.dark import DarkTheme
from PyQt5.QtGui import QColor, QPen, QFont
from PyQt5.QtCore import Qt

class ModernTheme(DarkTheme):
    """
    A modern theme for QNodeEditor with a clean, minimalist aesthetic.
    """
    
    # Override the base theme properties with your custom values
    def __init__(self):
        super().__init__()
        
        # Editor colors
        self._editor_color_background = QColor("#14141e")
        self._editor_color_grid = QColor("#1e1e2d")
        self._editor_grid_spacing = 30
        self._editor_grid_point_size = 1
        self._editor_color_region_select = QColor(99, 102, 241, 50)
        self._editor_color_cut = QColor(255, 0, 0, 100)
        self._editor_cut_dash_pattern = [5, 5]
        self._editor_cut_width = 2.0
        
        # Node styling
        self._node_color_body = QColor("#2a2a3a")
        self._node_color_header = QColor("#35354d")
        self._node_color_title = QColor("#ffffff")
        self._node_color_outline_default = QColor("#444455")
        self._node_color_outline_selected = QColor("#6366f1")
        self._node_color_outline_hovered = QColor("#818cf8")
        self._node_border_radius = 0  # No curved corners
        self._node_outline_width = 1.5
        self._node_color_shadow = QColor(20, 20, 20, 80)
        self._node_shadow_radius = 10
        self._node_shadow_offset = (3, 3)  # X and Y offset as a tuple
        self._node_padding = (8, 8)  # (horizontal, vertical) padding
        self._node_entry_spacing = 4
        
        # Socket styling
        self._socket_radius = 6
        self._socket_color_fill = QColor("#6366f1")
        self._socket_color_outline = QColor("#ffffff")
        self._socket_outline_width = 1.0
        
        # Edge styling
        self._edge_type = "bezier"
        self._edge_color_default = QColor("#6366f1")
        self._edge_color_selected = QColor("#818cf8")
        self._edge_color_hover = QColor("#a5b4fc")
        self._edge_color_drag = QColor("#6366f1")
        self._edge_width_default = 1.5
        self._edge_width_selected = 2.5
        self._edge_width_hover = 2.0
        self._edge_width_drag = 1.5
        self._edge_style_default = Qt.SolidLine
        self._edge_style_selected = Qt.SolidLine
        self._edge_style_hover = Qt.SolidLine
        self._edge_style_drag = Qt.DashLine
        
        # Font styling - Use system fonts
        self._font_name = ""  # Empty string to use system default
        self._font_size = 11
        self._icon_path = None  # Don't use custom icons
        
        # Widget styling
        self._widget_color_base = QColor("#2a2a3a")
        self._widget_color_hovered = QColor("#3c3c4e")
        self._widget_color_pressed = QColor("#5a5a70")
        self._widget_color_active = QColor("#6366f1")
        self._widget_color_text = QColor("#ffffff")
        self._widget_color_text_hover = QColor("#ffffff")
        self._widget_color_text_disabled = QColor("#9999aa")
        self._widget_border_radius = 2  # Very minimal border radius
        self._widget_outline_width = 1.0
        self._widget_height = 24
        self._widget_color_hovered_accent = QColor("#818cf8")
        self._widget_color_pressed_accent = QColor("#4f46e5")
        self._widget_combo_box_arrow_name = None  # Use default arrow
        
    # Add a method to override font path resolution
    def get_font_path(self):
        """Override font path to avoid file not found errors"""
        return None
        
    # Add a method to override icon path resolution
    def get_icon_path(self, name):
        """Override icon path to avoid file not found errors"""
        return None
        
    # Override the font method to directly return a QFont without loading files
    def font(self):
        """Return a system font instead of trying to load a font file"""
        font = QFont()
        font.setPointSize(self.font_size)
        return font
    
    # Define getter properties for each theme attribute
    @property
    def editor_color_background(self):
        return self._editor_color_background
        
    @property
    def editor_color_grid(self):
        return self._editor_color_grid
    
    @property
    def editor_grid_spacing(self):
        return self._editor_grid_spacing
    
    @property
    def editor_grid_point_size(self):
        return self._editor_grid_point_size
        
    @property
    def editor_color_region_select(self):
        return self._editor_color_region_select
    
    @property 
    def editor_color_cut(self):
        return self._editor_color_cut
    
    @property
    def editor_cut_dash_pattern(self):
        return self._editor_cut_dash_pattern
    
    @property
    def editor_cut_width(self):
        return self._editor_cut_width
    
    @property
    def node_color_body(self):
        return self._node_color_body
        
    @property
    def node_color_header(self):
        return self._node_color_header
        
    @property
    def node_color_title(self):
        return self._node_color_title
        
    @property
    def node_color_outline_default(self):
        return self._node_color_outline_default
        
    @property
    def node_color_outline_selected(self):
        return self._node_color_outline_selected
        
    @property
    def node_color_outline_hovered(self):
        return self._node_color_outline_hovered
    
    @property
    def node_border_radius(self):
        return self._node_border_radius
        
    @property
    def node_outline_width(self):
        return self._node_outline_width
    
    @property
    def node_color_shadow(self):
        return self._node_color_shadow
        
    @property
    def node_shadow_radius(self):
        return self._node_shadow_radius
        
    @property
    def node_shadow_offset(self):
        return self._node_shadow_offset
        
    @property
    def node_padding(self):
        return self._node_padding
        
    @property
    def node_entry_spacing(self):
        return self._node_entry_spacing
    
    @property
    def socket_radius(self):
        return self._socket_radius
    
    @property
    def socket_color_fill(self):
        return self._socket_color_fill
        
    @property
    def socket_color_outline(self):
        return self._socket_color_outline
        
    @property
    def socket_outline_width(self):
        return self._socket_outline_width
    
    @property
    def edge_type(self):
        return self._edge_type
    
    @property
    def edge_color_default(self):
        return self._edge_color_default
    
    @property
    def edge_color_selected(self):
        return self._edge_color_selected
    
    @property
    def edge_color_hover(self):
        return self._edge_color_hover
        
    @property
    def edge_color_drag(self):
        return self._edge_color_drag
    
    @property
    def edge_width_default(self):
        return self._edge_width_default
        
    @property
    def edge_width_selected(self):
        return self._edge_width_selected
        
    @property
    def edge_width_hover(self):
        return self._edge_width_hover
        
    @property
    def edge_width_drag(self):
        return self._edge_width_drag
        
    @property
    def edge_style_default(self):
        return self._edge_style_default
        
    @property
    def edge_style_selected(self):
        return self._edge_style_selected
        
    @property
    def edge_style_hover(self):
        return self._edge_style_hover
        
    @property
    def edge_style_drag(self):
        return self._edge_style_drag
    
    @property
    def font_name(self):
        return self._font_name
        
    @property
    def font_size(self):
        return self._font_size
    
    @property
    def widget_color_base(self):
        return self._widget_color_base
    
    @property
    def widget_color_hovered(self):
        return self._widget_color_hovered
        
    @property
    def widget_color_pressed(self):
        return self._widget_color_pressed
        
    @property
    def widget_color_active(self):
        return self._widget_color_active
        
    @property
    def widget_color_text(self):
        return self._widget_color_text
        
    @property
    def widget_color_text_hover(self):
        return self._widget_color_text_hover
        
    @property
    def widget_color_text_disabled(self):
        return self._widget_color_text_disabled
        
    @property
    def widget_border_radius(self):
        return self._widget_border_radius
        
    @property
    def widget_outline_width(self):
        return self._widget_outline_width
        
    @property
    def widget_height(self):
        return self._widget_height
        
    @property
    def widget_color_hovered_accent(self):
        return self._widget_color_hovered_accent
        
    @property
    def widget_color_pressed_accent(self):
        return self._widget_color_pressed_accent
        
    @property
    def widget_combo_box_arrow_name(self):
        return self._widget_combo_box_arrow_name
