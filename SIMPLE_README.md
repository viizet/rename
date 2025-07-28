# Simple Telegram Thumbnail Bot

A straightforward Telegram bot for adding custom thumbnails to videos. Single file structure, no folders, no AI features - just the essentials.

## Features

- Add custom thumbnails to videos using FFmpeg
- Premium user support (2GB free, 4GB premium)
- Basic admin commands (ban, unban, stats, premium management)
- SQLite database (or PostgreSQL)
- Single file structure - everything in `simple_bot.py`

## Quick Setup

```bash
# 1. Install dependencies
pip install -r simple_requirements.txt

# 2. Run setup script (optional)
python simple_setup.py

# 3. Configure environment
cp simple.env .env
# Edit .env with your credentials

# 4. Run the bot
python simple_bot.py
```

## Requirements

- Python 3.8+
- FFmpeg installed on system
- Telegram Bot API credentials

## Environment Variables

Create `.env` file:

```env
# Required
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
OWNER_ID=your_user_id
DATABASE_URL=sqlite:///bot.db

# Optional
CUSTOM_CAPTION=🎬 Processed by Simple Bot
FORCE_SUB=your_channel_username
TEMP_DIR=./temp
```

## User Commands

- `/start` - Welcome message
- `/viewthumb` - View current thumbnail
- `/delthumb` - Delete thumbnail
- `/set_caption <text>` - Set custom caption
- `/see_caption` - View current caption
- `/del_caption` - Delete caption
- `/myplan` - View subscription plan
- `/ping` - Check bot status

## Admin Commands (Owner only)

- `/stats` - Bot statistics
- `/ban <user_id>` - Ban user
- `/unban <user_id>` - Unban user
- `/addpremium <user_id>` - Grant premium access

## How It Works

1. Send a photo to set as your thumbnail
2. Send a video file to process
3. Bot applies thumbnail and returns processed video

## File Structure

```
simple-thumbnail-bot/
├── simple_bot.py           # Main bot file (everything here)
├── simple_requirements.txt # Dependencies
├── simple_setup.py        # Setup script
├── simple.env             # Environment template
├── SIMPLE_README.md       # This file
└── temp/                  # Temporary files
```

## Database

Automatically creates SQLite database (`bot.db`) with tables:
- `users` - User information and premium status
- `thumbnails` - User thumbnail file IDs
- `captions` - User custom captions

## Dependencies

- `pyrogram` - Telegram Bot API
- `sqlalchemy` - Database ORM
- `ffmpeg-python` - Video processing
- `psycopg2-binary` - PostgreSQL support (optional)

## License

MIT License

## Troubleshooting

- Ensure FFmpeg is installed: `ffmpeg -version`
- Check environment variables in `.env`
- Look at console output for errors
- Test with small video files first
- Make sure temp directory is writable

That's it! Simple and straightforward.