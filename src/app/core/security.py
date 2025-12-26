"""
Security utilities including authentication, encryption, and 2FA
"""
import hashlib
import secrets
import pyotp
import jwt
from datetime import datetime, timedelta
from typing import Optional, Tuple
from cryptography.fernet import Fernet


class PasswordHasher:
    """Password hashing utilities"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password with salt"""
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return f"{salt}${pwd_hash.hex()}"
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify a password against its hash"""
        try:
            salt, stored_hash = password_hash.split('$')
            pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
            return pwd_hash.hex() == stored_hash
        except Exception:
            return False


class TwoFactorAuth:
    """Two-factor authentication utilities"""
    
    @staticmethod
    def generate_secret() -> str:
        """Generate a new TOTP secret"""
        return pyotp.random_base32()
    
    @staticmethod
    def get_provisioning_uri(secret: str, username: str, issuer: str = "Analysis Dashboard") -> str:
        """Get provisioning URI for QR code"""
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(name=username, issuer_name=issuer)
    
    @staticmethod
    def verify_totp(secret: str, token: str) -> bool:
        """Verify a TOTP token"""
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=1)


class TokenManager:
    """JWT token management"""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
    
    def create_token(self, user_id: int, username: str, role: str, expires_in: int = 86400) -> str:
        """Create a JWT token"""
        payload = {
            'user_id': user_id,
            'username': username,
            'role': role,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token: str) -> Optional[dict]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None


class SessionManager:
    """Session management utilities"""
    
    @staticmethod
    def generate_session_token() -> str:
        """Generate a secure session token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def validate_session_token(token: str) -> bool:
        """Validate session token format"""
        return len(token) >= 32


class IPWhitelist:
    """IP whitelist management"""
    
    def __init__(self):
        self.whitelist = set()
    
    def add_ip(self, ip_address: str):
        """Add IP to whitelist"""
        self.whitelist.add(ip_address)
    
    def remove_ip(self, ip_address: str):
        """Remove IP from whitelist"""
        self.whitelist.discard(ip_address)
    
    def is_allowed(self, ip_address: str) -> bool:
        """Check if IP is allowed"""
        if not self.whitelist:
            return True  # If whitelist is empty, allow all
        return ip_address in self.whitelist


class RateLimiter:
    """Rate limiting for API calls"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}  # {identifier: [(timestamp, count)]}
    
    def is_allowed(self, identifier: str) -> Tuple[bool, int]:
        """Check if request is allowed and return remaining requests"""
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=self.window_seconds)
        
        # Clean old requests
        if identifier in self.requests:
            self.requests[identifier] = [
                (ts, count) for ts, count in self.requests[identifier]
                if ts > window_start
            ]
        else:
            self.requests[identifier] = []
        
        # Count requests in current window
        current_count = sum(count for _, count in self.requests[identifier])
        
        if current_count >= self.max_requests:
            return False, 0
        
        # Add current request
        self.requests[identifier].append((now, 1))
        remaining = self.max_requests - current_count - 1
        
        return True, remaining


class DataEncryption:
    """Data encryption utilities"""
    
    def __init__(self, key: Optional[bytes] = None):
        if key is None:
            key = Fernet.generate_key()
        self.fernet = Fernet(key)
    
    def encrypt(self, data: str) -> bytes:
        """Encrypt data"""
        return self.fernet.encrypt(data.encode('utf-8'))
    
    def decrypt(self, encrypted_data: bytes) -> str:
        """Decrypt data"""
        return self.fernet.decrypt(encrypted_data).decode('utf-8')


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(c in special_chars for c in password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is strong"
