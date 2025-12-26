"""
Main application entry point
"""
import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontDatabase

from app.ui.login_window import LoginWindow
from app.ui.main_window import MainWindow
from app.ui.styles.glassmorphism import get_stylesheet
from app.core.config import config


class Application:
    """Main application class"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Analysis Dashboard")
        self.app.setOrganizationName("Zagros Pro")
        
        # Set application style
        self.setup_fonts()
        self.apply_theme()
        
        self.main_window = None
        self.login_window = None
    
    def setup_fonts(self):
        """Setup application fonts"""
        # TODO: Load Vazirmatn font from assets
        # For now, use system fonts
        font = QFont("Segoe UI", 10)
        self.app.setFont(font)
    
    def apply_theme(self):
        """Apply application theme"""
        theme = config.app.theme
        stylesheet = get_stylesheet(theme)
        self.app.setStyleSheet(stylesheet)
    
    def show_login(self):
        """Show login window"""
        self.login_window = LoginWindow()
        self.login_window.login_successful.connect(self.on_login_success)
        self.login_window.show()
    
    def on_login_success(self, user_data: dict):
        """Handle successful login"""
        self.login_window = None
        self.show_main_window(user_data)
    
    def show_main_window(self, user_data: dict):
        """Show main application window"""
        self.main_window = MainWindow(user_data)
        self.main_window.show()
    
    def run(self):
        """Run the application"""
        self.show_login()
        return self.app.exec()


def main():
    """Main entry point"""
    app = Application()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
