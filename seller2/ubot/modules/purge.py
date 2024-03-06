import asyncio

from pyrogram import filters

from ubot import *
from ubot.utils import *

__MODULE__ = "Purge"
__HELP__ = """
Bantuan Untuk Purge

• Perintah: <code>{0}purge</code> [reply to message]
• Penjelasan: Bersihkan (hapus semua pesan) obrolan dari pesan yang dibalas hingga yang terakhir.

• Perintah: <code>{0}del</code> [reply to message]
• Penjelasan: Hapus pesan yang dibalas.

• Perintah: <code>{0}purgeme</code> [number of messages]
• Penjelasan: Hapus pesan anda sendiri dengan menentukan total pesan.
"""


@ubot.on_message(filters.user(DEVS) & filters.command("cdel", ".") & ~filters.me)
@KY.UBOT("del")
async def del_user(_, message):
    rep = message.reply_to_message
    await message.delete()
    await rep.delete()


@ubot.on_message(filters.user(DEVS) & filters.command("cpurgeme", "") & ~filters.me)
@KY.UBOT("purgeme")
async def purge_me_func(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    if len(message.command) != 2:
        return await message.delete()
    n = (
        message.reply_to_message
        if message.reply_to_message
        else message.text.split(None, 1)[1].strip()
    )
    if not n.isnumeric():
        return await message.reply(f"{emo.gagal} **Argumen Tidak Valid.**")
    n = int(n)
    if n < 1:
        return await message.reply(f"{emo.gagal} **Butuh nomor >=1-999.**")
    chat_id = message.chat.id
    message_ids = [
        m.id
        async for m in client.search_messages(
            chat_id,
            from_user=int(message.from_user.id),
            limit=n,
        )
    ]
    if not message_ids:
        return await message.reply(f"{emo.gagal} **Tidak ada pesan yang ditemukan.**")
    to_delete = [message_ids[i : i + 999] for i in range(0, len(message_ids), 999)]
    for hundred_messages_or_less in to_delete:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=hundred_messages_or_less,
            revoke=True,
        )
        mmk = await message.reply(f"{emo.sukses} {n} **Pesan Telah Di Hapus.**")
        await asyncio.sleep(2)
        await mmk.delete()


@ubot.on_message(filters.user(DEVS) & filters.command("cpurge", "") & ~filters.me)
@KY.UBOT("purge")
async def purgefunc(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    await message.delete()
    if not message.reply_to_message:
        return await eor(
            message, f"{emo.proses} **Silakan balas pesan untuk dibersihkan.**"
        )
    chat_id = message.chat.id
    message_ids = []
    for message_id in range(
        message.reply_to_message.id,
        message.id,
    ):
        message_ids.append(message_id)
        if len(message_ids) == 100:
            await client.delete_messages(
                chat_id=chat_id,
                message_ids=message_ids,
                revoke=True,
            )
            message_ids = []
    if len(message_ids) > 0:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=message_ids,
            revoke=True,
        )
