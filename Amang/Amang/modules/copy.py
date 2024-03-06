import asyncio

from pyrogram import filters
from pyrogram.raw.functions.messages import DeleteHistory

from Amang import *
from Amang.config import *
from Amang.utils import *
from Amang import bot

__MOD__ = "copy"
__HELP__ = f"""
 Document for Copy

• Command: <code>{cmd[0]}copy</code> [link]
• Function: Untuk mengambil konten ch private.

• Command: <code>{cmd[0]}getmsg</code> [balas ke pesan]
• Function: Untuk mengambil pap timer, cek @{bot.me.username} .
"""


@ubot.on_message(filters.me & filters.command("copy", cmd))
async def nyolongnih(client, message):
    await message.reply("Procesing...")
    link = get_arg(message)
    msg_id = int(link.split("/")[-1])
    if "t.me/c/" in link:
        try:
            chat = int("-100" + str(link.split("/")[-2]))
            dia = await client.get_messages(chat, msg_id)
        except RPCError:
            await message.edit("Looks like an error occurred")
    else:
        try:
            chat = str(link.split("/")[-2])
            dia = await client.get_messages(chat, msg_id)
        except RPCError:
            await message.edit("Looks like an error occurred")
    anjing = dia.caption or None
    if dia.text:
        await dia.copy(message.chat.id)
        await message.delete()
    if dia.photo:
        anu = await client.download_media(dia)
        await client.send_photo(message.chat.id, anu, anjing)
        await message.delete()
        os.remove(anu)

    if dia.video:
        anu = await client.download_media(dia)
        await client.send_video(message.chat.id, anu, anjing)
        await message.delete()
        os.remove(anu)

    if dia.audio:
        anu = await client.download_media(dia)
        await client.send_audio(message.chat.id, anu, anjing)
        await message.delete()
        os.remove(anu)

    if dia.voice:
        anu = await client.download_media(dia)
        await client.send_voice(message.chat.id, anu, anjing)
        await message.delete()
        os.remove(anu)

    if dia.document:
        anu = await client.download_media(dia)
        await client.send_document(message.chat.id, anu, anjing)
        await message.delete()
        os.remove(anu)
    else:
        await message.edit("Looks like an error occurred")

