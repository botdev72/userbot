from ubot import *

__MODULE__ = "Convert"
__HELP__ = """
 Bantuan Untuk Convert

• Perintah : <code>{0}toanime</code> [balas foto/sticker]
• Penjelasan : Merubah gambar ke anime.

• Perintah : <code>{0}toimg</code> [balas stiker/gif]
• Penjelasan : Merubah stiker/gif ke foto.

• Perintah : <code>{0}tosticker</code> [balas ke foto]
• Penjelasan : Merubah foto ke stiker.

• Perintah : <code>{0}togif</code> [balas stiker]
• Penjelasan : Merubah stiker ke gif.

• Perintah : <code>{0}toaudio</code> [balas video]
• Penjelasan : Merubah video menjadi audio mp3.

• Perintah : <code>{0}efek</code> [efek kode - nama efek]
  <b>• efek kode:</b>  <code>bengek</code> <code>robot</code> <code>jedug</code> <code>fast</code> <code>echo</code>
• Penjelasan : Merubah suara voice note.
  
• Perintah : <code>{0}curi</code> [balas pesan]
• Penjelasan : Untuk mencuri media timer, cek pesan tersimpan
"""


@PY.UBOT("toanime", sudo=True)
async def _(client, message):
    await convert_anime(client, message)


@PY.UBOT("toimg", sudo=True)
async def _(client, message):
    await convert_photo(client, message)


@PY.UBOT("tosticker", sudo=True)
async def _(client, message):
    await convert_sticker(client, message)


@PY.UBOT("togif", sudo=True)
async def _(client, message):
    await convert_gif(client, message)


@PY.UBOT("toaudio", sudo=True)
async def _(client, message):
    await convert_audio(client, message)


@PY.UBOT("efek", sudo=True)
async def _(client, message):
    await convert_efek(client, message)


@PY.UBOT("curi", sudo=True)
async def _(client, message):
    await colong_cmn(client, message)
