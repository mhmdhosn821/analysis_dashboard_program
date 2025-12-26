"""
Dialog Widgets - Modal dialogs for various purposes
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QComboBox, QCheckBox, QFormLayout,
    QDialogButtonBox, QFrame, QWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class BaseDialog(QDialog):
    """Base dialog with common styling"""
    
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setup_style()
    
    def setup_style(self):
        """Setup dialog style"""
        self.setStyleSheet("""
            QDialog {
                background: #F5F5F5;
            }
            QLabel {
                color: #333;
            }
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
            QPushButton:pressed {
                background: #D7740D;
            }
            QLineEdit, QTextEdit, QComboBox {
                padding: 8px;
                border: 1px solid #DDD;
                border-radius: 6px;
                background: white;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 2px solid #F7941D;
            }
        """)


class SettingsDialog(BaseDialog):
    """Dialog for managing settings"""
    
    settings_saved = pyqtSignal(dict)
    
    def __init__(self, current_settings: dict = None, parent=None):
        super().__init__("تنظیمات", parent)
        self.current_settings = current_settings or {}
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("تنظیمات سیستم")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2D2D2D;")
        layout.addWidget(title_label)
        
        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # Language
        self.language_combo = QComboBox()
        self.language_combo.addItems(["فارسی", "English"])
        form_layout.addRow("زبان:", self.language_combo)
        
        # Theme
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["روشن", "تاریک"])
        form_layout.addRow("تم:", self.theme_combo)
        
        # Auto refresh
        self.refresh_combo = QComboBox()
        self.refresh_combo.addItems(["30 ثانیه", "60 ثانیه", "5 دقیقه", "خاموش"])
        form_layout.addRow("به‌روزرسانی خودکار:", self.refresh_combo)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("لغو")
        cancel_btn.setStyleSheet("background: #999;")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("ذخیره")
        save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def save_settings(self):
        """Save settings"""
        settings = {
            'language': self.language_combo.currentText(),
            'theme': self.theme_combo.currentText(),
            'auto_refresh': self.refresh_combo.currentText()
        }
        self.settings_saved.emit(settings)
        self.accept()


class APIKeyDialog(BaseDialog):
    """Dialog for managing API keys"""
    
    api_key_saved = pyqtSignal(str, str)  # service, key
    
    def __init__(self, service_name: str, current_key: str = "", parent=None):
        self.service_name = service_name
        self.current_key = current_key
        super().__init__(f"تنظیم API Key - {service_name}", parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Info
        info_label = QLabel(f"کلید API برای {self.service_name}")
        info_label.setStyleSheet("font-size: 14px; color: #666;")
        layout.addWidget(info_label)
        
        # API Key input
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("کلید API را وارد کنید")
        self.api_key_input.setText(self.current_key)
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.api_key_input)
        
        # Show/Hide checkbox
        self.show_key_check = QCheckBox("نمایش کلید")
        self.show_key_check.stateChanged.connect(self.toggle_key_visibility)
        layout.addWidget(self.show_key_check)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("لغو")
        cancel_btn.setStyleSheet("background: #999;")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("ذخیره")
        save_btn.clicked.connect(self.save_api_key)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def toggle_key_visibility(self, state):
        """Toggle API key visibility"""
        if state:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
    
    def save_api_key(self):
        """Save API key"""
        api_key = self.api_key_input.text().strip()
        if api_key:
            self.api_key_saved.emit(self.service_name, api_key)
            self.accept()


class AlertDialog(BaseDialog):
    """Dialog for creating/editing alerts"""
    
    alert_saved = pyqtSignal(dict)
    
    def __init__(self, alert_data: dict = None, parent=None):
        self.alert_data = alert_data or {}
        super().__init__("تنظیم هشدار", parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("ایجاد هشدار جدید")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # Alert name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("نام هشدار")
        self.name_input.setText(self.alert_data.get('name', ''))
        form_layout.addRow("نام:", self.name_input)
        
        # Metric
        self.metric_combo = QComboBox()
        self.metric_combo.addItems([
            "افت ترافیک",
            "افزایش خطاها",
            "کاهش فروش",
            "افزایش نرخ Crash",
            "کاهش نرخ تبدیل"
        ])
        form_layout.addRow("متریک:", self.metric_combo)
        
        # Condition
        self.condition_combo = QComboBox()
        self.condition_combo.addItems(["بیشتر از", "کمتر از", "برابر"])
        form_layout.addRow("شرط:", self.condition_combo)
        
        # Threshold
        self.threshold_input = QLineEdit()
        self.threshold_input.setPlaceholderText("مقدار آستانه")
        self.threshold_input.setText(str(self.alert_data.get('threshold', '')))
        form_layout.addRow("آستانه:", self.threshold_input)
        
        layout.addLayout(form_layout)
        
        # Notification channels
        channels_label = QLabel("کانال‌های اطلاع‌رسانی:")
        channels_label.setStyleSheet("font-weight: 600; margin-top: 10px;")
        layout.addWidget(channels_label)
        
        self.email_check = QCheckBox("ایمیل")
        self.telegram_check = QCheckBox("تلگرام")
        self.slack_check = QCheckBox("Slack")
        self.app_check = QCheckBox("اپلیکیشن")
        self.app_check.setChecked(True)
        
        layout.addWidget(self.email_check)
        layout.addWidget(self.telegram_check)
        layout.addWidget(self.slack_check)
        layout.addWidget(self.app_check)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("لغو")
        cancel_btn.setStyleSheet("background: #999;")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("ذخیره")
        save_btn.clicked.connect(self.save_alert)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def save_alert(self):
        """Save alert"""
        channels = []
        if self.email_check.isChecked():
            channels.append('email')
        if self.telegram_check.isChecked():
            channels.append('telegram')
        if self.slack_check.isChecked():
            channels.append('slack')
        if self.app_check.isChecked():
            channels.append('app')
        
        alert = {
            'name': self.name_input.text(),
            'metric': self.metric_combo.currentText(),
            'condition': self.condition_combo.currentText(),
            'threshold': float(self.threshold_input.text() or 0),
            'channels': channels
        }
        self.alert_saved.emit(alert)
        self.accept()


class ConfirmDialog(BaseDialog):
    """Confirmation dialog"""
    
    def __init__(self, title: str, message: str, parent=None):
        super().__init__(title, parent)
        self.message = message
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Message
        message_label = QLabel(self.message)
        message_label.setWordWrap(True)
        message_label.setStyleSheet("font-size: 13px; color: #333;")
        layout.addWidget(message_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        no_btn = QPushButton("خیر")
        no_btn.setStyleSheet("background: #999;")
        no_btn.clicked.connect(self.reject)
        button_layout.addWidget(no_btn)
        
        yes_btn = QPushButton("بله")
        yes_btn.clicked.connect(self.accept)
        button_layout.addWidget(yes_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)


class AIChatDialog(BaseDialog):
    """Dialog for AI chat interface"""
    
    query_sent = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__("چت با هوش مصنوعی", parent)
        self.setMinimumSize(600, 500)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("💬 سوالات خود را از داده‌ها بپرسید")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Chat history
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setPlaceholderText("تاریخچه چت...")
        layout.addWidget(self.chat_history, 1)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("سوال خود را بپرسید...")
        self.query_input.returnPressed.connect(self.send_query)
        input_layout.addWidget(self.query_input, 1)
        
        send_btn = QPushButton("ارسال")
        send_btn.clicked.connect(self.send_query)
        input_layout.addWidget(send_btn)
        
        layout.addLayout(input_layout)
        
        # Close button
        close_btn = QPushButton("بستن")
        close_btn.setStyleSheet("background: #999;")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.setLayout(layout)
    
    def send_query(self):
        """Send query to AI"""
        query = self.query_input.text().strip()
        if query:
            # Add to chat history
            self.chat_history.append(f"<b>شما:</b> {query}<br>")
            self.query_sent.emit(query)
            self.query_input.clear()
    
    def add_response(self, response: str):
        """Add AI response to chat"""
        self.chat_history.append(f"<b>AI:</b> {response}<br><br>")
