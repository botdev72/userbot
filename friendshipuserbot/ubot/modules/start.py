from ubot import *

__MODULE__ = "Emoji"
__HELP__ = """
Bantuan Untuk Emoji

• Perintah: <code>{0}setemo</code>
• Penjelasan: Untuk mengubah tampilan emoji ping.

• Perintah: <code>{0}setemo2</code>
• Penjelasan: Untuk mengubah tampilan emoji ping.
"""


@PY.UBOT("ping", sudo=True)
@ubot.on_message(filters.user(USER_ID) & filters.command("ping", "f") & ~filters.me)
async def _(client, message):
    await ping_cmd(client, message)


@PY.UBOT("setemo", sudo=True)
async def _(client, message):
    await set_emoji(client, message)


@PY.UBOT("setemo2", sudo=True)
async def _(client, message):
    await set_emoji2(client, message)


@PY.BOT("start")
async def _(client, message):
    await start_cmd(client, message)
