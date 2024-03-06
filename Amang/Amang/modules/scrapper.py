from os import remove
from re import findall

from pyrogram.enums import ChatType
from pyrogram.types import *
from pyrogram import *

from Amang import *
from Amang.config import *

_SCRTXT = """
**✅ CC Scrapped Successfully!**

**Source ->** {}
**Amount ->** {}
**Skipped ->** {}
**Cc Found ->** {}


🥷 **Scrapped By ->** {}
👨‍🎤 **Developed By ->** @AmangProject 🐲
"""


@ubot.on_message(filters.me & filters.command("scrape", cmd))
async def _(client, message: Message):
    txt = ""
    skp = 0
    spl = message.text.split(" ")
    e3 = await message.reply_text("...", quote=True)
    if not spl:
        return await e3.edit("full cmd de vai.. 😔")
    elif len(spl) == 2:
        _chat = spl[1].strip()
        limit = 100
    elif len(spl) > 2:
        _chat = spl[1].strip()
        try:
            limit = int(spl[2].strip())
        except ValueError:
            return await e3.edit("No. of card to Scrape must be Integer!")

    await e3.edit(f"`Scrapping from {_chat}. \nHold your Horses...`")
    _get = lambda message: getattr(message, "text", 0) or getattr(message, "caption", 0)
    _getcc = lambda message: list(filter(bool, findall("\d{16}\|\d{2,4}\|\d{2,4}\|\d{2,4}", message)))

    async for x in c.get_chat_history(_chat, limit=limit):
        if not (text := _get(x)):
            skp += 1
            continue
        if not (cc := _getcc(text)):
            skp += 1
        else:
            txt += "\n".join(cc) + "\n"

    cap = _SCRTXT.format(
        _chat,
        str(limit),
        str(skp),
        str(txt.count("\n")),
        message.from_user.mention,
    )
    file = f"x{limit} CC Scrapped by AmangUb.txt"
    with open(file, "w+") as f:
        f.write(txt)
    del txt
    y = await client.send_document(
        message.chat.id,
        file,
        caption=cap,
        reply_to_message_id=message.id,
    )
    remove(file)
    await e3.delete()