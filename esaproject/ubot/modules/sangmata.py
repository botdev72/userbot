import asyncio
import random
from pyrogram import *
from pyrogram.errors import *
from pyrogram.raw.functions.messages import *
from pyrogram.types import *

from . import bot, ubot, anjay, cobadah

from ubot.utils import eor, extract_user

__MODULE__ = "Sangmata"
__HELP__ = """
Bantuan Untuk Sangmata

• Perintah: <code>{cobadah}sg</code> [user_id/reply user]
• Penjelasan: Untuk memeriksa histori nama/username.
"""


@ubot.on_message(filters.me & anjay("sg"))
async def _(client, message):
    args = await extract_user(message)
    lol = await message.edit("Sedang Memproses...")
    if args:
        try:
            user = await client.get_users(args)
        except Exception as error:
            return await lol.edit(error)
    bot = ["@Sangmata_bot", "@SangMata_beta_bot"]
    getbot = random.choice(bot)
    try:
        txt = await client.send_message(getbot, f"{user.id}")
    except YouBlockedUser:
        await client.unblock_user(getbot)
        txt = await client.send_message(getbot, f"{user.id}")
    await txt.delete()
    await asyncio.sleep(5)
    await lol.delete()
    async for stalk in client.search_messages(getbot, query="History", limit=2):
        if not stalk:
            NotFound = await client.send_message(client.me.id, "Tidak ada komentar")
            await NotFound.delete()
        elif stalk:
            await message.reply(stalk.text)
    user_info = await client.resolve_peer(getbot)
    return await client.invoke(DeleteHistory(peer=user_info, max_id=0, revoke=True))
