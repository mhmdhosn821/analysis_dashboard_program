"""
Settings Interface
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QLineEdit, QComboBox, QCheckBox, QGroupBox,
    QScrollArea, QTabWidget, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from app.core.config import config
from app.core.db_manager import db_manager


class SettingsPanel(QWidget):
    """Settings panel"""
    
    settings_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Setup the UI"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("⚙️ تنظیمات")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2D2D2D;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Save button
        save_btn = QPushButton("💾 ذخیره تنظیمات")
        save_btn.clicked.connect(self.save_settings)
        save_btn.setStyleSheet("""
            QPushButton {
                background: #10B981;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #059669;
            }
        """)
        header_layout.addWidget(save_btn)
        
        main_layout.addLayout(header_layout)
        
        # Tabs
        tabs = QTabWidget()
        
        # General tab
        general_tab = self.create_general_tab()
        tabs.addTab(general_tab, "عمومی")
        
        # API Keys tab
        api_tab = self.create_api_tab()
        tabs.addTab(api_tab, "کلیدهای API")
        
        # Alerts tab
        alerts_tab = self.create_alerts_tab()
        tabs.addTab(alerts_tab, "هشدارها")
        
        # Notifications tab
        notifications_tab = self.create_notifications_tab()
        tabs.addTab(notifications_tab, "اطلاع‌رسانی")
        
        main_layout.addWidget(tabs)
        self.setLayout(main_layout)
    
    def create_general_tab(self):
        """Create general settings tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        scroll_content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(20)
        
        # Application settings group
        app_group = QGroupBox("تنظیمات برنامه")
        app_layout = QGridLayout()
        app_layout.setSpacing(15)
        
        # Language
        app_layout.addWidget(QLabel("زبان:"), 0, 0)
        self.language_combo = QComboBox()
        self.language_combo.addItems(["فارسی (fa)", "English (en)"])
        app_layout.addWidget(self.language_combo, 0, 1)
        
        # Theme
        app_layout.addWidget(QLabel("تم:"), 1, 0)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["روشن", "تاریک"])
        app_layout.addWidget(self.theme_combo, 1, 1)
        
        # Auto refresh
        app_layout.addWidget(QLabel("به‌روزرسانی خودکار:"), 2, 0)
        self.refresh_combo = QComboBox()
        self.refresh_combo.addItems(["30 ثانیه", "60 ثانیه", "5 دقیقه", "10 دقیقه", "خاموش"])
        app_layout.addWidget(self.refresh_combo, 2, 1)
        
        # 2FA
        app_layout.addWidget(QLabel("احراز هویت دو مرحله‌ای:"), 3, 0)
        self.twofa_check = QCheckBox("فعال")
        app_layout.addWidget(self.twofa_check, 3, 1)
        
        app_group.setLayout(app_layout)
        content_layout.addWidget(app_group)
        
        # Display settings group
        display_group = QGroupBox("تنظیمات نمایش")
        display_layout = QGridLayout()
        display_layout.setSpacing(15)
        
        # Currency
        display_layout.addWidget(QLabel("واحد پول:"), 0, 0)
        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["دلار ($)", "یورو (€)", "ریال (﷼)", "تومان"])
        display_layout.addWidget(self.currency_combo, 0, 1)
        
        # Date format
        display_layout.addWidget(QLabel("فرمت تاریخ:"), 1, 0)
        self.date_format_combo = QComboBox()
        self.date_format_combo.addItems(["YYYY-MM-DD", "DD/MM/YYYY", "MM/DD/YYYY"])
        display_layout.addWidget(self.date_format_combo, 1, 1)
        
        # Timezone
        display_layout.addWidget(QLabel("منطقه زمانی:"), 2, 0)
        self.timezone_combo = QComboBox()
        self.timezone_combo.addItems(["UTC", "Asia/Tehran", "Europe/London", "America/New_York"])
        display_layout.addWidget(self.timezone_combo, 2, 1)
        
        display_group.setLayout(display_layout)
        content_layout.addWidget(display_group)
        
        content_layout.addStretch()
        scroll_content.setLayout(content_layout)
        scroll.setWidget(scroll_content)
        
        layout.addWidget(scroll)
        widget.setLayout(layout)
        return widget
    
    def create_api_tab(self):
        """Create API keys tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        scroll_content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(20)
        
        # Google Analytics group
        ga_group = QGroupBox("Google Analytics 4")
        ga_layout = QGridLayout()
        ga_layout.setSpacing(15)
        
        ga_layout.addWidget(QLabel("Client ID:"), 0, 0)
        self.ga_client_id = QLineEdit()
        self.ga_client_id.setPlaceholderText("Google Analytics Client ID")
        ga_layout.addWidget(self.ga_client_id, 0, 1)
        
        ga_layout.addWidget(QLabel("Client Secret:"), 1, 0)
        self.ga_client_secret = QLineEdit()
        self.ga_client_secret.setPlaceholderText("Google Analytics Client Secret")
        self.ga_client_secret.setEchoMode(QLineEdit.EchoMode.Password)
        ga_layout.addWidget(self.ga_client_secret, 1, 1)
        
        ga_layout.addWidget(QLabel("Property IDs:"), 2, 0)
        self.ga_property_ids = QLineEdit()
        self.ga_property_ids.setPlaceholderText("Property IDs (جدا شده با کاما)")
        ga_layout.addWidget(self.ga_property_ids, 2, 1)
        
        ga_group.setLayout(ga_layout)
        content_layout.addWidget(ga_group)
        
        # Microsoft Clarity group
        clarity_group = QGroupBox("Microsoft Clarity")
        clarity_layout = QGridLayout()
        clarity_layout.setSpacing(15)
        
        clarity_layout.addWidget(QLabel("API Key:"), 0, 0)
        self.clarity_api_key = QLineEdit()
        self.clarity_api_key.setPlaceholderText("Clarity API Key")
        self.clarity_api_key.setEchoMode(QLineEdit.EchoMode.Password)
        clarity_layout.addWidget(self.clarity_api_key, 0, 1)
        
        clarity_layout.addWidget(QLabel("Project IDs:"), 1, 0)
        self.clarity_project_ids = QLineEdit()
        self.clarity_project_ids.setPlaceholderText("Project IDs (جدا شده با کاما)")
        clarity_layout.addWidget(self.clarity_project_ids, 1, 1)
        
        clarity_group.setLayout(clarity_layout)
        content_layout.addWidget(clarity_group)
        
        # AI Services group
        ai_group = QGroupBox("خدمات هوش مصنوعی")
        ai_layout = QGridLayout()
        ai_layout.setSpacing(15)
        
        ai_layout.addWidget(QLabel("OpenAI API Key:"), 0, 0)
        self.openai_key = QLineEdit()
        self.openai_key.setPlaceholderText("OpenAI API Key")
        self.openai_key.setEchoMode(QLineEdit.EchoMode.Password)
        ai_layout.addWidget(self.openai_key, 0, 1)
        
        ai_layout.addWidget(QLabel("Google Gemini API Key:"), 1, 0)
        self.gemini_key = QLineEdit()
        self.gemini_key.setPlaceholderText("Gemini API Key")
        self.gemini_key.setEchoMode(QLineEdit.EchoMode.Password)
        ai_layout.addWidget(self.gemini_key, 1, 1)
        
        ai_layout.addWidget(QLabel("Anthropic Claude API Key:"), 2, 0)
        self.claude_key = QLineEdit()
        self.claude_key.setPlaceholderText("Claude API Key")
        self.claude_key.setEchoMode(QLineEdit.EchoMode.Password)
        ai_layout.addWidget(self.claude_key, 2, 1)
        
        ai_layout.addWidget(QLabel("ارائه‌دهنده پیش‌فرض:"), 3, 0)
        self.ai_provider_combo = QComboBox()
        self.ai_provider_combo.addItems(["OpenAI", "Gemini", "Claude"])
        ai_layout.addWidget(self.ai_provider_combo, 3, 1)
        
        ai_group.setLayout(ai_layout)
        content_layout.addWidget(ai_group)
        
        content_layout.addStretch()
        scroll_content.setLayout(content_layout)
        scroll.setWidget(scroll_content)
        
        layout.addWidget(scroll)
        widget.setLayout(layout)
        return widget
    
    def create_alerts_tab(self):
        """Create alerts settings tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        scroll_content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(20)
        
        # Alert thresholds group
        thresholds_group = QGroupBox("آستانه‌های هشدار")
        thresholds_layout = QGridLayout()
        thresholds_layout.setSpacing(15)
        
        thresholds_layout.addWidget(QLabel("افت ترافیک (%):"), 0, 0)
        self.traffic_drop_threshold = QLineEdit()
        self.traffic_drop_threshold.setPlaceholderText("50")
        thresholds_layout.addWidget(self.traffic_drop_threshold, 0, 1)
        
        thresholds_layout.addWidget(QLabel("افزایش خطاها (%):"), 1, 0)
        self.error_increase_threshold = QLineEdit()
        self.error_increase_threshold.setPlaceholderText("50")
        thresholds_layout.addWidget(self.error_increase_threshold, 1, 1)
        
        thresholds_layout.addWidget(QLabel("کاهش فروش (%):"), 2, 0)
        self.sales_drop_threshold = QLineEdit()
        self.sales_drop_threshold.setPlaceholderText("50")
        thresholds_layout.addWidget(self.sales_drop_threshold, 2, 1)
        
        thresholds_group.setLayout(thresholds_layout)
        content_layout.addWidget(thresholds_group)
        
        content_layout.addStretch()
        scroll_content.setLayout(content_layout)
        scroll.setWidget(scroll_content)
        
        layout.addWidget(scroll)
        widget.setLayout(layout)
        return widget
    
    def create_notifications_tab(self):
        """Create notifications settings tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        scroll_content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(20)
        
        # Email group
        email_group = QGroupBox("ایمیل")
        email_layout = QGridLayout()
        email_layout.setSpacing(15)
        
        self.email_enabled = QCheckBox("فعال")
        email_layout.addWidget(self.email_enabled, 0, 0, 1, 2)
        
        email_layout.addWidget(QLabel("SMTP Host:"), 1, 0)
        self.smtp_host = QLineEdit()
        email_layout.addWidget(self.smtp_host, 1, 1)
        
        email_layout.addWidget(QLabel("SMTP Port:"), 2, 0)
        self.smtp_port = QLineEdit()
        email_layout.addWidget(self.smtp_port, 2, 1)
        
        email_layout.addWidget(QLabel("Username:"), 3, 0)
        self.email_username = QLineEdit()
        email_layout.addWidget(self.email_username, 3, 1)
        
        email_layout.addWidget(QLabel("Password:"), 4, 0)
        self.email_password = QLineEdit()
        self.email_password.setEchoMode(QLineEdit.EchoMode.Password)
        email_layout.addWidget(self.email_password, 4, 1)
        
        email_group.setLayout(email_layout)
        content_layout.addWidget(email_group)
        
        # Telegram group
        telegram_group = QGroupBox("تلگرام")
        telegram_layout = QGridLayout()
        telegram_layout.setSpacing(15)
        
        self.telegram_enabled = QCheckBox("فعال")
        telegram_layout.addWidget(self.telegram_enabled, 0, 0, 1, 2)
        
        telegram_layout.addWidget(QLabel("Bot Token:"), 1, 0)
        self.telegram_token = QLineEdit()
        self.telegram_token.setEchoMode(QLineEdit.EchoMode.Password)
        telegram_layout.addWidget(self.telegram_token, 1, 1)
        
        telegram_layout.addWidget(QLabel("Chat ID:"), 2, 0)
        self.telegram_chat_id = QLineEdit()
        telegram_layout.addWidget(self.telegram_chat_id, 2, 1)
        
        telegram_group.setLayout(telegram_layout)
        content_layout.addWidget(telegram_group)
        
        # Slack group
        slack_group = QGroupBox("Slack")
        slack_layout = QGridLayout()
        slack_layout.setSpacing(15)
        
        self.slack_enabled = QCheckBox("فعال")
        slack_layout.addWidget(self.slack_enabled, 0, 0, 1, 2)
        
        slack_layout.addWidget(QLabel("Webhook URL:"), 1, 0)
        self.slack_webhook = QLineEdit()
        slack_layout.addWidget(self.slack_webhook, 1, 1)
        
        slack_group.setLayout(slack_layout)
        content_layout.addWidget(slack_group)
        
        content_layout.addStretch()
        scroll_content.setLayout(content_layout)
        scroll.setWidget(scroll_content)
        
        layout.addWidget(scroll)
        widget.setLayout(layout)
        return widget
    
    def load_settings(self):
        """Load current settings"""
        # Load from config
        # General
        lang_index = 0 if config.app.language == 'fa' else 1
        self.language_combo.setCurrentIndex(lang_index)
        
        theme_index = 0 if config.app.theme == 'light' else 1
        self.theme_combo.setCurrentIndex(theme_index)
        
        self.twofa_check.setChecked(config.app.enable_2fa)
        
        # API Keys
        self.ga_client_id.setText(config.google_analytics.client_id)
        self.ga_client_secret.setText(config.google_analytics.client_secret)
        self.ga_property_ids.setText(','.join(config.google_analytics.property_ids))
        
        self.clarity_api_key.setText(config.clarity.api_key)
        self.clarity_project_ids.setText(','.join(config.clarity.project_ids))
        
        self.openai_key.setText(config.ai.openai_api_key)
        self.gemini_key.setText(config.ai.gemini_api_key)
        self.claude_key.setText(config.ai.claude_api_key)
        
        # Alert thresholds
        self.traffic_drop_threshold.setText(str(config.thresholds.traffic_drop_percent))
        self.error_increase_threshold.setText(str(config.thresholds.crash_rate_increase_percent))
        self.sales_drop_threshold.setText(str(config.thresholds.sales_drop_percent))
        
        # Notifications
        self.email_enabled.setChecked(config.notification.email_enabled)
        self.smtp_host.setText(config.notification.email_smtp_host)
        self.smtp_port.setText(str(config.notification.email_smtp_port))
        self.email_username.setText(config.notification.email_username)
        self.email_password.setText(config.notification.email_password)
        
        self.telegram_enabled.setChecked(config.notification.telegram_enabled)
        self.telegram_token.setText(config.notification.telegram_bot_token)
        self.telegram_chat_id.setText(config.notification.telegram_chat_id)
        
        self.slack_enabled.setChecked(config.notification.slack_enabled)
        self.slack_webhook.setText(config.notification.slack_webhook_url)
    
    def save_settings(self):
        """Save settings"""
        try:
            # Update config
            # General
            config.app.language = 'fa' if self.language_combo.currentIndex() == 0 else 'en'
            config.app.theme = 'light' if self.theme_combo.currentIndex() == 0 else 'dark'
            config.app.enable_2fa = self.twofa_check.isChecked()
            
            # API Keys
            config.google_analytics.client_id = self.ga_client_id.text()
            config.google_analytics.client_secret = self.ga_client_secret.text()
            config.google_analytics.property_ids = [
                pid.strip() for pid in self.ga_property_ids.text().split(',') if pid.strip()
            ]
            
            config.clarity.api_key = self.clarity_api_key.text()
            config.clarity.project_ids = [
                pid.strip() for pid in self.clarity_project_ids.text().split(',') if pid.strip()
            ]
            
            config.ai.openai_api_key = self.openai_key.text()
            config.ai.gemini_api_key = self.gemini_key.text()
            config.ai.claude_api_key = self.claude_key.text()
            
            # Alert thresholds
            config.thresholds.traffic_drop_percent = float(self.traffic_drop_threshold.text() or 50)
            config.thresholds.crash_rate_increase_percent = float(self.error_increase_threshold.text() or 50)
            config.thresholds.sales_drop_percent = float(self.sales_drop_threshold.text() or 50)
            
            # Notifications
            config.notification.email_enabled = self.email_enabled.isChecked()
            config.notification.email_smtp_host = self.smtp_host.text()
            config.notification.email_smtp_port = int(self.smtp_port.text() or 587)
            config.notification.email_username = self.email_username.text()
            config.notification.email_password = self.email_password.text()
            
            config.notification.telegram_enabled = self.telegram_enabled.isChecked()
            config.notification.telegram_bot_token = self.telegram_token.text()
            config.notification.telegram_chat_id = self.telegram_chat_id.text()
            
            config.notification.slack_enabled = self.slack_enabled.isChecked()
            config.notification.slack_webhook_url = self.slack_webhook.text()
            
            # Save to file
            config.save()
            
            QMessageBox.information(self, "موفقیت", "تنظیمات با موفقیت ذخیره شد.")
            self.settings_changed.emit()
            
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در ذخیره تنظیمات:\n{str(e)}")
