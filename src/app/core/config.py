"""
Configuration Management System
"""
import os
from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
import json
from cryptography.fernet import Fernet


class BrandConfig(BaseModel):
    """Brand configuration"""
    logo_path: str = ""
    organization_name: str = "Zagros Pro"
    primary_color: str = "#F7941D"
    secondary_color: str = "#F5E6D3"
    dark_color: str = "#2D2D2D"


class DatabaseConfig(BaseModel):
    """Database configuration"""
    host: str = "localhost"
    port: int = 5432
    database: str = "analysis_dashboard"
    username: str = ""
    password: str = ""


class GoogleAnalyticsConfig(BaseModel):
    """Google Analytics configuration"""
    client_id: str = ""
    client_secret: str = ""
    property_ids: list[str] = Field(default_factory=list)


class ClarityConfig(BaseModel):
    """Microsoft Clarity configuration"""
    api_key: str = ""
    project_ids: list[str] = Field(default_factory=list)


class AIConfig(BaseModel):
    """AI Services configuration"""
    openai_api_key: str = ""
    gemini_api_key: str = ""
    claude_api_key: str = ""
    default_provider: str = "openai"


class NotificationConfig(BaseModel):
    """Notification configuration"""
    email_enabled: bool = False
    email_smtp_host: str = ""
    email_smtp_port: int = 587
    email_username: str = ""
    email_password: str = ""
    telegram_enabled: bool = False
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    slack_enabled: bool = False
    slack_webhook_url: str = ""


class AlertThresholds(BaseModel):
    """Alert thresholds configuration"""
    traffic_drop_percent: float = 50.0
    crash_rate_increase_percent: float = 50.0
    sales_drop_percent: float = 50.0


class AppConfig(BaseModel):
    """Application configuration"""
    language: str = "fa"  # fa or en
    timezone: str = "UTC"
    currency: str = "USD"
    currency_symbol: str = "$"
    date_format: str = "%Y-%m-%d"
    theme: str = "light"  # light or dark
    auto_refresh_interval: int = 60  # seconds
    session_timeout: int = 0  # 0 = no timeout
    enable_2fa: bool = True
    max_concurrent_users: int = 4


class Config:
    """Main configuration manager"""
    
    def __init__(self, config_dir: Optional[Path] = None):
        if config_dir is None:
            config_dir = Path.home() / ".analysis_dashboard"
        
        self.config_dir = config_dir
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.config_dir / "config.json"
        self.secrets_file = self.config_dir / "secrets.enc"
        self.key_file = self.config_dir / ".key"
        
        self._init_encryption()
        self._load_config()
    
    def _init_encryption(self):
        """Initialize encryption key"""
        if not self.key_file.exists():
            key = Fernet.generate_key()
            self.key_file.write_bytes(key)
            os.chmod(self.key_file, 0o600)
        
        self.fernet = Fernet(self.key_file.read_bytes())
    
    def _load_config(self):
        """Load configuration from files"""
        # Load main config
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
        else:
            config_data = {}
        
        # Initialize configuration objects
        self.brand = BrandConfig(**config_data.get('brand', {}))
        self.database = DatabaseConfig(**config_data.get('database', {}))
        self.app = AppConfig(**config_data.get('app', {}))
        self.thresholds = AlertThresholds(**config_data.get('thresholds', {}))
        
        # Load encrypted secrets
        if self.secrets_file.exists():
            encrypted_data = self.secrets_file.read_bytes()
            decrypted_data = self.fernet.decrypt(encrypted_data)
            secrets_data = json.loads(decrypted_data)
        else:
            secrets_data = {}
        
        self.google_analytics = GoogleAnalyticsConfig(**secrets_data.get('google_analytics', {}))
        self.clarity = ClarityConfig(**secrets_data.get('clarity', {}))
        self.ai = AIConfig(**secrets_data.get('ai', {}))
        self.notification = NotificationConfig(**secrets_data.get('notification', {}))
    
    def save(self):
        """Save configuration to files"""
        # Save main config
        config_data = {
            'brand': self.brand.model_dump(),
            'database': self.database.model_dump(exclude={'password'}),
            'app': self.app.model_dump(),
            'thresholds': self.thresholds.model_dump(),
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        
        # Save encrypted secrets
        secrets_data = {
            'google_analytics': self.google_analytics.model_dump(),
            'clarity': self.clarity.model_dump(),
            'ai': self.ai.model_dump(),
            'notification': self.notification.model_dump(),
            'database_password': self.database.password,
        }
        
        encrypted_data = self.fernet.encrypt(json.dumps(secrets_data).encode())
        self.secrets_file.write_bytes(encrypted_data)
        os.chmod(self.secrets_file, 0o600)
    
    def get_database_url(self) -> str:
        """Get database connection URL"""
        return (
            f"postgresql://{self.database.username}:{self.database.password}"
            f"@{self.database.host}:{self.database.port}/{self.database.database}"
        )


# Global config instance
config = Config()
