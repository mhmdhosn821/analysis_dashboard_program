"""
Database Models and Connection Management
"""
from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, DateTime, 
    Float, Text, ForeignKey, JSON, Enum as SQLEnum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum

Base = declarative_base()


class UserRole(enum.Enum):
    """User role enumeration"""
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    MANAGER = "manager"
    VIEWER = "viewer"
    ANALYST = "analyst"


class User(Base):
    """User model"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    require_2fa = Column(Boolean, default=True)
    totp_secret = Column(String(32), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
    dashboards = relationship("Dashboard", back_populates="owner", cascade="all, delete-orphan")


class UserSession(Base):
    """User session model"""
    __tablename__ = 'user_sessions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    session_token = Column(String(255), unique=True, nullable=False)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="sessions")


class AuditLog(Base):
    """Audit log model"""
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    action = Column(String(100), nullable=False)
    resource = Column(String(100), nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")


class Dashboard(Base):
    """Dashboard model"""
    __tablename__ = 'dashboards'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    layout_config = Column(JSON, nullable=True)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="dashboards")
    widgets = relationship("Widget", back_populates="dashboard", cascade="all, delete-orphan")


class Widget(Base):
    """Widget model"""
    __tablename__ = 'widgets'
    
    id = Column(Integer, primary_key=True)
    dashboard_id = Column(Integer, ForeignKey('dashboards.id'), nullable=False)
    widget_type = Column(String(50), nullable=False)  # line, bar, pie, heatmap, gauge, table
    title = Column(String(100), nullable=False)
    data_source = Column(String(100), nullable=False)  # ga4, clarity, etc.
    config = Column(JSON, nullable=True)
    position_x = Column(Integer, default=0)
    position_y = Column(Integer, default=0)
    width = Column(Integer, default=4)
    height = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    dashboard = relationship("Dashboard", back_populates="widgets")


class Alert(Base):
    """Alert model"""
    __tablename__ = 'alerts'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    metric = Column(String(100), nullable=False)
    condition = Column(String(50), nullable=False)  # above, below, equals
    threshold = Column(Float, nullable=False)
    channels = Column(JSON, nullable=False)  # [email, telegram, slack]
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AlertHistory(Base):
    """Alert history model"""
    __tablename__ = 'alert_history'
    
    id = Column(Integer, primary_key=True)
    alert_id = Column(Integer, ForeignKey('alerts.id'), nullable=False)
    triggered_at = Column(DateTime, default=datetime.utcnow)
    metric_value = Column(Float, nullable=False)
    message = Column(Text, nullable=True)
    channels_sent = Column(JSON, nullable=True)


class ReportTemplate(Base):
    """Report template model"""
    __tablename__ = 'report_templates'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    template_config = Column(JSON, nullable=False)
    schedule = Column(String(50), nullable=True)  # daily, weekly, monthly
    recipients = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CachedData(Base):
    """Cached data model"""
    __tablename__ = 'cached_data'
    
    id = Column(Integer, primary_key=True)
    cache_key = Column(String(255), unique=True, nullable=False)
    data_source = Column(String(100), nullable=False)
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)


class AnalyticsData(Base):
    """Analytics data model"""
    __tablename__ = 'analytics_data'
    
    id = Column(Integer, primary_key=True)
    property_id = Column(String(100), nullable=False)
    date = Column(DateTime, nullable=False)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    dimensions = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Sale(Base):
    """Sales data model"""
    __tablename__ = 'sales'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(String(100), unique=True, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=True)
    customer_name = Column(String(200), nullable=True)
    amount = Column(Float, nullable=False)
    quantity = Column(Integer, default=1)
    status = Column(String(50), default='pending')  # pending, completed, cancelled
    sale_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="sales")


class Product(Base):
    """Product model"""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    sku = Column(String(100), unique=True, nullable=True)
    category = Column(String(100), nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sales = relationship("Sale", back_populates="product", cascade="all, delete-orphan")


class Setting(Base):
    """Settings model"""
    __tablename__ = 'settings'
    
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text, nullable=True)
    category = Column(String(50), nullable=False)  # api_keys, thresholds, display, etc.
    is_encrypted = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Database:
    """Database connection manager"""
    
    def __init__(self, database_url: str = None):
        """Initialize database connection
        
        Args:
            database_url: Database URL. If None, uses SQLite with default path
        """
        if database_url is None:
            # Use SQLite with default path in user's home directory
            from pathlib import Path
            db_dir = Path.home() / ".analysis_dashboard"
            db_dir.mkdir(parents=True, exist_ok=True)
            database_url = f"sqlite:///{db_dir}/dashboard.db"
        
        # SQLite specific settings
        connect_args = {}
        if database_url.startswith('sqlite'):
            connect_args = {'check_same_thread': False}
        
        self.engine = create_engine(database_url, connect_args=connect_args, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(bind=self.engine)
    
    def drop_tables(self):
        """Drop all tables"""
        Base.metadata.drop_all(bind=self.engine)
    
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
    
    def init_default_data(self):
        """Initialize database with default data"""
        from app.core.security import PasswordHasher
        session = self.get_session()
        try:
            # Check if admin user exists
            from sqlalchemy import select
            stmt = select(User).where(User.username == 'admin')
            admin = session.execute(stmt).scalar_one_or_none()
            
            if not admin:
                # Create default admin user
                admin = User(
                    username='admin',
                    email='admin@example.com',
                    password_hash=PasswordHasher.hash_password('admin'),
                    role=UserRole.SUPER_ADMIN,
                    is_active=True,
                    require_2fa=False
                )
                session.add(admin)
                session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


# Global database instance
db = Database()
