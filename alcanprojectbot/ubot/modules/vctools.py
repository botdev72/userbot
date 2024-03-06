from ubot import *


__MODULE__ = "VoiceChat"
__HELP__ = """
Bantuan Untuk Voice Chat

• Perintah: <code>{0}startvc</code>
• Penjelasan: Untuk memulai voice chat grup.

• Perintah: <code>{0}stopvc</code>
• Penjelasan: Untuk mengakhiri voice chat grup.

• Perintah: <code>{0}joinvc</code>
• Penjelasan: Untuk bergabung voice chat grup.

• Perintah: <code>{0}leavevc</code>
• Penjelasan: Untuk meninggalkan voice chat grup.
"""



@PY.UBOT("startvc")
async def _(client, message):
    await start_vctools(client, message)


@PY.UBOT("stopvc")
async def _(client, message):
    await stop_vctools(client, message)


@PY.UBOT("joinvc")
@cek_pro
async def _(client, message):
    await joinvc(client, message)


@PY.UBOT("leavevc")
@cek_pro
async def _(client, message):
    await leavevc(client, message)
