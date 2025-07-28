#!/usr/bin/env python3
"""
Simple Setup Script for Telegram Thumbnail Bot
Single file structure without folders
"""

import os
import sys
import subprocess

def check_python():
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")

def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True)
        print("✅ FFmpeg found")
        return True
    except FileNotFoundError:
        print("❌ FFmpeg not found - install it first")
        return False

def install_deps():
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'simple_requirements.txt'], check=True)
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def setup_env():
    if os.path.exists('.env'):
        print("✅ .env exists")
        return
    
    env_content = """# Telegram Bot Configuration
API_ID=your_api_id
API_HASH=your_api_hash  
BOT_TOKEN=your_bot_token
OWNER_ID=your_user_id
DATABASE_URL=sqlite:///bot.db

# Optional
AUTH_USERS=
BANNED_USERS=
TIME_GAP=5
CUSTOM_CAPTION=
FORCE_SUB=
TRACE_CHANNEL=
TEMP_DIR=./temp
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    print("📝 Created .env file - please edit with your credentials")

def create_temp():
    os.makedirs('temp', exist_ok=True)
    print("✅ Created temp directory")

def main():
    print("🚀 Simple Telegram Thumbnail Bot Setup")
    print("=" * 40)
    
    check_python()
    ffmpeg_ok = check_ffmpeg()
    deps_ok = install_deps()
    setup_env()
    create_temp()
    
    print("\n" + "=" * 40)
    if ffmpeg_ok and deps_ok:
        print("✅ Setup complete!")
        print("\nNext steps:")
        print("1. Edit .env with your credentials")
        print("2. Run: python bot.py")
    else:
        print("❌ Setup failed - fix errors above")

if __name__ == "__main__":
    main()