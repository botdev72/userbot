from pyrogram import *
from pyrogram.enums import *
from pyrogram.types import *

from ubot import *

__MODULE__ = "ShowID"
__HELP__ = """
Bantuan Untuk Show ID

• Perintah: <code>{0}id</code>
• Penjelasan: Untuk mengetahui ID dari user/grup/channel.

• Perintah: <code>{0}id</code> [reply to user/media]
• Penjelasan: Untuk mengetahui ID dari user/media.

• Perintah: <code>{0}getid</code> [username user/grup/channel].
• Penjelasan: Untuk mengetahui ID user/grup/channel melalui username dengan simbol @.
"""


@KY.UBOT("id", sudo=True)
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
            return await message.reply("Pengguna tidak ditemukan.")

    text += f"**[Chat ID:](https://t.me/{chat.username})** `{chat.id}`\n\n"
    if not getattr(reply, "empty", True):
        id_ = reply.from_user.id if reply.from_user else reply.sender_chat.id
        text += f"**[Replied Message ID:]({reply.link})** `{reply.id}`\n"
        text += f"**[Replied User ID:](tg://user?id={id_})** `{id_}`"

    await message.edit(
        text,
        disable_web_page_preview=True,
        parse_mode=enums.ParseMode.MARKDOWN,
    )
