from pyrate_limiter import (
    BucketFullException,
    Duration,
    Limiter,
    MemoryListBucket,
    RequestRate,
)
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters

import MukeshRobot.modules.sql.blacklistusers_sql as sql
from MukeshRobot import ALLOW_EXCL, DEMONS, DEV_USERS, DRAGONS, TIGERS, WOLVES

if ALLOW_EXCL:
    CMD_STARTERS = ("/", "!")
else:
    CMD_STARTERS = ("/",)

class AntiSpam:
    def __init__(self):
        # Perhatikan: ubah ke list agar bisa dicheck dengan "in"
        self.whitelist = (
            list(DEV_USERS or [])
            + list(DRAGONS or [])
            + list(WOLVES or [])
            + list(DEMONS or [])
            + list(TIGERS or [])
        )
        Duration.CUSTOM = 15  # Custom duration 15 seconds
        self.sec_limit = RequestRate(6, Duration.CUSTOM)   # 6 / 15 seconds
        self.min_limit = RequestRate(20, Duration.MINUTE)  # 20 / minute
        self.hour_limit = RequestRate(100, Duration.HOUR)  # 100 / hour
        self.daily_limit = RequestRate(1000, Duration.DAY) # 1000 / day
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

class CustomCommandHandler(CommandHandler):
    def __init__(self, command, callback, admin_ok=False, allow_edit=False, **kwargs):
        # Handler PTB v20+ wajib async
        super().__init__(command, callback, **kwargs)
        # Mendukung edited (fitur PTB v20+: gunakan filter update)
        if allow_edit is False:
            self.filters = self.filters & ~(
                filters.Update.EDITED_MESSAGE | filters.Update.EDITED_CHANNEL_POST
            )

    def check_update(self, update):
        if isinstance(update, Update) and update.effective_message:
            message = update.effective_message
            user_id = getattr(update.effective_user, "id", None)

            if user_id and sql.is_user_blacklisted(user_id):
                return False

            if message.text and len(message.text) > 1:
                fst_word = message.text.split(None, 1)[0]
                if len(fst_word) > 1 and any(
                    fst_word.startswith(start) for start in CMD_STARTERS
                ):
                    args = message.text.split()[1:]
                    command = fst_word[1:].split("@")
                    command.append(message.bot.username)
                    if user_id == 1087968824:
                        user_id = update.effective_chat.id
                    if not (
                        command[0].lower() in self.command
                        and command[1].lower() == message.bot.username.lower()
                    ):
                        return None
                    if SpamChecker.check_user(user_id):
                        return None
                    filter_result = self.filters(update)
                    if filter_result:
                        return args, filter_result
                    else:
                        return False

    async def handle_update(self, update, context):
        # ALL handler PTB v20+ wajib async!
        check_result = self.check_update(update)
        if check_result:
            # context.args bisa didapat dari check_result
            context.args = check_result[0]
            await self.callback(update, context)

class CustomRegexHandler(MessageHandler):
    def __init__(self, pattern, callback, friendly="", **kwargs):
        # PTB v20+: gunakan MessageHandler dengan filters.Regex
        super().__init__(filters.Regex(pattern), callback, **kwargs)

class CustomMessageHandler(MessageHandler):
    def __init__(self, filters_, callback, friendly="", allow_edit=False, **kwargs):
        super().__init__(filters_, callback, **kwargs)
        if allow_edit is False:
            self.filters = self.filters & ~(
                filters.Update.EDITED_MESSAGE | filters.Update.EDITED_CHANNEL_POST
            )

    def check_update(self, update):
        if isinstance(update, Update) and update.effective_message:
            return self.filters(update)
