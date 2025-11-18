from pyrate_limiter import (
    BucketFullException,
    Duration,
    Limiter,
    MemoryListBucket,
    RequestRate,
)
from telegram.ext import CommandHandler, MessageHandler, filters

import MukeshRobot.modules.sql.blacklistusers_sql as sql
from MukeshRobot import ALLOW_EXCL, DEMONS, DEV_USERS, DRAGONS, TIGERS, WOLVES

if ALLOW_EXCL:
    CMD_STARTERS = ("/", "!")
else:
    CMD_STARTERS = ("/",)

class AntiSpam:
    def __init__(self):
        self.whitelist = (
            list(DEV_USERS or [])
            + list(DRAGONS or [])
            + list(WOLVES or [])
            + list(DEMONS or [])
            + list(TIGERS or [])
        )
        Duration.CUSTOM = 15
        self.sec_limit = RequestRate(6, Duration.CUSTOM)
        self.min_limit = RequestRate(20, Duration.MINUTE)
        self.hour_limit = RequestRate(100, Duration.HOUR)
        self.daily_limit = RequestRate(1000, Duration.DAY)
        self.limiter = Limiter(
            self.sec_limit,
            self.min_limit,
            self.hour_limit,
            self.daily_limit,
            bucket_class=MemoryListBucket,
        )

    def check_user(self, user):
        if user in self.whitelist:
            return False
        try:
            self.limiter.try_acquire(user)
            return False
        except BucketFullException:
            return True

SpamChecker = AntiSpam()
MessageHandlerChecker = AntiSpam()

# ========== Handler Async untuk PTB v20+ ==========
async def start(update, context):
    await update.message.reply_text("Bot PTB v20+ siap digunakan!")

async def handle_text_message(update, context):
    await update.message.reply_text("Ini pesan teks biasa.")

async def handle_regex(update, context):
    await update.message.reply_text("Terdeteksi pattern regex!")

# Handler objek siap didaftarkan di __init__.py
CustomCommandHandler = CommandHandler("start", start)
CustomMessageHandler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message)
CustomRegexHandler = MessageHandler(filters.Regex(r"pattern"), handle_regex)
