from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *

from . import bot, ubot, anjay, cobadah
from ubot.utils import eor
from ubot.utils.get_file_id import get_file_id

__MODULE__ = "Show ID"
__HELP__ = f"""
Bantuan Untuk Show ID


• Perintah: <code>{cobadah}id</code>
• Penjelasan: Untuk mengetahui ID dari user/grup/channel.

• Perintah: <code>{cobadah}id</code> [reply to user/media]
• Penjelasan: Untuk mengetahui ID dari user/media.

• Perintah: <code>{cobadah}getid</code> [username user/grup/channel].
• Penjelasan: Untuk mengetahui ID user/grup/channel melalui username dengan simbol @.


© {bot.me.first_name.split()[0]}
"""

@ubot.on_message(filters.me & anjay("id"))
async def getid(client, message):
    chat = message.chat
    your_id = message.from_user.id
    message_id = message.id
    reply = message.reply_to_message

    text = f"**[Message ID:]({message.link})** `{message_id}`\n"
    text += f"**[Your ID:](tg://user?id={your_id})** `{your_id}`\n"

    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user_id = (await client.get_users(split)).id
            text += f"**[User ID:](tg://user?id={user_id})** `{user_id}`\n"
        except Exception:
            return await eor(message, "Pengguna tidak ditemukan.")

    text += f"**[Chat ID:](https://t.me/{chat.username})** `{chat.id}`\n\n"
    if not getattr(reply, "empty", True):
        id_ = reply.from_user.id if reply.from_user else reply.sender_chat.id
        text += f"**[Replied Message ID:]({reply.link})** `{reply.id}`\n"
        text += f"**[Replied User ID:](tg://user?id={id_})** `{id_}`"

    await eor(
        message,
        text,
        disable_web_page_preview=True,
        parse_mode=enums.ParseMode.MARKDOWN,
    )