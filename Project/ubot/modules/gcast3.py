import asyncio
import time

from pyrogram.errors import (ChatWriteForbidden, FloodWait, PeerIdInvalid,
                             SlowmodeWait)

from ubot import (BLACKLIST_CHAT, KY, ambil_daftar, daftar_rndm, get_chat,
                  kureng_kata, kureng_rndm, tambah_kata, tambah_rndm)

from .gcast import get_broadcast_id

spam_gikesan = {}

__MODULE__ = "Broadcast 3"
__HELP__ = """
 Bantuan Untuk Broadcast 3

• Perintah : <code>{0}addkata</code> [Balas ke pesan]
• Penjelasan : Tambah kata gikes .

• Perintah : <code>{0}remkata</code> [Kasih Teks]
• Penjelasan : Apus kats gikes.

• Perintah : <code>{0}gcast3</code> 
• Penjelasan : Gas random gikes.

• Perintah : <code>{0}addrndm</code> [Balas ke pesan]
• Penjelasan : Tambah kata random.

• Perintah : <code>{0}remrndm</code> [Kasih Teks]
• Penjelasan : Apus kata random.

• Perintah : <code>{0}cekrndm</code> 
• Penjelasan : Cek kata random

• Perintah : <code>{0}cekkata</code> 
• Penjelasan : Cek kata gikes

• Perintah : <code>{0}stgcs3</code> 
• Penjelasan : Matiin spam gikes random.
"""


async def spam_kontol_gikes_memek(
    client, gc, kata_list, kirim_kata, index_gikes, rndm_list, kirim_rndm, index_random
):
    try:
        while True:
            await asyncio.sleep(2)
            katanya = index_gikes % len(kata_list)
            kondomnya = index_random % len(rndm_list)
            mulai = time.time()
            tititnya = 0
            while tititnya < 180:
                await asyncio.sleep(5)
                try:
                    ii = rndm_list[kondomnya]
                    xx = kata_list[katanya]
                    kata = f"**{xx} {ii}**"
                    await client.send_message(gc, kata)
                    index_random += 1
                    index_gikes += 1
                    kirim_rndm.append(kondomnya)
                    kirim_kata.append(katanya)

                except (PeerIdInvalid, ChatWriteForbidden, SlowmodeWait):
                    continue
                katanya = index_gikes % len(kata_list)
                # kondomnya = index_random % len(rndm_list)
                kondomnya += 1
                if kondomnya == len(rndm_list):
                    kondomnya = 0

                tititnya = time.time() - mulai

    except FloodWait:
        if gc in spam_gikesan:
            task = spam_gikesan[gc]
            task.cancel()
            del spam_gikesan[gc]


@KY.UBOT("gcast3", sudo=True)
async def _(client, message):
    cek_gc = await get_broadcast_id(client, "group")
    blacklist = await get_chat(client.me.id)
    ambil_bang = await ambil_daftar(client.me.id)
    rndm = await daftar_rndm(client.me.id)

    for gc in cek_gc:
        if gc in blacklist or gc in BLACKLIST_CHAT:
            continue

        try:
            kirim_kata = []
            kirim_rndm = []
            index_gikes = 0
            index_random = 0

            task = asyncio.create_task(
                spam_kontol_gikes_memek(
                    client,
                    gc,
                    ambil_bang,
                    kirim_kata,
                    index_gikes,
                    rndm,
                    kirim_rndm,
                    index_random,
                )
            )
            spam_gikesan[gc] = task
        except Exception as e:
            print(e)

    await message.reply("**Ok Anj Diproses, kalo mo matiin ketik .stoptes.**")


@KY.UBOT("addkata", sudo=True)
async def _(client, message):
    if message.reply_to_message:
        kata = message.reply_to_message.text
    else:
        kata = message.text.split(None, 1)[1]
    if not kata:
        return await message.reply_text("**Minimal kasih teks lah anj**")
    await tambah_kata(client.me.id, kata)
    await message.reply_text(f"**Masuk `{kata}` ke kata gikes.**")


@KY.UBOT("remkata", sudo=True)
async def _(client, message):
    if message.reply_to_message:
        kata = message.reply_to_message.text
    else:
        kata = message.text.split(None, 1)[1]
    if not kata:
        return await message.reply_text("**Minimal kasih teks lah anj**")
    await kureng_kata(client.me.id, kata)
    await message.reply_text(f"**Dihapus `{kata}` dari kata gikes.**")


@KY.UBOT("cekkata", sudo=True)
async def _(client, message):
    gua = await client.get_me()
    data = await ambil_daftar(client.me.id)
    if not data:
        await message.reply_text("**Kosong kintl kata gikesnya**")
    else:
        msg = f"Nih kata kata gikes jamet lu `{gua.first_name}` :\n"
        for kata in data:
            msg += f"**-** `{kata}`\n"
        await message.reply_text(msg)


@KY.UBOT("stgcs3", sudo=True)
async def _(client, message):
    cek_gc = await get_broadcast_id(client, "group")
    for chat_id in cek_gc:
        if chat_id in spam_gikesan:
            task = spam_gikesan[chat_id]
            task.cancel()
            del spam_gikesan[chat_id]
    await message.reply("**Oke jing berenti.**")


@KY.UBOT("addrndm", sudo=True)
async def _(client, message):
    if message.reply_to_message:
        kata = message.reply_to_message.text
    else:
        kata = message.text.split(None, 1)[1]
    if not kata:
        return await message.reply_text("**Minimal kasih teks lah anj**")
    await tambah_rndm(client.me.id, kata)
    await message.reply_text(f"**Masuk `{kata}` sebagai kata random.**")


@KY.UBOT("remrndm", sudo=True)
async def _(client, message):
    if message.reply_to_message:
        kata = message.reply_to_message.text
    else:
        kata = message.text.split(None, 1)[1]
    if not kata:
        return await message.reply_text("**Minimal kasih teks lah anj**")
    await kureng_rndm(client.me.id, kata)
    await message.reply_text(f"**Keluar `{kata}` dari kata random.**")


@KY.UBOT("cekrndm", sudo=True)
async def _(client, message):
    gua = await client.get_me()
    data = await daftar_rndm(client.me.id)
    if not data:
        await message.reply_text("**Kosong kintl kata random nya**")
    else:
        msg = f"Nih kata kata random jamet lu **{gua.first_name}** :\n"
        for kata in data:
            msg += f"**-** `{kata}`\n"
        await message.reply_text(msg)
