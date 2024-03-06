from ubot import *

__MODULE__ = "Purge"
__HELP__ = """
Bantuan Untuk Purge

• Perintah: <code>{0}purge</code> [reply to message]
• Penjelasan: Bersihkan (hapus semua pesan) obrolan dari pesan yang dibalas hingga yang terakhir.

• Perintah: <code>{0}del</code> [reply to message]
• Penjelasan: Hapus pesan yang dibalas.

• Perintah: <code>{0}purgeme</code> [number of messages]
• Penjelasan: Hapus pesan anda sendiri dengan menentukan total pesan.
"""


@PY.UBOT("del", sudo=True)
async def _(client, message):
    await del_cmd(client, message)


@PY.UBOT("purgeme", sudo=True)
async def _(client, message):
    await purgeme_cmd(client, message)


@PY.UBOT("purge", sudo=True)
async def _(client, message):
    await purge_cmd(client, message)
