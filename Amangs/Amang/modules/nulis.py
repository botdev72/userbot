# Copas Teriak Copas MONYET
# Gay Teriak Gay Anjeng
# @Rizzvbss | @Kenapanan
# Kok Bacot
# © @KynanSupport
# FULL MONGO NIH JING FIX MULTI CLIENT


import requests
from pyrogram import *
from pyrogram.types import *

from Amang import *
from Amang.config import *
from Amang.utils import *


@ubot.on_message(filters.me & anjay("nulis"))
async def handwrite(client, message):
    if message.reply_to_message:
        naya = message.reply_to_message.text
    else:
        naya = message.text.split(None, 1)[1]
    nan = await eor(message, "Processing...")
    ajg = requests.get(f"https://api.sdbots.tk/write?text={naya}").url
    await message.reply_photo(
        photo=ajg, caption=f"<b>Ditulis Oleh :</b> {client.me.mention}"
    )
    await nan.delete()
