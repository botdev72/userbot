from ubot import *

__MODULE__ = "Notes"
__HELP__ = """
 Bantuan Untuk Notes

• Perintah : <code>{0}save</code> [nama - balas pesan]
• Penjelasan : Untuk menyimpan catatan.

• Perintah : <code>{0}get</code> [nama]
• Penjelasan : Untuk mengambil catatan yang tersimpan.

• Perintah : <code>{0}rm</code> [nama]
• Penjelasan : Untuk menghapus nama catatan.

• Perintah : <code>{0}notes</code>
• Penjelasan : Untuk melihat daftar catatan yang disimpan.

• Note: Untuk menggunakan button, Gunakan Format :
<code>Mbah google [google|google.com]</code>
"""


@PY.UBOT("save", sudo=True)
async def _(client, message):
    await addnote_cmd(client, message)


@PY.UBOT("get", sudo=True)
async def _(client, message):
    await get_cmd(client, message)


@PY.INLINE("^get_notes")
@INLINE.QUERY
async def _(client, inline_query):
    await get_notes_button(client, inline_query)


@PY.UBOT("rm", sudo=True)
async def _(client, message):
    await delnote_cmd(client, message)


@PY.UBOT("notes", sudo=True)
async def _(client, message):
    await notes_cmd(client, message)
