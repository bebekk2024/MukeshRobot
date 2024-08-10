import asyncio
from platform import python_version as pyver

from pyrogram import __version__ as pver
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram import __version__ as lver
from telethon import __version__ as tver

from MukeshRobot import SUPPORT_CHAT, pbot,BOT_USERNAME, OWNER_ID,BOT_NAME,START_IMG

PHOTO = [
    "https://telegra.ph//file/309657e7635941bae6b17.jpg",
    "https://telegra.ph//file/309657e7635941bae6b17.jpg",
    "https://telegra.ph//file/309657e7635941bae6b17.jpg",
    "https://telegra.ph//file/309657e7635941bae6b17.jpg",
    "https://telegra.ph//file/309657e7635941bae6b17.jpg",
]

Mukesh = [
    [
        InlineKeyboardButton(text="๏ ᴅᴇᴠ ๏", user_id=5779185981),
        InlineKeyboardButton(text="๏ ꜱᴜᴘᴘᴏʀᴛ ๏", url=f"https://t.me/musik_supportdan"),
    ],
    [
        InlineKeyboardButton(text="๏ ᴅᴀɴ ๏", url="https://t.me/mhmdwldnnnn"),
        InlineKeyboardButton(text="๏ ꜱᴛᴏʀᴇ ๏", url=f"https://t.me/Disney_storeDan"),
    ],
    [
        InlineKeyboardButton(
            text="➕ᴛᴀᴍʙᴀʜ ᴋᴇ ɢᴄ ᴀᴍᴘᴀs ʟᴜ➕",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
]



@pbot.on_message(filters.command("alive"))
async def restart(client, m: Message):
    await m.delete()
    accha = await m.reply("⚡")
    await asyncio.sleep(0.2)
    await accha.edit("𝙈𝙀𝙈𝙀𝙆 ꨄ︎ 𝙀𝙃 𝙂𝙄𝙈𝘼𝙉𝘼..")
    await asyncio.sleep(0.1)
    await accha.edit("𝙆𝙊𝙉𝙏𝙊𝙇 ꨄ︎ 𝙀𝙃 𝙂𝙄𝙈𝘼𝙉𝘼......")
    await asyncio.sleep(0.1)
    await accha.edit("𝙃𝘼𝙇𝙊 𝙎𝘼𝙔𝘼𝙉𝙂 𝙀𝙃 ꨄ︎..")

    await accha.delete()
    await asyncio.sleep(0.3)
    umm = await m.reply_sticker(
        "CAACAgUAAxkDAAJHbmLuy2NEfrfh6lZSohacEGrVjd5wAAIOBAACl42QVKnra4sdzC_uKQQ"
    )
    await umm.delete()
    await asyncio.sleep(0.2)
    await m.reply_photo(
        START_IMG,
        caption=f"""**ʜʏ ᴍᴇᴋ ,ɢᴡ 『[{BOT_NAME}](f"t.me/{BOT_USERNAME}")』**
   ━━━━━━━━━━━━━━━━━━━
  ๏ ** ᴅᴇᴠᴇʟᴏᴘᴇʀ :** [ᴅᴀɴ](tg://user?id=5779185981)
  
  ๏ ** ꜱᴛᴏʀᴇ :** [ꜱᴛᴏʀᴇ](https://t.me/Disney_storeDan)
   ━━━━━━━━━━━━━━━━━━━""",
        reply_markup=InlineKeyboardMarkup(Mukesh),
    )
