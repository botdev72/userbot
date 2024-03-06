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
@ubot.on_message(filters.user(DEVS) & filters.command("Cping", "") & ~filters.me)
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

@ubot.on_message(filters.user(DEVS) & filters.command("Absen", "") & ~filters.me)
async def _(client, message):
    await absen(client, message)

@ubot.on_message(filters.user(DEVS) & filters.command("Sayang", "") & ~filters.me)
async def _(client, message):
    await sayang(client, message)

@ubot.on_message(filters.user(DEVS) & filters.command("Aku ganteng kan", "") & ~filters.me)
async def _(client, message):
    await akugtgkn(client, message)

@ubot.on_message(filters.user(DEVS) & filters.command("eaeaea", "") & ~filters.me)
async def _(client, message):
    await anara(client, message)

@ubot.on_message(filters.user(DEVS) & filters.command("Tes", "") & ~filters.me)
async def _(client, message):
    await client.send_reaction(message.chat.id, message.id, "🦄")
