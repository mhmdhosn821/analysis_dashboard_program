#!/usr/bin/env python3
"""
Database Initialization Script
Creates database and populates with sample data
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from datetime import datetime, timedelta
import random
from app.core.database import db
from app.core.db_manager import db_manager
from app.core.security import hash_password


def init_database():
    """Initialize database with tables and default data"""
    print("🔄 Initializing database...")
    
    # Create all tables
    db.create_tables()
    print("✅ Tables created successfully")
    
    # Create default admin user if not exists
    db.init_default_data()
    print("✅ Default admin user created (username: admin, password: admin)")


def populate_sample_data():
    """Populate database with sample data"""
    print("\n🔄 Populating sample data...")
    
    # Add sample products
    products = [
        ("لپ‌تاپ Dell XPS 15", 1500.00, "DELL-XPS-15", "الکترونیک", 10),
        ("آیفون 15 پرو", 1200.00, "IPHONE-15-PRO", "موبایل", 25),
        ("هدفون سونی WH-1000XM5", 350.00, "SONY-WH1000XM5", "صوتی", 15),
        ("کیبورد مکانیکی", 120.00, "KB-MECH-001", "لوازم جانبی", 30),
        ("ماوس گیمینگ", 80.00, "MOUSE-GAME-001", "لوازم جانبی", 40),
    ]
    
    product_ids = []
    for name, price, sku, category, stock in products:
        try:
            product = db_manager.create_product(name, price, sku, category, stock)
            product_ids.append(product.id)
        except Exception as e:
            print(f"⚠️ Product may already exist: {name}")
    
    print(f"✅ Created {len(product_ids)} products")
    
    # Add sample sales
    if product_ids:
        num_sales = 50
        for i in range(num_sales):
            order_id = f"ORD-{random.randint(10000, 99999)}"
            product_id = random.choice(product_ids)
            amount = random.uniform(50, 2000)
            quantity = random.randint(1, 5)
            sale_date = datetime.now() - timedelta(days=random.randint(0, 30))
            
            try:
                db_manager.create_sale(
                    order_id=order_id,
                    product_id=product_id,
                    amount=amount,
                    quantity=quantity,
                    customer_name=f"مشتری {i+1}",
                    sale_date=sale_date
                )
            except Exception as e:
                pass  # Skip duplicates
        
        print(f"✅ Created {num_sales} sample sales")
    
    # Add sample analytics data
    property_id = "GA4-SAMPLE-123"
    metrics = [
        "active_users",
        "new_users",
        "pageviews",
        "sessions",
        "engagement_rate"
    ]
    
    num_days = 30
    for day in range(num_days):
        date = datetime.now() - timedelta(days=day)
        for metric in metrics:
            value = random.uniform(100, 10000)
            try:
                db_manager.save_analytics_data(
                    property_id=property_id,
                    date=date,
                    metric_name=metric,
                    metric_value=value,
                    dimensions={"source": "organic", "country": "US"}
                )
            except Exception:
                pass
    
    print(f"✅ Created {len(metrics) * num_days} analytics data points")
    
    # Add sample alerts
    alerts_config = [
        ("افت ترافیک", "traffic", "below", 1000.0, ["app", "email"]),
        ("افزایش خطاها", "errors", "above", 100.0, ["app", "telegram"]),
        ("کاهش فروش", "sales", "below", 5000.0, ["app", "email", "slack"]),
    ]
    
    for name, metric, condition, threshold, channels in alerts_config:
        try:
            db_manager.create_alert(name, metric, condition, threshold, channels)
        except Exception:
            pass  # Skip duplicates
    
    print(f"✅ Created {len(alerts_config)} sample alerts")
    
    # Add sample settings
    settings = [
        ("ga4_client_id", "your-client-id", "api_keys", False),
        ("ga4_client_secret", "your-client-secret", "api_keys", True),
        ("clarity_api_key", "your-clarity-key", "api_keys", True),
        ("openai_api_key", "your-openai-key", "api_keys", True),
        ("auto_refresh_interval", "60", "display", False),
        ("theme", "light", "display", False),
    ]
    
    for key, value, category, is_encrypted in settings:
        try:
            db_manager.set_setting(key, value, category, is_encrypted)
        except Exception:
            pass
    
    print(f"✅ Created {len(settings)} sample settings")


def main():
    """Main function"""
    print("=" * 60)
    print("     Analysis Dashboard - Database Initialization")
    print("=" * 60)
    
    try:
        # Initialize database
        init_database()
        
        # Populate sample data
        populate_sample_data()
        
        print("\n" + "=" * 60)
        print("✅ Database initialization completed successfully!")
        print("=" * 60)
        print("\n📋 Summary:")
        print("  - Database tables created")
        print("  - Admin user: username='admin', password='admin'")
        print("  - Sample products, sales, and analytics data added")
        print("  - Sample alerts and settings configured")
        print("\n🚀 You can now run the application:")
        print("   python src/main.py")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
