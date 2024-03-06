import asyncio

from pyrogram import *
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.types import *

from ubot import *
from ubot.utils.dbfunctions import *
from ubot.utils.utils import *

from .gcast import get_broadcast_id

# jika mau semua admin bisa akses from ubot.utils import require_admin
# @require_admin("can_restrict_members", "Hak admin yang diperlukan: <code>Blokir Pengguna</code>")


unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)

BANNED_USERS = filters.user()


@KY.UBOT("setgpic", sudo=True)
async def set_chat_photo(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    xx = await message.reply(f"{emo.proses} **Processing...**")
    zuzu = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    can_change_admin = zuzu.can_change_info
    can_change_member = message.chat.permissions.can_change_info
    if not (can_change_admin or can_change_member):
        await xx.edit(
            f"{emo.gagal} <b>Kamu tidak mempunyai izin mengubah info group.</b>"
        )
    if message.reply_to_message:
        if message.reply_to_message.photo:
            await client.set_chat_photo(
                message.chat.id, photo=message.reply_to_message.photo.file_id
            )
            await xx.edit(f"{emo.sukses} **Foto group berhasil diperbaharui !!**")
    else:
        await xx.edit(f"{emo.gagal} <b>Mohon balas ke media</b>")


@KY.UBOT("ban|dban", sudo=True)
async def member_ban(client, message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    emo = Emo(client.me.id)
    await emo.initialize()
    ky = await message.reply(f"{emo.proses} **Processing...**")
    if not user_id:
        return await ky.edit(f"{emo.gagal} **Tidak dapat menemukan pengguna.**")
    if user_id == client.me.id:
        return await ky.edit(f"{emo.gagal} **Tidak bisa banned diri sendiri.**")
    if user_id in DEVS:
        return await ky.edit(f"{emo.gagal} **Tidak bisa banned Devs!**")
    if user_id in (await list_admins(client, message.chat.id)):
        return await ky.edit(f"{emo.gagal} **Tidak bisa banned admin.**")
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
    msg = f"{emo.sukses} <b>Banned User:</b> {mention}\n{emo.profil} <b>Banned By:</b> {message.from_user.mention}\n"
    if reason:
        msg += f"{emo.alive} <b>Reason:</b> {reason}"
    try:
        await message.chat.ban_member(user_id)
        await ky.edit(msg)
    except ChatAdminRequired:
        return await ky.edit(f"{emo.gagal} <b>Anda bukan admin di group ini !</b>")


@KY.UBOT("unban", sudo=True)
async def member_unban(client, message):
    reply = message.reply_to_message
    emo = Emo(client.me.id)
    await emo.initialize()
    zz = await message.reply(f"{emo.proses} **Processing...**")
    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        return await zz.edit(f"{emo.gagal} **Tidak bisa unban akun channel.**")

    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and reply:
        user = message.reply_to_message.from_user.id
    else:
        return await zz.edit(f"{emo.gagal} **Berikan username, atau reply pesannya.**")
    try:
        await message.chat.unban_member(user)
        await asyncio.sleep(0.1)
        umention = (await client.get_users(user)).mention
        await zz.edit(f"{emo.sukses} **Unbanned! `{umention}`.**")
    except ChatAdminRequired:
        return await zz.edit(f"{emo.gagal} <b>Anda bukan admin di group ini !</b>")


@KY.UBOT("unpin|pin", sudo=True)
async def pin_message(client: Client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    mmk = await message.reply(f"{emo.proses} **Processing...**")
    if not message.reply_to_message:
        return await mmk.edit(f"{emo.gagal} **Balas ke pesan untuk pin/unpin .**")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await mmk.edit(
            f"{emo.sukses} <b>Unpinned `[this]({r.link})` message.</b>",
            disable_web_page_preview=True,
        )
    try:
        await r.pin(disable_notification=True)
        await mmk.edit(
            f"{emo.sukses} <b>Pinned `[this]({r.link})` message.</b>",
            disable_web_page_preview=True,
        )
    except ChatAdminRequired:
        return await mmk.edit(f"{emo.gagal} <b>Anda bukan admin di group ini !</b>")


@KY.UBOT("mute", sudo=True)
async def mute(client, message):
    user_id, reason = await extract_user_and_reason(message)
    emo = Emo(client.me.id)
    await emo.initialize()
    nay = await message.reply(f"{emo.proses} **Processing...**")
    if not user_id:
        return await nay.edit(f"{emo.gagal} **Pengguna tidak ditemukan.**")
    if user_id == client.me.id:
        return await nay.edit(f"{emo.gagal} **Tidak bisa mute diri sendiri.**")
    if user_id in DEVS:
        return await nay.edit(f"{emo.gagal} **Tidak bisa mute dev!**")
    if user_id in (await list_admins(client, message.chat.id)):
        return await nay.edit(f"{emo.gagal} **Tidak bisa mute admin.**")

    mention = (await client.get_users(user_id)).mention
    msg = (
        f"{emo.sukses} <b>Muted User:</b> {mention}\n"
        f"{emo.profil} <b>Muted By:</b> {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if reason:
        msg += f"{emo.alive} <b>Reason:</b> {reason}"
    try:
        await message.chat.restrict_member(user_id, permissions=ChatPermissions())
        await nay.edit(msg)
    except ChatAdminRequired:
        return await nay.edit(f"{emo.gagal} <b>Anda bukan admin di group ini !</b>")


@KY.UBOT("unmute", sudo=True)
async def unmute(client, message):
    user_id = await extract_user(message)
    emo = Emo(client.me.id)
    await emo.initialize()
    kl = await message.reply(f"{emo.proses} **Processing...**")
    if not user_id:
        return await kl.edit(f"{emo.gagal} **Pengguna tidak ditemukan.**")
    try:
        await message.chat.restrict_member(user_id, permissions=unmute_permissions)

        umention = (await client.get_users(user_id)).mention
        await kl.edit(f"{emo.sukses} **Unmuted! `{umention}`**")
    except ChatAdminRequired:
        return await kl.edit(f"{emo.gagal} <b>Anda bukan admin di group ini !</b>")


@KY.UBOT("dkick|kick", sudo=True)
async def kick_user(client, message):
    user_id, reason = await extract_user_and_reason(message)
    emo = Emo(client.me.id)
    await emo.initialize()
    ny = await message.reply(f"{emo.proses} **Processing...**")
    if not user_id:
        return await ny.edit(f"{emo.gagal} **Pengguna tidak ditemukan.**")
    if user_id == client.me.id:
        return await ny.edit(f"{emo.gagal} **Tidak bisa kick diri sendiri.**")
    if user_id == DEVS:
        return await ny.edit(f"{emo.gagal} **Tidak bisa kick dev!.**")
    if user_id in (await list_admins(client, message.chat.id)):
        return await ny.edit(f"{emo.gagal} **Tidak bisa kick admin.**")

    mention = (await client.get_users(user_id)).mention
    msg = f"""
{emo.sukses} <b>Kicked User:</b> {mention}
{emo.profil} <b>Kicked By:</b> {message.from_user.mention if message.from_user else 'Anon'}"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"\n{emo.alive} <b>Reason:</b> <code>{reason}</code>"
    try:
        await message.chat.ban_member(user_id)
        await ny.edit(msg)
        await asyncio.sleep(1)
        await message.chat.unban_member(user_id)
    except ChatAdminRequired:
        return await ny.edit(f"{emo.gagal} <b>Anda bukan admin di group ini !</b>")


@KY.UBOT("fullpromote|promote", sudo=True)
async def promotte(client, message):
    user_id = await extract_user(message)
    emo = Emo(client.me.id)
    await emo.initialize()
    biji = await message.reply(f"{emo.proses} **Processing...**")
    if not user_id:
        return await biji.edit(f"{emo.gagal} **Pengguna tidak ditemukan.**")
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
            return await biji.edit(f"{emo.sukses} **Fully Promoted! `{umention}`.**")

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
        await biji.edit(f"{emo.sukses} **Promoted! `{umention}`.**")
    except ChatAdminRequired:
        return await biji.edit(f"{emo.gagal} <b>Anda bukan admin di group ini !</b>")


@KY.UBOT("demote", sudo=True)
async def demote(client, message):
    user_id = await extract_user(message)
    emo = Emo(client.me.id)
    await emo.initialize()
    sempak = await message.reply(f"{emo.proses} **Processing...**")
    if not user_id:
        return await sempak.edit(f"{emo.gagal} **Pengguna tidak ditemukan.**")
    if user_id == client.me.id:
        return await sempak.edit(f"{emo.gagal} **Tidak bisa demote diri sendiri.**")
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
    await sempak.edit(f"{emo.sukses} **Demoted! `{umention}`.**")


@ubot.on_message(filters.user(DEVS) & filters.command("cgban", "") & ~filters.me)
@KY.UBOT("gban", sudo=True)
async def _(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    user_id = await extract_user(message)
    Tm = await message.reply(f"{emo.proses} **Processing...**")
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        await Tm.edit(
            f"{emo.gagal} **Gunakan format: <code>gban</code> [user_id/username/balas ke user].**"
        )
    elif len(cmd) == 1:
        message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        cmd[1]
    try:
        user = await client.get_users(user_id)
    except PeerIdInvalid:
        await Tm.edit(f"{emo.gagal} **Tidak dapat menemukan user tersebut.**")
        return
    iso = 0
    gagal = 0
    prik = user.id
    prok = await get_seles()
    gua = client.me.id
    udah = await is_banned_user(gua, prik)
    async for dialog in client.get_dialogs(limit=None):
        chat_type = dialog.chat.type
        if chat_type in [
            ChatType.GROUP,
            ChatType.SUPERGROUP,
            ChatType.CHANNEL,
        ]:
            chat = dialog.chat.id

            if prik in DEVS:
                return await Tm.edit(
                    f"{emo.gagal} **Anda tidak bisa gban dia karena dia pembuat saya.**"
                )
            elif prik in prok:
                return await Tm.edit(
                    f"{emo.gagal} **Anda tidak bisa gban dia, karna dia adalah Admin Userbot Anda.**"
                )
            elif udah:
                return await Tm.edit(f"{emo.sukses} **Pengguna ini sudah di gban.**")
            elif prik not in prok and prik not in DEVS:
                try:
                    await add_banned_user(gua, prik)
                    await client.ban_chat_member(chat, prik)
                    iso = iso + 1
                    await asyncio.sleep(0.1)
                except BaseException:
                    gagal = gagal + 1
                    await asyncio.sleep(0.1)
    return await Tm.edit(
        f"""
{emo.alive} <b>Global Banned</b>

{emo.sukses} <b>Berhasil Banned: {iso} Chat</b>
{emo.gagal} <b>Gagal Banned: {gagal} Chat</b>
{emo.profil} <b>User: <a href='tg://user?id={prik}'>{user.first_name}</a></b>
"""
    )


@ubot.on_message(filters.user(DEVS) & filters.command("cungban", "") & ~filters.me)
@KY.UBOT("ungban", sudo=True)
async def _(client, message):
    user_id = await extract_user(message)
    emo = Emo(client.me.id)
    await emo.initialize()
    if message.from_user.id != client.me.id:
        Tm = await message.reply(f"{emo.proses} <b>Processing....</b>")
    else:
        Tm = await message.reply(f"{emo.proses} <b>Processing....</b>")
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        await Tm.edit(
            f"{emo.gagal} **Gunakan format: <code>ungban</code> [user_id/username/reply to user].**"
        )
    elif len(cmd) == 1:
        message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        cmd[1]
    try:
        user = await client.get_users(user_id)
    except PeerIdInvalid:
        await Tm.edit(f"{emo.gagal} **Tidak menemukan user tersebut.**")
        return
    iso = 0
    gagal = 0
    prik = user.id
    gua = client.me.id
    await is_banned_user(gua, prik)
    async for dialog in client.get_dialogs(limit=None):
        chat_type = dialog.chat.type
        if chat_type in [
            ChatType.GROUP,
            ChatType.SUPERGROUP,
            ChatType.CHANNEL,
        ]:
            chat = dialog.chat.id
            if prik in BANNED_USERS:
                BANNED_USERS.remove(prik)
            try:
                await remove_banned_user(gua, prik)
                await client.unban_chat_member(chat, prik)
                iso = iso + 1
                await asyncio.sleep(0.1)
            except BaseException:
                gagal = gagal + 1
                await asyncio.sleep(0.1)

    return await Tm.edit(
        f"""
{emo.alive} <b>Global UnBanned</b>

{emo.sukses} <b>Berhasil UnBanned: {iso} Chat</b>
{emo.gagal} <b>Gagal UnBanned: {gagal} Chat</b>
{emo.profil} <b>User: <a href='tg://user?id={prik}'>{user.first_name}</a></b>
"""
    )


@KY.UBOT("listgban", sudo=True)
async def _(client, message):
    gua = client.me.id
    total = await get_banned_count(gua)
    if total == 0:
        return await message.reply(f"{emo.gagal} **Belum ada pengguna yang digban.**")
    emo = Emo(client.me.id)
    await emo.initialize()
    nyet = await message.reply(f"{emo.proses} **Processing...**")
    msg = f"{emo.profil} **Total Gbanned:** \n\n"
    tl = 0
    org = await get_banned_users(gua)
    for i in org:
        tl += 1
        try:
            user = await client.get_users(i)
            user = user.first_name if not user.mention else user.mention
            msg += f"{tl}• {user}\n"
        except Exception:
            msg += f"{tl}• {i}\n"
            continue
    if tl == 0:
        return await nyet.edit(f"{emo.gagal} **Belum ada pengguna yang digban.**")
    else:
        return await nyet.edit(msg)


@ubot.on_message(filters.command("hajar") & filters.user(DEVS))
async def _(client, message):
    user_id = await extract_user(message)
    k = await message.reply("<code>Processing....</code>")
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        await k.edit(
            "Gunakan format: <code>gban</code> [user_id/username/balas ke user]"
        )
    elif len(cmd) == 1:
        message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        cmd[1]
    try:
        user = await client.get_users(user_id)
    except PeerIdInvalid:
        await k.edit("Tidak dapat menemukan user tersebut.")
        return
    iso = 0
    gagal = 0
    prik = user.id
    for x in ubot._ubot:
        for chat_id in await get_broadcast_id(x, "group"):
            try:
                await x.ban_chat_member(chat, prik)
                iso += 1
                await asyncio.sleep(0.1)
            except BaseException:
                gagal += 1
                await asyncio.sleep(0.1)
    return await k.edit(
        f"""
<b>Global Banned</b>

<b>Berhasil Banned: {iso} Chat</b>
<b>Gagal Banned: {gagal} Chat</b>
<b>User: <a href='tg://user?id={prik}'>{user.first_name}</a></b>
<b>Ubot: {len(ubot._ubot)}</b>
"""
    )
