from QNodeEditor.themes.theme import Theme
from PyQt5.QtGui import QColor, QPen, QBrush
from PyQt5.QtCore import Qt

class ModernTheme(Theme):
    """
    A modern theme for QNodeEditor with a shadcn-inspired aesthetic.
    Features higher contrast, rounded corners, and modern styling.
    """
    
    # Editor colors
    @property
    def editor_color_background(self):
        return QColor("#14141e")  # Dark background
        
    @property
    def editor_color_grid(self):
        return QColor("#292938")  # Slightly lighter grid
    
    @property
    def editor_grid_spacing(self):
        return 25  # Larger grid spacing
    
    @property
    def editor_grid_point_size(self):
        return 2  # Smaller grid points
        
    @property
    def editor_color_region_select(self):
        return QColor(42, 130, 218, 50)  # Semi-transparent blue selection
    
    # Node styling
    @property
    def node_color_body(self):
        return QColor("#2a2a3a")  # Dark node body
        
    @property
    def node_color_header(self):
        return QColor("#35354d")  # Slightly lighter header
        
    @property
    def node_color_title(self):
        return QColor("#ffffff")  # White title text
        
    @property
    def node_color_outline_default(self):
        return QColor("#444455")  # Light outline
        
    @property
    def node_color_outline_selected(self):
        return QColor("#6366f1")  # Indigo highlight
        
    @property
    def node_color_outline_hovered(self):
        return QColor("#818cf8")  # Lighter indigo hover
    
    @property
    def node_border_radius(self):
        return 10  # More rounded corners
        
    @property
    def node_outline_width(self):
        return 2.0  # Thicker outline
    
    # Socket styling
    @property
    def socket_radius(self):
        return 8  # Larger socket radius
    
    @property
    def socket_color_fill(self):
        return QColor("#6366f1")  # Indigo socket fill
        
    @property
    def socket_color_outline(self):
        return QColor("#ffffff")  # White outline
        
    @property
    def socket_outline_width(self):
        return 1.5  # Thicker socket outline
    
    # Edge styling
    @property
    def edge_type(self):
        return "bezier"  # Curved edges
    
    @property
    def edge_color_default(self):
        return QColor("#6366f1")  # Indigo edge color
    
    @property
    def edge_color_selected(self):
        return QColor("#818cf8")  # Light indigo for selected
    
    @property
    def edge_color_hover(self):
        return QColor("#a5b4fc")  # Very light indigo on hover
    
    @property
    def edge_width_default(self):
        return 2.0  # Thicker edge
        
    @property
    def edge_width_selected(self):
        return 3.0  # Even thicker when selected
        
    # Font styling
    @property
    def font_name(self):
        return "Inter"  # Modern sans-serif font
        
    @property
    def font_size(self):
        return 11  # Slightly larger font
    
    # Widget styling
    @property
    def widget_color_base(self):
        return QColor("#2a2a3a")  # Dark widget base
    
    @property
    def widget_color_hovered(self):
        return QColor("#3c3c4e")  # Lighter on hover
        
    @property
    def widget_color_pressed(self):
        return QColor("#5a5a70")  # Even lighter when pressed
        
    @property
    def widget_color_active(self):
        return QColor("#6366f1")  # Indigo accent for active state
        
    @property
    def widget_color_text(self):
        return QColor("#ffffff")  # White text
        
    @property
    def widget_color_text_hover(self):
        return QColor("#ffffff")  # White text on hover
        
    @property
    def widget_border_radius(self):
        return 6  # Rounded widget corners
        
    @property
    def widget_outline_width(self):
        return 1.5  # Thicker outline width
