import random
from asyncio import sleep

from pyrogram.types import InputMediaPhoto

from ubot import *
from ubot.utils import *

__MODULE__ = "Search"
__HELP__ = """
Bantuan Untuk Search

• Perintah: <code>{0}pic</code> [query]
• Penjelasan: Untuk gambar secara limit 5.

• Perintah: <code>{0}gif</code> [query]
• Penjelasan: Untuk gif.
"""


@KY.UBOT("pic", sudo=True)
async def pic_bing_cmd(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    TM = await message.reply(f"{emo.proses} **Processing...**")
    await sleep(2)
    if len(message.command) < 2:
        return await TM.edit(f"{emo.gagal} <code>{message.text}</code> [query]")
    x = await client.get_inline_bot_results(
        message.command[0], message.text.split(None, 1)[1]
    )
    get_media = []
    for X in range(5):
        try:
            saved = await client.send_inline_bot_result(
                client.me.id, x.query_id, x.results[random.randrange(30)].id
            )
            saved = await client.get_messages(
                client.me.id, int(saved.updates[1].message.id), replies=0
            )
            get_media.append(InputMediaPhoto(saved.photo.file_id))
            await saved.delete()
        except BaseException:
            await TM.edit(f"{emo.gagal} <b>Image Photo Ke {X} Tidak Ditemukan</b>")
    await client.send_media_group(
        message.chat.id,
        get_media,
        reply_to_message_id=message.id,
    )
    await TM.delete()


@KY.UBOT("gif", sudo=True)
async def gif_cmd(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    Tm = await message.reply(f"{emo.proses} **Processing...**")
    await sleep(2)
    if len(message.command) < 2:
        return await Tm.edit(f"{emo.gagal} <code>{message.text}</code> [query]")
    x = await client.get_inline_bot_results(
        message.command[0], message.text.split(None, 1)[1]
    )
    try:
        saved = await client.send_inline_bot_result(
            client.me.id, x.query_id, x.results[random.randrange(30)].id
        )
    except BaseException:
        await Tm.edit(f"{emo.gagal} <b>Gif tidak ditemukan</b>")
        await TM.delete()
    saved = await client.get_messages(
        client.me.id, int(saved.updates[1].message.id), replies=0
    )
    await client.send_animation(
        message.chat.id, saved.animation.file_id, reply_to_message_id=message.id
    )
    await TM.delete()
    await saved.delete()
