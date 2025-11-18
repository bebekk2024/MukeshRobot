import html
import re
import requests
import urllib.parse
from typing import Optional

from telegram import (
    CallbackQuery,
    Chat,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    Update,
    User,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.utils.helpers import mention_html

import MukeshRobot.modules.sql.chatbot_sql as sql
from MukeshRobot import BOT_ID, BOT_NAME, BOT_USERNAME, dispatcher
from MukeshRobot.modules.helper_funcs.chat_status import user_admin, user_admin_no_reply
from MukeshRobot.modules.log_channel import gloggable

API_KEY = "5935608297-fallen-usbk33kbsu"
API_URL = "https://fallenxbot.vercel.app/api/group-controller/mukesh"  # Perhatikan, endpoint ini harus sesuai dokumentasi API server

@user_admin_no_reply
@gloggable
def mukeshrm(update: Update, context: CallbackContext) -> str:
    """Disable chatbot (AI) in chat."""
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"rm_chat\((.+?)\)", query.data)
    if match:
        chat: Optional[Chat] = update.effective_chat
        is_mukesh = sql.set_mukesh(chat.id)
        if is_mukesh:
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"AI Disabled\n"
                f"<b>Admin :</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "{} chatbot disabled by {}.".format(
                    dispatcher.bot.first_name, mention_html(user.id, user.first_name)
                ),
                parse_mode=ParseMode.HTML,
            )
    return ""

@user_admin_no_reply
@gloggable
def mukeshadd(update: Update, context: CallbackContext) -> str:
    """Enable chatbot (AI) in chat."""
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"add_chat\((.+?)\)", query.data)
    if match:
        chat: Optional[Chat] = update.effective_chat
        is_mukesh = sql.rem_mukesh(chat.id)
        if is_mukesh:
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"AI Enabled\n"
                f"<b>Admin :</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "{} chatbot enabled by {}.".format(
                    dispatcher.bot.first_name, mention_html(user.id, user.first_name)
                ),
                parse_mode=ParseMode.HTML,
            )
    return ""

@user_admin
@gloggable
def mukesh(update: Update, context: CallbackContext):
    """Send chatbot enable/disable options."""
    message = update.effective_message
    msg = "• Choose an option to enable/disable chatbot"
    chat_id = update.effective_chat.id
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="Enable", callback_data=f"add_chat({chat_id})"),
            InlineKeyboardButton(text="Disable", callback_data=f"rm_chat({chat_id})"),
        ],
    ])
    message.reply_text(
        text=msg,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )

def mukesh_message(context: CallbackContext, message) -> bool:
    """Cek apakah pesan trigger chatbot."""
    reply_message = getattr(message, 'reply_to_message', None)
    msg_txt = message.text or ""
    if msg_txt.lower() == "mukesh":
        return True
    elif BOT_USERNAME.lower() in msg_txt.lower():
        return True
    elif reply_message and reply_message.from_user and reply_message.from_user.id == BOT_ID:
        return True
    return False

def chatbot(update: Update, context: CallbackContext):
    """Handle pesan chatbot jika aktif."""
    message = update.effective_message
    chat_id = update.effective_chat.id
    bot = context.bot
    is_mukesh = sql.is_mukesh(chat_id)
    if is_mukesh:
        return

    if message.text and not message.document:
        # trigger reply bot
        if not mukesh_message(context, message):
            return
        bot.send_chat_action(chat_id, action="typing")
        msg_txt = urllib.parse.quote(message.text)
        url = f"{API_URL}?apikey={API_KEY}&message={msg_txt}"
        try:
            response = requests.get(url, timeout=10)
            if not response.ok:
                reply = f"Chatbot API error ({response.status_code}): {response.text}"
            else:
                try:
                    out = response.json()
                    reply = out.get("reply", "No reply from chatbot API.")
                except Exception as e:
                    reply = f"Gagal decode JSON: {str(e)}\nRespon: {response.text}"
        except Exception as e:
            reply = f"Error from chatbot: {str(e)}"
        message.reply_text(reply)

CHATBOTK_HANDLER = CommandHandler("chatbot", mukesh, run_async=True)
ADD_CHAT_HANDLER = CallbackQueryHandler(mukeshadd, pattern=r"add_chat\(", run_async=True)
RM_CHAT_HANDLER = CallbackQueryHandler(mukeshrm, pattern=r"rm_chat\(", run_async=True)
CHATBOT_HANDLER = MessageHandler(
    Filters.text
    & (~Filters.regex(r"^#[^\s]+") & ~Filters.regex(r"^!") & ~Filters.regex(r"^\/")),
    chatbot,
    run_async=True,
)

dispatcher.add_handler(ADD_CHAT_HANDLER)
dispatcher.add_handler(CHATBOTK_HANDLER)
dispatcher.add_handler(RM_CHAT_HANDLER)
dispatcher.add_handler(CHATBOT_HANDLER)

__handlers__ = [
    ADD_CHAT_HANDLER,
    CHATBOTK_HANDLER,
    RM_CHAT_HANDLER,
    CHATBOT_HANDLER,
]
