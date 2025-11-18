import logging
import os
import sys
import time
from telegram.ext import Application
from aiohttp import ClientSession
from pyrogram import Client
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
    # ... [isi parsing env/config sama seperti kode kamu]
    API_ID = int(os.environ.get("API_ID", 0) or 0)
    API_HASH = os.environ.get("API_HASH", "")
    TOKEN = os.environ.get("TOKEN", "")
    WORKERS = int(os.environ.get("WORKERS", 8))
    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", "5779185981"))
    except ValueError:
        raise Exception("OWNER_ID invalid")
    try:
        DRAGONS = set(int(x) for x in os.environ.get("DRAGONS", "").split())
        DEV_USERS = set(int(x) for x in os.environ.get("DEV_USERS", "5779185981").split())
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")
else:
    from MukeshRobot.config import Development as Config
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    TOKEN = Config.TOKEN
    WORKERS = Config.WORKERS
    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("OWNER_ID invalid")
    try:
        DRAGONS = set(int(x) for x in Config.DRAGONS or [])
        DEV_USERS = set(int(x) for x in Config.DEV_USERS or [])
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

DRAGONS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)

telethn = TelegramClient("mukesh", API_ID, API_HASH)
pbot = Client("MukeshRobot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN, in_memory=True)
aiohttpsession = ClientSession()

application = Application.builder().token(TOKEN).concurrent_updates(WORKERS).build()

import asyncio
async def get_bot_info():
    bot_data = await application.bot.get_me()
    global BOT_ID, BOT_NAME, BOT_USERNAME
    BOT_ID = bot_data.id
    BOT_NAME = bot_data.first_name
    BOT_USERNAME = bot_data.username
asyncio.run(get_bot_info())

from MukeshRobot.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

application.add_handler(CustomCommandHandler)
application.add_handler(CustomMessageHandler)
application.add_handler(CustomRegexHandler)

async def close_aiohttp_session(app):
    await aiohttpsession.close()
application.post_shutdown.append(close_aiohttp_session)

if __name__ == "__main__":
    application.run_polling()
