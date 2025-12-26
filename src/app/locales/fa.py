"""
Persian (Farsi) localization
"""

TRANSLATIONS = {
    # General
    "app_name": "داشبورد مدیریتی آنالیز",
    "welcome": "خوش آمدید",
    "loading": "در حال بارگذاری...",
    "error": "خطا",
    "success": "موفق",
    "warning": "هشدار",
    "info": "اطلاعات",
    "cancel": "لغو",
    "save": "ذخیره",
    "delete": "حذف",
    "edit": "ویرایش",
    "add": "افزودن",
    "close": "بستن",
    "refresh": "بروزرسانی",
    "export": "خروجی",
    "settings": "تنظیمات",
    
    # Authentication
    "login": "ورود",
    "logout": "خروج",
    "username": "نام کاربری",
    "password": "رمز عبور",
    "email": "ایمیل",
    "remember_me": "مرا به خاطر بسپار",
    "forgot_password": "فراموشی رمز عبور",
    "2fa_code": "کد تایید دو مرحله‌ای",
    "enter_2fa_code": "کد تایید را وارد کنید",
    
    # Dashboard
    "dashboard": "داشبورد",
    "performance_overview": "بررسی عملکرد",
    "user_behavior": "رفتار کاربران",
    "product_sales": "فروش محصولات",
    "campaign_metrics": "معیارهای کمپین",
    "tech_performance": "عملکرد فنی",
    
    # Metrics
    "total_users": "کل کاربران",
    "active_users": "کاربران فعال",
    "new_users": "کاربران جدید",
    "returning_users": "کاربران بازگشتی",
    "sessions": "بازدیدها",
    "avg_session_duration": "میانگین مدت بازدید",
    "bounce_rate": "نرخ پرش",
    "engagement_rate": "نرخ تعامل",
    "conversion_rate": "نرخ تبدیل",
    "total_revenue": "کل درآمد",
    "total_sales": "کل فروش",
    "orders": "سفارشات",
    "aov": "میانگین ارزش سفارش",
    
    # Time ranges
    "last_7_days": "۷ روز گذشته",
    "last_30_days": "۳۰ روز گذشته",
    "last_90_days": "۹۰ روز گذشته",
    "custom_range": "بازه سفارشی",
    "from_date": "از تاریخ",
    "to_date": "تا تاریخ",
    
    # Charts
    "line_chart": "نمودار خطی",
    "bar_chart": "نمودار میله‌ای",
    "pie_chart": "نمودار دایره‌ای",
    "heatmap": "نقشه حرارتی",
    "gauge": "گیج",
    "table": "جدول",
    
    # User roles
    "super_admin": "مدیر ارشد",
    "admin": "مدیر",
    "manager": "مدیر میانی",
    "viewer": "مشاهده‌گر",
    "analyst": "تحلیلگر",
    
    # Alerts
    "alerts": "هشدارها",
    "create_alert": "ایجاد هشدار",
    "alert_name": "نام هشدار",
    "metric": "معیار",
    "threshold": "آستانه",
    "channels": "کانال‌ها",
    
    # Reports
    "reports": "گزارش‌ها",
    "generate_report": "تولید گزارش",
    "schedule_report": "زمان‌بندی گزارش",
    "report_template": "قالب گزارش",
    
    # Settings
    "general_settings": "تنظیمات عمومی",
    "brand_settings": "تنظیمات برند",
    "integration_settings": "تنظیمات یکپارچگی",
    "notification_settings": "تنظیمات اعلان",
    "organization_name": "نام سازمان",
    "logo": "لوگو",
    "theme": "پوسته",
    "light_theme": "پوسته روشن",
    "dark_theme": "پوسته تیره",
    "language": "زبان",
    "timezone": "منطقه زمانی",
    "currency": "واحد پول",
    
    # Google Analytics
    "google_analytics": "گوگل آنالیتیکس",
    "connect_ga": "اتصال به GA4",
    "disconnect_ga": "قطع اتصال GA4",
    "property_id": "شناسه پراپرتی",
    
    # Microsoft Clarity
    "clarity": "کلریتی مایکروسافت",
    "connect_clarity": "اتصال به Clarity",
    "disconnect_clarity": "قطع اتصال Clarity",
    "project_id": "شناسه پروژه",
    
    # AI Services
    "ai_insights": "بینش‌های هوش مصنوعی",
    "ai_provider": "ارائه‌دهنده AI",
    "api_key": "کلید API",
    "summarize": "خلاصه‌سازی",
    "forecast": "پیش‌بینی",
    "anomalies": "ناهنجاری‌ها",
    "recommendations": "پیشنهادات",
    
    # Messages
    "login_success": "ورود موفقیت‌آمیز بود",
    "login_failed": "ورود ناموفق بود",
    "save_success": "با موفقیت ذخیره شد",
    "save_failed": "ذخیره ناموفق بود",
    "connection_success": "اتصال موفق",
    "connection_failed": "اتصال ناموفق",
    "data_loaded": "داده‌ها بارگذاری شدند",
    "no_data": "داده‌ای موجود نیست",
    
    # Errors
    "invalid_credentials": "نام کاربری یا رمز عبور اشتباه است",
    "network_error": "خطای شبکه",
    "server_error": "خطای سرور",
    "permission_denied": "دسترسی رد شد",
}


def get_translation(key: str, default: str = "") -> str:
    """Get translation for a key"""
    return TRANSLATIONS.get(key, default or key)


# Alias
_ = get_translation
