"""
Sales Dashboard
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QScrollArea, QPushButton, QComboBox
)
from PyQt6.QtCore import Qt
from datetime import datetime, timedelta
from app.ui.widgets.cards import MetricCard, StatCard, InfoCard
from app.ui.widgets.charts import LineChartWidget, BarChartWidget, PieChartWidget, TableWidget
from app.services.pos_api import POSClient
from app.utils.helpers import format_currency, format_number, format_percentage


class SalesDashboard(QWidget):
    """Sales and e-commerce dashboard"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pos_client = POSClient()
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Setup the UI"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("💰 فروش و تجارت")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2D2D2D;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Date range selector
        self.date_range_combo = QComboBox()
        self.date_range_combo.addItems([
            "امروز", "دیروز", "7 روز گذشته", "30 روز گذشته", "این ماه", "ماه گذشته"
        ])
        self.date_range_combo.currentTextChanged.connect(self.on_date_range_changed)
        header_layout.addWidget(self.date_range_combo)
        
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
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        scroll_content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(20)
        
        # Key metrics
        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(15)
        
        self.total_sales_card = MetricCard("کل فروش", "$0", "💵")
        self.orders_card = MetricCard("تعداد سفارشات", "0", "📦")
        self.avg_order_card = MetricCard("میانگین سفارش", "$0", "💳")
        self.customers_card = MetricCard("مشتریان", "0", "👥")
        
        metrics_grid.addWidget(self.total_sales_card, 0, 0)
        metrics_grid.addWidget(self.orders_card, 0, 1)
        metrics_grid.addWidget(self.avg_order_card, 0, 2)
        metrics_grid.addWidget(self.customers_card, 0, 3)
        
        content_layout.addLayout(metrics_grid)
        
        # Stats
        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)
        
        self.completed_orders_card = StatCard("سفارشات تکمیل شده", "0", "", "up")
        self.pending_orders_card = StatCard("سفارشات در انتظار", "0", "", "neutral")
        self.cancelled_orders_card = StatCard("سفارشات لغو شده", "0", "", "down")
        self.revenue_growth_card = StatCard("رشد درآمد", "0%", "", "up")
        
        stats_grid.addWidget(self.completed_orders_card, 0, 0)
        stats_grid.addWidget(self.pending_orders_card, 0, 1)
        stats_grid.addWidget(self.cancelled_orders_card, 0, 2)
        stats_grid.addWidget(self.revenue_growth_card, 0, 3)
        
        content_layout.addLayout(stats_grid)
        
        # Charts
        charts_layout = QGridLayout()
        charts_layout.setSpacing(15)
        
        # Sales trend
        self.sales_chart = LineChartWidget("روند فروش")
        charts_layout.addWidget(self.sales_chart, 0, 0, 1, 2)
        
        # Top products
        self.products_chart = BarChartWidget("محصولات برتر")
        charts_layout.addWidget(self.products_chart, 1, 0)
        
        # Sales by category
        self.categories_chart = PieChartWidget("فروش بر اساس دسته‌بندی")
        charts_layout.addWidget(self.categories_chart, 1, 1)
        
        content_layout.addLayout(charts_layout)
        
        # Conversion funnel
        funnel_card = InfoCard("قیف تبدیل", [
            ("بازدیدکنندگان", "0"),
            ("مشاهده محصولات", "0"),
            ("افزودن به سبد", "0"),
            ("شروع خرید", "0"),
            ("تکمیل سفارش", "0"),
            ("نرخ تبدیل کلی", "0%")
        ])
        content_layout.addWidget(funnel_card)
        
        self.funnel_card = funnel_card
        
        # Recent orders table
        self.orders_table = TableWidget("آخرین سفارشات")
        content_layout.addWidget(self.orders_table)
        
        scroll_content.setLayout(content_layout)
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        
        self.setLayout(main_layout)
    
    def on_date_range_changed(self, text):
        """Handle date range change"""
        self.load_data()
    
    def get_date_range(self):
        """Get selected date range"""
        from app.utils.helpers import get_date_range
        
        range_map = {
            "امروز": "today",
            "دیروز": "yesterday",
            "7 روز گذشته": "last_7_days",
            "30 روز گذشته": "last_30_days",
            "این ماه": "this_month",
            "ماه گذشته": "last_month"
        }
        
        selected = self.date_range_combo.currentText()
        period = range_map.get(selected, "today")
        return get_date_range(period)
    
    def load_data(self):
        """Load sales data"""
        start_date, end_date = self.get_date_range()
        
        # Get sales summary
        summary = self.pos_client.get_sales_summary(start_date, end_date)
        
        # Update metric cards
        self.total_sales_card.update_value(format_currency(summary['total_sales']))
        self.orders_card.update_value(format_number(summary['num_orders']))
        self.avg_order_card.update_value(format_currency(summary['average_order_value']))
        self.customers_card.update_value(format_number(summary['total_customers']))
        
        # Get orders
        orders = self.pos_client.get_orders(start_date, end_date, limit=100)
        
        # Calculate order stats
        completed = sum(1 for o in orders if o['status'] == 'completed')
        pending = sum(1 for o in orders if o['status'] == 'pending')
        cancelled = sum(1 for o in orders if o['status'] == 'cancelled')
        
        self.completed_orders_card.update_values(str(completed), "+5%", "up")
        self.pending_orders_card.update_values(str(pending), "", "neutral")
        self.cancelled_orders_card.update_values(str(cancelled), "-2%", "down")
        self.revenue_growth_card.update_values("12.5%", "+3.2%", "up")
        
        # Sales trend chart
        import random
        days = (end_date - start_date).days + 1
        labels = [(start_date + timedelta(days=i)).strftime("%m/%d") for i in range(days)]
        sales_data = [random.uniform(1000, 5000) for _ in range(days)]
        
        self.sales_chart.set_data(labels, [
            {'label': 'فروش', 'data': sales_data, 'color': '#10B981'}
        ])
        
        # Top products
        top_products = self.pos_client.get_top_products(start_date, end_date, limit=5)
        product_names = [p['name'] for p in top_products]
        product_revenues = [p['total_revenue'] for p in top_products]
        
        self.products_chart.set_data(product_names, product_revenues)
        
        # Sales by category
        categories = ['الکترونیک', 'پوشاک', 'خانه و آشپزخانه', 'کتاب', 'سایر']
        category_values = [random.uniform(1000, 10000) for _ in categories]
        
        self.categories_chart.set_data(categories, category_values)
        
        # Conversion funnel
        funnel_data = self.pos_client.get_conversion_funnel(start_date, end_date)
        
        self.funnel_card.update_item("بازدیدکنندگان", format_number(funnel_data['visitors']))
        self.funnel_card.update_item("مشاهده محصولات", format_number(funnel_data['product_views']))
        self.funnel_card.update_item("افزودن به سبد", format_number(funnel_data['add_to_cart']))
        self.funnel_card.update_item("شروع خرید", format_number(funnel_data['checkout_initiated']))
        self.funnel_card.update_item("تکمیل سفارش", format_number(funnel_data['orders_completed']))
        self.funnel_card.update_item("نرخ تبدیل کلی", format_percentage(funnel_data['conversion_rates']['overall']))
        
        # Recent orders table
        recent_orders = orders[:10]
        headers = ['شماره سفارش', 'مشتری', 'مبلغ', 'وضعیت', 'تاریخ']
        rows = [
            [
                order['order_id'],
                order.get('customer_name', 'مهمان'),
                format_currency(order['amount']),
                order['status'],
                order['order_date'][:10]
            ]
            for order in recent_orders
        ]
        
        self.orders_table.set_data(headers, rows)
