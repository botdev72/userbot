from ubot import *

__MODULE__ = "Read"
__HELP__ = """
 Bantuan Untuk Ocr

• Perintah : <code>{0}ocr</code> [balas media]
• Penjelasan : Untuk membaca teks dari media.
"""


@PY.UBOT("ocr", sudo=True)
async def _(client, message):
    await read_cmd(client, message)
