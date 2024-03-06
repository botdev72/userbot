import asyncio

from pyrogram import filters
from pyrogram.errors import YouBlockedUser
from pyrogram.raw.functions.messages import DeleteHistory

from . import bot, ubot, anjay, cobadah
from ubot.config import OWNER_ID, PREFIX
from ubot.utils import eor, extract_user

__MODULE__ = "Sangmata"
__HELP__ = f"""
Bantuan Untuk Sangmata


• Perintah: <code>{cobadah}sg</code> [user_id/reply user]
• Penjelasan: Untuk memeriksa histori nama/username.


© {bot.me.first_name.split()[0]}
"""


@ubot.on_message(filters.user(OWNER_ID) & filters.command("sg", "^"))
@ubot.on_message(filters.me & anjay("sg"))
async def _(client, message):
    args = await extract_user(message)
    lol = await eor(message, "Sedang Memproses...")
    if args:
        try:
            user = await client.get_users(args)
        except Exception as error:
            return await lol.edit(error)
    bot = "SangMata_BOT"
    try:
        txt = await client.send_message(bot, f"{user.id}")
    except YouBlockedUser:
        await client.unblock_user(bot)
        txt = await client.send_message(bot, f"{user.id}")
    await txt.delete()
    await asyncio.sleep(5)
    await lol.delete()
    async for stalk in client.search_messages(bot, query="History", limit=1):
        if not stalk:
            NotFound = await client.send_message(client.me.id, "Tidak ada komentar")
            await NotFound.delete()
        elif stalk:
            await message.reply(stalk.text)
    user_info = await client.resolve_peer(bot)
    return await client.invoke(DeleteHistory(peer=user_info, max_id=0, revoke=True))
