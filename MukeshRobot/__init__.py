import logging
import os
import sys
import time
import ast
import base64

from telegram.ext import Application, CommandHandler, MessageHandler, filters
from aiohttp import ClientSession
from pyrogram import Client, errors
from telethon import TelegramClient

StartTime = time.time()

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger("telethon").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)

if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)

ENV = bool(os.environ.get("ENV", False))

if ENV:
    # ... [bagian parsing environment sama persis]
    API_ID = int(os.environ.get("API_ID", None))
    API_HASH = os.environ.get("API_HASH", None)
    # [dst...]
    TOKEN = os.environ.get("TOKEN", None)
    WORKERS = int(os.environ.get("WORKERS", 8))
    # [dst...]
else:
    from MukeshRobot.config import Development as Config
    # ... [bagian parsing config sama persis]
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    TOKEN = Config.TOKEN
    WORKERS = Config.WORKERS
    # [dst...]

# [Penambahan DRAGONS, DEV_USERS, DLL tetap]

telethn = TelegramClient("mukesh", API_ID, API_HASH)
pbot = Client("MukeshRobot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN, in_memory=True)
aiohttpsession = ClientSession()

# === PTB v20+ Application Builder ===
application = Application.builder().token(TOKEN).concurrent_updates(WORKERS).build()

print("[INFO]: Getting Bot Info...")
async def get_bot_info():
    bot_data = await application.bot.get_me()
    global BOT_ID, BOT_NAME, BOT_USERNAME
    BOT_ID = bot_data.id
    BOT_NAME = bot_data.first_name
    BOT_USERNAME = bot_data.username

# Inisialisasi async untuk bot info
import asyncio
asyncio.run(get_bot_info())

DRAGONS = list(DRAGONS) + list(DEV_USERS) 
DEV_USERS = list(DEV_USERS)
WOLVES = list(WOLVES)
DEMONS = list(DEMONS)
TIGERS = list(TIGERS)

from MukeshRobot.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

# Assign handler jika ingin custom handler
application.add_handler(CustomCommandHandler("start", ...))   # Ganti ... dengan handler anda
application.add_handler(CustomMessageHandler(...))            # Sesuaikan kebutuhan
application.add_handler(CustomRegexHandler(...))

# Untuk menjalankan polling
if __name__ == "__main__":
    application.run_polling()
