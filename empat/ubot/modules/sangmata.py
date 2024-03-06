import asyncio
import random

from pyrogram import *
from pyrogram.errors import *
from pyrogram.raw.functions.messages import *
from pyrogram.types import *

from ubot import *
from ubot.utils import extract_user

__MODULE__ = "Sangmata"
__HELP__ = """
Bantuan Untuk Sangmata

• Perintah: <code>{0}sg</code> [user_id/reply user]
• Penjelasan: Untuk memeriksa histori nama/username.
"""


@KY.UBOT("sg")
async def _(client, message):
    args = await extract_user(message)
    emo = Emo(client.me.id)
    await emo.initialize()
    lol = await message.reply(f"{emo.proses} **Processing...**")
    await asyncio.sleep(2)
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
    # await lol.delete()
    async for stalk in client.search_messages(getbot, query="History", limit=2):
        if not stalk:
            NotFound = await client.send_message(client.me.id, "Tidak ada komentar")
            await NotFound.delete()
        elif stalk:
            await lol.edit(stalk.text)
    user_info = await client.resolve_peer(getbot)
    return await client.invoke(DeleteHistory(peer=user_info, max_id=0, revoke=True))
