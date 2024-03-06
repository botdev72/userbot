from telegraph import Telegraph, exceptions, upload_file

from .. import *
from ..modules.convert import dl_pic

__MODULE__ = "TELEGRAPH"
__HELP__ = f"""
Perintah:
         <code>{PREFIX[0]}tg</code> [reply media/text]
Penjelasan:
           Untuk mengapload media/text ke telegra.ph 
"""

telegraph = Telegraph()


@PY.UBOT("tg", PREFIX)
async def _(client, message):
    XD = await message.reply("<code>Sedang Memproses . . .</code>")
    if not message.reply_to_message:
        await XD.edit(
            "<b>Mohon Balas Ke Pesan, Untuk Mendapatkan Link dari Telegraph.</b>"
        )
        return
    if message.reply_to_message.media:
        m_d = await dl_pic(client, message.reply_to_message)
        try:
            media_url = upload_file(m_d)
        except exceptions.TelegraphException as exc:
            return await XD.edit(f"<b>ERROR:</b> <code>{exc}</code>")
        U_done = f"<b>Berhasil diupload ke</b> <a href='https://telegra.ph/{media_url[0]}'>Telegraph</a>"
        await XD.edit(U_done)
    elif message.reply_to_message.text:
        page_title = f"{client.me.first_name} {client.me.last_name or ''}"
        page_text = message.reply_to_message.text
        page_text = page_text.replace("\n", "<br>")
        try:
            response = telegraph.create_page(page_title, html_content=page_text)
        except exceptions.TelegraphException as exc:
            return await XD.edit(f"<b>ERROR:</b> <code>{exc}</code>")
        wow_graph = f"<b>Berhasil diupload ke</b> <a href='https://telegra.ph/{response['path']}'>Telegraph</a>"
        await XD.edit(wow_graph)
