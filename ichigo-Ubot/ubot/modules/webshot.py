from ubot import *

__MODULE__ = "Webshot"
__HELP__ = """
Bantuan Untuk Webshot

• Perintah: <code>{0}ss</code> [link]
• Penjelasan: Untuk mendapatkan screenshot dari link tersebut.
"""


@PY.UBOT("webss", sudo=True)
async def _(client, message):
    await take_ss(client, message)
