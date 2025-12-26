"""
Database Manager - Helper functions for database operations
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy import select, func, and_, or_
from app.core.database import (
    db, User, UserSession, AuditLog, Dashboard, Widget,
    Alert, AlertHistory, ReportTemplate, CachedData,
    AnalyticsData, Sale, Product, Setting
)


class DatabaseManager:
    """Database operations manager"""
    
    def __init__(self):
        self.db = db
    
    # User Management
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        session = self.db.get_session()
        try:
            stmt = select(User).where(User.username == username)
            return session.execute(stmt).scalar_one_or_none()
        finally:
            session.close()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        session = self.db.get_session()
        try:
            stmt = select(User).where(User.id == user_id)
            return session.execute(stmt).scalar_one_or_none()
        finally:
            session.close()
    
    def create_user(self, username: str, email: str, password_hash: str, role: str) -> User:
        """Create a new user"""
        from app.core.database import UserRole
        session = self.db.get_session()
        try:
            user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                role=UserRole[role.upper()],
                is_active=True
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        finally:
            session.close()
    
    def update_user_last_login(self, user_id: int):
        """Update user's last login timestamp"""
        session = self.db.get_session()
        try:
            stmt = select(User).where(User.id == user_id)
            user = session.execute(stmt).scalar_one_or_none()
            if user:
                user.last_login = datetime.utcnow()
                session.commit()
        finally:
            session.close()
    
    # Analytics Data
    def save_analytics_data(self, property_id: str, date: datetime, 
                           metric_name: str, metric_value: float,
                           dimensions: Optional[Dict] = None):
        """Save analytics data"""
        session = self.db.get_session()
        try:
            analytics = AnalyticsData(
                property_id=property_id,
                date=date,
                metric_name=metric_name,
                metric_value=metric_value,
                dimensions=dimensions
            )
            session.add(analytics)
            session.commit()
        finally:
            session.close()
    
    def get_analytics_data(self, property_id: str, metric_name: str,
                          start_date: datetime, end_date: datetime) -> List[AnalyticsData]:
        """Get analytics data for a date range"""
        session = self.db.get_session()
        try:
            stmt = select(AnalyticsData).where(
                and_(
                    AnalyticsData.property_id == property_id,
                    AnalyticsData.metric_name == metric_name,
                    AnalyticsData.date >= start_date,
                    AnalyticsData.date <= end_date
                )
            ).order_by(AnalyticsData.date)
            return list(session.execute(stmt).scalars().all())
        finally:
            session.close()
    
    # Sales
    def create_sale(self, order_id: str, amount: float, product_id: Optional[int] = None,
                    customer_name: Optional[str] = None, quantity: int = 1,
                    sale_date: Optional[datetime] = None) -> Sale:
        """Create a new sale"""
        session = self.db.get_session()
        try:
            sale = Sale(
                order_id=order_id,
                product_id=product_id,
                customer_name=customer_name,
                amount=amount,
                quantity=quantity,
                status='completed',
                sale_date=sale_date or datetime.utcnow()
            )
            session.add(sale)
            session.commit()
            session.refresh(sale)
            return sale
        finally:
            session.close()
    
    def get_sales_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Sale]:
        """Get sales for a date range"""
        session = self.db.get_session()
        try:
            stmt = select(Sale).where(
                and_(
                    Sale.sale_date >= start_date,
                    Sale.sale_date <= end_date
                )
            ).order_by(Sale.sale_date.desc())
            return list(session.execute(stmt).scalars().all())
        finally:
            session.close()
    
    def get_total_sales(self, start_date: datetime, end_date: datetime) -> float:
        """Get total sales amount for a date range"""
        session = self.db.get_session()
        try:
            stmt = select(func.sum(Sale.amount)).where(
                and_(
                    Sale.sale_date >= start_date,
                    Sale.sale_date <= end_date,
                    Sale.status == 'completed'
                )
            )
            result = session.execute(stmt).scalar()
            return result or 0.0
        finally:
            session.close()
    
    # Products
    def create_product(self, name: str, price: float, sku: Optional[str] = None,
                      category: Optional[str] = None, stock: int = 0) -> Product:
        """Create a new product"""
        session = self.db.get_session()
        try:
            product = Product(
                name=name,
                sku=sku,
                category=category,
                price=price,
                stock=stock
            )
            session.add(product)
            session.commit()
            session.refresh(product)
            return product
        finally:
            session.close()
    
    def get_products(self) -> List[Product]:
        """Get all products"""
        session = self.db.get_session()
        try:
            stmt = select(Product).order_by(Product.name)
            return list(session.execute(stmt).scalars().all())
        finally:
            session.close()
    
    def get_top_selling_products(self, limit: int = 10) -> List[Dict]:
        """Get top selling products"""
        session = self.db.get_session()
        try:
            stmt = select(
                Product.id,
                Product.name,
                func.sum(Sale.quantity).label('total_quantity'),
                func.sum(Sale.amount).label('total_amount')
            ).join(Sale).group_by(Product.id, Product.name).order_by(
                func.sum(Sale.amount).desc()
            ).limit(limit)
            
            results = session.execute(stmt).all()
            return [
                {
                    'id': r.id,
                    'name': r.name,
                    'total_quantity': r.total_quantity,
                    'total_amount': r.total_amount
                }
                for r in results
            ]
        finally:
            session.close()
    
    # Settings
    def get_setting(self, key: str) -> Optional[str]:
        """Get a setting value"""
        session = self.db.get_session()
        try:
            stmt = select(Setting).where(Setting.key == key)
            setting = session.execute(stmt).scalar_one_or_none()
            return setting.value if setting else None
        finally:
            session.close()
    
    def set_setting(self, key: str, value: str, category: str = 'general',
                   is_encrypted: bool = False):
        """Set a setting value"""
        session = self.db.get_session()
        try:
            stmt = select(Setting).where(Setting.key == key)
            setting = session.execute(stmt).scalar_one_or_none()
            
            if setting:
                setting.value = value
                setting.category = category
                setting.is_encrypted = is_encrypted
                setting.updated_at = datetime.utcnow()
            else:
                setting = Setting(
                    key=key,
                    value=value,
                    category=category,
                    is_encrypted=is_encrypted
                )
                session.add(setting)
            
            session.commit()
        finally:
            session.close()
    
    def get_settings_by_category(self, category: str) -> Dict[str, str]:
        """Get all settings in a category"""
        session = self.db.get_session()
        try:
            stmt = select(Setting).where(Setting.category == category)
            settings = session.execute(stmt).scalars().all()
            return {s.key: s.value for s in settings}
        finally:
            session.close()
    
    # Alerts
    def create_alert(self, name: str, metric: str, condition: str,
                    threshold: float, channels: List[str]) -> Alert:
        """Create a new alert"""
        session = self.db.get_session()
        try:
            alert = Alert(
                name=name,
                metric=metric,
                condition=condition,
                threshold=threshold,
                channels=channels,
                is_active=True
            )
            session.add(alert)
            session.commit()
            session.refresh(alert)
            return alert
        finally:
            session.close()
    
    def get_active_alerts(self) -> List[Alert]:
        """Get all active alerts"""
        session = self.db.get_session()
        try:
            stmt = select(Alert).where(Alert.is_active == True)
            return list(session.execute(stmt).scalars().all())
        finally:
            session.close()
    
    def log_alert_trigger(self, alert_id: int, metric_value: float,
                         message: str, channels_sent: List[str]):
        """Log an alert trigger"""
        session = self.db.get_session()
        try:
            history = AlertHistory(
                alert_id=alert_id,
                metric_value=metric_value,
                message=message,
                channels_sent=channels_sent
            )
            session.add(history)
            session.commit()
        finally:
            session.close()
    
    # Audit Logs
    def log_action(self, user_id: int, action: str, resource: Optional[str] = None,
                  details: Optional[Dict] = None, ip_address: Optional[str] = None):
        """Log a user action"""
        session = self.db.get_session()
        try:
            log = AuditLog(
                user_id=user_id,
                action=action,
                resource=resource,
                details=details,
                ip_address=ip_address
            )
            session.add(log)
            session.commit()
        finally:
            session.close()
    
    # Cache
    def get_cached_data(self, cache_key: str, data_source: str) -> Optional[Dict]:
        """Get cached data if not expired"""
        session = self.db.get_session()
        try:
            stmt = select(CachedData).where(
                and_(
                    CachedData.cache_key == cache_key,
                    CachedData.data_source == data_source,
                    CachedData.expires_at > datetime.utcnow()
                )
            )
            cached = session.execute(stmt).scalar_one_or_none()
            return cached.data if cached else None
        finally:
            session.close()
    
    def set_cached_data(self, cache_key: str, data_source: str, data: Dict,
                       ttl_seconds: int = 300):
        """Set cached data with TTL"""
        session = self.db.get_session()
        try:
            expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)
            
            stmt = select(CachedData).where(
                and_(
                    CachedData.cache_key == cache_key,
                    CachedData.data_source == data_source
                )
            )
            cached = session.execute(stmt).scalar_one_or_none()
            
            if cached:
                cached.data = data
                cached.expires_at = expires_at
                cached.created_at = datetime.utcnow()
            else:
                cached = CachedData(
                    cache_key=cache_key,
                    data_source=data_source,
                    data=data,
                    expires_at=expires_at
                )
                session.add(cached)
            
            session.commit()
        finally:
            session.close()


# Global database manager instance
db_manager = DatabaseManager()
