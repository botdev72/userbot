import asyncio

from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.errors import ChatAdminRequired, PeerIdInvalid
from pyrogram.types import ChatPermissions, ChatPrivileges, Message

from Amang import *
from Amang.utils import get_seles
from Amang.utils.utils import *


unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@ubot.on_message(filters.command(["setgpic"], cmd) & filters.me)
async def set_chat_photo(client: Client, message: Message):
    zuzu = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    can_change_admin = zuzu.can_change_info
    can_change_member = message.chat.permissions.can_change_info
    if not (can_change_admin or can_change_member):
        await eor(message, "<code>Kamu tidak punya akses wewenang</code>")
    if message.reply_to_message:
        if message.reply_to_message.photo:
            await client.set_chat_photo(
                message.chat.id, photo=message.reply_to_message.photo.file_id
            )
            return
    else:
        await eor(message, "<code>Mohon balas ke media</code>")


@ubot.on_message(filters.command(["ban", "dban"], cmd) & filters.me)
async def member_ban(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    ky = await eor(message, "<code>Processing...</code>")
    if not user_id:
        return await ky.edit("Tidak dapat menemukan pengguna.")
    if user_id == client.me.id:
        return await ky.edit("Tidak bisa banned diri sendiri.")
    if user_id in DEVS:
        return await ky.edit("Tidak bisa banned Devs!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await ky.edit("Tidak bisa banned admin.")
    try:
        mention = (await client.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    msg = f"<b>Banned User:</b> {mention}\n<b>Banned By:</b> {message.from_user.mention}\n"
    if reason:
        msg += f"<b>Reason:</b> {reason}"
    try:
        await message.chat.ban_member(user_id)
        await ky.edit(msg)
    except ChatAdminRequired:
        return await ky.edit("<b>Anda bukan admin di group ini !</b>")


@ubot.on_message(filters.command(["unban"], cmd) & filters.me)
async def member_unban(client: Client, message: Message):
    reply = message.reply_to_message
    zz = await eor(message, "<code>Processing...</code>")
    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        return await zz.edit("Tidak bisa unban akun channel")

    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and reply:
        user = message.reply_to_message.from_user.id
    else:
        return await zz.edit("Berikan username, atau reply pesannya.")
    try:
        await message.chat.unban_member(user)
        await asyncio.sleep(0.1)
        umention = (await client.get_users(user)).mention
        await zz.edit(f"Unbanned! {umention}")
    except ChatAdminRequired:
        return await zz.edit("<b>Anda bukan admin di group ini !</b>")


@ubot.on_message(filters.command(["pin", "unpin"], cmd) & filters.me)
async def pin_message(client: Client, message):
    if not message.reply_to_message:
        return await eor(message, "Balas ke pesan untuk pin/unpin .")
    await eor(message, "<code>Processing...</code>")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await eor(
            message,
            f"<code>Unpinned [this]({r.link}) message.</code>",
            disable_web_page_preview=True,
        )
    try:
        await r.pin(disable_notification=True)
        await eor(
            message,
            f"<code>Pinned [this]({r.link}) message.</code>",
            disable_web_page_preview=True,
        )
    except ChatAdminRequired:
        return await eor(message, "<b>Anda bukan admin di group ini !</b>")


@ubot.on_message(filters.command(["mute"], cmd) & filters.me)
async def mute(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    nay = await eor(message, "<code>Processing...</code>")
    if not user_id:
        return await nay.edit("Pengguna tidak ditemukan.")
    if user_id == client.me.id:
        return await nay.edit("Tidak bisa mute diri sendiri.")
    if user_id in DEVS:
        return await nay.edit("Tidak bisa mute dev!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await nay.edit("Tidak bisa mute admin.")

    mention = (await client.get_users(user_id)).mention
    msg = (
        f"<b>Muted User:</b> {mention}\n"
        f"<b>Muted By:</b> {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if reason:
        msg += f"<b>Reason:</b> {reason}"
    try:
        await message.chat.restrict_member(user_id, permissions=ChatPermissions())
        await nay.edit(msg)
    except ChatAdminRequired:
        return await nay.edit("<b>Anda bukan admin di group ini !</b>")


@ubot.on_message(filters.command(["unmute"], cmd) & filters.me)
async def unmute(client: Client, message: Message):
    user_id = await extract_user(message)
    kl = await eor(message, "<code>Processing...</code>")
    if not user_id:
        return await kl.edit("Pengguna tidak ditemukan.")
    try:
        await message.chat.restrict_member(user_id, permissions=unmute_permissions)

        umention = (await client.get_users(user_id)).mention
        await kl.edit(f"Unmuted! {umention}")
    except ChatAdminRequired:
        return await kl.edit("<b>Anda bukan admin di group ini !</b>")


@ubot.on_message(filters.command(["kick", "dkick"], cmd) & filters.me)
async def kick_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    ny = await eor(message, "<code>Processing...</code>")
    if not user_id:
        return await ny.edit("Pengguna tidak ditemukan.")
    if user_id == client.me.id:
        return await ny.edit("Tidak bisa kick diri sendiri.")
    if user_id == DEVS:
        return await ny.edit("Tidak bisa kick dev!.")
    if user_id in (await list_admins(client, message.chat.id)):
        return await ny.edit("Tidak bisa kick admin.")

    mention = (await client.get_users(user_id)).mention
    msg = f"""
<b>Kicked User:</b> {mention}
<b>Kicked By:</b> {message.from_user.mention if message.from_user else 'Anon'}"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"\n<b>Reason:</b> <code>{reason}</code>"
    try:
        await message.chat.ban_member(user_id)
        await ny.edit(msg)
        await asyncio.sleep(1)
        await message.chat.unban_member(user_id)
    except ChatAdminRequired:
        return await ny.edit("<b>Anda bukan admin di group ini !</b>")


@ubot.on_message(
    filters.group & filters.command(["promote", "fullpromote"], cmd) & filters.me
)
async def promotte(client: Client, message: Message):
    user_id = await extract_user(message)
    biji = await eor(message, "<code>Processing...</code>")
    if not user_id:
        return await biji.edit("Pengguna tidak ditemukan.")
    (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    try:
        if message.command[0][0] == "f":
            await message.chat.promote_member(
                user_id,
                privileges=ChatPrivileges(
                    can_manage_chat=True,
                    can_delete_messages=True,
                    can_manage_video_chats=True,
                    can_restrict_members=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                    can_promote_members=True,
                ),
            )
            await asyncio.sleep(1)

            umention = (await client.get_users(user_id)).mention
            return await biji.edit(f"Fully Promoted! {umention}")

        await message.chat.promote_member(
            user_id,
            privileges=ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=False,
            ),
        )
        await asyncio.sleep(1)

        umention = (await client.get_users(user_id)).mention
        await biji.edit(f"Promoted! {umention}")
    except ChatAdminRequired:
        return await biji.edit("<b>Anda bukan admin di group ini !</b>")


@ubot.on_message(
    filters.group
    & filters.command(["cdemote"], ["."])
    & filters.user(DEVS)
    & ~filters.me
)

@ubot.on_message(filters.group & filters.command(["demote"], cmd) & filters.me)
async def demote(client: Client, message: Message):
    user_id = await extract_user(message)
    sempak = await eor(message, "<code>Processing...</code>")
    if not user_id:
        return await sempak.edit("Pengguna tidak ditemukan")
    if user_id == client.me.id:
        return await sempak.edit("Tidak bisa demote diri sendiri.")
    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=False,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False,
        ),
    )
    await asyncio.sleep(1)

    umention = (await client.get_users(user_id)).mention
    await sempak.edit(f"Demoted! {umention}")


@ubot.on_message(filters.user(DEVS) & filters.command("cgban", ".") & ~filters.me)
@ubot.on_message(filters.me & filters.command("gban", cmd))
async def _(client, message):
    Tm = await eor(message, "<code>Processing...</code>")
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        await Tm.edit(
            "Gunakan format: <code>gban</code> [user_id/username/balas ke user]"
        )
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
    try:
        user = await client.get_users(get_user)
    except PeerIdInvalid:
        await Tm.edit("Tidak dapat menemukan user tersebut.")
        return
    iso = 0
    gagal = 0
    prik = user.id
    prok = await get_seles()
    async for dialog in client.get_dialogs():
        chat_type = dialog.chat.type
        if chat_type in [
            ChatType.GROUP,
            ChatType.SUPERGROUP,
            ChatType.CHANNEL,
        ]:
            chat = dialog.chat.id
            if prik in DEVS:
                return await Tm.edit(
                    "Anda tidak bisa gban dia karena dia pembuat saya."
                )
            elif prik in prok:
                return await Tm.edit(
                    "Anda tidak bisa gban dia, karna dia adalah Admin Userbot Anda."
                )
            elif prik not in prok and prik not in DEVS:
                try:
                    await client.ban_chat_member(chat, prik)
                    iso = iso + 1
                    await asyncio.sleep(0.1)
                except:
                    gagal = gagal + 1
                    await asyncio.sleep(0.1)
    return await Tm.edit(
        f"""
<b> Global Banned</b>

<b>✅ Berhasil Banned: {iso} Chat</b>
<b>❌ Gagal Banned: {gagal} Chat</b>
<b>👤 User: <a href='tg://user?id={prik}'>{user.first_name}</a></b>
"""
    )


@ubot.on_message(filters.user(DEVS) & filters.command("cungban", ".") & ~filters.me)
@ubot.on_message(filters.me & filters.command("ungban", cmd))
async def _(client, message):
    Tm = await eor(message, "Memproses ungban user")
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        await Tm.edit(
            "Gunakan format: <code>ungban</code> [user_id/username/reply to user]"
        )
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
    try:
        user = await client.get_users(get_user)
    except PeerIdInvalid:
        await Tm.edit("Tidak menemukan user tersebut.")
        return
    iso = 0
    gagal = 0
    prik = user.id
    async for dialog in client.get_dialogs():
        chat_type = dialog.chat.type
        if chat_type in [
            ChatType.GROUP,
            ChatType.SUPERGROUP,
            ChatType.CHANNEL,
        ]:
            chat = dialog.chat.id
            try:
                await client.unban_chat_member(chat, prik)
                iso = iso + 1
                await asyncio.sleep(0.1)
            except:
                gagal = gagal + 1
                await asyncio.sleep(0.1)

    return await Tm.edit(
        f"""
<b> Global UnBanned</b>

<b>✅ Berhasil UnBanned: {iso} Chat</b>
<b>❌ Gagal UnBanned: {gagal} Chat</b>
<b>👤 User: <a href='tg://user?id={prik}'>{user.first_name}</a></b>
"""
    )


__MOD__ = "admin"
__HELP__ = f"""
 Document for Admins

• Command: <code>{cmd[0]}ban, dban or unban</code> [balas pesan atau berikan username]
• Function: Untuk blokir, hapus pesan dengan blokir serta buka blokir

• Command: <code>{cmd[0]}pin or unpin</code> [balas pesan]
• Function: Untuk menyematkan dan melepas sematan pesan grup.

• Command: <code>{cmd[0]}setgpic</code> [balas foto]
• Function: Untuk mengubah foto grup.

• Command: <code>{cmd[0]}kick or dkick</code> [balas pesan atau berikan username]
• Function: Untuk menendang atau hapus pesan dengan menendang pengguna.

• Command: <code>{cmd[0]}promote or fullpromote</code> [balas pesan atau berikan username]
• Function: Untuk menjadikan admin digrup anda.

• Command: <code>{cmd[0]}mute or unmute</code> [balas pesan atau berikan username]
• Function: Untuk membisukan atau membuka bisu pengguna digrup.

• Command: <code>{cmd[0]}staff</code>
• Function: Untuk mengetahui daftar semua admin didalam grup.
"""
