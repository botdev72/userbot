from .. import *

__MODULE__ = "Emoji"
__HELP__ = """
Bantuan Untuk Emoji

• Perintah: <code>{0}setemo</code>
• Penjelasan: Untuk mengubah tampilan emoji ping.

• Perintah: <code>{0}setemo2</code>
• Penjelasan: Untuk mengubah tampilan emoji ping.
"""

@PY.UBOT("ping")
async def _(client, message):
    await ping_cmd(client, message)

@PY.UBOT("setemo")
async def _(client, message):
    await set_emoji(client, message)
    
@PY.UBOT("setemo2")
async def _(client, message):
    await set_emoji2(client, message)
    
@PY.BOT("start")
async def _(client, message):
    await start_cmd(client, message)
