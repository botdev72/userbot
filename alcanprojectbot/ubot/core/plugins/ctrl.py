from asyncio import QueueEmpty

from pyrogram import filters
from pyrogram.types import Message
from pytgcalls.exceptions import NoActiveGroupCall, NotInGroupCallError

from ubot import *
from ubot.core.pytgcalls import queues

# from tomimusic.utils import require_admin
# @require_admin("can_manage_video_chats", "Hak admin yang diperlukan: <code>Manage Live Streams</code>",)



async def pausnya(client, message):
    if len(message.command) < 2:
        chat_id = message.chat.id
    else:
        chat_id = int(message.text.split()[1])
    await client.call_py.pause_stream(chat_id)
    await message.reply_text(
        "❏ <b>Lagu dijeda.</b>\n\n• Untuk melanjutkan pemutaran, gunakan <b>perintah</b> » resume.",
        quote=False,
    )
    await message.delete()




async def resumenua(client, message):
    if len(message.command) < 2:
        chat_id = message.chat.id
    else:
        chat_id = int(message.text.split()[1])
    await client.call_py.resume_stream(chat_id)
    await message.reply_text(
        "❏ <b>Melanjutkan pemutaran lagu yang dijeda.</b>\n\n• Untuk menjeda pemutaran, gunakan <b>perintah</b> » pause.",
        quote=False,
    )
    await message.delete()


async def endnua(client, message):
    if len(message.command) < 2:
        chat_id = message.chat.id
    else:
        chat_id = int(message.text.split()[1])
    try:
        queues.clear(chat_id)
    except QueueEmpty:
        pass
    try:
        await client.call_py.leave_group_call(chat_id)
        await message.reply_text(
            "❏<b>Berhasil Meninggalkan Voice Chat Grup.</b>", quote=False
        )
        await message.delete()
    except (NotInGroupCallError, NoActiveGroupCall):
        pass



async def sekipnya(client, message):
    if len(message.command) < 2:
        chat_id = message.chat.id
    else:
        chat_id = int(message.text.split()[1])
    queues.task_done(chat_id)
    await client.call_py.change_stream(chat_id, queues.get(chat_id)["file"])
    await message.reply_text(
        "❏ <b>Memutar lagu berikutnya...</b>", quote=False
    )
    await message.delete()
