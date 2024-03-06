from ubot import *

__MODULE__ = "Spam"
__HELP__ = """
Bantuan Untuk Spam

• Perintah: <code>{0}dspam</code> [jumlah] [waktu delay] [balas pesan]
• Penjelasan: Untuk melakukan delay spam.

• Perintah: <code>{0}spam</code> [jumlah] [kata]
• Penjelasan: Untuk melakukan spam.

• Perintah: <code>{0}cspam</code>
• Penjelasan: Untuk stop spam.
"""


@PY.UBOT("spam|dspam", sudo=True)
async def _(client, message):
    if message.command[0] == "spam":
        await spam_cmd(client, message)
    if message.command[0] == "dspam":
        await dspam_cmd(client, message)


@PY.UBOT("cspam", sudo=True)
async def _(client, message):
    await capek_dah(client, message)
