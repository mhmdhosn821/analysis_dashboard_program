"""
UI Cards - Metric and Stat Cards
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class MetricCard(QFrame):
    """Card widget for displaying a single metric"""
    
    clicked = pyqtSignal()
    
    def __init__(self, title: str, value: str, icon: str = "📊", 
                 subtitle: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("metricCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setup_ui(title, value, icon, subtitle)
    
    def setup_ui(self, title: str, value: str, icon: str, subtitle: str):
        """Setup the UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)
        
        # Header with icon and title
        header_layout = QHBoxLayout()
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        header_layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 12px; color: #666;")
        header_layout.addWidget(title_label, 1)
        
        layout.addLayout(header_layout)
        
        # Value
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #F7941D;")
        layout.addWidget(self.value_label)
        
        # Subtitle
        if subtitle:
            self.subtitle_label = QLabel(subtitle)
            self.subtitle_label.setStyleSheet("font-size: 11px; color: #999;")
            layout.addWidget(self.subtitle_label)
        else:
            self.subtitle_label = None
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Style
        self.setStyleSheet("""
            QFrame#metricCard {
                background: rgba(255, 255, 255, 0.9);
                border-radius: 12px;
                border: 1px solid rgba(247, 148, 29, 0.2);
            }
            QFrame#metricCard:hover {
                background: rgba(255, 255, 255, 1);
                border: 1px solid rgba(247, 148, 29, 0.4);
            }
        """)
    
    def update_value(self, value: str):
        """Update the metric value"""
        self.value_label.setText(value)
    
    def update_subtitle(self, subtitle: str):
        """Update the subtitle"""
        if self.subtitle_label:
            self.subtitle_label.setText(subtitle)
    
    def mousePressEvent(self, event):
        """Handle mouse press"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class StatCard(QFrame):
    """Card widget for displaying statistics with trend"""
    
    def __init__(self, title: str, current_value: str, previous_value: str = "",
                 trend: str = "up", parent=None):
        super().__init__(parent)
        self.setObjectName("statCard")
        self.setup_ui(title, current_value, previous_value, trend)
    
    def setup_ui(self, title: str, current_value: str, previous_value: str, trend: str):
        """Setup the UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(8)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 13px; color: #666; font-weight: 500;")
        layout.addWidget(title_label)
        
        # Current value
        self.current_label = QLabel(current_value)
        self.current_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #2D2D2D;")
        layout.addWidget(self.current_label)
        
        # Trend and previous value
        if previous_value:
            trend_layout = QHBoxLayout()
            
            # Trend indicator
            trend_icon = "📈" if trend == "up" else "📉"
            trend_color = "#10B981" if trend == "up" else "#EF4444"
            
            self.trend_label = QLabel(f"{trend_icon} {previous_value}")
            self.trend_label.setStyleSheet(f"font-size: 12px; color: {trend_color}; font-weight: 500;")
            trend_layout.addWidget(self.trend_label)
            trend_layout.addStretch()
            
            layout.addLayout(trend_layout)
        else:
            self.trend_label = None
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Style
        self.setStyleSheet("""
            QFrame#statCard {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 10px;
                border: 1px solid rgba(200, 200, 200, 0.3);
            }
        """)
    
    def update_values(self, current_value: str, previous_value: str = "", trend: str = "up"):
        """Update the stat values"""
        self.current_label.setText(current_value)
        if self.trend_label and previous_value:
            trend_icon = "📈" if trend == "up" else "📉"
            trend_color = "#10B981" if trend == "up" else "#EF4444"
            self.trend_label.setText(f"{trend_icon} {previous_value}")
            self.trend_label.setStyleSheet(f"font-size: 12px; color: {trend_color}; font-weight: 500;")


class InfoCard(QFrame):
    """Card widget for displaying information"""
    
    def __init__(self, title: str, items: list, parent=None):
        """
        Initialize info card
        
        Args:
            title: Card title
            items: List of tuples (label, value)
        """
        super().__init__(parent)
        self.setObjectName("infoCard")
        self.setup_ui(title, items)
    
    def setup_ui(self, title: str, items: list):
        """Setup the UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(12)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 600;")
        layout.addWidget(title_label)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background: rgba(200, 200, 200, 0.3); max-height: 1px;")
        layout.addWidget(separator)
        
        # Items
        self.item_widgets = []
        for label, value in items:
            item_layout = QHBoxLayout()
            
            label_widget = QLabel(label)
            label_widget.setStyleSheet("font-size: 12px; color: #666;")
            item_layout.addWidget(label_widget)
            
            value_widget = QLabel(str(value))
            value_widget.setStyleSheet("font-size: 12px; color: #2D2D2D; font-weight: 500;")
            value_widget.setAlignment(Qt.AlignmentFlag.AlignLeft)
            item_layout.addWidget(value_widget, 1)
            
            layout.addLayout(item_layout)
            self.item_widgets.append((label_widget, value_widget))
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Style
        self.setStyleSheet("""
            QFrame#infoCard {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 10px;
                border: 1px solid rgba(200, 200, 200, 0.3);
            }
        """)
    
    def update_item(self, label: str, value: str):
        """Update an item value"""
        for label_widget, value_widget in self.item_widgets:
            if label_widget.text() == label:
                value_widget.setText(str(value))
                break


class AlertCard(QFrame):
    """Card widget for displaying alerts"""
    
    dismiss_clicked = pyqtSignal()
    
    def __init__(self, title: str, message: str, alert_type: str = "info", parent=None):
        """
        Initialize alert card
        
        Args:
            title: Alert title
            message: Alert message
            alert_type: Type of alert (info, warning, error, success)
        """
        super().__init__(parent)
        self.setObjectName("alertCard")
        self.alert_type = alert_type
        self.setup_ui(title, message)
    
    def setup_ui(self, title: str, message: str):
        """Setup the UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(8)
        
        # Header
        header_layout = QHBoxLayout()
        
        # Icon based on type
        icons = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'error': '❌',
            'success': '✅'
        }
        icon_label = QLabel(icons.get(self.alert_type, 'ℹ️'))
        icon_label.setStyleSheet("font-size: 20px;")
        header_layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 13px; font-weight: 600;")
        header_layout.addWidget(title_label, 1)
        
        # Dismiss button
        dismiss_btn = QLabel("✖")
        dismiss_btn.setStyleSheet("font-size: 14px; color: #999; cursor: pointer;")
        dismiss_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        dismiss_btn.mousePressEvent = lambda e: self.dismiss_clicked.emit()
        header_layout.addWidget(dismiss_btn)
        
        layout.addLayout(header_layout)
        
        # Message
        message_label = QLabel(message)
        message_label.setStyleSheet("font-size: 12px; color: #555;")
        message_label.setWordWrap(True)
        layout.addWidget(message_label)
        
        self.setLayout(layout)
        
        # Style based on type
        colors = {
            'info': '#3B82F6',
            'warning': '#F59E0B',
            'error': '#EF4444',
            'success': '#10B981'
        }
        color = colors.get(self.alert_type, '#3B82F6')
        
        self.setStyleSheet(f"""
            QFrame#alertCard {{
                background: rgba(255, 255, 255, 0.95);
                border-radius: 8px;
                border-left: 4px solid {color};
            }}
        """)
