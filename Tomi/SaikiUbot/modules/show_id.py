from pyrogram.enums import ChatType
from pyrogram.errors import BadRequest

from .. import *

__MODULE__ = "SHOWID"
__HELP__ = f"""
Perintah:
         <code>{PREFIX[0]}id</code>
Penjelasan:
           Untuk mengetahui ID dari user/grup/channel 

Perintah:
         <code>{PREFIX[0]}id</code> [reply to user/media]
Penjelasan:
           Untuk mengetahui ID dari user/media 

Perintah:
         <code>{PREFIX[0]}id</code> [username user/grup/channel]
Penjelasan:
           Untuk mengetahui ID user/grup/channel melalui username dengan simbol @
"""


@PY.UBOT("id", PREFIX)
async def showid(client, message):
    if len(message.command) < 2:
        chat_type = message.chat.type
        if chat_type == ChatType.PRIVATE:
            user_id = message.chat.id
            await message.reply_text(
                f"<b>ID</b> <code>{user_id}</code>",
            )
        elif chat_type == ChatType.CHANNEL:
            await message.reply(
                f"<b>ID {message.sender_chat.title} Adalah:</b> <code>{message.sender_chat.id}</code>",
            )
        elif chat_type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            _id = ""
            _id += f"<b>ID {message.from_user.first_name} {message.from_user.last_name or ''} Adalah:</b> <code>{message.from_user.id}</code>\n<b>ID {message.chat.title} Adalah:</b> <code>{message.chat.id}</code>\n"
            if message.reply_to_message:
                _id += f"\n<b>ID {message.reply_to_message.from_user.first_name} {message.reply_to_message.from_user.last_name or ''} Adalah:</b> <code>{message.reply_to_message.from_user.id}</code>\n"
                file_info = get_file_id(message.reply_to_message)
                if file_info:
                    _id += f"<b>ID {file_info.message_type} Adalah:</b> <code>{file_info.file_id}</code>\n"
            m = message.reply_to_message or message
            return await m.reply_text(_id)
    try:
        chat_id = message.text.split()[1]
        get = await client.get_chat(chat_id)
        name = f"{get.title}"
        if name == "None":
            get = await client.get_users(chat_id)
            name = f"{get.first_name} {get.last_name or ''}"
        msg = f"<b>ID {name} Adalah:</b> <code>{get.id}</code>"
        return await message.reply(msg)
    except BadRequest as why:
        return await message.reply(why)
