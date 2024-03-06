from ubot import *

__MODULE__ = "Kang"
__HELP__ = """
 Bantuan Untuk Kang

• Perintah : <code>{0}kang</code> [balas ke stiker]
• Penjelasan : Untuk membuat kosum stiker pak.
"""


#@PY.BOT("kang")
#async def _(client, message):
    #await kang_cmd_bot(client, message)


@PY.UBOT("kang")
async def _(client, message):
    await kang(client, message)
