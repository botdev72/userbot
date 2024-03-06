from ubot import *


__MODULE__ = "VoiceChat"
__HELP__ = """
Bantuan Untuk Voice Chat

• Perintah: <code>{0}startvc</code>
• Penjelasan: Untuk memulai voice chat grup.

• Perintah: <code>{0}stopvc</code>
• Penjelasan: Untuk mengakhiri voice chat grup.
"""



@PY.UBOT("startvc")
async def _(client, message):
    await start_vctools(client, message)


@PY.UBOT("stopvc")
async def _(client, message):
    await stop_vctools(client, message)


@PY.UBOT("naikygy")
async def _(client, message):
    await join_os(client, message)


@PY.UBOT("turunygy")
async def _(client, message):
    await turun_os(client, message)
