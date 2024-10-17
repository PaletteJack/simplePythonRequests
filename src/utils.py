from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtGui import QColor
import json

def apply_shadow(widget, blur_radius=0, x_offset=3, y_offset=3, color=QColor(0,0,0,255)):
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(blur_radius)
    shadow.setXOffset(x_offset)
    shadow.setYOffset(y_offset)
    shadow.setColor(color)
    widget.setGraphicsEffect(shadow)
    
def parse_json_body(body):
        try:
            return json.loads(body)
        except json.JSONDecodeError as e:
            line_col = f"line {e.lineno} column {e.colno}"
            if e.msg.startswith('Expecting'):
                return f"JSON Error: {e.msg} at {line_col}"
            else:
                return f"Invalid JSON: {e.msg} at {line_col}"