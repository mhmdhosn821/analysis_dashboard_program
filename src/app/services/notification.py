"""
Notification Service for alerts
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any, Optional
import asyncio

# Optional imports for telegram and slack
try:
    from telegram import Bot
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False

try:
    from slack_sdk.webhook import WebhookClient
    SLACK_AVAILABLE = True
except ImportError:
    SLACK_AVAILABLE = False


class EmailNotification:
    """Email notification sender"""
    
    def __init__(self, smtp_host: str, smtp_port: int, username: str, password: str):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
    
    def send(self, to: List[str], subject: str, body: str, html: bool = False) -> bool:
        """
        Send email notification
        
        Args:
            to: List of recipient email addresses
            subject: Email subject
            body: Email body
            html: Whether body is HTML
        
        Returns:
            True if sent successfully
        """
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.username
            msg['To'] = ', '.join(to)
            
            if html:
                msg.attach(MIMEText(body, 'html', 'utf-8'))
            else:
                msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False


class TelegramNotification:
    """Telegram notification sender"""
    
    def __init__(self, bot_token: str, chat_id: str):
        if not TELEGRAM_AVAILABLE:
            print("Warning: Telegram module not available")
            self.bot = None
            self.chat_id = None
            return
        self.bot = Bot(token=bot_token)
        self.chat_id = chat_id
    
    async def send_async(self, message: str) -> bool:
        """Send Telegram message asynchronously"""
        if not TELEGRAM_AVAILABLE or not self.bot:
            return False
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=message, parse_mode='HTML')
            return True
        except Exception as e:
            print(f"Error sending Telegram message: {e}")
            return False
    
    def send(self, message: str) -> bool:
        """
        Send Telegram notification
        
        Args:
            message: Message to send
        
        Returns:
            True if sent successfully
        """
        if not TELEGRAM_AVAILABLE or not self.bot:
            return False
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.send_async(message))
            loop.close()
            return result
        except Exception as e:
            print(f"Error in Telegram send: {e}")
            return False


class SlackNotification:
    """Slack notification sender"""
    
    def __init__(self, webhook_url: str):
        if not SLACK_AVAILABLE:
            print("Warning: Slack SDK not available")
            self.webhook = None
            return
        self.webhook = WebhookClient(webhook_url)
    
    def send(self, message: str, blocks: Optional[List[Dict]] = None) -> bool:
        """
        Send Slack notification
        
        Args:
            message: Message to send
            blocks: Optional Slack blocks for rich formatting
        
        Returns:
            True if sent successfully
        """
        if not SLACK_AVAILABLE or not self.webhook:
            return False
        try:
            if blocks:
                response = self.webhook.send(text=message, blocks=blocks)
            else:
                response = self.webhook.send(text=message)
            
            return response.status_code == 200
        except Exception as e:
            print(f"Error sending Slack message: {e}")
            return False


class NotificationService:
    """Unified notification service"""
    
    def __init__(self, config):
        """
        Initialize notification service
        
        Args:
            config: Notification configuration (NotificationConfig or dict)
        """
        self.email = None
        self.telegram = None
        self.slack = None
        
        # Handle both pydantic model and dict
        if hasattr(config, 'email_enabled'):
            # Pydantic model
            email_enabled = config.email_enabled
            telegram_enabled = config.telegram_enabled
            slack_enabled = config.slack_enabled
        else:
            # Dictionary
            email_enabled = config.get('email_enabled', False)
            telegram_enabled = config.get('telegram_enabled', False)
            slack_enabled = config.get('slack_enabled', False)
        
        # Initialize email if configured
        if email_enabled:
            smtp_host = config.email_smtp_host if hasattr(config, 'email_smtp_host') else config['email_smtp_host']
            smtp_port = config.email_smtp_port if hasattr(config, 'email_smtp_port') else config['email_smtp_port']
            username = config.email_username if hasattr(config, 'email_username') else config['email_username']
            password = config.email_password if hasattr(config, 'email_password') else config['email_password']
            
            self.email = EmailNotification(smtp_host, smtp_port, username, password)
        
        # Initialize Telegram if configured
        if telegram_enabled:
            bot_token = config.telegram_bot_token if hasattr(config, 'telegram_bot_token') else config['telegram_bot_token']
            chat_id = config.telegram_chat_id if hasattr(config, 'telegram_chat_id') else config['telegram_chat_id']
            
            self.telegram = TelegramNotification(bot_token, chat_id)
        
        # Initialize Slack if configured
        if slack_enabled:
            webhook_url = config.slack_webhook_url if hasattr(config, 'slack_webhook_url') else config['slack_webhook_url']
            
            self.slack = SlackNotification(webhook_url)
    
    def send_alert(self, alert_type: str, message: str, channels: List[str], 
                   details: Optional[Dict] = None) -> Dict[str, bool]:
        """
        Send alert through specified channels
        
        Args:
            alert_type: Type of alert (traffic_drop, crash_increase, sales_drop)
            message: Alert message
            channels: List of channels to send through (email, telegram, slack)
            details: Optional additional details
        
        Returns:
            Dictionary of channel: success status
        """
        results = {}
        
        # Format message
        formatted_message = self._format_alert_message(alert_type, message, details)
        
        # Send through each channel
        if 'email' in channels and self.email:
            results['email'] = self.email.send(
                to=details.get('email_recipients', []),
                subject=f"Alert: {alert_type}",
                body=formatted_message,
                html=True
            )
        
        if 'telegram' in channels and self.telegram:
            results['telegram'] = self.telegram.send(formatted_message)
        
        if 'slack' in channels and self.slack:
            results['slack'] = self.slack.send(formatted_message)
        
        return results
    
    def _format_alert_message(self, alert_type: str, message: str, 
                             details: Optional[Dict] = None) -> str:
        """Format alert message"""
        formatted = f"<b>🚨 Alert: {alert_type.replace('_', ' ').title()}</b>\n\n"
        formatted += f"{message}\n\n"
        
        if details:
            formatted += "<b>Details:</b>\n"
            for key, value in details.items():
                if key not in ['email_recipients']:
                    formatted += f"• {key}: {value}\n"
        
        formatted += f"\n<i>Timestamp: {details.get('timestamp', 'N/A')}</i>"
        
        return formatted
    
    def send_report(self, title: str, content: str, channels: List[str], 
                    recipients: List[str]) -> Dict[str, bool]:
        """
        Send scheduled report
        
        Args:
            title: Report title
            content: Report content
            channels: Channels to send through
            recipients: Email recipients
        
        Returns:
            Dictionary of channel: success status
        """
        results = {}
        
        if 'email' in channels and self.email:
            results['email'] = self.email.send(
                to=recipients,
                subject=title,
                body=content,
                html=True
            )
        
        return results
