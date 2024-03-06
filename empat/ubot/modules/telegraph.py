import os
from asyncio import sleep

from telegraph import Telegraph, exceptions, upload_file

from ubot import *
from ubot.utils import *

__MODULE__ = "Telegraph"
__HELP__ = """
Bantuan Untuk Telegraph

• Perintah: <code>{0}tg</code> [reply media/text]
• Penjelasan: Untuk mengapload media/text ke telegra.ph.
"""

telegraph = Telegraph()


@KY.UBOT("tg")
async def _(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    XD = await message.reply(f"{emo.proses} <b>Processing...</b>")
    await sleep(1)
    if not message.reply_to_message:
        await XD.edit(
            f"{emo.gagal} <b>Mohon Balas Ke Pesan, Untuk Mendapatkan Link dari Telegraph.</b>"
        )
        return
    if message.reply_to_message.media:
        m_d = await message.reply_to_message.download()
        try:
            media_url = upload_file(m_d)
        except exceptions.TelegraphException as exc:
            await XD.edit(f"{emo.gagal} <b>ERROR:</b> <code>{exc}</code>")
            os.remove(m_d)
            return
        U_done = f"{emo.sukses} <b>Berhasil diupload ke</b> <a href='https://telegra.ph/{media_url[0]}'>Telegraph</a>"
        await XD.edit(U_done)
        os.remove(m_d)
    elif message.reply_to_message.text:
        page_title = f"{client.me.first_name} {client.me.last_name or ''}"
        page_text = message.reply_to_message.text
        page_text = page_text.replace("\n", "<br>")
        try:
            response = telegraph.create_page(page_title, html_content=page_text)
        except exceptions.TelegraphException as exc:
            await XD.edit(f"{emo.gagal} <b>ERROR:</b> <code>{exc}</code>")
            return
        wow_graph = f"{emo.sukses} <b>Berhasil diupload ke</b> <a href='https://telegra.ph/{response['path']}'>Telegraph</a>"
        await XD.edit(wow_graph)
