"""
English localization
"""

TRANSLATIONS = {
    # General
    "app_name": "Analysis Management Dashboard",
    "welcome": "Welcome",
    "loading": "Loading...",
    "error": "Error",
    "success": "Success",
    "warning": "Warning",
    "info": "Information",
    "cancel": "Cancel",
    "save": "Save",
    "delete": "Delete",
    "edit": "Edit",
    "add": "Add",
    "close": "Close",
    "refresh": "Refresh",
    "export": "Export",
    "settings": "Settings",
    
    # Authentication
    "login": "Login",
    "logout": "Logout",
    "username": "Username",
    "password": "Password",
    "email": "Email",
    "remember_me": "Remember me",
    "forgot_password": "Forgot password",
    "2fa_code": "2FA Code",
    "enter_2fa_code": "Enter verification code",
    
    # Dashboard
    "dashboard": "Dashboard",
    "performance_overview": "Performance Overview",
    "user_behavior": "User Behavior",
    "product_sales": "Product Sales",
    "campaign_metrics": "Campaign Metrics",
    "tech_performance": "Tech Performance",
    
    # Metrics
    "total_users": "Total Users",
    "active_users": "Active Users",
    "new_users": "New Users",
    "returning_users": "Returning Users",
    "sessions": "Sessions",
    "avg_session_duration": "Avg. Session Duration",
    "bounce_rate": "Bounce Rate",
    "engagement_rate": "Engagement Rate",
    "conversion_rate": "Conversion Rate",
    "total_revenue": "Total Revenue",
    "total_sales": "Total Sales",
    "orders": "Orders",
    "aov": "Average Order Value",
    
    # Time ranges
    "last_7_days": "Last 7 Days",
    "last_30_days": "Last 30 Days",
    "last_90_days": "Last 90 Days",
    "custom_range": "Custom Range",
    "from_date": "From Date",
    "to_date": "To Date",
    
    # Charts
    "line_chart": "Line Chart",
    "bar_chart": "Bar Chart",
    "pie_chart": "Pie Chart",
    "heatmap": "Heatmap",
    "gauge": "Gauge",
    "table": "Table",
    
    # User roles
    "super_admin": "Super Admin",
    "admin": "Admin",
    "manager": "Manager",
    "viewer": "Viewer",
    "analyst": "Analyst",
    
    # Alerts
    "alerts": "Alerts",
    "create_alert": "Create Alert",
    "alert_name": "Alert Name",
    "metric": "Metric",
    "threshold": "Threshold",
    "channels": "Channels",
    
    # Reports
    "reports": "Reports",
    "generate_report": "Generate Report",
    "schedule_report": "Schedule Report",
    "report_template": "Report Template",
    
    # Settings
    "general_settings": "General Settings",
    "brand_settings": "Brand Settings",
    "integration_settings": "Integration Settings",
    "notification_settings": "Notification Settings",
    "organization_name": "Organization Name",
    "logo": "Logo",
    "theme": "Theme",
    "light_theme": "Light Theme",
    "dark_theme": "Dark Theme",
    "language": "Language",
    "timezone": "Timezone",
    "currency": "Currency",
    
    # Google Analytics
    "google_analytics": "Google Analytics",
    "connect_ga": "Connect GA4",
    "disconnect_ga": "Disconnect GA4",
    "property_id": "Property ID",
    
    # Microsoft Clarity
    "clarity": "Microsoft Clarity",
    "connect_clarity": "Connect Clarity",
    "disconnect_clarity": "Disconnect Clarity",
    "project_id": "Project ID",
    
    # AI Services
    "ai_insights": "AI Insights",
    "ai_provider": "AI Provider",
    "api_key": "API Key",
    "summarize": "Summarize",
    "forecast": "Forecast",
    "anomalies": "Anomalies",
    "recommendations": "Recommendations",
    
    # Messages
    "login_success": "Login successful",
    "login_failed": "Login failed",
    "save_success": "Saved successfully",
    "save_failed": "Save failed",
    "connection_success": "Connection successful",
    "connection_failed": "Connection failed",
    "data_loaded": "Data loaded",
    "no_data": "No data available",
    
    # Errors
    "invalid_credentials": "Invalid username or password",
    "network_error": "Network error",
    "server_error": "Server error",
    "permission_denied": "Permission denied",
}


def get_translation(key: str, default: str = "") -> str:
    """Get translation for a key"""
    return TRANSLATIONS.get(key, default or key)


# Alias
_ = get_translation
