import os
from asyncio import sleep

from pyrogram.types import *
from removebg import RemoveBg

from ubot import *
from ubot.config import *
from ubot.utils import *

RMBG_API = os.environ.get("RMBG_API", "a6qxsmMJ3CsNo7HyxuKGsP1o")

DOWN_PATH = "ubot/resources/"

IMG_PATH = DOWN_PATH + "sky.jpg"

__MODULE__ = "Rmbg"
__HELP__ = """
Bantuan Untuk Remove BG

• Perintah: <code>{0}rmbg</code> [reply to photo]
• Penjelasan: Untuk menghapus background dari foto.
"""


@KY.UBOT("rmbg")
async def remove_bg(client, message):
    if not RMBG_API:
        return
    emo = Emo(client.me.id)
    await emo.initialize()
    Tm = await message.reply(f"{emo.proses} **Processing...**")
    await sleep(2)
    replied = message.reply_to_message
    if replied.photo or replied.document or replied.sticker or replied.animation:
        if os.path.exists(IMG_PATH):
            os.remove(IMG_PATH)
        await client.download_media(message=replied, file_name=IMG_PATH)
        await Tm.edit(f"{emo.proses} **Removing...**")
        try:
            rmbg = RemoveBg(RMBG_API, "rm_bg_error.log")
            rmbg.remove_background_from_img_file(IMG_PATH)
            remove_img = IMG_PATH + "_no_bg.png"
            await client.send_photo(
                chat_id=message.chat.id,
                photo=remove_img,
                reply_to_message_id=message.id,
                disable_notification=True,
            )
            await Tm.delete()
        except Exception as e:
            await Tm.edit(f"{emo.gagal} **Error :\n\n`{e}`.**")
    else:
        await Tm.edit(
            f"{emo.gagal} **Usage: Mohon reply ke gambar yang ingin dihapus backgroundnya.**"
        )
