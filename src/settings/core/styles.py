PRIMARY       = "#7A5AF8"
PRIMARY_DARK  = "#5B3ED6"
PRIMARY_LIGHT = "rgba(122, 90, 248, 0.10)"
BG_COLOR      = "#F8F9FA"
BORDER        = "#E0E0E0"
TEXT_COLOR    = "#1A1A2E"

TAB_WIDGET_STYLE = f"""
QTabWidget::pane {{
    border: 1px solid {BORDER};
    border-radius: 0 8px 8px 8px;
    background: {BG_COLOR};
}}
QTabBar::tab {{
    background: white;
    color: #333333;
    border: 2px solid {BORDER};
    border-bottom: none;
    border-radius: 8px 8px 0 0;
    padding: 10px 28px;
    font-size: 11pt;
    font-weight: bold;
    min-width: 100px;
    min-height: 40px;
}}
QTabBar::tab:selected {{
    background: white;
    color: {PRIMARY};
    border-color: {PRIMARY};
    border-bottom: 2px solid white;
}}
QTabBar::tab:hover:!selected {{
    background: {PRIMARY_LIGHT};
}}
"""

GROUP_STYLE = f"""
QGroupBox {{
    color: #333333;
    font-size: 12pt;
    font-weight: bold;
    border: 2px solid {BORDER};
    border-radius: 8px;
    margin-top: 14px;
    padding-top: 10px;
    background: white;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 14px;
    padding: 0 8px;
    background: {BG_COLOR};
    border-radius: 4px;
}}
"""

SAVE_BUTTON_STYLE = f"""
QPushButton {{
    background-color: {PRIMARY};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 12pt;
    font-weight: bold;
    min-height: 52px;
}}
QPushButton:hover   {{ background-color: {PRIMARY_DARK}; }}
QPushButton:pressed {{ background-color: #4A2EC6; }}
"""

LABEL_STYLE = f"""
QLabel {{
    color: #333333;
    font-size: 11pt;
    font-weight: bold;
    background: transparent;
}}
"""

ACTION_BTN_STYLE = f"""
QPushButton {{
    background-color: {PRIMARY};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0 16px;
    font-size: 11pt;
    font-weight: bold;
    min-height: 44px;
}}
QPushButton:hover   {{ background-color: {PRIMARY_DARK}; }}
QPushButton:pressed {{ background-color: {PRIMARY_DARK}; }}
"""

GHOST_BTN_STYLE = f"""
QPushButton {{
    background-color: white;
    color: {PRIMARY};
    border: 2px solid {PRIMARY};
    border-radius: 8px;
    padding: 0 16px;
    font-size: 11pt;
    font-weight: bold;
    min-height: 44px;
}}
QPushButton:hover   {{ background-color: {PRIMARY_LIGHT}; }}
QPushButton:pressed {{ background-color: {PRIMARY_LIGHT}; }}
"""
