# Architecture Documentation

## Overview

The Analysis Dashboard is built using a modern, layered architecture that separates concerns and promotes maintainability and scalability.

## Architecture Layers

### 1. Core Layer (`src/app/core/`)

The foundation of the application containing essential utilities:

- **config.py**: Configuration management with encryption
  - Brand settings (logo, colors, organization name)
  - Database connection settings
  - Application preferences (language, theme, timezone)
  - API credentials (encrypted storage)
  
- **security.py**: Security utilities
  - Password hashing using PBKDF2
  - Two-factor authentication (TOTP)
  - JWT token management
  - Session management
  - IP whitelisting
  - Rate limiting
  - Data encryption
  
- **database.py**: Database models and ORM
  - User management
  - Role-based access control
  - Audit logging
  - Dashboard and widget storage
  - Alert configurations
  - Report templates
  - Data caching
  
- **cache.py**: In-memory caching system
  - TTL-based expiration
  - Automatic cleanup
  - Performance optimization

### 2. Services Layer (`src/app/services/`)

Integration with external services:

- **google_analytics.py**: Google Analytics 4 API
  - OAuth2 authentication flow
  - Multi-property support
  - Metrics retrieval (users, sessions, revenue, etc.)
  - Custom reports and queries
  
- **clarity.py**: Microsoft Clarity API
  - Project statistics
  - Heatmap data
  - Session recordings
  - User behavior insights
  
- **ai_service.py**: AI/ML integration
  - OpenAI (GPT-4)
  - Google Gemini
  - Claude (Anthropic)
  - Features:
    - Data summarization
    - Trend forecasting
    - Anomaly detection
    - Recommendation engine
    - Natural language queries
    
- **notification.py**: Multi-channel notifications
  - Email (SMTP)
  - Telegram Bot
  - Slack Webhooks
  - In-app notifications

### 3. UI Layer (`src/app/ui/`)

User interface components built with PyQt6:

- **login_window.py**: Authentication interface
  - Username/password input
  - 2FA code entry
  - Remember me option
  - RTL support
  
- **main_window.py**: Main application window
  - Menu bar with all features
  - Toolbar for quick access
  - Tab-based dashboard layout
  - Status bar with connection status
  - Auto-refresh timer
  
- **styles/glassmorphism.py**: Design system
  - Light and dark themes
  - Glassmorphism effects
  - Consistent styling
  - RTL-aware layouts
  
- **dashboard/**: Dashboard components (to be implemented)
- **widgets/**: Reusable UI widgets (to be implemented)
- **settings/**: Settings panels (to be implemented)

### 4. Localization Layer (`src/app/locales/`)

Multi-language support:

- **fa.py**: Persian (Farsi) translations
- **en.py**: English translations
- Translation function for easy use throughout the app

### 5. Models Layer (`src/app/models/`)

Data models (future expansion):
- Business logic models
- Data transformation utilities
- Validation schemas

### 6. Utils Layer (`src/app/utils/`)

Helper utilities (future expansion):
- Date/time utilities
- Formatting functions
- Export helpers

## Data Flow

```
User Input
    ↓
UI Layer (PyQt6)
    ↓
Services Layer
    ↓
External APIs (GA4, Clarity, AI)
    ↓
Data Processing
    ↓
Cache Layer
    ↓
Database Layer
    ↓
UI Display
```

## Security Architecture

### Authentication Flow

1. User enters credentials
2. Password verified against hash
3. 2FA token validated (if enabled)
4. JWT token generated
5. Session created in database
6. Token stored securely

### Authorization Flow

1. User action requested
2. JWT token validated
3. User role checked
4. Permission verified
5. Action allowed/denied
6. Audit log entry created

## Database Schema

### Users Table
- User credentials
- Role assignment
- 2FA settings
- Last login tracking

### Sessions Table
- Active sessions
- Token management
- IP tracking
- Expiration handling

### Dashboards Table
- Dashboard configurations
- Owner tracking
- Layout storage

### Widgets Table
- Widget definitions
- Data source mappings
- Position and size
- Configuration settings

### Alerts Table
- Alert definitions
- Threshold values
- Channel preferences
- Active/inactive status

### Audit Logs Table
- User actions
- Timestamp tracking
- Resource access
- Detail storage

## API Integration Architecture

### Google Analytics 4

**Authentication**: OAuth2 with refresh token
**Rate Limiting**: Handled by service layer
**Data Caching**: 5-minute TTL for metrics

### Microsoft Clarity

**Authentication**: API Key
**Rate Limiting**: Applied per project
**Data Caching**: 10-minute TTL for heatmaps

### AI Services

**Authentication**: API Keys (encrypted)
**Provider Fallback**: Automatic failover
**Request Queuing**: Async processing

## Performance Optimization

### Caching Strategy

1. **In-Memory Cache**: Fast access for frequent queries
2. **Database Cache**: Historical data storage
3. **TTL Management**: Automatic expiration
4. **Cache Invalidation**: On data updates

### Lazy Loading

- Widgets load data on demand
- Dashboards render progressively
- Images and charts load asynchronously

### Connection Pooling

- Database connection pool (5-10 connections)
- API request pooling
- Thread pool for background tasks

## Scalability Considerations

### Horizontal Scaling

- Stateless session management (JWT)
- Distributed caching (Redis support)
- Load balancer compatible

### Vertical Scaling

- Efficient database queries
- Indexed tables
- Optimized data structures

## Future Enhancements

### Planned Features

1. **Microservices Architecture**
   - Separate API service
   - Background worker service
   - Report generation service

2. **Real-time Updates**
   - WebSocket support
   - Live dashboard updates
   - Notification streaming

3. **Advanced Analytics**
   - Predictive modeling
   - Custom ML models
   - Advanced forecasting

4. **Enhanced Security**
   - Biometric authentication
   - Hardware security keys
   - Advanced threat detection

## Technology Stack

### Backend
- Python 3.11+
- SQLAlchemy ORM
- PostgreSQL Database
- Cryptography library

### Frontend
- PyQt6 framework
- Custom Glassmorphism theme
- RTL layout support

### APIs
- Google Analytics Data API
- Microsoft Clarity API
- OpenAI API
- Google Gemini API
- Anthropic Claude API

### Communication
- SMTP for emails
- Telegram Bot API
- Slack Webhooks

## Development Guidelines

### Code Style
- PEP 8 compliant
- Type hints for functions
- Comprehensive docstrings
- RTL-friendly variable names

### Testing
- Unit tests for all modules
- Integration tests for services
- UI tests for critical flows
- Minimum 80% code coverage

### Documentation
- Inline code documentation
- API documentation
- User guides
- Architecture documents

## Deployment Architecture

### Desktop Application
- Windows 10+ support
- Single executable package
- Auto-update mechanism
- Local data storage

### Configuration
- User-specific config directory
- Encrypted secrets storage
- Portable settings

### Updates
- Automatic version checking
- Background downloading
- User-prompted installation

## Monitoring and Logging

### Application Logs
- Error logging
- Access logging
- Performance metrics
- Debug information

### Audit Logs
- User actions
- Data access
- Configuration changes
- Security events

### Health Checks
- Service availability
- Database connection
- API connectivity
- Resource usage

---

*Document Version: 1.0*  
*Last Updated: 2024*  
*Zagros Pro Technical Team*
