"""credits Tomi Setiawan > @T0M1_X"""
# Copas Teriak Copas MONYET
# Gay Teriak Gay Anjeng
# @Rizzvbss | @Kenapanan
# Kok Bacot
# © @KynanSupport
# FULL MONGO NIH JING FIX MULTI CLIENT


import random

from Amang import *

__MODULE__ = "meme"
__HELP__ = f"""
 Document for Meme

• Command: <code>{cmd[0]}meme or memes</code>
• Function: Membuat kata meme.
"""


@ubot.on_message(filters.me & filters.command(["meme", "memes"], cmd))
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply(f"<code>{cmd}memes</code> [text]")
    text = f"#{random.randrange(67)} {message.text.split(None, 1)[1]}"
    TM = await message.reply("<code>Processing...</code>")
    x = await client.get_inline_bot_results("StickerizerBot", text)
    saved = await client.send_inline_bot_result(
        client.me.id, x.query_id, x.results[0].id
    )
    saved = await client.get_messages(client.me.id, int(saved.updates[1].message.id))
    await client.send_sticker(
        message.chat.id, saved.sticker.file_id, reply_to_message_id=message.id
    )
    await saved.delete()
    await TM.delete()
