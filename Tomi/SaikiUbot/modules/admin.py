import asyncio

from pyrogram.enums import ChatType
from pyrogram.types import ChatPermissions

from .. import *

__MODULE__ = "ADMIN"
__HELP__ = f"""
• <code>{PREFIX[0]}help global</code>
• <code>{PREFIX[0]}help restrict</code>
"""


@PY.UBOT(["kick", "ban", "mute", "unmute", "unban"], PREFIX, FILTERS.ME_GROUP)
async def _(client, message):
    if message.command[0] == "kick":
        user_id, reason = await extract_user_and_reason(message)
        if not user_id:
            return await message.reply_text("Saya tidak dapat menemukan pengguna itu.")
        if user_id == (await client.get_me()).id:
            return await message.reply_text(
                "Aku tidak bisa menendang diriku sendiri, aku bisa pergi jika kamu mau."
            )
        if user_id == OWNER_ID:
            return await message.reply_text("Anda Tidak Bisa Menendang Anggota Ini")
        if user_id in (await list_admins(message)):
            return await message.reply_text(
                "Saya tidak bisa menendang admin, Anda tahu aturannya, saya juga."
            )
        try:
            mention = (await client.get_users(user_id)).mention
        except Exception as error:
            await message.reply(error)
        msg = f"<b>👤 Ditendang:</b> {mention}\n<b>👑 Admin:</b> {message.from_user.mention}"
        if reason:
            msg += f"\n<b>💬 Alasan:</b> {reason}"
        try:
            await message.chat.ban_member(user_id)
            await message.reply(msg)
            await asyncio.sleep(1)
            await message.chat.unban_member(user_id)
        except Exception as error:
            await message.reply(error)
    elif message.command[0] == "ban":
        user_id, reason = await extract_user_and_reason(message)
        if not user_id:
            return await message.reply_text("Saya tidak dapat menemukan anggota itu.")
        if user_id == (await client.get_me()).id:
            return await message.reply_text(
                "Aku tidak bisa membanned diriku sendiri, aku bisa pergi jika kamu mau."
            )
        if user_id == OWNER_ID:
            return await message.reply_text("Anda Tidak Bisa Membanned Anggota Ini")
        if user_id in (await list_admins(message)):
            return await message.reply_text(
                "Saya tidak bisa membanned admin, Anda tahu aturannya, saya juga."
            )
        try:
            mention = (await client.get_users(user_id)).mention
        except Exception as error:
            await message.reply(error)
        msg = (
            f"<b>👤 Dibanned:</b> {mention}\n<b>👑 Admin:</b> {message.from_user.mention}"
        )
        if reason:
            msg += f"\n<b>💬 Alasan:</b> {reason}"
        try:
            await message.chat.ban_member(user_id)
            await message.reply(msg)
        except Exception as error:
            await message.reply(error)
    elif message.command[0] == "mute":
        user_id, reason = await extract_user_and_reason(message)
        if not user_id:
            return await message.reply_text("Saya tidak dapat menemukan anggota itu.")
        if user_id == (await client.get_me()).id:
            return await message.reply_text(
                "Aku tidak bisa membisukan diriku sendiri, aku bisa pergi jika kamu mau."
            )
        if user_id == OWNER_ID:
            return await message.reply_text("Anda Tidak Bisa Membisukan Anggota Ini")
        if user_id in (await list_admins(message)):
            return await message.reply_text(
                "Saya tidak bisa membisukan admin, Anda tahu aturannya, saya juga."
            )
        try:
            mention = (await client.get_users(user_id)).mention
        except Exception as error:
            await message.reply(error)
        msg = f"<b>👤 Membisukan:</b> {mention}\n<b>👑 Admin:</b> {message.from_user.mention}"
        if reason:
            msg += f"\n<b>💬 Alasan:</b> {reason}"
        try:
            await message.chat.restrict_member(user_id, ChatPermissions())
            await message.reply(msg)
        except Exception as error:
            await message.reply(error)
    elif message.command[0] == "unmute":
        user_id = await extract_user(message)
        if not user_id:
            return await message.reply_text("Saya tidak dapat menemukan anggota itu.")
        try:
            mention = (await client.get_users(user_id)).mention
        except Exception as error:
            await message.reply(error)
        try:
            await message.chat.unban_member(user_id)
            await message.reply(f"<b>✅ {mention} Sudah Bisa Chat Lagi</b>")
        except Exception as error:
            await message.reply(error)
    elif message.command[0] == "unban":
        user_id = await extract_user(message)
        if not user_id:
            return await message.reply_text("Saya tidak dapat menemukan anggota itu.")
        try:
            mention = (await client.get_users(user_id)).mention
        except Exception as error:
            await message.reply(error)
        try:
            await message.chat.unban_member(user_id)
            await message.reply(f"<b>✅ {mention} Sudah Join Lagi</b>")
        except Exception as error:
            await message.reply(error)


@PY.UBOT(["gban", "ungban"], PREFIX)
async def _(client, message):
    user_id = await extract_user(message)
    Tm = await message.reply("</b>Memproses. . .</b>")
    if not user_id:
        return await Tm.edit("<b>user tidak ditemukan</b>")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    done = 0
    failed = 0
    text = "<b>💬 Global {}</b>\n\n<b>✅ Berhasil: {} Chat</b>\n<b>❌ Gagal: {} Chat</b>\n<b>👤 User: <a href='tg://user?id={}'>{} {}</a></b>"
    if message.command[0] == "gban":
        async for dialog in client.get_dialogs():
            chat_type = dialog.chat.type
            if chat_type in [
                ChatType.GROUP,
                ChatType.SUPERGROUP,
                ChatType.CHANNEL,
            ]:
                chat_id = dialog.chat.id
                if user.id == OWNER_ID:
                    return await Tm.edit(
                        "Anda tidak bisa gban dia karena dia pembuat saya"
                    )
                elif not user.id == OWNER_ID:
                    try:
                        await client.ban_chat_member(chat_id, user.id)
                        done += 1
                        await asyncio.sleep(0.1)
                    except:
                        failed += 1
                        await asyncio.sleep(0.1)
        await Tm.delete()
        return await message.reply(
            text.format(
                "Banned", done, failed, user.id, user.first_name, (user.last_name or "")
            )
        )
    elif message.command[0] == "ungban":
        async for dialog in client.get_dialogs():
            chat_type = dialog.chat.type
            if chat_type in [
                ChatType.GROUP,
                ChatType.SUPERGROUP,
                ChatType.CHANNEL,
            ]:
                chat_id = dialog.chat.id
                try:
                    await client.unban_chat_member(chat_id, user.id)
                    done += 1
                    await asyncio.sleep(0.1)
                except:
                    failed += 1
                    await asyncio.sleep(0.1)
        await Tm.delete()
        return await message.reply(
            text.format(
                "Unbanned",
                done,
                failed,
                user.id,
                user.first_name,
                (user.last_name or ""),
            )
        )
