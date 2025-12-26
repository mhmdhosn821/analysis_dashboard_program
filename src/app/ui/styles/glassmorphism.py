"""
Glassmorphism styles for PyQt6 application
"""

# Color scheme
COLORS = {
    'primary': '#F7941D',  # Orange
    'secondary': '#F5E6D3',  # Cream
    'dark': '#2D2D2D',
    'light': '#FFFFFF',
    'gray': '#E0E0E0',
    'success': '#4CAF50',
    'error': '#F44336',
    'warning': '#FF9800',
    'info': '#2196F3',
}

# Light theme styles
LIGHT_THEME = f"""
QMainWindow {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 {COLORS['secondary']}, stop:1 #FFFFFF);
}}

QWidget {{
    font-family: 'Vazirmatn', 'Segoe UI', Tahoma, sans-serif;
    font-size: 14px;
    color: {COLORS['dark']};
}}

/* Glassmorphism effect */
.glass-panel {{
    background: rgba(255, 255, 255, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 15px;
    backdrop-filter: blur(10px);
}}

/* Push buttons */
QPushButton {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 {COLORS['primary']}, stop:1 #FF9933);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: bold;
    font-size: 14px;
}}

QPushButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #FF9933, stop:1 {COLORS['primary']});
}}

QPushButton:pressed {{
    background: #E07010;
}}

QPushButton:disabled {{
    background: {COLORS['gray']};
    color: #999999;
}}

/* Secondary buttons */
QPushButton[secondary="true"] {{
    background: rgba(255, 255, 255, 0.8);
    color: {COLORS['dark']};
    border: 2px solid {COLORS['primary']};
}}

QPushButton[secondary="true"]:hover {{
    background: rgba(247, 148, 29, 0.1);
}}

/* Line edit */
QLineEdit {{
    background: rgba(255, 255, 255, 0.9);
    border: 2px solid {COLORS['gray']};
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
}}

QLineEdit:focus {{
    border: 2px solid {COLORS['primary']};
}}

/* Combo box */
QComboBox {{
    background: rgba(255, 255, 255, 0.9);
    border: 2px solid {COLORS['gray']};
    border-radius: 8px;
    padding: 8px;
    min-width: 120px;
}}

QComboBox:hover {{
    border: 2px solid {COLORS['primary']};
}}

QComboBox::drop-down {{
    border: none;
    width: 30px;
}}

QComboBox::down-arrow {{
    image: url(assets/icons/arrow_down.png);
    width: 12px;
    height: 12px;
}}

/* Scroll bar */
QScrollBar:vertical {{
    background: rgba(255, 255, 255, 0.5);
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background: {COLORS['primary']};
    border-radius: 6px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background: #FF9933;
}}

/* Tab widget */
QTabWidget::pane {{
    border: none;
    background: transparent;
}}

QTabBar::tab {{
    background: rgba(255, 255, 255, 0.6);
    border: none;
    border-radius: 10px 10px 0 0;
    padding: 10px 20px;
    margin-right: 5px;
    color: {COLORS['dark']};
}}

QTabBar::tab:selected {{
    background: {COLORS['primary']};
    color: white;
    font-weight: bold;
}}

QTabBar::tab:hover:!selected {{
    background: rgba(247, 148, 29, 0.3);
}}

/* Table widget */
QTableWidget {{
    background: rgba(255, 255, 255, 0.8);
    border: none;
    border-radius: 10px;
    gridline-color: {COLORS['gray']};
}}

QTableWidget::item {{
    padding: 8px;
}}

QTableWidget::item:selected {{
    background: rgba(247, 148, 29, 0.3);
    color: {COLORS['dark']};
}}

QHeaderView::section {{
    background: {COLORS['primary']};
    color: white;
    font-weight: bold;
    padding: 8px;
    border: none;
}}

/* Menu bar */
QMenuBar {{
    background: rgba(255, 255, 255, 0.8);
    border-bottom: 2px solid {COLORS['primary']};
    padding: 5px;
}}

QMenuBar::item {{
    background: transparent;
    padding: 8px 15px;
    border-radius: 5px;
}}

QMenuBar::item:selected {{
    background: rgba(247, 148, 29, 0.3);
}}

QMenu {{
    background: rgba(255, 255, 255, 0.95);
    border: 2px solid {COLORS['primary']};
    border-radius: 10px;
    padding: 5px;
}}

QMenu::item {{
    padding: 8px 25px;
    border-radius: 5px;
}}

QMenu::item:selected {{
    background: {COLORS['primary']};
    color: white;
}}

/* Progress bar */
QProgressBar {{
    background: rgba(255, 255, 255, 0.8);
    border: 2px solid {COLORS['gray']};
    border-radius: 10px;
    text-align: center;
    height: 25px;
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 {COLORS['primary']}, stop:1 #FF9933);
    border-radius: 8px;
}}

/* Check box */
QCheckBox {{
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 20px;
    height: 20px;
    border: 2px solid {COLORS['gray']};
    border-radius: 5px;
    background: rgba(255, 255, 255, 0.9);
}}

QCheckBox::indicator:checked {{
    background: {COLORS['primary']};
    border-color: {COLORS['primary']};
    image: url(assets/icons/check.png);
}}

/* Radio button */
QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid {COLORS['gray']};
    border-radius: 9px;
    background: rgba(255, 255, 255, 0.9);
}}

QRadioButton::indicator:checked {{
    background: {COLORS['primary']};
    border-color: {COLORS['primary']};
}}

/* Slider */
QSlider::groove:horizontal {{
    height: 8px;
    background: rgba(255, 255, 255, 0.8);
    border-radius: 4px;
}}

QSlider::handle:horizontal {{
    background: {COLORS['primary']};
    width: 20px;
    height: 20px;
    border-radius: 10px;
    margin: -6px 0;
}}

/* Status bar */
QStatusBar {{
    background: rgba(255, 255, 255, 0.9);
    border-top: 2px solid {COLORS['primary']};
}}
"""

# Dark theme styles
DARK_THEME = f"""
QMainWindow {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #1a1a1a, stop:1 {COLORS['dark']});
}}

QWidget {{
    font-family: 'Vazirmatn', 'Segoe UI', Tahoma, sans-serif;
    font-size: 14px;
    color: #FFFFFF;
}}

/* Glassmorphism effect for dark theme */
.glass-panel {{
    background: rgba(45, 45, 45, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    backdrop-filter: blur(10px);
}}

/* Push buttons */
QPushButton {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 {COLORS['primary']}, stop:1 #FF9933);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: bold;
    font-size: 14px;
}}

QPushButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #FF9933, stop:1 {COLORS['primary']});
}}

QPushButton:pressed {{
    background: #E07010;
}}

QPushButton:disabled {{
    background: #444444;
    color: #888888;
}}

/* Secondary buttons */
QPushButton[secondary="true"] {{
    background: rgba(45, 45, 45, 0.8);
    color: white;
    border: 2px solid {COLORS['primary']};
}}

QPushButton[secondary="true"]:hover {{
    background: rgba(247, 148, 29, 0.2);
}}

/* Line edit */
QLineEdit {{
    background: rgba(45, 45, 45, 0.9);
    border: 2px solid #555555;
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
    color: white;
}}

QLineEdit:focus {{
    border: 2px solid {COLORS['primary']};
}}

/* Combo box */
QComboBox {{
    background: rgba(45, 45, 45, 0.9);
    border: 2px solid #555555;
    border-radius: 8px;
    padding: 8px;
    min-width: 120px;
    color: white;
}}

QComboBox:hover {{
    border: 2px solid {COLORS['primary']};
}}

/* Table widget */
QTableWidget {{
    background: rgba(45, 45, 45, 0.8);
    border: none;
    border-radius: 10px;
    gridline-color: #555555;
    color: white;
}}

QTableWidget::item:selected {{
    background: rgba(247, 148, 29, 0.3);
}}

QHeaderView::section {{
    background: {COLORS['primary']};
    color: white;
    font-weight: bold;
    padding: 8px;
    border: none;
}}

/* Menu bar */
QMenuBar {{
    background: rgba(45, 45, 45, 0.9);
    border-bottom: 2px solid {COLORS['primary']};
    padding: 5px;
    color: white;
}}

QMenuBar::item {{
    background: transparent;
    padding: 8px 15px;
    border-radius: 5px;
}}

QMenuBar::item:selected {{
    background: rgba(247, 148, 29, 0.3);
}}

QMenu {{
    background: rgba(45, 45, 45, 0.95);
    border: 2px solid {COLORS['primary']};
    border-radius: 10px;
    padding: 5px;
    color: white;
}}

QMenu::item:selected {{
    background: {COLORS['primary']};
}}

/* Tab widget */
QTabBar::tab {{
    background: rgba(45, 45, 45, 0.6);
    color: white;
}}

QTabBar::tab:selected {{
    background: {COLORS['primary']};
    color: white;
}}

/* Scroll bar */
QScrollBar:vertical {{
    background: rgba(45, 45, 45, 0.5);
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background: {COLORS['primary']};
    border-radius: 6px;
    min-height: 20px;
}}

/* Status bar */
QStatusBar {{
    background: rgba(45, 45, 45, 0.9);
    border-top: 2px solid {COLORS['primary']};
    color: white;
}}
"""


def get_stylesheet(theme: str = "light") -> str:
    """
    Get stylesheet for the given theme
    
    Args:
        theme: Theme name (light or dark)
    
    Returns:
        CSS stylesheet
    """
    if theme == "dark":
        return DARK_THEME
    return LIGHT_THEME
