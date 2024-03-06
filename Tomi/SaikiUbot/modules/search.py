import random

from pyrogram.types import InputMediaPhoto

from .. import *

__MODULE__ = "SEARCH"
__HELP__ = f"""
Perintah:
          <code>{PREFIX[0]}bing</code> or <code>{PREFIX[0]}pic</code> [query]
Penjelasan:
           Untuk mencari photo random dari google 

Perintah:
          <code>{PREFIX[0]}gif</code> [query]
Penjelasan:
           Untuk mencari gift/animation random dari google 
"""


@PY.UBOT(["bing", "pic"], PREFIX)
async def _(client, message):
    TM = await message.reply("<b>Memproses...</b>")
    if len(message.command) < 2:
        return await TM.edit(f"<code>{message.text}</code> [query]")
    x = await client.get_inline_bot_results(
        message.command[0], message.text.split(None, 1)[1]
    )
    get_media = []
    for X in range(2):
        try:
            saved = await client.send_inline_bot_result(
                client.me.id, x.query_id, x.results[random.randrange(len(x.results))].id
            )
            saved = await client.get_messages(
                client.me.id, int(saved.updates[1].message.id)
            )
            get_media.append(InputMediaPhoto(saved.photo.file_id))
            await saved.delete()
        except:
            await TM.edit(f"<b>❌ Image Photo Ke {X} Tidak Ditemukan</b>")
    await client.send_media_group(
        message.chat.id,
        get_media,
        reply_to_message_id=message.id,
    )
    await TM.delete()


@PY.UBOT("gif", PREFIX)
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply(f"<code>{message.text}</code> [query]")
    TM = await message.reply("<b>Memproses...</b>")
    x = await client.get_inline_bot_results(
        message.command[0], message.text.split(None, 1)[1]
    )
    try:
        saved = await client.send_inline_bot_result(
            client.me.id, x.query_id, x.results[random.randrange(len(x.results))].id
        )
    except:
        await message.reply("<b>❌ Gif tidak ditemukan</b>")
        await TM.delete()
    saved = await client.get_messages(client.me.id, int(saved.updates[1].message.id))
    await client.send_animation(
        message.chat.id, saved.animation.file_id, reply_to_message_id=message.id
    )
    await TM.delete()
    await saved.delete()
