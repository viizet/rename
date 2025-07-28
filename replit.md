# AI-Powered Telegram Thumbnail Bot

## Overview

This is a complete, production-ready Telegram bot built with Python that allows users to add custom thumbnails to their video files. The bot processes video files, applies user-provided thumbnail images, and returns the modified videos. It includes premium user features, AI-powered enhancements, admin controls, and comprehensive user management. **The project is now fully prepared for GitHub deployment with complete documentation, deployment scripts, and multiple deployment options.**

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes (January 2024)

✅ **Simple File Structure Version Complete**
- Created `simple_bot.py` - everything in one file, no folders
- Removed AI features as requested by user
- Maintained all core thumbnail functionality
- Added simple admin commands (ban, unban, stats, premium)
- Created simplified documentation and setup files
- Single file structure for easy GitHub deployment
- No complex folder hierarchy - just essential files

## System Architecture

The application follows a modular architecture pattern with clear separation of concerns:

### Backend Architecture
- **Framework**: Pyrogram (Telegram Bot API wrapper)
- **Language**: Python 3.x with async/await patterns
- **Architecture Pattern**: Handler-based modular design
- **Database ORM**: SQLAlchemy with declarative base models

### Core Components Structure
```
├── main.py              # Application entry point and bot initialization
├── config.py            # Configuration management
├── models.py            # Database models and schemas
├── handlers/            # Request handlers by functionality
│   ├── user_commands.py # User command handlers
│   ├── admin_commands.py# Admin command handlers
│   └── file_handlers.py # File processing handlers
└── utils/               # Utility modules
    ├── database.py      # Database operations
    ├── auth.py          # Authentication and authorization
    ├── video_processor.py# Video processing with FFmpeg
    └── ai_helpers.py    # OpenAI integration
```

## Key Components

### 1. Database Layer
- **Technology**: SQLAlchemy ORM with support for multiple database backends
- **Models**: User management, thumbnail storage, captions, file processing logs, bot statistics, admin actions
- **Features**: User state management, premium subscriptions, activity tracking

### 2. Authentication & Authorization
- **Multi-level Access**: Owner, admin users, authenticated users, regular users
- **User Management**: Ban/unban functionality, premium user features
- **State Management**: Tracks user interaction states for multi-step operations

### 3. File Processing Engine
- **Video Processing**: FFmpeg integration for thumbnail application
- **Supported Formats**: Multiple video formats (MP4, AVI, MKV, MOV, etc.)
- **Thumbnail Formats**: JPEG, PNG, WebP support
- **File Size Limits**: Different limits for free and premium users

### 4. AI Integration
- **Provider**: OpenAI GPT-4o for AI-powered features
- **Features**: Thumbnail description generation using vision capabilities
- **Optional**: AI features gracefully degrade when API key not provided

### 5. Bot Command System
- **User Commands**: Start, help, settings, file upload handling
- **Admin Commands**: User management, ban/unban, premium subscriptions
- **File Handlers**: Photo uploads for thumbnails, video processing

## Data Flow

1. **User Registration**: Automatic user creation on first interaction
2. **Authentication Check**: Verify user permissions and ban status
3. **File Upload Processing**:
   - Receive photo → Store as user thumbnail
   - Receive video → Apply stored thumbnail → Return processed video
4. **AI Enhancement**: Optional thumbnail analysis and description
5. **State Management**: Track user progress through multi-step operations
6. **Admin Operations**: User management, statistics, system monitoring

## External Dependencies

### Required Services
- **Telegram Bot API**: Core bot functionality (API_ID, API_HASH, BOT_TOKEN)
- **Database**: Configurable via DATABASE_URL (PostgreSQL recommended)

### Optional Services
- **OpenAI API**: AI-powered thumbnail descriptions (OPENAI_API_KEY)
- **Force Subscribe Channel**: Optional user subscription enforcement

### System Dependencies
- **FFmpeg**: Video processing and thumbnail application
- **Python Libraries**: Pyrogram, SQLAlchemy, OpenAI client

## Deployment Strategy

### Environment Configuration
The application uses environment variables for all configuration:
- Telegram API credentials (required)
- Database connection string (required)
- OpenAI API key (optional)
- User access control lists
- File processing limits and paths

### File Storage
- **Temporary Files**: Configurable temporary directory for processing
- **Thumbnail Storage**: Database-stored thumbnail references
- **Processing Pipeline**: Download → Process → Upload → Cleanup

### Scalability Considerations
- Async/await patterns for concurrent request handling
- Session-based database connections
- Configurable file size limits based on user tiers
- Modular handler system for easy feature extension

### Error Handling
- Comprehensive logging throughout the application
- Graceful degradation when optional services unavailable
- User-friendly error messages for common failures
- Database transaction management with rollback support