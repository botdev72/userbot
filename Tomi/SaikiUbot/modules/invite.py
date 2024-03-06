import asyncio

from pyrogram.enums import UserStatus

from .. import *

__MODULE__ = "INVITE"
__HELP__ = f"""
Perintah:
         <code>{PREFIX[0]}invite</code> [username]
Penjelasan:
           Untuk Mengundang Anggota ke grup Anda

Perintah:
         <code>{PREFIX[0]}inviteall</code> [username_group - cooldown=detik per invite]
Penjelasan:
           Untuk Mengundang Anggota dari obrolan grup lain ke obrolan grup Anda

Perintah:
         <code>{PREFIX[0]}cancel</code>
Penjelasan:
           Untuk membatalkan perintah inviteall"""


@PY.UBOT("invite", PREFIX)
async def _(client, message):
    mg = await message.reply("<b>Menambahkan Pengguna!</b>")
    if len(message.command) < 2:
        return await mg.delete()
    user_s_to_add = message.text.split(" ", 1)[1]
    if not user_s_to_add:
        await mg.edit(
            "<b>Beri Saya Pengguna Untuk Ditambahkan! Periksa Menu Bantuan Untuk Info Lebih Lanjut!</b>"
        )
        return
    user_list = user_s_to_add.split(" ")
    try:
        await client.add_chat_members(message.chat.id, user_list, forward_limit=100)
    except BaseException as e:
        await mg.edit(f"<b>Tidak Dapat Menambahkan Pengguna!\nTraceBack:</b> {e}")
        return
    await mg.edit(f"<b>berhasil ditambahkan {len(user_list)} Ke Grup Ini</b>")


invite_id = []


@PY.UBOT("inviteall", PREFIX)
async def _(client, message):
    Tm = await message.reply("<b>Processing . . .</b>")
    if len(message.command) < 3:
        await message.delete()
        return await Tm.delete()
    try:
        chat = await client.get_chat(message.command[1])
    except Exception as error:
        return await Tm.edit(error)
    if message.chat.id in invite_id:
        return await Tm.edit_text(
            f"sedang menginvite member silahkan coba lagi nanti atau gunakan perintah: <code>{PREFIX[0]}cancel</code>"
        )
    else:
        done = 0
        failed = 0
        invite_id.append(message.chat.id)
        await Tm.edit_text(f"mengundang anggota dari {chat.title}")
        async for member in client.get_chat_members(chat.id):
            stats = [
                UserStatus.ONLINE,
                UserStatus.OFFLINE,
                UserStatus.RECENTLY,
                UserStatus.LAST_WEEK,
            ]
            if member.user.status in stats:
                try:
                    await client.add_chat_members(message.chat.id, member.user.id)
                    done = done + 1
                    await asyncio.sleep(int(message.command[2]))
                except Exception:
                    failed = failed + 1
                    await asyncio.sleep(int(message.command[2]))
        invite_id.remove(message.chat.id)
        await Tm.delete()
        return await message.reply(
            f"""
<b>✅ <code>{done}</code> Anggota Yang Berhasil Diundang</b>
<b>❌ <code>{failed}</code> Anggota Yang Gagal Diundang</b>
"""
        )


@PY.UBOT("cancel", PREFIX)
async def _(client, message):
    if message.chat.id not in invte_id:
        return await message.reply_text(
            f"sedang tidak ada perintah: <code>{PREFIX[0]}inviteall</code> yang digunakan"
        )
    try:
        invite_id.remove(message.chat.id)
        await message.reply_text("ok inviteall berhasil dibatalkan")
    except Exception as e:
        await message.reply_text(e)
