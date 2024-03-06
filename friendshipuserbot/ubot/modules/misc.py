__MODULE__ = "Misc"
__HELP__ = """
Bantuan Untuk Misc

• Perintah: <code>{0}logger</code> [on/off]
• Penjelasan: Untuk mengetahui jika ada pesan masuk dari pengguna lain, atau ketika anda ditandai oleh orang lain.

- <code>{0}logger on</code> ->  Untuk menghidupkan grup log.
- <code>{0}logger off</code> ->  Untuk mematikan grup log.


• Perintah: <code>{0}addsudo</code> [reply/username/id]
• Penjelasan: Tambah pengguna sudo.

• Perintah: <code>{0}delsudo</code> [reply/username/id]
• Penjelasan: Hapus pengguna sudo.

• Perintah: <code>{0}sudolist</code>
• Penjelasan: Cek pengguna sudo.
"""


import asyncio

from pyrogram.enums import *
from pyrogram.errors import FloodWait
from pyrogram.types import *

from ubot import *


@PY.GC()
async def _(client, message):
    log = await get_log(client)
    cek = await get_log_group(client.me.id)
    if not cek:
        return
    user = f"[{message.from_user.first_name} {message.from_user.last_name or ''}](tg://user?id={message.from_user.id})"
    message_link = message.link
    text = f"""
📨 <b>TAGS MESSAGE</b>
• <b>Logs:</b> <code>{client.me.first_name}</code>
• <b>Group:</b> <code>{message.chat.title}</code>
• <b>Dari :</b> <code>{user}</code>
• <b>Pesan:</b> <code>{message.text}</code>

• <b>Tautan Grup:</b> [Disini]({message_link})
"""
    try:
        await client.send_message(
            log.id,
            text,
            disable_web_page_preview=True,
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await client.send_message(
            log.id,
            text,
            disable_web_page_preview=True,
        )


@PY.PC()
async def _(client, message):
    log = await get_log(client)
    cek = await get_log_group(client.me.id)
    if not cek:
        return
    if message.chat.id == 777000:
        return
    async for x in client.search_messages(message.chat.id, limit=1):
        await x.forward(log.id)


@PY.UBOT("logger", sudo=True)
async def _(client, message):
    xx = await message.reply(f"**Processing...**")
    cek = get_arg(message)
    logs = await get_log_group(client.me.id)
    if cek.lower() == "on":
        if not logs:
            await set_log_group(client.me.id, logger=True)
            await create_botlog(client)
            ajg = await get_log(client)
            babi = await client.export_chat_invite_link(int(ajg.id))
            return await xx.edit(f"**Log Group Berhasil Diaktifkan :\n\n{babi}**")
        else:
            return await xx.edit(f"**Log Group Anda Sudah Aktif.**")
    if cek.lower() == "off":
        if logs:
            await del_log_group(client.me.id)
            ajg = await get_log(client)
            await client.delete_supergroup(int(ajg.id))
            return await xx.edit(f"**Log Group Berhasil Dinonaktifkan.**")
        else:
            return await xx.edit(f"**Log Group Anda Sudah Dinonaktifkan.**")
    else:
        return await xx.edit(
            f"**Format yang anda berikan salah. silahkan gunakan <code>{message.text} on/off</code>**"
        )


@PY.UBOT("addsudo", sudo=True)
async def _(client, message):
    msg = await message.reply(f"<b>Processing...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>Silakan balas pesan pengguna/username/user id</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    sudo_users = await ambil_list_var(client.me.id, "SUDO_USER", "ID_NYA")

    if user.id in sudo_users:
        return await msg.edit(
            f"<b>[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) Sudah menjadi pengguna sudo.</b>"
        )

    try:
        await add_var(client.me.id, "SUDO_USER", user.id, "ID_NYA")
        return await msg.edit(
            f"<b>[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) Ditambahkan ke pengguna sudo.</b>"
        )
    except Exception as error:
        return await msg.edit(error)


@PY.UBOT("delsudo", sudo=True)
async def _(client, message):
    msg = await message.reply(f"<b>Processing...</b>")
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply(
            f"<b>Silakan balas pesan penggjna/username/user id.</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    sudo_users = await ambil_list_var(client.me.id, "SUDO_USER", "ID_NYA")

    if user.id not in sudo_users:
        return await msg.edit(
            f"<b>{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) Bukan bagian pengguna sudo.</b>"
        )

    try:
        await rem_var(client.me.id, "SUDO_USER", user.id, "ID_NYA")
        return await msg.edit(
            f"<b>[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) Dihapus dari pengguna sudo.</b>"
        )
    except Exception as error:
        return await msg.edit(error)


@PY.UBOT("sudolist", sudo=True)
async def _(client, message):
    msg = await message.reply(f"<b>Processing...</b>")
    sudo_users = await ambil_list_var(client.me.id, "SUDO_USER", "ID_NYA")

    if not sudo_users:
        return await msg.edit(f"<b>Tidak ada pengguna sudo ditemukan.</b>")

    sudo_list = []
    for user_id in sudo_users:
        try:
            user = await client.get_users(int(user_id))
            sudo_list.append(
                f" • [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code>"
            )
        except:
            continue

    if sudo_list:
        response = (
            f"<b>Daftar Pengguna:</b>\n"
            + "\n".join(sudo_list)
            + f"\n<b> • </b> <code>{len(sudo_list)}</code>"
        )
        return await msg.edit(response)
    else:
        return await msg.edit("<b>Eror</b>")
