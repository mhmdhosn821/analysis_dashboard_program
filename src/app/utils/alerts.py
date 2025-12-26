"""
Alert System - Monitor metrics and trigger notifications
"""
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
from app.core.db_manager import db_manager
from app.services.notification import NotificationService


class AlertMonitor:
    """Monitor metrics and trigger alerts"""
    
    def __init__(self):
        self.notification_service = NotificationService()
        self.last_check = {}
    
    def check_traffic_drop(self, current_traffic: int, previous_traffic: int,
                          threshold_percent: float = 50.0) -> Optional[Dict]:
        """
        Check for traffic drop
        
        Args:
            current_traffic: Current traffic count
            previous_traffic: Previous traffic count
            threshold_percent: Threshold percentage for alert
            
        Returns:
            Alert data if triggered, None otherwise
        """
        if previous_traffic == 0:
            return None
        
        drop_percent = ((previous_traffic - current_traffic) / previous_traffic) * 100
        
        if drop_percent >= threshold_percent:
            return {
                'type': 'traffic_drop',
                'severity': 'warning',
                'message': f'افت ترافیک: {drop_percent:.1f}% کاهش نسبت به دوره قبل',
                'current_value': current_traffic,
                'previous_value': previous_traffic,
                'threshold': threshold_percent
            }
        
        return None
    
    def check_error_rate_increase(self, current_errors: int, previous_errors: int,
                                  threshold_percent: float = 50.0) -> Optional[Dict]:
        """
        Check for error rate increase
        
        Args:
            current_errors: Current error count
            previous_errors: Previous error count
            threshold_percent: Threshold percentage for alert
            
        Returns:
            Alert data if triggered, None otherwise
        """
        if previous_errors == 0:
            # If previous was 0 and current is not, that's significant
            if current_errors > 0:
                return {
                    'type': 'error_increase',
                    'severity': 'error',
                    'message': f'افزایش خطاها: {current_errors} خطای جدید شناسایی شد',
                    'current_value': current_errors,
                    'previous_value': previous_errors,
                    'threshold': threshold_percent
                }
            return None
        
        increase_percent = ((current_errors - previous_errors) / previous_errors) * 100
        
        if increase_percent >= threshold_percent:
            return {
                'type': 'error_increase',
                'severity': 'error',
                'message': f'افزایش خطاها: {increase_percent:.1f}% افزایش نسبت به دوره قبل',
                'current_value': current_errors,
                'previous_value': previous_errors,
                'threshold': threshold_percent
            }
        
        return None
    
    def check_sales_drop(self, current_sales: float, previous_sales: float,
                        threshold_percent: float = 50.0) -> Optional[Dict]:
        """
        Check for sales drop
        
        Args:
            current_sales: Current sales amount
            previous_sales: Previous sales amount
            threshold_percent: Threshold percentage for alert
            
        Returns:
            Alert data if triggered, None otherwise
        """
        if previous_sales == 0:
            return None
        
        drop_percent = ((previous_sales - current_sales) / previous_sales) * 100
        
        if drop_percent >= threshold_percent:
            return {
                'type': 'sales_drop',
                'severity': 'warning',
                'message': f'کاهش فروش: {drop_percent:.1f}% کاهش نسبت به دوره قبل',
                'current_value': current_sales,
                'previous_value': previous_sales,
                'threshold': threshold_percent
            }
        
        return None
    
    def check_conversion_rate_drop(self, current_rate: float, previous_rate: float,
                                   threshold_percent: float = 20.0) -> Optional[Dict]:
        """
        Check for conversion rate drop
        
        Args:
            current_rate: Current conversion rate (0-100)
            previous_rate: Previous conversion rate (0-100)
            threshold_percent: Threshold percentage for alert
            
        Returns:
            Alert data if triggered, None otherwise
        """
        if previous_rate == 0:
            return None
        
        drop_percent = ((previous_rate - current_rate) / previous_rate) * 100
        
        if drop_percent >= threshold_percent:
            return {
                'type': 'conversion_drop',
                'severity': 'warning',
                'message': f'کاهش نرخ تبدیل: {drop_percent:.1f}% کاهش نسبت به دوره قبل',
                'current_value': current_rate,
                'previous_value': previous_rate,
                'threshold': threshold_percent
            }
        
        return None
    
    def trigger_alert(self, alert_data: Dict, channels: List[str]):
        """
        Trigger alert and send notifications
        
        Args:
            alert_data: Alert information
            channels: List of notification channels
        """
        # Format message
        message = self._format_alert_message(alert_data)
        
        # Send notifications
        results = {}
        for channel in channels:
            if channel == 'email':
                results['email'] = self.notification_service.send_email(
                    to_address="admin@example.com",
                    subject=f"هشدار: {alert_data['type']}",
                    body=message
                )
            elif channel == 'telegram':
                results['telegram'] = self.notification_service.send_telegram(message)
            elif channel == 'slack':
                results['slack'] = self.notification_service.send_slack(message)
            elif channel == 'app':
                results['app'] = True  # App notification handled by UI
        
        return results
    
    def _format_alert_message(self, alert_data: Dict) -> str:
        """Format alert message"""
        severity_emoji = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'error': '❌',
            'success': '✅'
        }
        
        emoji = severity_emoji.get(alert_data.get('severity', 'info'), 'ℹ️')
        
        message = f"{emoji} {alert_data['message']}\n\n"
        message += f"مقدار فعلی: {alert_data.get('current_value', 'N/A')}\n"
        message += f"مقدار قبلی: {alert_data.get('previous_value', 'N/A')}\n"
        message += f"آستانه: {alert_data.get('threshold', 'N/A')}%\n"
        message += f"زمان: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return message
    
    def monitor_metrics(self, metrics: Dict[str, Any], thresholds: Dict[str, float]):
        """
        Monitor all metrics and trigger alerts if needed
        
        Args:
            metrics: Dictionary of current metrics
            thresholds: Dictionary of alert thresholds
        """
        alerts_triggered = []
        
        # Check traffic
        if 'current_traffic' in metrics and 'previous_traffic' in metrics:
            alert = self.check_traffic_drop(
                metrics['current_traffic'],
                metrics['previous_traffic'],
                thresholds.get('traffic_drop_percent', 50.0)
            )
            if alert:
                alerts_triggered.append(alert)
        
        # Check errors
        if 'current_errors' in metrics and 'previous_errors' in metrics:
            alert = self.check_error_rate_increase(
                metrics['current_errors'],
                metrics['previous_errors'],
                thresholds.get('error_increase_percent', 50.0)
            )
            if alert:
                alerts_triggered.append(alert)
        
        # Check sales
        if 'current_sales' in metrics and 'previous_sales' in metrics:
            alert = self.check_sales_drop(
                metrics['current_sales'],
                metrics['previous_sales'],
                thresholds.get('sales_drop_percent', 50.0)
            )
            if alert:
                alerts_triggered.append(alert)
        
        # Check conversion rate
        if 'current_conversion_rate' in metrics and 'previous_conversion_rate' in metrics:
            alert = self.check_conversion_rate_drop(
                metrics['current_conversion_rate'],
                metrics['previous_conversion_rate'],
                thresholds.get('conversion_drop_percent', 20.0)
            )
            if alert:
                alerts_triggered.append(alert)
        
        return alerts_triggered
    
    def get_active_alerts_from_db(self) -> List[Dict]:
        """Get all active alerts from database"""
        alerts = db_manager.get_active_alerts()
        return [
            {
                'id': alert.id,
                'name': alert.name,
                'metric': alert.metric,
                'condition': alert.condition,
                'threshold': alert.threshold,
                'channels': alert.channels
            }
            for alert in alerts
        ]
    
    def evaluate_custom_alert(self, alert: Dict, current_value: float) -> bool:
        """
        Evaluate if a custom alert should be triggered
        
        Args:
            alert: Alert configuration
            current_value: Current metric value
            
        Returns:
            True if alert should be triggered
        """
        condition = alert.get('condition', 'above')
        threshold = alert.get('threshold', 0)
        
        if condition == 'above' or condition == 'بیشتر از':
            return current_value > threshold
        elif condition == 'below' or condition == 'کمتر از':
            return current_value < threshold
        elif condition == 'equals' or condition == 'برابر':
            return abs(current_value - threshold) < 0.01
        
        return False


# Global alert monitor instance
alert_monitor = AlertMonitor()
