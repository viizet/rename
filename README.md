# Simple Telegram Thumbnail Bot

A straightforward Telegram bot for adding custom thumbnails to videos. Single file structure, no folders, no AI features - just the essentials.

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/simple-thumbnail-bot.git
cd simple-thumbnail-bot

# Install dependencies
pip install -r simple_requirements.txt

# Configure environment
cp simple.env .env
# Edit .env with your API credentials

# Run the bot
python simple_thumbnail_bot.py
```

## ✨ Features

- Add custom thumbnails to videos using FFmpeg
- Premium user support (2GB free, 4GB premium)
- Basic admin commands (ban, unban, stats, premium management)
- SQLite database (no complex setup needed)
- Single file structure for easy deployment
- Force subscription support (optional)

## 📋 Requirements

- Python 3.8+
- FFmpeg installed on system
- Telegram Bot API credentials

### Install FFmpeg

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows - Download from https://ffmpeg.org/download.html
```

## ⚙️ Configuration

Create `.env` file with your credentials:

```env
# Required
API_ID=your_api_id_from_my_telegram_org
API_HASH=your_api_hash_from_my_telegram_org
BOT_TOKEN=your_bot_token_from_botfather
OWNER_ID=your_telegram_user_id

# Optional
DATABASE_URL=sqlite:///bot.db
CUSTOM_CAPTION=🎬 Processed by Simple Bot
FORCE_SUB=your_channel_username
TEMP_DIR=./temp
```

### Getting API Credentials

1. **API_ID & API_HASH**: Get from https://my.telegram.org/apps
2. **BOT_TOKEN**: Create bot with @BotFather on Telegram
3. **OWNER_ID**: Your Telegram user ID (use @userinfobot to find it)

## 📖 User Commands

- `/start` - Welcome message and instructions
- `/viewthumb` - View your current thumbnail
- `/delthumb` - Delete your thumbnail
- `/set_caption <text>` - Set custom video caption
- `/see_caption` - View your current caption
- `/del_caption` - Delete your caption
- `/myplan` - View your subscription plan
- `/ping` - Check bot status

## 🔧 Admin Commands (Owner Only)

- `/stats` - View bot statistics
- `/ban <user_id>` - Ban user from bot
- `/unban <user_id>` - Unban user
- `/addpremium <user_id>` - Grant premium access

## 📱 How to Use

1. **Set Thumbnail**: Send any photo to the bot
2. **Process Video**: Send a video file
3. **Get Result**: Bot returns video with your thumbnail applied

## 📁 File Structure

```
simple-thumbnail-bot/
├── simple_thumbnail_bot.py    # Main bot (everything in one file)
├── simple_requirements.txt    # Python dependencies
├── simple_setup.py           # Automated setup script
├── simple.env                # Environment template
├── SIMPLE_README.md          # Detailed documentation
├── README.md                 # This file
└── temp/                     # Temporary files (auto-created)
```

## 🗄️ Database

- Automatically creates SQLite database (`bot.db`) on first run
- For PostgreSQL: Set `DATABASE_URL=postgresql://user:pass@host:5432/dbname`

**Tables:**
- `users` - User profiles and premium status
- `thumbnails` - User thumbnail file IDs
- `captions` - Custom user captions

## 📦 Dependencies

- `pyrogram` - Telegram Bot API wrapper
- `sqlalchemy` - Database ORM
- `ffmpeg-python` - Video processing wrapper
- `psycopg2-binary` - PostgreSQL support (optional)

## 🚀 Deployment Options

### Local Development
```bash
python simple_thumbnail_bot.py
```

### Using Screen (Linux/macOS)
```bash
screen -S thumbnail-bot
python simple_thumbnail_bot.py
# Ctrl+A, D to detach
# screen -r thumbnail-bot to reattach
```

### Systemd Service (Linux)
Create `/etc/systemd/system/thumbnail-bot.service`:
```ini
[Unit]
Description=Simple Thumbnail Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=/path/to/bot
ExecStart=/usr/bin/python3 simple_thumbnail_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## 🔍 Troubleshooting

**Bot won't start:**
- Check `.env` file has correct API credentials
- Ensure FFmpeg is installed: `ffmpeg -version`
- Verify Python version: `python --version` (3.8+ required)

**Video processing fails:**
- Check FFmpeg installation
- Test with smaller video files first
- Ensure temp directory is writable
- Check bot logs for specific errors

**Permission errors:**
- Ensure bot has required permissions in your channel/group
- Check if user is banned from bot
- Verify owner ID is correct

## 📄 License

MIT License - feel free to use and modify

## 🤝 Contributing

1. Fork the repository
2. Make your changes
3. Test thoroughly
4. Submit a pull request

---

**Note**: This bot requires API credentials to function. The error about missing environment variables is normal until you configure your `.env` file.