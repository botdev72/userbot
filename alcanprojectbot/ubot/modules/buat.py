from ubot import *

__MODULE__ = "Create"
__HELP__ = """
 Bantuan Untuk Create

• Perintah: <code>{0}create</code> gc
• Penjelasan: Untuk membuat grup telegram.

• Perintah: <code>{0}create</code> ch
• Penjelasan: Untuk membuat channel telegram.
"""


@PY.UBOT("create")
async def _(client, message):
    await buat_apaam(client, message)
