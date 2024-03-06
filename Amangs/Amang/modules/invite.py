import asyncio

from pyrogram import filters
from pyrogram.enums import UserStatus

from Amang import *
from Amang.config import *
from Amang.utils import eor

__MOD__ = "Invite"
__HELP__ = f"""
 Document for Invite
• Command: <code>{cmd[0]}invite</code> [username]
• Function: Untuk Mengundang Anggota ke grup Anda.

• Command: <code>{cmd[0]}inviteall</code> [username_group - colldown=detik per invite]
• Function: Untuk Mengundang Anggota dari obrolan grup lain ke obrolan grup Anda.

• Command: <code>{cmd[0]}cancelinvite</code>
• Function: Membatalkan proses inviteall.

• Note: Untuk ID5 & ID6 Dilarang menggunakan fitur inviteall karna kemungkinan akan deak.
"""


@ubot.on_message(filters.me & anjay("invite"))
async def inviteee(client, message):
    mg = await eor(message, "<b>Menambahkan Pengguna!</b>")
    if len(message.command) < 2:
        return await mg.delete()
    user_s_to_add = message.text.split(" ", 1)[1]
    if not user_s_to_add:
        await mg.edit(
            "<b>Beri Saya Pengguna Untuk Ditambahkan! Periksa Menu Document for Info Lebih Lanjut!</b>"
        )
        return
    user_list = user_s_to_add.split(" ")
    try:
        await client.add_chat_members(message.chat.id, user_list, forward_limit=100)
    except BaseException as e:
        await mg.edit(f"<b>Tidak Dapat Menambahkan Pengguna!\nTraceBack:</b> {e}")
        return
    await mg.edit(f"<b>berhasil ditambahkan {len(user_list)} Ke Grup Ini</b>")


invte_id = []


@ubot.on_message(filters.me & anjay("inviteall") & filters.me)
async def inv(client, message):
    Tm = await eor(message, "<b>Processing . . .</b>")
    if len(message.command) < 3:
        await message.delete()
        return await Tm.delete()
    queryy = message.text.split()[1]
    colldown = message.text.split()[2]
    chat = await client.get_chat(queryy)
    tgchat = message.chat
    if tgchat.id in invte_id:
        return await Tm.edit_text(
            "Sedang menginvite member silahkan coba lagi nanti atau gunakan perintah: <code>{cancel}</code>"
        )
    else:
        invte_id.append(tgchat.id)
        await Tm.edit_text(f"mengundang anggota dari {chat.title}")
        done = 0
        async for member in client.get_chat_members(chat.id):
            user = member.user
            zxb = [
                UserStatus.ONLINE,
                UserStatus.OFFLINE,
                UserStatus.RECENTLY,
                UserStatus.LAST_WEEK,
            ]
            if user.status in zxb:
                try:
                    await client.add_chat_members(tgchat.id, user.id)
                    done += 1
                    await asyncio.sleep(int(colldown))
                except:
                    pass
        invte_id.remove(tgchat.id)
        await Tm.delete()
        return await eor(
            message, f"<b>✅ <code>{done}</code> Anggota Telah Berhasil Diundang</b>"
        )


@ubot.on_message(filters.me & anjay("cancelinvite") & filters.me)
async def cancel(client, message):
    if message.chat.id not in invte_id:
        return await eor(
            message, "Sedang tidak ada perintah: <code>inviteall</code> yang digunakan"
        )
    try:
        invte_id.remove(message.chat.id)
        await eor(message, "Ok inviteall berhasil dibatalkan")
    except Exception as e:
        await eor(message, e)
