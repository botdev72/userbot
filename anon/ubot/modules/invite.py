import asyncio

from pyrogram.enums import ChatType, UserStatus

from ubot import *
from ubot.utils import *

__MODULE__ = "Invite"
__HELP__ = """
Bantuan Untuk Invite


• Perintah: <code>{0}invite</code> [username]
• Penjelasan: Untuk Mengundang Anggota ke grup Anda.

• Perintah: <code>{0}getlink</code>
• Penjelasan: Untuk mengambil tautan undangan grup Anda.

• Perintah: <code>{0}inviteall</code> [username_group - colldown=detik per invite]
• Penjelasan: Untuk Mengundang Anggota dari obrolan grup lain ke obrolan grup Anda.

• Perintah: <code>{0}cinvite</code>
• Penjelasan: Untuk membatalkan perintah inviteall.

• Note: Untuk ID5 & ID6 Dilarang menggunakan fitur inviteall karna kemungkinan akan deak.
"""


@KY.UBOT("invite")
async def inviteee(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    mg = await message.reply(f"{emo.proses} <b>Processing Invite..</b>")
    await asyncio.sleep(2)
    if len(message.command) < 2:
        return await mg.delete()
    user_s_to_add = message.text.split(" ", 1)[1]
    if not user_s_to_add:
        await mg.edit(
            f"{emo.gagal} <b>Beri Saya Pengguna Untuk Ditambahkan! Periksa Menu Bantuan Untuk Info Lebih Lanjut!</b>"
        )
        return
    user_list = user_s_to_add.split(" ")
    try:
        await client.add_chat_members(message.chat.id, user_list, forward_limit=100)
    except BaseException as e:
        await mg.edit(
            f"{emo.gagal}<b>Tidak Dapat Menambahkan Pengguna!\nTraceBack:</b> {e}"
        )
        return
    await mg.edit(
        f"{emo.sukses} <b>Berhasil ditambahkan {len(user_list)} Ke Grup Ini</b>"
    )


invte_id = []


@KY.UBOT("inviteall")
async def inv(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    Tm = await message.reply(f"{emo.proses} <b>Processing...</b>")
    await asyncio.sleep(2)
    if len(message.command) < 3:
        await message.delete()
        return await Tm.delete()
    queryy = message.text.split()[1]
    colldown = message.text.split()[2]
    chat = await client.get_chat(queryy)
    tgchat = message.chat
    if tgchat.id in invte_id:
        return await Tm.edit_text(
            f"{emo.proses} **Sedang ada proses yang berjalan . Silahkan tunggu !**"
        )
    else:
        invte_id.append(tgchat.id)
        await Tm.edit_text(f"{emo.proses} **Processing invite from `{chat.title}`**")
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
                except BaseException:
                    pass
        invte_id.remove(tgchat.id)
        await Tm.delete()
        return await eor(
            message,
            f"<b>{emo.sukses} <code>{done}</code> Anggota Telah Berhasil Diundang</b>",
        )


@KY.UBOT("cinvite")
async def cancel(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    if message.chat.id not in invte_id:
        return await eor(
            message,
            f"{emo.gagal} **Sedang tidak ada perintah: <code>inviteall</code> yang digunakan.**",
        )
    try:
        invte_id.remove(message.chat.id)
        await message.reply(f"{emo.sukses} **Ok inviteall berhasil dibatalkan.**")
    except Exception as e:
        await message.reply(e)


@KY.UBOT("getlink")
async def invite_link(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    um = await message.edit_text(f"{emo.proses} **Processing...**")
    await asyncio.sleep(2)
    if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        message.chat.title
        try:
            link = await client.export_chat_invite_link(message.chat.id)
            await um.edit_text(f"{emo.sukses} **Link Invite:** {link}")
        except Exception:
            await um.edit_text(f"{emo.gagal} **Denied permission.**")
