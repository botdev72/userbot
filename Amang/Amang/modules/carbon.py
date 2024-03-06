# Copas Teriak Copas MONYET
# Gay Teriak Gay Anjeng
# @Rizzvbss | @Kenapanan
# Kok Bacot
# © @KynanSupport
# FULL MONGO NIH JING FIX MULTI CLIENT

import asyncio

from pyrogram import *
from pyrogram.types import *

from Amang import *
from Amang.config import *
from Amang.utils import *

__MOD__ = "carbon"
__HELP__ = f"""
 Document for Carbon

• Command: <code>{cmd[0]}carbon</code> [balas pesan]
• Function: Untuk membuat teks menjadi carbonara.
"""


@ubot.on_message(filters.me & filters.command(["carbon"], cmd))
async def carbon_func(client, message):
    text = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    if not text:
        return await message.delete()
    ex = await eor(message, "Processing . . .")
    carbon = await make_carbon(text)
    await ex.edit("Uploading . . .")
    await asyncio.gather(
        ex.delete(),
        client.send_photo(
            message.chat.id,
            carbon,
            caption=f"<b>Carbonised by :</b>{client.me.mention}",
        ),
    )
    carbon.close()
