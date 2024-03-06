import asyncio

from pyrogram import *
from pyrogram.types import *

from . import bot, ubot, anjay, cobadah
from Amang.utils import *

__MOD__ = "Misc"
__HELP__ = f"""
 Document for misc

• Command: <code>{cmd[0]}carbon</code> [balas pesan]
• Function: Untuk membuat teks menjadi carbonara.

• Command: <code>{cmd[0]}ip</code> [ip host]
• Function: Untuk mencari lokasi ip address.

• Command: <code>{cmd[0]}meme or memes</code>
• Function: Membuat kata meme.

• Command: <code>{cmd[0]}nulis</code> [text/reply to text/media]
• Function: Buat kamu yang malas nulis.

• Command: <code>{cmd[0]}paste</code> [balas ke file]
• Function: Untuk memposting file ke pastebin.

• Command: <code>{cmd[0]}zombies</code>
• Function: Ban Deleted Accounts.

• Command: <code>{cmd[0]}ss or webss</code> [link]
• Function: Untuk mendapatkan screenshot dari link tersebut.

• Command: <code>{cmd[0]}logo</code> [text]
• Function: Untuk membuat sebuah logo dengan background random.

• Command: <code>{cmd[0]}rmbg</code> [reply to photo]
• Function: Untuk menghapus background dari foto.
"""


@ubot.on_message(filters.me & anjay("carbon"))
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
