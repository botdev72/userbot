from pyrogram.errors.exceptions.bad_request_400 import (ChatAdminRequired,
                                                        ChatNotModified)
from pyrogram.types import ChatPermissions

from ubot import KY, Emo

data = {
    "msg": "can_send_messages",
    "stiker": "can_send_other_messages",
    "gifs": "can_send_other_messages",
    "media": "can_send_media_messages",
    "games": "can_send_other_messages",
    "inline": "can_send_other_messages",
    "url": "can_add_web_page_previews",
    "polls": "can_send_polls",
    "info": "can_change_info",
    "invite": "can_invite_users",
    "pin": "can_pin_messages",
}


async def current_chat_permissions(client, chat_id):
    perms = []
    perm = (await client.get_chat(chat_id)).permissions
    if perm.can_send_messages:
        perms.append("can_send_messages")
    if perm.can_send_media_messages:
        perms.append("can_send_media_messages")
    if perm.can_send_other_messages:
        perms.append("can_send_other_messages")
    if perm.can_add_web_page_previews:
        perms.append("can_add_web_page_previews")
    if perm.can_send_polls:
        perms.append("can_send_polls")
    if perm.can_change_info:
        perms.append("can_change_info")
    if perm.can_invite_users:
        perms.append("can_invite_users")
    if perm.can_pin_messages:
        perms.append("can_pin_messages")
    return perms


async def tg_lock(
    client,
    message,
    parameter,
    permissions: list,
    perm: str,
    lock: bool,
):
    emo = Emo(client.me.id)
    await emo.initialize()
    if lock:
        if perm not in permissions:
            return await message.edit_text(
                f"{emo.sukses} 🔒 `{parameter}` **Sudah terkunci!**"
            )
        permissions.remove(perm)
    else:
        if perm in permissions:
            return await message.edit_text(
                f"{emo.sukses} 🔓 `{parameter}` **Sudah terbuka!**"
            )
        permissions.append(perm)
    permissions = {perm: True for perm in list(set(permissions))}
    try:
        await client.set_chat_permissions(
            message.chat.id, ChatPermissions(**permissions)
        )
    except ChatNotModified:
        return await message.edit_text(
            f"{emo.gagal} **Untuk membuka ini anda harus menggunakan perintah : `unlock msg` terlebih dahulu.**"
        )
    except ChatAdminRequired:
        return await message.edit_text(
            f"{emo.gagal} **Saya tidak mempunyai izin admin disini.**"
        )
    await message.edit_text(
        (
            f"{emo.sukses} 🔒 **Terkunci untuk non-admin!**\n  **Tipe:** `{parameter}`\n  **Grup:** {message.chat.title}"
            if lock
            else f"{emo.sukses} 🔓 **Terbuka untuk non-admin!**\n  **Tipe:** `{parameter}`\n  **Grup:** {message.chat.title}"
        )
    )


@KY.UBOT("lock|unlock")
async def _(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    ky = await message.reply(f"{emo.proses} **Processing...**")
    if len(message.command) != 2:
        return await ky.edit(
            f"{emo.gagal} Parameter yang anda masukan salah silakan ketik `.help locks`"
        )
    chat_id = message.chat.id
    parameter = message.text.strip().split(None, 1)[1].lower()
    state = message.command[0].lower()
    if parameter not in data and parameter != "all":
        return await ky.edit(
            f"{emo.gagal} Parameter yang anda masukan salah silakan ketik `.help locks`"
        )
    permissions = await current_chat_permissions(client, chat_id)
    if parameter in data:
        await tg_lock(
            client,
            message,
            parameter,
            permissions,
            data[parameter],
            bool(state == "lock"),
        )
    elif parameter == "all" and state == "lock":
        try:
            await client.set_chat_permissions(chat_id, ChatPermissions())
            await ky.edit(
                f"{emo.sukses} 🔒 **Terkunci untuk non-admin!**\n  **Tipe:** `{parameter}`\n  **Grup:** {message.chat.title}"
            )
        except ChatAdminRequired:
            return await ky.edit(
                f"{emo.gagal} **Saya tidak mempunyai izin admin disini.**"
            )
        except ChatNotModified:
            return await ky.edit(
                f"{emo.sukses} 🔒 **Sudah terkunci!**\n  **Tipe:** `{parameter}`\n  **Grup:** {message.chat.title}"
            )
        await ky.delete()
    elif parameter == "all" and state == "unlock":
        try:
            await client.set_chat_permissions(
                chat_id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                    can_send_polls=True,
                    can_change_info=False,
                    can_invite_users=True,
                    can_pin_messages=False,
                ),
            )
        except ChatAdminRequired:
            return await ky.edit(
                f"{emo.gagal} **Saya tidak mempunyai izin admin disini.**"
            )
        await ky.edit(
            f"{emo.sukses} 🔓 **Terbuka untuk non-admin!**\n  **Tipe:** `{parameter}`\n  **Grup:** {message.chat.title}"
        )


@KY.UBOT("locks")
async def _(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    permissions = await current_chat_permissions(client, message.chat.id)
    ky = await message.reply(f"{emo.proses} <b>Processing...</b>")

    if not permissions:
        return await ky.edit(f"{emo.sukses} 🔒 **Terkunci untuk semua!**")

    perms = ""
    for i in permissions:
        perms += f" • __**{i}**__\n"

    await message.edit(perms)


__MODULE__ = "Locks"
__HELP__ = """

 Bantuan Untuk Locks

• Perintah : `{0}lock [all or type]`
• Penjelasan : Untuk mengubah izin grup.

• Perintah : `{0}unlock [all or type]`
• Penjelasan : Untuk membuka izin grup.

• Perintah : `{0}locks`
• Penjelasan : Untuk melihat izin saat ini.

• Type : `msg`|`media`|`stickers`|`polls`|`info`|`invite`|`webprev`|`pin`
"""
