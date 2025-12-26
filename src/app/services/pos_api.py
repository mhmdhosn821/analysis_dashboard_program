"""
POS Plus API Client
Handles integration with POS system for sales data
"""
import requests
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
import random


class POSClient:
    """POS Plus API Client"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize POS client
        
        Args:
            api_key: API key for authentication
            base_url: Base URL for POS API
        """
        self.api_key = api_key
        self.base_url = base_url or "https://api.posplus.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}" if api_key else "",
            "Content-Type": "application/json"
        }
    
    def is_connected(self) -> bool:
        """Check if API is connected"""
        return bool(self.api_key)
    
    def get_sales_summary(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """
        Get sales summary for date range
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            Sales summary data
        """
        if not self.is_connected():
            return self._generate_mock_sales_summary(start_date, end_date)
        
        try:
            response = requests.get(
                f"{self.base_url}/sales/summary",
                headers=self.headers,
                params={
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat()
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching sales summary: {e}")
            return self._generate_mock_sales_summary(start_date, end_date)
    
    def get_orders(self, start_date: datetime, end_date: datetime, 
                   limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get orders for date range
        
        Args:
            start_date: Start date
            end_date: End date
            limit: Maximum number of orders to return
            
        Returns:
            List of orders
        """
        if not self.is_connected():
            return self._generate_mock_orders(start_date, end_date, limit)
        
        try:
            response = requests.get(
                f"{self.base_url}/orders",
                headers=self.headers,
                params={
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'limit': limit
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json().get('orders', [])
        except Exception as e:
            print(f"Error fetching orders: {e}")
            return self._generate_mock_orders(start_date, end_date, limit)
    
    def get_top_products(self, start_date: datetime, end_date: datetime,
                        limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get top selling products
        
        Args:
            start_date: Start date
            end_date: End date
            limit: Maximum number of products to return
            
        Returns:
            List of top products
        """
        if not self.is_connected():
            return self._generate_mock_top_products(limit)
        
        try:
            response = requests.get(
                f"{self.base_url}/products/top",
                headers=self.headers,
                params={
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'limit': limit
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json().get('products', [])
        except Exception as e:
            print(f"Error fetching top products: {e}")
            return self._generate_mock_top_products(limit)
    
    def get_monthly_sales(self, year: int, month: int) -> Dict[str, Any]:
        """
        Get monthly sales breakdown
        
        Args:
            year: Year
            month: Month (1-12)
            
        Returns:
            Monthly sales data
        """
        if not self.is_connected():
            return self._generate_mock_monthly_sales(year, month)
        
        try:
            response = requests.get(
                f"{self.base_url}/sales/monthly",
                headers=self.headers,
                params={'year': year, 'month': month},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching monthly sales: {e}")
            return self._generate_mock_monthly_sales(year, month)
    
    def get_conversion_funnel(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """
        Get conversion funnel data
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            Conversion funnel data
        """
        if not self.is_connected():
            return self._generate_mock_conversion_funnel()
        
        try:
            response = requests.get(
                f"{self.base_url}/analytics/funnel",
                headers=self.headers,
                params={
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat()
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching conversion funnel: {e}")
            return self._generate_mock_conversion_funnel()
    
    # Mock data generators
    def _generate_mock_sales_summary(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Generate mock sales summary"""
        days = (end_date - start_date).days + 1
        total_sales = random.uniform(10000, 50000) * days
        num_orders = random.randint(50, 200) * days
        
        return {
            'total_sales': round(total_sales, 2),
            'num_orders': num_orders,
            'average_order_value': round(total_sales / num_orders, 2) if num_orders > 0 else 0,
            'total_customers': random.randint(30, 150) * days,
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            }
        }
    
    def _generate_mock_orders(self, start_date: datetime, end_date: datetime, limit: int) -> List[Dict[str, Any]]:
        """Generate mock orders"""
        orders = []
        for i in range(min(limit, 50)):
            order_date = start_date + timedelta(
                days=random.randint(0, (end_date - start_date).days)
            )
            orders.append({
                'order_id': f"ORD-{random.randint(10000, 99999)}",
                'customer_name': f"Customer {i+1}",
                'amount': round(random.uniform(10, 500), 2),
                'status': random.choice(['completed', 'pending', 'cancelled']),
                'order_date': order_date.isoformat(),
                'items_count': random.randint(1, 10)
            })
        return orders
    
    def _generate_mock_top_products(self, limit: int) -> List[Dict[str, Any]]:
        """Generate mock top products"""
        products = [
            'لپ‌تاپ', 'موبایل', 'تبلت', 'هدفون', 'کیبورد',
            'ماوس', 'مانیتور', 'پرینتر', 'دوربین', 'اسپیکر'
        ]
        
        return [
            {
                'product_id': i + 1,
                'name': products[i] if i < len(products) else f'محصول {i+1}',
                'sku': f'SKU-{random.randint(1000, 9999)}',
                'total_quantity': random.randint(10, 500),
                'total_revenue': round(random.uniform(1000, 10000), 2),
                'avg_price': round(random.uniform(50, 1000), 2)
            }
            for i in range(min(limit, len(products)))
        ]
    
    def _generate_mock_monthly_sales(self, year: int, month: int) -> Dict[str, Any]:
        """Generate mock monthly sales"""
        import calendar
        num_days = calendar.monthrange(year, month)[1]
        
        daily_sales = []
        for day in range(1, num_days + 1):
            daily_sales.append({
                'date': f"{year}-{month:02d}-{day:02d}",
                'sales': round(random.uniform(500, 5000), 2),
                'orders': random.randint(10, 100)
            })
        
        total_sales = sum(d['sales'] for d in daily_sales)
        total_orders = sum(d['orders'] for d in daily_sales)
        
        return {
            'year': year,
            'month': month,
            'total_sales': round(total_sales, 2),
            'total_orders': total_orders,
            'daily_breakdown': daily_sales
        }
    
    def _generate_mock_conversion_funnel(self) -> Dict[str, Any]:
        """Generate mock conversion funnel"""
        visitors = random.randint(1000, 5000)
        product_views = int(visitors * random.uniform(0.6, 0.8))
        add_to_cart = int(product_views * random.uniform(0.3, 0.5))
        checkout = int(add_to_cart * random.uniform(0.5, 0.7))
        completed = int(checkout * random.uniform(0.7, 0.9))
        
        return {
            'visitors': visitors,
            'product_views': product_views,
            'add_to_cart': add_to_cart,
            'checkout_initiated': checkout,
            'orders_completed': completed,
            'conversion_rates': {
                'view_to_cart': round((add_to_cart / product_views * 100), 2) if product_views > 0 else 0,
                'cart_to_checkout': round((checkout / add_to_cart * 100), 2) if add_to_cart > 0 else 0,
                'checkout_to_order': round((completed / checkout * 100), 2) if checkout > 0 else 0,
                'overall': round((completed / visitors * 100), 2) if visitors > 0 else 0
            }
        }
