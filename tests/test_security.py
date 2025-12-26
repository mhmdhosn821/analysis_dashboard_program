"""
Tests for security utilities
"""
import pytest
from app.core.security import (
    PasswordHasher, TwoFactorAuth, TokenManager, 
    validate_password_strength
)


class TestPasswordHasher:
    """Test password hashing"""
    
    def test_hash_password(self):
        """Test password hashing"""
        password = "SecureP@ss123"
        hashed = PasswordHasher.hash_password(password)
        
        assert hashed is not None
        assert "$" in hashed
        assert len(hashed) > 50
    
    def test_verify_password(self):
        """Test password verification"""
        password = "SecureP@ss123"
        hashed = PasswordHasher.hash_password(password)
        
        assert PasswordHasher.verify_password(password, hashed) is True
        assert PasswordHasher.verify_password("WrongPassword", hashed) is False


class TestTwoFactorAuth:
    """Test 2FA"""
    
    def test_generate_secret(self):
        """Test TOTP secret generation"""
        secret = TwoFactorAuth.generate_secret()
        assert secret is not None
        assert len(secret) == 32
    
    def test_provisioning_uri(self):
        """Test provisioning URI generation"""
        secret = TwoFactorAuth.generate_secret()
        uri = TwoFactorAuth.get_provisioning_uri(secret, "testuser")
        
        assert "otpauth://" in uri
        assert "testuser" in uri


class TestTokenManager:
    """Test JWT token management"""
    
    def test_create_token(self):
        """Test token creation"""
        manager = TokenManager("test_secret_key")
        token = manager.create_token(1, "testuser", "admin")
        
        assert token is not None
        assert isinstance(token, str)
    
    def test_verify_token(self):
        """Test token verification"""
        manager = TokenManager("test_secret_key")
        token = manager.create_token(1, "testuser", "admin")
        
        payload = manager.verify_token(token)
        assert payload is not None
        assert payload['user_id'] == 1
        assert payload['username'] == "testuser"
        assert payload['role'] == "admin"
    
    def test_verify_invalid_token(self):
        """Test verification of invalid token"""
        manager = TokenManager("test_secret_key")
        payload = manager.verify_token("invalid_token")
        
        assert payload is None


class TestPasswordValidation:
    """Test password strength validation"""
    
    def test_valid_password(self):
        """Test valid password"""
        valid, msg = validate_password_strength("SecureP@ss123")
        assert valid is True
    
    def test_too_short(self):
        """Test password too short"""
        valid, msg = validate_password_strength("Short1!")
        assert valid is False
        assert "8 characters" in msg
    
    def test_no_uppercase(self):
        """Test password without uppercase"""
        valid, msg = validate_password_strength("password123!")
        assert valid is False
        assert "uppercase" in msg
    
    def test_no_lowercase(self):
        """Test password without lowercase"""
        valid, msg = validate_password_strength("PASSWORD123!")
        assert valid is False
        assert "lowercase" in msg
    
    def test_no_digit(self):
        """Test password without digit"""
        valid, msg = validate_password_strength("Password!")
        assert valid is False
        assert "digit" in msg
    
    def test_no_special_char(self):
        """Test password without special character"""
        valid, msg = validate_password_strength("Password123")
        assert valid is False
        assert "special character" in msg
