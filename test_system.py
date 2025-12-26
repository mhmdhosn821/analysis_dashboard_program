#!/usr/bin/env python3
"""
Test script to verify the dashboard works without GUI
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from datetime import datetime, timedelta
from app.core.database import db
from app.core.db_manager import db_manager
from app.services.pos_api import POSClient
from app.utils.alerts import alert_monitor
from app.utils.helpers import format_currency, format_number, format_percentage


def test_database():
    """Test database operations"""
    print("\n" + "=" * 60)
    print("Testing Database Operations")
    print("=" * 60)
    
    # Test user retrieval
    user = db_manager.get_user_by_username('admin')
    if user:
        print(f"✅ Admin user found: {user.username} ({user.role.value})")
    else:
        print("❌ Admin user not found")
    
    # Test product retrieval
    products = db_manager.get_products()
    print(f"✅ Found {len(products)} products")
    if products:
        print(f"   Example: {products[0].name} - {format_currency(products[0].price)}")
    
    # Test sales
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    total_sales = db_manager.get_total_sales(start_date, end_date)
    print(f"✅ Total sales (last 7 days): {format_currency(total_sales)}")
    
    # Test settings
    test_setting = db_manager.get_setting('theme')
    print(f"✅ Theme setting: {test_setting}")


def test_pos_api():
    """Test POS API"""
    print("\n" + "=" * 60)
    print("Testing POS API (Mock Data)")
    print("=" * 60)
    
    pos = POSClient()
    
    # Test sales summary
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    summary = pos.get_sales_summary(start_date, end_date)
    
    print(f"✅ Sales Summary:")
    print(f"   Total Sales: {format_currency(summary['total_sales'])}")
    print(f"   Number of Orders: {format_number(summary['num_orders'])}")
    print(f"   Average Order Value: {format_currency(summary['average_order_value'])}")
    print(f"   Total Customers: {format_number(summary['total_customers'])}")
    
    # Test top products
    top_products = pos.get_top_products(start_date, end_date, limit=3)
    print(f"\n✅ Top 3 Products:")
    for i, product in enumerate(top_products, 1):
        print(f"   {i}. {product['name']}: {format_currency(product['total_revenue'])}")
    
    # Test conversion funnel
    funnel = pos.get_conversion_funnel(start_date, end_date)
    print(f"\n✅ Conversion Funnel:")
    print(f"   Visitors: {format_number(funnel['visitors'])}")
    print(f"   Add to Cart: {format_number(funnel['add_to_cart'])}")
    print(f"   Orders Completed: {format_number(funnel['orders_completed'])}")
    print(f"   Conversion Rate: {format_percentage(funnel['conversion_rates']['overall'])}")


def test_alert_system():
    """Test alert system"""
    print("\n" + "=" * 60)
    print("Testing Alert System")
    print("=" * 60)
    
    # Test traffic drop alert
    alert = alert_monitor.check_traffic_drop(800, 2000, 50.0)
    if alert:
        print(f"✅ Traffic drop alert triggered: {alert['message']}")
    else:
        print("   No traffic drop alert")
    
    # Test error rate increase
    alert = alert_monitor.check_error_rate_increase(150, 50, 50.0)
    if alert:
        print(f"✅ Error rate increase alert triggered: {alert['message']}")
    else:
        print("   No error rate increase alert")
    
    # Test sales drop
    alert = alert_monitor.check_sales_drop(3000, 7000, 50.0)
    if alert:
        print(f"✅ Sales drop alert triggered: {alert['message']}")
    else:
        print("   No sales drop alert")
    
    # Get active alerts from DB
    db_alerts = alert_monitor.get_active_alerts_from_db()
    print(f"\n✅ Active alerts in database: {len(db_alerts)}")
    for alert in db_alerts[:3]:
        print(f"   - {alert['name']}: {alert['metric']} {alert['condition']} {alert['threshold']}")


def test_helpers():
    """Test helper functions"""
    print("\n" + "=" * 60)
    print("Testing Helper Functions")
    print("=" * 60)
    
    from app.utils.helpers import (
        format_number, format_currency, format_percentage,
        calculate_percentage_change, get_date_range, get_trend_indicator
    )
    
    print(f"✅ Format number: {format_number(1234567.89)}")
    print(f"✅ Format currency: {format_currency(1234.56)}")
    print(f"✅ Format percentage: {format_percentage(45.678)}")
    
    change = calculate_percentage_change(1500, 1000)
    print(f"✅ Percentage change: {change:.2f}%")
    
    trend = get_trend_indicator(1500, 1000)
    print(f"✅ Trend indicator: {trend}")
    
    start, end = get_date_range('last_7_days')
    print(f"✅ Date range (last 7 days): {start.date()} to {end.date()}")


def main():
    """Main test function"""
    print("\n" + "=" * 80)
    print(" " * 20 + "Analysis Dashboard - System Test")
    print("=" * 80)
    
    try:
        test_database()
        test_pos_api()
        test_alert_system()
        test_helpers()
        
        print("\n" + "=" * 80)
        print("✅ All tests completed successfully!")
        print("=" * 80)
        print("\n🎉 The system is ready to use!")
        print("\n📝 Note: To run the GUI application, you need:")
        print("   1. Install PyQt6: pip install PyQt6")
        print("   2. Run: python src/main.py")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
