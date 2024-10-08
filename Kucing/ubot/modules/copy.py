import asyncio

from pyrogram import filters
from pyrogram.raw.functions.messages import DeleteHistory

from . import bot, ubot, anjay, cobadah, check_access

from ubot.utils import *

__MODULE__ = "Content"
__HELP__ = """
Bantuan Untuk Content

• Perintah: <code>{0}copy</code> [link]
• Penjelasan: Untuk mengambil konten ch private.

• Perintah: <code>{0}curi</code> [balas ke pesan]
• Penjelasan: Untuk mengambil pap timer, cek pesan tersimpan.
"""


@ubot.on_message(filters.me & anjay("copy"))
@check_access
async def _(client, message):
    if len(message.command) < 2:
        return
    else:
        Tm = await eor(message, "<code>Processing . . .</code>")
        link = message.text.split()[1]
        bot = "Nyolongbang_bot"
        await client.unblock_user(bot)
        xnxx = await client.send_message(bot, link)
        await xnxx.delete()
        await asyncio.sleep(5)
        await Tm.delete()
        async for sosmed in client.search_messages(bot, limit=1):
            try:
                await sosmed.copy(
                    message.chat.id,
                    reply_to_message_id=message.id,
                )
            except Exception:
                await Tm.edit(
                    "<b>Video tidak ditemukan silahkan ulangi beberapa saat lagi</b>"
                )
        user_info = await client.resolve_peer(bot)
        return await client.invoke(DeleteHistory(peer=user_info, max_id=0, revoke=True))
