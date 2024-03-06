import asyncio

from pyrogram.errors import FloodWait

from ubot import *

from .gcast import get_message

__MODULE__ = "Broadcast 2"
__HELP__ = """
 Bantuan Untuk Broadcast 2

• Perintah : <code>{0}gcsdb</code> [Waktu] [Balas ke pesan]
• Penjelasan : Untuk mengirim pesan ke semua group di database.

• Perintah : <code>{0}listgcdb</code> 
• Penjelasan : Melihat daftar grup gcast didalam database.

• Perintah : <code>{0}addgcdb</code> 
• Penjelasan : Menambahkan grup ke dalam database gcast.

• Perintah : <code>{0}delgcdb</code> 
• Penjelasan : Menghapus grup dari database gcast.
"""


@KY.UBOT("gcsdb", sudo=True)
async def _(c, m):
    emo = Emo(c.me.id)
    await emo.initialize()
    pler = await m.reply(f"{emo.proses} **Processing...**")
    teks = get_message(m)
    if not teks:
        return await pler.edit(
            f"{emo.gagal} **Silakan balas ke pesan atau berikan pesan.**"
        )
    bunting = 0
    mandul = 0
    gcnyadb = await ambil_gcs(c.me.id)
    for mmk in gcnyadb:
        try:
            if m.reply_to_message:
                await teks.copy(mmk)
            else:
                await c.send_message(mmk, teks)
            await asyncio.sleep(0.2)
            bunting += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            if m.reply_to_message:
                await teks.copy(mmk)
            else:
                await c.send_message(mmk, teks)
            bunting += 1
        except Exception:
            mandul += 1
    await pler.delete()
    return await c.send_message(
        m.chat.id,
        f"{emo.alive} **Pesan Broadcast Terkirim :\n{emo.sukses} Berhasil di `{bunting}` Grup.\n{emo.gagal} Gagal di `{mandul}` Grup.**",
    )


@KY.UBOT("listgcdb", sudo=True)
async def _(c, m):
    emo = Emo(c.me.id)
    await emo.initialize()
    user_id = c.me.id
    await ambil_gcs(user_id)
    coli = await m.reply(f"{emo.proses} **Processing...**")
    msg = f"{emo.sukses} **Daftar Broadcast Database `{len(await ambil_gcs(user_id))}`:**\n\n"
    for gg in await ambil_gcs(c.me.id):
        try:
            get = await c.get_chat(gg)
            msg += f"**• {get.title} | `{get.id}`**\n"
        except:
            msg += f"**• `{gg}`**\n"
    await coli.delete()
    await m.reply(msg)


@KY.UBOT("addgcdb|delgcdb", sudo=True)
async def _(c, m):
    emo = Emo(c.me.id)
    await emo.initialize()
    user_id = c.me.id
    chat_id = m.command[1] if len(m.command) > 1 else m.chat.id
    mmk = await m.reply(f"{emo.proses} **Processing...**")
    if m.command[0] == "addgcdb":
        await tambah_gcs(user_id, chat_id)
        await mmk.edit(f"`{chat_id}` **Berhasil di tambahkan ke database gcast.**")
    elif m.command[0] == "delgcdb":
        await kureng_gcs(user_id, chat_id)
        await mmk.edit(f"`{chat_id}` **Berhasil di hapus dari database gcast.**")
    else:
        return await mmk.edit(f"**Silakan ketik {m.text}.**")
