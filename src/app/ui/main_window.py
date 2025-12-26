"""
Main Window
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QLabel, QPushButton, QMenuBar, QMenu, QStatusBar, QToolBar,
    QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QIcon


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, user_data: dict, parent=None):
        super().__init__(parent)
        self.user_data = user_data
        self.setWindowTitle("Analysis Dashboard - داشبورد مدیریتی آنالیز")
        self.setMinimumSize(1200, 800)
        
        # Auto-refresh timer (60 seconds)
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.auto_refresh)
        self.refresh_timer.start(60000)  # 60 seconds
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Set RTL layout
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Central widget
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Header section
        header_layout = QHBoxLayout()
        
        # Welcome message
        welcome_label = QLabel(f"خوش آمدید، {self.user_data.get('username', 'کاربر')} ({self.user_data.get('role', '')})")
        welcome_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        header_layout.addWidget(welcome_label)
        
        header_layout.addStretch()
        
        # Refresh button
        refresh_button = QPushButton("🔄 بروزرسانی")
        refresh_button.clicked.connect(self.manual_refresh)
        header_layout.addWidget(refresh_button)
        
        main_layout.addLayout(header_layout)
        
        # Tab widget for different dashboards
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        
        # Add dashboard tabs
        self.add_dashboard_tabs()
        
        main_layout.addWidget(self.tab_widget)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Status bar
        self.create_status_bar()
    
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("فایل")
        
        new_dashboard_action = QAction("داشبورد جدید", self)
        new_dashboard_action.triggered.connect(self.create_new_dashboard)
        file_menu.addAction(new_dashboard_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("خروج", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("نمایش")
        
        toggle_theme_action = QAction("تغییر پوسته", self)
        toggle_theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(toggle_theme_action)
        
        kiosk_mode_action = QAction("حالت نمایش (Kiosk)", self)
        kiosk_mode_action.triggered.connect(self.toggle_kiosk_mode)
        view_menu.addAction(kiosk_mode_action)
        
        # Data menu
        data_menu = menubar.addMenu("داده‌ها")
        
        connect_ga_action = QAction("اتصال به Google Analytics", self)
        connect_ga_action.triggered.connect(self.connect_google_analytics)
        data_menu.addAction(connect_ga_action)
        
        connect_clarity_action = QAction("اتصال به Microsoft Clarity", self)
        connect_clarity_action.triggered.connect(self.connect_clarity)
        data_menu.addAction(connect_clarity_action)
        
        # Reports menu
        reports_menu = menubar.addMenu("گزارش‌ها")
        
        generate_report_action = QAction("تولید گزارش", self)
        generate_report_action.triggered.connect(self.generate_report)
        reports_menu.addAction(generate_report_action)
        
        schedule_report_action = QAction("زمان‌بندی گزارش", self)
        schedule_report_action.triggered.connect(self.schedule_report)
        reports_menu.addAction(schedule_report_action)
        
        # Alerts menu
        alerts_menu = menubar.addMenu("هشدارها")
        
        create_alert_action = QAction("ایجاد هشدار", self)
        create_alert_action.triggered.connect(self.create_alert)
        alerts_menu.addAction(create_alert_action)
        
        view_alerts_action = QAction("مشاهده هشدارها", self)
        view_alerts_action.triggered.connect(self.view_alerts)
        alerts_menu.addAction(view_alerts_action)
        
        # Settings menu
        settings_menu = menubar.addMenu("تنظیمات")
        
        general_settings_action = QAction("تنظیمات عمومی", self)
        general_settings_action.triggered.connect(self.open_general_settings)
        settings_menu.addAction(general_settings_action)
        
        user_management_action = QAction("مدیریت کاربران", self)
        user_management_action.triggered.connect(self.open_user_management)
        settings_menu.addAction(user_management_action)
        
        # Help menu
        help_menu = menubar.addMenu("راهنما")
        
        about_action = QAction("درباره", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """Create toolbar"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)
        
        # Add toolbar actions
        toolbar.addAction("📊 داشبورد", self.show_dashboard)
        toolbar.addSeparator()
        toolbar.addAction("📈 گزارش‌ها", self.generate_report)
        toolbar.addSeparator()
        toolbar.addAction("⚙️ تنظیمات", self.open_general_settings)
    
    def create_status_bar(self):
        """Create status bar"""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        
        # Connection status
        self.connection_label = QLabel("🟢 متصل")
        status_bar.addPermanentWidget(self.connection_label)
        
        # Last update time
        self.update_label = QLabel("آخرین بروزرسانی: --")
        status_bar.addPermanentWidget(self.update_label)
        
        status_bar.showMessage("آماده")
    
    def add_dashboard_tabs(self):
        """Add dashboard tabs"""
        # Performance Overview
        performance_widget = QWidget()
        performance_layout = QVBoxLayout()
        performance_layout.addWidget(QLabel("بررسی عملکرد"))
        performance_layout.addStretch()
        performance_widget.setLayout(performance_layout)
        self.tab_widget.addTab(performance_widget, "بررسی عملکرد")
        
        # User Behavior
        behavior_widget = QWidget()
        behavior_layout = QVBoxLayout()
        behavior_layout.addWidget(QLabel("رفتار کاربران"))
        behavior_layout.addStretch()
        behavior_widget.setLayout(behavior_layout)
        self.tab_widget.addTab(behavior_widget, "رفتار کاربران")
        
        # Product Sales
        sales_widget = QWidget()
        sales_layout = QVBoxLayout()
        sales_layout.addWidget(QLabel("فروش محصولات"))
        sales_layout.addStretch()
        sales_widget.setLayout(sales_layout)
        self.tab_widget.addTab(sales_widget, "فروش محصولات")
        
        # Campaign Metrics
        campaign_widget = QWidget()
        campaign_layout = QVBoxLayout()
        campaign_layout.addWidget(QLabel("معیارهای کمپین"))
        campaign_layout.addStretch()
        campaign_widget.setLayout(campaign_layout)
        self.tab_widget.addTab(campaign_widget, "معیارهای کمپین")
        
        # Tech Performance
        tech_widget = QWidget()
        tech_layout = QVBoxLayout()
        tech_layout.addWidget(QLabel("عملکرد فنی"))
        tech_layout.addStretch()
        tech_widget.setLayout(tech_layout)
        self.tab_widget.addTab(tech_widget, "عملکرد فنی")
    
    def auto_refresh(self):
        """Auto-refresh data"""
        from datetime import datetime
        self.update_label.setText(f"آخرین بروزرسانی: {datetime.now().strftime('%H:%M:%S')}")
        self.statusBar().showMessage("در حال بروزرسانی داده‌ها...", 2000)
        # TODO: Implement actual data refresh
    
    def manual_refresh(self):
        """Manual refresh"""
        self.auto_refresh()
    
    def create_new_dashboard(self):
        """Create new dashboard"""
        QMessageBox.information(self, "داشبورد جدید", "قابلیت ایجاد داشبورد جدید")
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        QMessageBox.information(self, "تغییر پوسته", "تغییر بین پوسته روشن و تیره")
    
    def toggle_kiosk_mode(self):
        """Toggle kiosk/presentation mode"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    
    def connect_google_analytics(self):
        """Connect to Google Analytics"""
        QMessageBox.information(self, "Google Analytics", "اتصال به Google Analytics 4")
    
    def connect_clarity(self):
        """Connect to Microsoft Clarity"""
        QMessageBox.information(self, "Microsoft Clarity", "اتصال به Microsoft Clarity")
    
    def generate_report(self):
        """Generate report"""
        QMessageBox.information(self, "گزارش", "تولید گزارش")
    
    def schedule_report(self):
        """Schedule report"""
        QMessageBox.information(self, "زمان‌بندی گزارش", "زمان‌بندی گزارش خودکار")
    
    def create_alert(self):
        """Create alert"""
        QMessageBox.information(self, "هشدار", "ایجاد هشدار جدید")
    
    def view_alerts(self):
        """View alerts"""
        QMessageBox.information(self, "هشدارها", "مشاهده همه هشدارها")
    
    def open_general_settings(self):
        """Open general settings"""
        QMessageBox.information(self, "تنظیمات", "تنظیمات عمومی")
    
    def open_user_management(self):
        """Open user management"""
        QMessageBox.information(self, "مدیریت کاربران", "مدیریت کاربران و دسترسی‌ها")
    
    def show_dashboard(self):
        """Show dashboard"""
        self.tab_widget.setCurrentIndex(0)
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "درباره",
            "داشبورد مدیریتی آنالیز\n\n"
            "نسخه: 1.0.0\n"
            "توسعه‌دهنده: تیم فنی زاگرس پرو\n\n"
            "یک نرمافزار دسکتاپی پایتونی (PyQt6) برای داشبورد BI مدیریتی"
        )
    
    def closeEvent(self, event):
        """Handle window close event"""
        reply = QMessageBox.question(
            self,
            "خروج",
            "آیا مطمئن هستید که می‌خواهید خارج شوید؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
