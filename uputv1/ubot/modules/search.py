from ubot import *

__MODULE__ = "Search"
__HELP__ = """
Bantuan Untuk Search

• Perintah: <code>{0}pic</code> [query]
• Penjelasan: Untuk gambar secara limit 5.

• Perintah: <code>{0}gif</code> [query]
• Penjelasan: Untuk gif.
"""



@PY.UBOT("bing|pic")
async def _(client, message):
    await pic_bing_cmd(client, message)


@PY.UBOT("gif")
async def _(client, message):
    await gif_cmd(client, message)
