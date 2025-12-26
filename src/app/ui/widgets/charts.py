"""
Chart Widgets - Various chart types for data visualization
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from typing import List, Dict, Any
import json


class ChartWidget(QFrame):
    """Base chart widget"""
    
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setObjectName("chartWidget")
        self.title = title
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)
        
        # Title
        title_label = QLabel(self.title)
        title_label.setStyleSheet("font-size: 14px; color: #333; font-weight: 600;")
        layout.addWidget(title_label)
        
        # Chart container
        self.chart_container = QWidget()
        self.chart_layout = QVBoxLayout()
        self.chart_container.setLayout(self.chart_layout)
        layout.addWidget(self.chart_container, 1)
        
        self.setLayout(layout)
        
        # Style
        self.setStyleSheet("""
            QFrame#chartWidget {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 10px;
                border: 1px solid rgba(200, 200, 200, 0.3);
            }
        """)


class LineChartWidget(ChartWidget):
    """Line chart widget"""
    
    def __init__(self, title: str, parent=None):
        super().__init__(title, parent)
    
    def set_data(self, labels: List[str], datasets: List[Dict[str, Any]]):
        """
        Set chart data
        
        Args:
            labels: X-axis labels
            datasets: List of datasets, each with 'label', 'data', and optional 'color'
        """
        # Clear existing content
        for i in reversed(range(self.chart_layout.count())): 
            self.chart_layout.itemAt(i).widget().setParent(None)
        
        # Simple text-based visualization (can be replaced with matplotlib/plotly)
        data_label = QLabel(f"📈 نمودار خطی: {len(labels)} نقطه داده")
        data_label.setStyleSheet("font-size: 12px; color: #666; padding: 10px;")
        self.chart_layout.addWidget(data_label)
        
        # Show legend
        legend_widget = QWidget()
        legend_layout = QVBoxLayout()
        
        for dataset in datasets:
            color = dataset.get('color', '#F7941D')
            label = dataset.get('label', 'داده')
            data = dataset.get('data', [])
            
            legend_item = QLabel(f"● {label}: {len(data)} مقدار")
            legend_item.setStyleSheet(f"font-size: 11px; color: {color}; padding: 5px;")
            legend_layout.addWidget(legend_item)
        
        legend_widget.setLayout(legend_layout)
        self.chart_layout.addWidget(legend_widget)
        self.chart_layout.addStretch()


class BarChartWidget(ChartWidget):
    """Bar chart widget"""
    
    def __init__(self, title: str, parent=None):
        super().__init__(title, parent)
    
    def set_data(self, labels: List[str], values: List[float], colors: List[str] = None):
        """
        Set chart data
        
        Args:
            labels: Bar labels
            values: Bar values
            colors: Optional bar colors
        """
        # Clear existing content
        for i in reversed(range(self.chart_layout.count())): 
            self.chart_layout.itemAt(i).widget().setParent(None)
        
        if not colors:
            colors = ['#F7941D'] * len(labels)
        
        # Simple bar visualization
        for label, value, color in zip(labels, values, colors):
            bar_widget = QWidget()
            bar_layout = QHBoxLayout()
            bar_layout.setContentsMargins(0, 5, 0, 5)
            
            # Label
            label_widget = QLabel(label)
            label_widget.setStyleSheet("font-size: 11px; color: #666; min-width: 100px;")
            bar_layout.addWidget(label_widget)
            
            # Bar
            max_value = max(values) if values else 1
            bar_width = int((value / max_value) * 200) if max_value > 0 else 0
            
            bar = QFrame()
            bar.setFixedHeight(20)
            bar.setFixedWidth(bar_width)
            bar.setStyleSheet(f"background: {color}; border-radius: 3px;")
            bar_layout.addWidget(bar)
            
            # Value
            value_widget = QLabel(f"{value:,.0f}")
            value_widget.setStyleSheet("font-size: 11px; color: #333; font-weight: 500;")
            bar_layout.addWidget(value_widget)
            
            bar_layout.addStretch()
            bar_widget.setLayout(bar_layout)
            self.chart_layout.addWidget(bar_widget)
        
        self.chart_layout.addStretch()


class PieChartWidget(ChartWidget):
    """Pie chart widget"""
    
    def __init__(self, title: str, parent=None):
        super().__init__(title, parent)
    
    def set_data(self, labels: List[str], values: List[float], colors: List[str] = None):
        """
        Set chart data
        
        Args:
            labels: Slice labels
            values: Slice values
            colors: Optional slice colors
        """
        # Clear existing content
        for i in reversed(range(self.chart_layout.count())): 
            self.chart_layout.itemAt(i).widget().setParent(None)
        
        if not colors:
            default_colors = ['#F7941D', '#F5E6D3', '#2D2D2D', '#10B981', '#3B82F6', '#EF4444']
            colors = default_colors[:len(labels)]
        
        total = sum(values) if values else 1
        
        # Center emoji representation
        center_label = QLabel("🥧")
        center_label.setStyleSheet("font-size: 48px; padding: 10px;")
        center_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.chart_layout.addWidget(center_label)
        
        # Legend with percentages
        for label, value, color in zip(labels, values, colors):
            percentage = (value / total * 100) if total > 0 else 0
            
            item_widget = QWidget()
            item_layout = QHBoxLayout()
            item_layout.setContentsMargins(5, 3, 5, 3)
            
            # Color indicator
            color_box = QFrame()
            color_box.setFixedSize(12, 12)
            color_box.setStyleSheet(f"background: {color}; border-radius: 2px;")
            item_layout.addWidget(color_box)
            
            # Label
            label_widget = QLabel(f"{label}: {percentage:.1f}%")
            label_widget.setStyleSheet("font-size: 11px; color: #666;")
            item_layout.addWidget(label_widget)
            
            # Value
            value_widget = QLabel(f"{value:,.0f}")
            value_widget.setStyleSheet("font-size: 11px; color: #333; font-weight: 500;")
            item_layout.addWidget(value_widget)
            
            item_layout.addStretch()
            item_widget.setLayout(item_layout)
            self.chart_layout.addWidget(item_widget)
        
        self.chart_layout.addStretch()


class GaugeWidget(QFrame):
    """Gauge widget for displaying a metric with min/max"""
    
    def __init__(self, title: str, value: float, min_value: float = 0, 
                 max_value: float = 100, unit: str = "%", parent=None):
        super().__init__(parent)
        self.setObjectName("gaugeWidget")
        self.title = title
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.unit = unit
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)
        
        # Title
        title_label = QLabel(self.title)
        title_label.setStyleSheet("font-size: 13px; color: #666; font-weight: 500;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Gauge visualization
        gauge_widget = QWidget()
        gauge_layout = QVBoxLayout()
        
        # Value
        self.value_label = QLabel(f"{self.value:.1f}{self.unit}")
        self.value_label.setStyleSheet("font-size: 36px; font-weight: bold; color: #F7941D;")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gauge_layout.addWidget(self.value_label)
        
        # Progress bar
        progress_container = QWidget()
        progress_layout = QVBoxLayout()
        progress_layout.setContentsMargins(0, 0, 0, 0)
        
        # Background
        bg_bar = QFrame()
        bg_bar.setFixedHeight(8)
        bg_bar.setStyleSheet("background: rgba(200, 200, 200, 0.3); border-radius: 4px;")
        
        # Progress
        percentage = ((self.value - self.min_value) / (self.max_value - self.min_value) * 100) if (self.max_value - self.min_value) > 0 else 0
        percentage = max(0, min(100, percentage))
        
        progress_bar = QFrame()
        progress_bar.setFixedHeight(8)
        progress_bar.setFixedWidth(int(200 * percentage / 100))
        
        # Color based on value
        if percentage < 33:
            color = '#EF4444'
        elif percentage < 66:
            color = '#F59E0B'
        else:
            color = '#10B981'
        
        progress_bar.setStyleSheet(f"background: {color}; border-radius: 4px;")
        
        progress_layout.addWidget(bg_bar)
        progress_container.setLayout(progress_layout)
        gauge_layout.addWidget(progress_container, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Min/Max labels
        range_layout = QHBoxLayout()
        min_label = QLabel(f"{self.min_value}{self.unit}")
        min_label.setStyleSheet("font-size: 10px; color: #999;")
        max_label = QLabel(f"{self.max_value}{self.unit}")
        max_label.setStyleSheet("font-size: 10px; color: #999;")
        range_layout.addWidget(min_label)
        range_layout.addStretch()
        range_layout.addWidget(max_label)
        gauge_layout.addLayout(range_layout)
        
        gauge_widget.setLayout(gauge_layout)
        layout.addWidget(gauge_widget)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Style
        self.setStyleSheet("""
            QFrame#gaugeWidget {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 10px;
                border: 1px solid rgba(200, 200, 200, 0.3);
            }
        """)
    
    def update_value(self, value: float):
        """Update the gauge value"""
        self.value = value
        self.value_label.setText(f"{self.value:.1f}{self.unit}")


class TableWidget(ChartWidget):
    """Table widget for displaying tabular data"""
    
    def __init__(self, title: str, parent=None):
        super().__init__(title, parent)
    
    def set_data(self, headers: List[str], rows: List[List[Any]]):
        """
        Set table data
        
        Args:
            headers: Column headers
            rows: Table rows
        """
        # Clear existing content
        for i in reversed(range(self.chart_layout.count())): 
            self.chart_layout.itemAt(i).widget().setParent(None)
        
        # Table container with scroll
        from PyQt6.QtWidgets import QScrollArea, QTableWidget, QHeaderView, QTableWidgetItem
        
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setRowCount(len(rows))
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        
        # Populate table
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                item = QTableWidgetItem(str(cell))
                table.setItem(i, j, item)
        
        table.setStyleSheet("""
            QTableWidget {
                background: transparent;
                border: none;
                gridline-color: rgba(200, 200, 200, 0.3);
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background: rgba(247, 148, 29, 0.1);
                padding: 8px;
                border: none;
                font-weight: 600;
            }
        """)
        
        self.chart_layout.addWidget(table)
