from ubot import *


__MODULE__ = "Music"
__HELP__ = """
Bantuan Untuk Music

• Perintah: <code>{0}play</code>
• Penjelasan: Untuk memulai voice chat grup.

• Perintah: <code>{0}end</code>
• Penjelasan: Untuk mengakhiri voice chat grup.

• Perintah: <code>{0}skip</code>
• Penjelasan: Untuk memulai voice chat grup.

• Perintah: <code>{0}pause</code>
• Penjelasan: Untuk mengakhiri voice chat grup.
"""



@PY.UBOT("play", FILTERS.ME_GROUP)
@cek_violet
async def _(client, message):
    await play_nya(client, message)


@PY.UBOT("end", FILTERS.ME_GROUP)
@cek_violet
async def _(client, message):
    await endnua(client, message)


@PY.UBOT("skip", FILTERS.ME_GROUP)
@cek_violet
async def _(client, message):
    await sekipnya(client, message)


@PY.UBOT("pause", FILTERS.ME_GROUP)
@cek_violet
async def _(client, message):
    await pausnya(client, message)
    
    
@PY.UBOT("resume", FILTERS.ME_GROUP)
@cek_violet
async def _(client, message):
    await resumenua(client, message)


@PY.INLINE("^_yts")
async def _(client, inline_query):
    await inline_play1(client, inline_query)
    
    
@PY.INLINE("^_x")
async def _(client, inline_query):
    await inline_play2(client, inline_query)


@PY.CALLBACK("^_c")
async def _(client, callback_query):
    await call_back1(client, callback_query)
    
    
@PY.CALLBACK("^_s")
async def _(client, callback_query):
    await call_back2(client, callback_query)
    
    
@PY.CALLBACK("^_p")
async def _(client, callback_query):
    await call_back3(client, callback_query)
    
    
@PY.CALLBACK("^_v")
async def _(client, callback_query):
    await call_back4(client, callback_query)
    
    
@PY.CALLBACK("^_xp")
async def _(client, callback_query):
    await call_back5(client, callback_query)
    
    
@PY.CALLBACK("^_mxv")
async def _(client, callback_query):
    await call_back6(client, callback_query)
    
@PY.CALLBACK("^1_cls")
async def _(client, callback_query):
    await call_back_close(client, callback_query)