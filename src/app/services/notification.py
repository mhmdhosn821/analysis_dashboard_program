"""
Notification Service for alerts
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telegram import Bot
from slack_sdk.webhook import WebhookClient
from typing import List, Dict, Any, Optional
import asyncio


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
        self.bot = Bot(token=bot_token)
        self.chat_id = chat_id
    
    async def send_async(self, message: str) -> bool:
        """Send Telegram message asynchronously"""
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
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize notification service
        
        Args:
            config: Notification configuration
        """
        self.email = None
        self.telegram = None
        self.slack = None
        
        # Initialize email if configured
        if config.get('email_enabled'):
            self.email = EmailNotification(
                config['email_smtp_host'],
                config['email_smtp_port'],
                config['email_username'],
                config['email_password']
            )
        
        # Initialize Telegram if configured
        if config.get('telegram_enabled'):
            self.telegram = TelegramNotification(
                config['telegram_bot_token'],
                config['telegram_chat_id']
            )
        
        # Initialize Slack if configured
        if config.get('slack_enabled'):
            self.slack = SlackNotification(config['slack_webhook_url'])
    
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
