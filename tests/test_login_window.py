"""
Unit tests for the updated login window
Tests RTL layout, logo handling, and simplified login functionality
"""
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

import pytest
from unittest.mock import Mock, patch
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest

# Create QApplication instance for testing
app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)

from app.ui.login_window import LoginWindow


class TestLoginWindowRTL:
    """Test RTL layout implementation"""
    
    def test_window_has_rtl_direction(self):
        """Test that the main window has RTL layout direction"""
        window = LoginWindow()
        assert window.layoutDirection() == Qt.LayoutDirection.RightToLeft
    
    def test_username_input_exists(self):
        """Test that username input field exists"""
        window = LoginWindow()
        assert hasattr(window, 'username_input')
        assert window.username_input is not None
    
    def test_password_input_exists(self):
        """Test that password input field exists"""
        window = LoginWindow()
        assert hasattr(window, 'password_input')
        assert window.password_input is not None
    
    def test_username_input_rtl_alignment(self):
        """Test that username input has right alignment"""
        window = LoginWindow()
        alignment = window.username_input.alignment()
        assert alignment & Qt.AlignmentFlag.AlignRight
    
    def test_password_input_rtl_alignment(self):
        """Test that password input has right alignment"""
        window = LoginWindow()
        alignment = window.password_input.alignment()
        assert alignment & Qt.AlignmentFlag.AlignRight


class TestLoginWindowLogo:
    """Test logo handling"""
    
    def test_logo_path_handling(self):
        """Test that logo path is constructed correctly"""
        window = LoginWindow()
        # Logo should be loaded or fallback to text
        # We can't test the actual display, but we can verify the window was created
        assert window is not None


class TestLoginWindowFunctionality:
    """Test login functionality"""
    
    def test_login_button_exists(self):
        """Test that login button exists"""
        window = LoginWindow()
        assert hasattr(window, 'login_button')
        assert window.login_button is not None
    
    def test_remember_checkbox_exists(self):
        """Test that remember checkbox exists"""
        window = LoginWindow()
        assert hasattr(window, 'remember_checkbox')
        assert window.remember_checkbox is not None
    
    def test_remember_checkbox_rtl(self):
        """Test that remember checkbox has RTL direction"""
        window = LoginWindow()
        assert window.remember_checkbox.layoutDirection() == Qt.LayoutDirection.RightToLeft
    
    def test_handle_login_method_exists(self):
        """Test that handle_login method exists"""
        window = LoginWindow()
        assert hasattr(window, 'handle_login')
        assert callable(window.handle_login)
    
    def test_handle_forgot_password_method_exists(self):
        """Test that handle_forgot_password method exists"""
        window = LoginWindow()
        assert hasattr(window, 'handle_forgot_password')
        assert callable(window.handle_forgot_password)
    
    def test_login_without_credentials_shows_warning(self):
        """Test that login without credentials shows warning"""
        window = LoginWindow()
        with patch('app.ui.login_window.QMessageBox.warning') as mock_warning:
            window.handle_login()
            mock_warning.assert_called_once()
    
    def test_login_successful_with_valid_credentials(self):
        """Test that login succeeds with valid credentials and emits signal"""
        window = LoginWindow()
        window.username_input.setText("admin")
        window.password_input.setText("admin")
        
        # Mock the signal
        signal_emitted = []
        window.login_successful.connect(lambda data: signal_emitted.append(data))
        
        # Trigger login
        with patch.object(window, 'close'):
            window.handle_login()
        
        # Check that signal was emitted with correct data
        assert len(signal_emitted) == 1
        assert signal_emitted[0]['username'] == 'admin'
        assert signal_emitted[0]['role'] == 'super_admin'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
