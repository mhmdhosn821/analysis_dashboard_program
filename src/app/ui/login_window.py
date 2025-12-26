"""
Login Window
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit, 
    QPushButton, QCheckBox, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont
from pathlib import Path


class LoginWindow(QWidget):
    """Login window with RTL support"""
    
    login_successful = pyqtSignal(dict)  # Emits user data on successful login
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Analysis Dashboard - Login")
        self.setFixedSize(450, 600)
        self.setup_ui()
    
    def _create_fallback_logo(self, logo_label):
        """Create fallback text logo when image is not available"""
        logo_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #F7941D, stop:1 #FF9933);
                border-radius: 60px;
                color: white;
                font-size: 48px;
                font-weight: bold;
            }
        """)
        logo_label.setText("ZP")
    
    def setup_ui(self):
        """Setup the user interface"""
        # Set layout direction for RTL
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        
        # Logo section
        logo_frame = QFrame()
        logo_frame.setObjectName("glass-panel")
        logo_layout = QVBoxLayout()
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo with actual image
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setFixedSize(120, 120)
        
        # Try to load the logo image
        logo_path = Path(__file__).parent / "assets" / "images" / "zagros_pro_logo.svg"
        if logo_path.exists():
            pixmap = QPixmap(str(logo_path))
            if not pixmap.isNull():
                logo_label.setPixmap(pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            else:
                # Fallback to text if image fails to load
                self._create_fallback_logo(logo_label)
        else:
            # Fallback to text if file doesn't exist
            self._create_fallback_logo(logo_label)
        
        logo_layout.addWidget(logo_label)
        
        # Title
        title_label = QLabel("داشبورد مدیریتی آنالیز")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        logo_layout.addWidget(title_label)
        
        subtitle_label = QLabel("تیم فنی زاگرس پرو")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #F7941D; font-size: 14px;")
        logo_layout.addWidget(subtitle_label)
        
        logo_frame.setLayout(logo_layout)
        main_layout.addWidget(logo_frame)
        
        main_layout.addSpacing(20)
        
        # Form section with proper RTL layout
        form_frame = QFrame()
        form_frame.setObjectName("glass-panel")
        form_container = QVBoxLayout()
        form_container.setSpacing(15)
        
        # Create form layout with RTL support
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        form_layout.setFormAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        form_layout.setHorizontalSpacing(15)
        form_layout.setVerticalSpacing(15)
        
        # Username field with label on the right
        username_label = QLabel("نام کاربری:")
        username_label.setStyleSheet("font-weight: bold; color: white;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("نام کاربری خود را وارد کنید")
        self.username_input.setMinimumHeight(40)
        self.username_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.addRow(username_label, self.username_input)
        
        # Password field with label on the right
        password_label = QLabel("رمز عبور:")
        password_label.setStyleSheet("font-weight: bold; color: white;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("رمز عبور خود را وارد کنید")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(40)
        self.password_input.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.password_input.returnPressed.connect(self.handle_login)
        form_layout.addRow(password_label, self.password_input)
        
        form_container.addLayout(form_layout)
        
        # Remember me checkbox
        self.remember_checkbox = QCheckBox("مرا به خاطر بسپار")
        self.remember_checkbox.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        form_container.addWidget(self.remember_checkbox)
        
        form_frame.setLayout(form_container)
        main_layout.addWidget(form_frame)
        
        # Login button
        self.login_button = QPushButton("ورود")
        self.login_button.setMinimumHeight(45)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.clicked.connect(self.handle_login)
        main_layout.addWidget(self.login_button)
        
        # Forgot password link
        forgot_button = QPushButton("فراموشی رمز عبور")
        forgot_button.setProperty("secondary", True)
        forgot_button.setFlat(True)
        forgot_button.setCursor(Qt.CursorShape.PointingHandCursor)
        forgot_button.clicked.connect(self.handle_forgot_password)
        main_layout.addWidget(forgot_button)
        
        main_layout.addStretch()
        
        self.setLayout(main_layout)
    
    def handle_login(self):
        """Handle login button click
        
        Note: 2FA verification has been removed from the UI. 
        If backend authentication requires 2FA, it should be handled 
        server-side or the backend configuration should be updated 
        to disable 2FA requirements.
        """
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "خطا", "لطفا نام کاربری و رمز عبور را وارد کنید")
            return
        
        # TODO: Implement actual authentication
        # For now, simulate successful login
        if username == "admin" and password == "admin":
            # Successful login
            user_data = {
                'username': username,
                'role': 'super_admin',
                'email': 'admin@example.com'
            }
            self.login_successful.emit(user_data)
            self.close()
        else:
            QMessageBox.warning(self, "خطا", "نام کاربری یا رمز عبور اشتباه است")
    
    def handle_forgot_password(self):
        """Handle forgot password"""
        QMessageBox.information(
            self, 
            "فراموشی رمز عبور", 
            "لطفا با مدیر سیستم تماس بگیرید"
        )
