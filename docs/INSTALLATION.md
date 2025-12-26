# راهنمای نصب

## پیش‌نیازها

### نرم‌افزارهای مورد نیاز

1. **Python 3.11 یا بالاتر**
   - دانلود از: https://www.python.org/downloads/
   - حتماً گزینه "Add Python to PATH" را فعال کنید

2. **PostgreSQL 14 یا بالاتر**
   - دانلود از: https://www.postgresql.org/download/
   - نصب با تنظیمات پیشفرض

3. **Git** (اختیاری، برای دانلود کد منبع)
   - دانلود از: https://git-scm.com/downloads

## مراحل نصب

### 1. دانلود کد منبع

#### روش اول: استفاده از Git
```bash
git clone https://github.com/mhmdhosn821/analysis_dashboard_program.git
cd analysis_dashboard_program
```

#### روش دوم: دانلود ZIP
1. به صفحه گیتهاب پروژه بروید
2. روی دکمه "Code" کلیک کنید
3. "Download ZIP" را انتخاب کنید
4. فایل را استخراج کنید

### 2. ایجاد محیط مجازی

```bash
python -m venv venv
```

### 3. فعالسازی محیط مجازی

#### Windows:
```bash
venv\Scripts\activate
```

#### Linux/Mac:
```bash
source venv/bin/activate
```

### 4. نصب وابستگیها

```bash
pip install -r requirements.txt
```

**نکته:** نصب ممکن است چند دقیقه طول بکشد.

### 5. راهاندازی دیتابیس

#### ایجاد دیتابیس PostgreSQL:

1. **باز کردن pgAdmin یا psql**
2. **اجرای دستورات زیر:**

```sql
CREATE DATABASE analysis_dashboard;
CREATE USER dashboard_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE analysis_dashboard TO dashboard_user;
```

#### تنظیم اطلاعات اتصال:

در اولین اجرا، برنامه فایل کانفیگ را ایجاد میکند. میتوانید آن را ویرایش کنید:

مسیر: `C:\Users\<USERNAME>\.analysis_dashboard\config.json`

```json
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "database": "analysis_dashboard",
    "username": "dashboard_user"
  }
}
```

رمز عبور دیتابیس در فایل رمزنگاری شده `secrets.enc` ذخیره میشود.

### 6. اجرای برنامه

```bash
python src/main.py
```

## اطلاعات ورود پیشفرض

- **نام کاربری:** `admin`
- **رمز عبور:** `admin`

**هشدار امنیتی:** حتماً بعد از اولین ورود، رمز عبور را تغییر دهید!

## تنظیمات اضافی

### اتصال به Google Analytics 4

1. به [Google Cloud Console](https://console.cloud.google.com/) بروید
2. یک پروژه جدید بسازید یا پروژه موجود را انتخاب کنید
3. Google Analytics Data API را فعال کنید
4. OAuth 2.0 credentials ایجاد کنید
5. Client ID و Client Secret را در برنامه وارد کنید

### اتصال به Microsoft Clarity

1. به [Clarity Dashboard](https://clarity.microsoft.com/) بروید
2. پروژه خود را انتخاب کنید
3. از بخش Settings، API Key را دریافت کنید
4. API Key را در برنامه وارد کنید

### تنظیم AI Services

برای استفاده از قابلیتهای هوش مصنوعی:

#### OpenAI:
1. به [OpenAI Platform](https://platform.openai.com/) بروید
2. API Key ایجاد کنید
3. در برنامه وارد کنید

#### Google Gemini:
1. به [Google AI Studio](https://makersuite.google.com/) بروید
2. API Key دریافت کنید
3. در برنامه وارد کنید

#### Claude (Anthropic):
1. به [Anthropic Console](https://console.anthropic.com/) بروید
2. API Key ایجاد کنید
3. در برنامه وارد کنید

## عیبیابی

### خطای Import Module

```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### خطای اتصال به دیتابیس

1. مطمئن شوید PostgreSQL در حال اجرا است
2. اطلاعات اتصال را بررسی کنید
3. دسترسیهای کاربر دیتابیس را چک کنید

### خطای PyQt6

در صورت مشکل در نصب PyQt6:

```bash
pip install PyQt6 --no-cache-dir
```

## پشتیبانی

در صورت بروز مشکل:
- [Issues در گیتهاب](https://github.com/mhmdhosn821/analysis_dashboard_program/issues)
- ایمیل: info@zagrospro.com
