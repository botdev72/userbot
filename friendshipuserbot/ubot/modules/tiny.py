from ubot import *

__MODULE__ = "Tiny"
__HELP__ = """
Bantuan Untuk Tiny

• Perintah: <code>{0}tiny</code> [reply to sticker]
• Penjelasan: Untuk merubah sticker menjadi kecil.
"""


@PY.UBOT("tiny", sudo=True)
async def _(client, message):
    await tiny_cmd(client, message)
