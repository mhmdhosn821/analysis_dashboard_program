"""
Performance Overview Dashboard
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QScrollArea, QPushButton, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from datetime import datetime, timedelta
from app.ui.widgets.cards import MetricCard, StatCard, InfoCard
from app.ui.widgets.charts import LineChartWidget, BarChartWidget, PieChartWidget
from app.utils.helpers import format_number, format_percentage, calculate_percentage_change


class PerformanceDashboard(QWidget):
    """Performance overview dashboard"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Setup the UI"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("📊 بررسی عملکرد")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2D2D2D;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Refresh button
        refresh_btn = QPushButton("🔄 به‌روزرسانی")
        refresh_btn.clicked.connect(self.load_data)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: #F7941D;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #E8840D;
            }
        """)
        header_layout.addWidget(refresh_btn)
        
        main_layout.addLayout(header_layout)
        
        # Scroll area for dashboard content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        scroll_content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(20)
        
        # Key metrics grid
        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(15)
        
        self.active_users_card = MetricCard("کاربران فعال", "0", "👥")
        self.new_users_card = MetricCard("کاربران جدید", "0", "✨")
        self.pageviews_card = MetricCard("بازدیدها", "0", "👁")
        self.engagement_card = MetricCard("نرخ تعامل", "0%", "🎯")
        
        metrics_grid.addWidget(self.active_users_card, 0, 0)
        metrics_grid.addWidget(self.new_users_card, 0, 1)
        metrics_grid.addWidget(self.pageviews_card, 0, 2)
        metrics_grid.addWidget(self.engagement_card, 0, 3)
        
        content_layout.addLayout(metrics_grid)
        
        # Stats with trends
        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)
        
        self.bounce_rate_card = StatCard("نرخ پرش", "0%", "", "down")
        self.avg_session_card = StatCard("میانگین مدت حضور", "0 دقیقه", "", "up")
        self.sessions_card = StatCard("جلسات", "0", "", "up")
        self.conversion_card = StatCard("نرخ تبدیل", "0%", "", "up")
        
        stats_grid.addWidget(self.bounce_rate_card, 0, 0)
        stats_grid.addWidget(self.avg_session_card, 0, 1)
        stats_grid.addWidget(self.sessions_card, 0, 2)
        stats_grid.addWidget(self.conversion_card, 0, 3)
        
        content_layout.addLayout(stats_grid)
        
        # Charts
        charts_layout = QGridLayout()
        charts_layout.setSpacing(15)
        
        # Traffic trend chart
        self.traffic_chart = LineChartWidget("روند ترافیک")
        charts_layout.addWidget(self.traffic_chart, 0, 0, 1, 2)
        
        # Top cities chart
        self.cities_chart = BarChartWidget("شهرهای برتر")
        charts_layout.addWidget(self.cities_chart, 1, 0)
        
        # Device distribution chart
        self.devices_chart = PieChartWidget("توزیع دستگاه‌ها")
        charts_layout.addWidget(self.devices_chart, 1, 1)
        
        content_layout.addLayout(charts_layout)
        
        # Additional info
        info_grid = QGridLayout()
        info_grid.setSpacing(15)
        
        self.user_info_card = InfoCard("اطلاعات کاربران", [
            ("کاربران جدید", "0"),
            ("کاربران بازگشتی", "0"),
            ("نرخ بازگشت", "0%")
        ])
        
        self.tech_info_card = InfoCard("اطلاعات فنی", [
            ("میانگین سرعت بارگذاری", "0s"),
            ("نرخ Crash", "0%"),
            ("خطاهای JS", "0")
        ])
        
        info_grid.addWidget(self.user_info_card, 0, 0)
        info_grid.addWidget(self.tech_info_card, 0, 1)
        
        content_layout.addLayout(info_grid)
        
        scroll_content.setLayout(content_layout)
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        
        self.setLayout(main_layout)
    
    def load_data(self):
        """Load dashboard data"""
        # Generate mock data for demonstration
        import random
        
        # Update metric cards
        active_users = random.randint(1000, 5000)
        new_users = random.randint(100, 500)
        pageviews = random.randint(10000, 50000)
        engagement_rate = random.uniform(40, 80)
        
        self.active_users_card.update_value(format_number(active_users))
        self.active_users_card.update_subtitle(f"+{random.randint(5, 20)}% از دیروز")
        
        self.new_users_card.update_value(format_number(new_users))
        self.new_users_card.update_subtitle(f"+{random.randint(10, 30)}% از دیروز")
        
        self.pageviews_card.update_value(format_number(pageviews))
        self.pageviews_card.update_subtitle(f"+{random.randint(5, 15)}% از دیروز")
        
        self.engagement_card.update_value(format_percentage(engagement_rate))
        self.engagement_card.update_subtitle(f"+{random.randint(2, 10)}% از دیروز")
        
        # Update stat cards
        bounce_rate = random.uniform(30, 50)
        avg_session = random.randint(2, 10)
        sessions = random.randint(5000, 20000)
        conversion = random.uniform(2, 8)
        
        prev_bounce = bounce_rate + random.uniform(-5, 5)
        self.bounce_rate_card.update_values(
            format_percentage(bounce_rate),
            format_percentage(abs(bounce_rate - prev_bounce)),
            "down" if bounce_rate < prev_bounce else "up"
        )
        
        self.avg_session_card.update_values(
            f"{avg_session} دقیقه",
            f"+{random.randint(1, 3)} دقیقه",
            "up"
        )
        
        self.sessions_card.update_values(
            format_number(sessions),
            f"+{random.randint(5, 15)}%",
            "up"
        )
        
        self.conversion_card.update_values(
            format_percentage(conversion),
            f"+{random.uniform(0.5, 2):.1f}%",
            "up"
        )
        
        # Update charts
        # Traffic trend
        days = 7
        labels = [(datetime.now() - timedelta(days=i)).strftime("%m/%d") for i in range(days-1, -1, -1)]
        traffic_data = [random.randint(1000, 5000) for _ in range(days)]
        
        self.traffic_chart.set_data(labels, [
            {'label': 'کاربران', 'data': traffic_data, 'color': '#F7941D'}
        ])
        
        # Top cities
        cities = ['تهران', 'اصفهان', 'مشهد', 'شیراز', 'تبریز']
        city_values = [random.randint(100, 1000) for _ in cities]
        self.cities_chart.set_data(cities, city_values)
        
        # Device distribution
        devices = ['موبایل', 'دسکتاپ', 'تبلت']
        device_values = [random.randint(100, 1000) for _ in devices]
        self.devices_chart.set_data(devices, device_values)
        
        # Update info cards
        returning_users = active_users - new_users
        return_rate = (returning_users / active_users * 100) if active_users > 0 else 0
        
        self.user_info_card.update_item("کاربران جدید", format_number(new_users))
        self.user_info_card.update_item("کاربران بازگشتی", format_number(returning_users))
        self.user_info_card.update_item("نرخ بازگشت", format_percentage(return_rate))
        
        load_time = random.uniform(1.5, 4.0)
        crash_rate = random.uniform(0.1, 2.0)
        js_errors = random.randint(0, 50)
        
        self.tech_info_card.update_item("میانگین سرعت بارگذاری", f"{load_time:.1f}s")
        self.tech_info_card.update_item("نرخ Crash", format_percentage(crash_rate))
        self.tech_info_card.update_item("خطاهای JS", str(js_errors))
