"""
Basic tests for configuration system
"""
import pytest
from pathlib import Path
import tempfile
import shutil

from app.core.config import Config, BrandConfig, AppConfig


class TestConfig:
    """Test configuration management"""
    
    @pytest.fixture
    def temp_config_dir(self):
        """Create temporary config directory"""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_config_initialization(self, temp_config_dir):
        """Test config initialization"""
        config = Config(temp_config_dir)
        assert config.config_dir.exists()
        assert config.key_file.exists()
    
    def test_brand_config_defaults(self, temp_config_dir):
        """Test brand configuration defaults"""
        config = Config(temp_config_dir)
        assert config.brand.organization_name == "Zagros Pro"
        assert config.brand.primary_color == "#F7941D"
        assert config.brand.secondary_color == "#F5E6D3"
    
    def test_app_config_defaults(self, temp_config_dir):
        """Test app configuration defaults"""
        config = Config(temp_config_dir)
        assert config.app.language == "fa"
        assert config.app.currency == "USD"
        assert config.app.auto_refresh_interval == 60
        assert config.app.enable_2fa is True
    
    def test_config_save_and_load(self, temp_config_dir):
        """Test saving and loading configuration"""
        config = Config(temp_config_dir)
        
        # Modify config
        config.brand.organization_name = "Test Org"
        config.app.language = "en"
        
        # Save
        config.save()
        
        # Load new instance
        config2 = Config(temp_config_dir)
        assert config2.brand.organization_name == "Test Org"
        assert config2.app.language == "en"
    
    def test_database_url(self, temp_config_dir):
        """Test database URL generation"""
        config = Config(temp_config_dir)
        config.database.username = "testuser"
        config.database.password = "testpass"
        config.database.database = "testdb"
        
        url = config.get_database_url()
        assert "postgresql://" in url
        assert "testuser" in url
        assert "testpass" in url
        assert "testdb" in url
