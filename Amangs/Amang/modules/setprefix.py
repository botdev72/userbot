import asyncio
import re

from pyrogram import enums, filters
from pyrogram.errors import *
from pyrogram.types import *

from Amang import *
from Amang.config import *
from Amang.utils import *


__MOD__ = "Prefixes"
__HELP__ = f"""
Document for Prefixes

• Command: <code>{cmd[0]}setprefix [new_prefix] (s)</code>
• Function: Mengubah prefix yang digunakan oleh bot.

🔹 Cara Menggunakan:
   Kirim perintah <code>{cmd[0]}setprefix</code> diikuti dengan prefix baru yang ingin Anda gunakan.

Contoh:
   - <code>{cmd[0]}setprefix !</code>
   - <code>{cmd[0]}setprefix .</code>
   - <code>{cmd[0]}setprefix /</code>

Ketika prefix diubah, bot akan menggunakan prefix baru yang Anda tentukan untuk menjalankan perintah-perintahnya.
"""


@ubot.on_message(filters.me & anjay("setprefix"))
@check_access
async def setprefix(client, message):
    Amang = await message.reply("`Processing...`")
    if len(message.command) < 2:
        return await Amang.edit(f"❔ Prefix mana yang harus diubah?")
    else:
        if message.command[1].lower() == "none":
            prefix = [""]
        else:
            prefix = message.command[1:]
        try:
            client.set_prefix(client.me.id, prefix)
            await set_pref(client.me.id, prefix)
            return await Amang.edit(
                f"✅ Prefix diubah ke : {' '.join(message.command[1:])}"
            )
        except Exception as error:
            await Amang.edit(error)


@ubot.on_message(filters.me & anjay("getprefix"))
async def getprefix(client, message):
    Tm = await message.reply("`Processing...`")
    try:
        # Mendapatkan prefix yang sedang digunakan dari penyimpanan atau database
        prefix = await get_prefix(client.me.id)
        if not prefix:
            prefix = "Tidak ada prefix yang ditentukan."

        await Tm.edit(f"🌐 Prefix yang digunakan: {prefix}")
    except Exception as error:
        await Tm.edit(error)
