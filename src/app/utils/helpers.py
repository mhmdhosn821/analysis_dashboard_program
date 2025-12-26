"""
Helper Utilities
"""
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import random
import string


def format_number(value: float, decimals: int = 0, suffix: str = "") -> str:
    """
    Format number with thousands separator
    
    Args:
        value: Number to format
        decimals: Number of decimal places
        suffix: Optional suffix (K, M, B)
        
    Returns:
        Formatted string
    """
    if suffix:
        if suffix == 'K':
            value = value / 1000
        elif suffix == 'M':
            value = value / 1_000_000
        elif suffix == 'B':
            value = value / 1_000_000_000
    
    if decimals == 0:
        return f"{int(value):,}{suffix}"
    else:
        return f"{value:,.{decimals}f}{suffix}"


def format_currency(amount: float, currency: str = "USD", symbol: str = "$") -> str:
    """
    Format currency amount
    
    Args:
        amount: Amount to format
        currency: Currency code
        symbol: Currency symbol
        
    Returns:
        Formatted currency string
    """
    return f"{symbol}{amount:,.2f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format percentage
    
    Args:
        value: Percentage value (0-100)
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    return f"{value:.{decimals}f}%"


def format_duration(seconds: int) -> str:
    """
    Format duration in human-readable format
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds} ثانیه"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} دقیقه"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours} ساعت"
    else:
        days = seconds // 86400
        return f"{days} روز"


def format_date(date: datetime, format_str: str = "%Y-%m-%d") -> str:
    """
    Format date
    
    Args:
        date: Date to format
        format_str: Format string
        
    Returns:
        Formatted date string
    """
    return date.strftime(format_str)


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime
    
    Args:
        dt: Datetime to format
        format_str: Format string
        
    Returns:
        Formatted datetime string
    """
    return dt.strftime(format_str)


def get_date_range(period: str) -> tuple:
    """
    Get date range for common periods
    
    Args:
        period: Period name (today, yesterday, last_7_days, last_30_days, this_month, last_month)
        
    Returns:
        Tuple of (start_date, end_date)
    """
    now = datetime.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    if period == 'today':
        return today, now
    elif period == 'yesterday':
        yesterday = today - timedelta(days=1)
        return yesterday, today
    elif period == 'last_7_days':
        start = today - timedelta(days=7)
        return start, now
    elif period == 'last_30_days':
        start = today - timedelta(days=30)
        return start, now
    elif period == 'this_month':
        start = today.replace(day=1)
        return start, now
    elif period == 'last_month':
        first_day_this_month = today.replace(day=1)
        last_day_last_month = first_day_this_month - timedelta(days=1)
        first_day_last_month = last_day_last_month.replace(day=1)
        return first_day_last_month, first_day_this_month
    else:
        return today, now


def calculate_percentage_change(current: float, previous: float) -> float:
    """
    Calculate percentage change
    
    Args:
        current: Current value
        previous: Previous value
        
    Returns:
        Percentage change
    """
    if previous == 0:
        return 100.0 if current > 0 else 0.0
    
    return ((current - previous) / previous) * 100


def generate_random_id(length: int = 8) -> str:
    """
    Generate random ID
    
    Args:
        length: Length of ID
        
    Returns:
        Random ID string
    """
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def validate_email(email: str) -> bool:
    """
    Validate email address
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename
    
    Args:
        filename: Filename to sanitize
        
    Returns:
        Sanitized filename
    """
    import re
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    return filename


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split list into chunks
    
    Args:
        lst: List to split
        chunk_size: Size of each chunk
        
    Returns:
        List of chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safe division that returns default on division by zero
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if division by zero
        
    Returns:
        Result of division or default
    """
    if denominator == 0:
        return default
    return numerator / denominator


def merge_dicts(*dicts: Dict) -> Dict:
    """
    Merge multiple dictionaries
    
    Args:
        *dicts: Dictionaries to merge
        
    Returns:
        Merged dictionary
    """
    result = {}
    for d in dicts:
        result.update(d)
    return result


def get_trend_indicator(current: float, previous: float) -> str:
    """
    Get trend indicator (up, down, neutral)
    
    Args:
        current: Current value
        previous: Previous value
        
    Returns:
        Trend indicator
    """
    if current > previous:
        return 'up'
    elif current < previous:
        return 'down'
    else:
        return 'neutral'


def color_for_trend(trend: str) -> str:
    """
    Get color for trend
    
    Args:
        trend: Trend indicator
        
    Returns:
        Color hex code
    """
    colors = {
        'up': '#10B981',    # Green
        'down': '#EF4444',  # Red
        'neutral': '#999'   # Gray
    }
    return colors.get(trend, '#999')


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def parse_date(date_str: str, format_str: str = "%Y-%m-%d") -> Optional[datetime]:
    """
    Parse date string
    
    Args:
        date_str: Date string to parse
        format_str: Format string
        
    Returns:
        Parsed datetime or None if invalid
    """
    try:
        return datetime.strptime(date_str, format_str)
    except ValueError:
        return None


def is_valid_url(url: str) -> bool:
    """
    Validate URL
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid, False otherwise
    """
    import re
    pattern = r'^https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b[-a-zA-Z0-9()@:%_\+.~#?&//=]*$'
    return bool(re.match(pattern, url))


def generate_color_palette(count: int, base_color: str = "#F7941D") -> List[str]:
    """
    Generate color palette
    
    Args:
        count: Number of colors
        base_color: Base color hex code
        
    Returns:
        List of color hex codes
    """
    # Simple implementation - can be enhanced with color theory
    colors = [
        '#F7941D',  # Orange
        '#F5E6D3',  # Cream
        '#2D2D2D',  # Dark
        '#10B981',  # Green
        '#3B82F6',  # Blue
        '#EF4444',  # Red
        '#F59E0B',  # Yellow
        '#8B5CF6',  # Purple
        '#EC4899',  # Pink
        '#14B8A6'   # Teal
    ]
    
    # Repeat if needed
    while len(colors) < count:
        colors.extend(colors)
    
    return colors[:count]
