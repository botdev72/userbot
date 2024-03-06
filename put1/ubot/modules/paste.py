import os
import re

import aiofiles
from pyrogram import filters

from ubot import *
from ubot.utils import *

__MODULE__ = "Paste"
__HELP__ = """
Bantuan Untuk Pastebin

• Perintah: <code>{0}paste</code> [balas ke file]
• Penjelasan: Untuk memposting file ke pastebin.
"""
pattern = re.compile(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$")


@ubot.on_message(anjay("paste") & filters.me)
async def paste_func(_, message):
    if not message.reply_to_message:
        return await message.reply("<code>Mohon balas ke file atau pesan</code> ")
    r = message.reply_to_message

    if not r.text and not r.document:
        return await message.reply("<code>Mohon balas ke file atau pesan</code> ")

    m = await message.reply("<code>Processing ...</code> ")

    if r.text:
        content = str(r.text)
    elif r.document:
        if r.document.file_size > 40000:
            return await m.edit("You can only paste files smaller than 40KB.")

        if not pattern.search(r.document.mime_type):
            return await m.edit("Only text files can be pasted.")

        doc = await message.reply_to_message.download()

        async with aiofiles.open(doc, mode="r") as f:
            content = await f.read()

        os.remove(doc)

    link = await paste(content)
    kb = ikb({"Paste Link": link})
    try:
        if m.from_user.is_bot:
            await message.reply_photo(
                photo=link,
                quote=False,
                reply_markup=kb,
            )
        else:
            await message.reply_photo(
                photo=link,
                quote=False,
                caption=f"<b>Paste Link:</b> [Here]({link})",
            )
        await m.delete()
    except Exception:
        await m.edit("Here's your paste", reply_markup=kb)
