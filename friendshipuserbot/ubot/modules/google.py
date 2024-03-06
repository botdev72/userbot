from ubot import *

__MODULE__ = "Google"
__HELP__ = """
 Bantuan Untuk Google

• Perintah: <code>{0}google</code> [query]
• Penjelasan: Untuk mencari something.
"""


@PY.UBOT("google", sudo=True)
async def _(client, message):
    await gsearch(client, message)
