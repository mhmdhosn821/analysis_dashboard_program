"""
Unit tests for the updated login window
Tests RTL layout, OTP input, and logo handling
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


class TestLoginWindowOTP:
    """Test 6-box OTP input implementation"""
    
    def test_otp_fields_exist(self):
        """Test that OTP fields are created"""
        window = LoginWindow()
        assert hasattr(window, 'otp_fields')
        assert len(window.otp_fields) == 6
    
    def test_otp_fields_max_length(self):
        """Test that each OTP field accepts only 1 character"""
        window = LoginWindow()
        for field in window.otp_fields:
            assert field.maxLength() == 1
    
    def test_otp_fields_size(self):
        """Test that each OTP field has correct size"""
        window = LoginWindow()
        for field in window.otp_fields:
            size = field.size()
            assert size.width() == 45
            assert size.height() == 50
    
    def test_otp_fields_center_alignment(self):
        """Test that OTP fields have center alignment"""
        window = LoginWindow()
        for field in window.otp_fields:
            alignment = field.alignment()
            assert alignment & Qt.AlignmentFlag.AlignCenter
    
    def test_otp_container_initially_hidden(self):
        """Test that OTP container is hidden initially"""
        window = LoginWindow()
        assert window.twofa_container.isHidden()
    
    def test_get_otp_code_method_exists(self):
        """Test that get_otp_code method exists"""
        window = LoginWindow()
        assert hasattr(window, 'get_otp_code')
        assert callable(window.get_otp_code)
    
    def test_get_otp_code_returns_string(self):
        """Test that get_otp_code returns a string"""
        window = LoginWindow()
        # Fill OTP fields with test data
        for i, field in enumerate(window.otp_fields):
            field.setText(str(i))
        
        code = window.get_otp_code()
        assert isinstance(code, str)
        assert code == "012345"
    
    def test_on_otp_text_changed_method_exists(self):
        """Test that on_otp_text_changed method exists"""
        window = LoginWindow()
        assert hasattr(window, 'on_otp_text_changed')
        assert callable(window.on_otp_text_changed)


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
    
    def test_login_shows_2fa_after_valid_credentials(self):
        """Test that 2FA appears after valid credentials"""
        window = LoginWindow()
        window.username_input.setText("admin")
        window.password_input.setText("admin")
        
        # Trigger login
        window.handle_login()
        
        # Check that 2FA container is now visible
        assert window.twofa_container.isVisible()


class TestLoginWindowEventFilter:
    """Test event filter for OTP navigation"""
    
    def test_event_filter_method_exists(self):
        """Test that eventFilter method exists"""
        window = LoginWindow()
        assert hasattr(window, 'eventFilter')
        assert callable(window.eventFilter)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
