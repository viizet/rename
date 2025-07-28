#!/usr/bin/env python3
"""
Simple Telegram Thumbnail Bot
Everything in one file, no folders, no AI features
"""

import os
import logging
import subprocess
from datetime import datetime
from typing import Optional

from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database models
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    is_premium = Column(Boolean, default=False)
    is_banned = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    join_date = Column(DateTime, default=datetime.utcnow)

class Thumbnail(Base):
    __tablename__ = 'thumbnails'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    file_id = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Caption(Base):
    __tablename__ = 'captions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    caption_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# Configuration
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///bot.db")
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "🎬 Processed by Simple Bot")
TEMP_DIR = os.environ.get("TEMP_DIR", "./temp")
FORCE_SUB = os.environ.get("FORCE_SUB")

# Setup database
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    return SessionLocal()

# Setup bot
app = Client("simple_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Helper functions
def is_banned(user_id: int) -> bool:
    session = get_db()
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        return user.is_banned if user else False
    finally:
        session.close()

def get_or_create_user(user_id: int, username: str = None, first_name: str = None) -> User:
    session = get_db()
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        if not user:
            user = User(
                user_id=user_id,
                username=username or "",
                first_name=first_name or "",
                is_admin=(user_id == OWNER_ID)
            )
            session.add(user)
            session.commit()
            session.refresh(user)
        return user
    finally:
        session.close()

async def check_subscription(client: Client, user_id: int) -> bool:
    if not FORCE_SUB:
        return True
    try:
        await client.get_chat_member(FORCE_SUB, user_id)
        return True
    except UserNotParticipant:
        return False
    except:
        return True

def process_video(video_path: str, thumb_path: str, output_path: str) -> bool:
    try:
        cmd = [
            'ffmpeg', '-i', video_path, '-i', thumb_path,
            '-map', '0', '-map', '1', '-c', 'copy', '-c:v:1', 'png',
            '-disposition:v:1', 'attached_pic', '-y', output_path
        ]
        result = subprocess.run(cmd, capture_output=True)
        return result.returncode == 0
    except:
        return False

# Bot handlers
@app.on_message(filters.command("start"))
async def start_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    
    if is_banned(user_id):
        await message.reply("❌ You are banned from using this bot.")
        return
    
    if not await check_subscription(client, user_id):
        await message.reply(f"❌ Please join @{FORCE_SUB} to use this bot.")
        return
    
    get_or_create_user(user_id, message.from_user.username, message.from_user.first_name)
    
    text = """
🎬 **Simple Thumbnail Bot**

Send me a photo to set as thumbnail
Send me a video to process with your thumbnail

**Commands:**
/viewthumb - View current thumbnail
/delthumb - Delete thumbnail  
/set_caption - Set custom caption
/see_caption - View caption
/del_caption - Delete caption
/myplan - View your plan
/ping - Bot status

**Limits:** 2GB free, 4GB premium
"""
    await message.reply(text)

@app.on_message(filters.command("viewthumb"))
async def view_thumb(client: Client, message: Message):
    user_id = message.from_user.id
    if is_banned(user_id):
        return
    
    session = get_db()
    try:
        thumb = session.query(Thumbnail).filter(Thumbnail.user_id == user_id).first()
        if thumb:
            await message.reply_photo(thumb.file_id, caption="Your current thumbnail")
        else:
            await message.reply("❌ No thumbnail set. Send me a photo first.")
    finally:
        session.close()

@app.on_message(filters.command("delthumb"))
async def del_thumb(client: Client, message: Message):
    user_id = message.from_user.id
    if is_banned(user_id):
        return
    
    session = get_db()
    try:
        session.query(Thumbnail).filter(Thumbnail.user_id == user_id).delete()
        session.commit()
        await message.reply("✅ Thumbnail deleted successfully.")
    finally:
        session.close()

@app.on_message(filters.command("set_caption"))
async def set_caption(client: Client, message: Message):
    user_id = message.from_user.id
    if is_banned(user_id):
        return
    
    if len(message.command) < 2:
        await message.reply("Usage: /set_caption Your caption here")
        return
    
    caption_text = message.text.split(None, 1)[1]
    
    session = get_db()
    try:
        session.query(Caption).filter(Caption.user_id == user_id).delete()
        caption = Caption(user_id=user_id, caption_text=caption_text)
        session.add(caption)
        session.commit()
        await message.reply("✅ Caption set successfully!")
    finally:
        session.close()

@app.on_message(filters.command("see_caption"))
async def see_caption(client: Client, message: Message):
    user_id = message.from_user.id
    if is_banned(user_id):
        return
    
    session = get_db()
    try:
        caption = session.query(Caption).filter(Caption.user_id == user_id).first()
        if caption:
            await message.reply(f"Your caption:\n\n{caption.caption_text}")
        else:
            await message.reply("❌ No caption set.")
    finally:
        session.close()

@app.on_message(filters.command("del_caption"))
async def del_caption(client: Client, message: Message):
    user_id = message.from_user.id
    if is_banned(user_id):
        return
    
    session = get_db()
    try:
        session.query(Caption).filter(Caption.user_id == user_id).delete()
        session.commit()
        await message.reply("✅ Caption deleted successfully.")
    finally:
        session.close()

@app.on_message(filters.command("myplan"))
async def my_plan(client: Client, message: Message):
    user_id = message.from_user.id
    
    session = get_db()
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        if user:
            plan = "Premium 💎" if user.is_premium else "Free 🆓"
            limit = "4GB" if user.is_premium else "2GB"
            text = f"**Your Plan:** {plan}\n**File Limit:** {limit}"
            await message.reply(text)
        else:
            await message.reply("User not found.")
    finally:
        session.close()

@app.on_message(filters.command("ping"))
async def ping_cmd(client: Client, message: Message):
    await message.reply("🏓 Pong! Bot is running.")

# Photo handler
@app.on_message(filters.photo)
async def photo_handler(client: Client, message: Message):
    user_id = message.from_user.id
    
    if is_banned(user_id):
        return
    
    if not await check_subscription(client, user_id):
        await message.reply(f"❌ Please join @{FORCE_SUB} to use this bot.")
        return
    
    file_id = message.photo.file_id
    
    session = get_db()
    try:
        session.query(Thumbnail).filter(Thumbnail.user_id == user_id).delete()
        thumb = Thumbnail(user_id=user_id, file_id=file_id)
        session.add(thumb)
        session.commit()
        await message.reply("✅ Thumbnail saved! Now send me a video to process.")
    finally:
        session.close()

# Video handler
@app.on_message(filters.video | filters.document)
async def video_handler(client: Client, message: Message):
    user_id = message.from_user.id
    
    if is_banned(user_id):
        return
    
    if not await check_subscription(client, user_id):
        await message.reply(f"❌ Please join @{FORCE_SUB} to use this bot.")
        return
    
    # Check if thumbnail exists
    session = get_db()
    try:
        thumb = session.query(Thumbnail).filter(Thumbnail.user_id == user_id).first()
        if not thumb:
            await message.reply("❌ Please set a thumbnail first by sending a photo.")
            return
        
        user = session.query(User).filter(User.user_id == user_id).first()
        caption_obj = session.query(Caption).filter(Caption.user_id == user_id).first()
        
        file = message.video or message.document
        if not file:
            return
        
        # Check file size
        max_size = 4 * 1024**3 if user and user.is_premium else 2 * 1024**3
        if file.file_size > max_size:
            limit = "4GB" if user and user.is_premium else "2GB"
            await message.reply(f"❌ File too large! Max size: {limit}")
            return
        
        status_msg = await message.reply("🔄 Processing video...")
        
        try:
            os.makedirs(TEMP_DIR, exist_ok=True)
            
            # Download files
            video_path = await client.download_media(message, TEMP_DIR)
            thumb_path = await client.download_media(thumb.file_id, TEMP_DIR)
            
            # Process video
            output_path = os.path.join(TEMP_DIR, f"output_{user_id}_{datetime.now().timestamp()}.mp4")
            
            if process_video(str(video_path), str(thumb_path), output_path):
                caption_text = caption_obj.caption_text if caption_obj else CUSTOM_CAPTION
                
                await client.send_video(
                    message.chat.id,
                    output_path,
                    caption=caption_text,
                    reply_to_message_id=message.id
                )
                await status_msg.edit("✅ Video processed successfully!")
            else:
                await status_msg.edit("❌ Failed to process video.")
            
            # Cleanup
            for path in [video_path, thumb_path, output_path]:
                if path and os.path.exists(str(path)):
                    os.remove(str(path))
                    
        except Exception as e:
            logger.error(f"Processing error: {e}")
            await status_msg.edit("❌ Processing failed.")
    finally:
        session.close()

# Admin commands
@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats(client: Client, message: Message):
    session = get_db()
    try:
        total = session.query(User).count()
        premium = session.query(User).filter(User.is_premium == True).count()
        banned = session.query(User).filter(User.is_banned == True).count()
        
        text = f"""
📊 **Bot Stats**
👥 Total Users: {total}
💎 Premium: {premium}
🚫 Banned: {banned}
        """
        await message.reply(text)
    finally:
        session.close()

@app.on_message(filters.command("ban") & filters.user(OWNER_ID))
async def ban_user(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("Usage: /ban <user_id>")
        return
    
    try:
        target_id = int(message.command[1])
        session = get_db()
        try:
            user = session.query(User).filter(User.user_id == target_id).first()
            if user:
                # Update user banned status
                session.query(User).filter(User.user_id == target_id).update({User.is_banned: True})
                session.commit()
                await message.reply(f"✅ User {target_id} banned.")
            else:
                await message.reply("❌ User not found.")
        finally:
            session.close()
    except ValueError:
        await message.reply("❌ Invalid user ID.")

@app.on_message(filters.command("unban") & filters.user(OWNER_ID))
async def unban_user(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("Usage: /unban <user_id>")
        return
    
    try:
        target_id = int(message.command[1])
        session = get_db()
        try:
            user = session.query(User).filter(User.user_id == target_id).first()
            if user:
                session.query(User).filter(User.user_id == target_id).update({User.is_banned: False})
                session.commit()
                await message.reply(f"✅ User {target_id} unbanned.")
            else:
                await message.reply("❌ User not found.")
        finally:
            session.close()
    except ValueError:
        await message.reply("❌ Invalid user ID.")

@app.on_message(filters.command("addpremium") & filters.user(OWNER_ID))
async def add_premium(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("Usage: /addpremium <user_id>")
        return
    
    try:
        target_id = int(message.command[1])
        session = get_db()
        try:
            user = session.query(User).filter(User.user_id == target_id).first()
            if user:
                session.query(User).filter(User.user_id == target_id).update({User.is_premium: True})
                session.commit()
                await message.reply(f"✅ Premium granted to {target_id}.")
            else:
                await message.reply("❌ User not found.")
        finally:
            session.close()
    except ValueError:
        await message.reply("❌ Invalid user ID.")

if __name__ == "__main__":
    print("🚀 Starting Simple Telegram Thumbnail Bot...")
    
    # Check if required environment variables are set
    if not all([API_ID, API_HASH, BOT_TOKEN, OWNER_ID]):
        print("❌ Missing required environment variables:")
        if not API_ID: print("  - API_ID")
        if not API_HASH: print("  - API_HASH") 
        if not BOT_TOKEN: print("  - BOT_TOKEN")
        if not OWNER_ID: print("  - OWNER_ID")
        print("\nPlease set these in your .env file or environment variables.")
        exit(1)
    
    app.run()