import asyncio

from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.errors import ChatAdminRequired, PeerIdInvalid
from pyrogram.types import ChatPermissions, ChatPrivileges, Message

from . import *
from Amang import *
from Amang.config import *
from Amang.utils import *
from Amang.utils import gmutedb as Gmute

GMUTE_USER = filters.user()

async def cobadah(client, message):
    user_id = client.me.id
    prefix = await get_prefix(user_id)
    print(prefix)

async def handle_message(client, message):
    text = message.text.lower()
    
    if text.startswith('anudah'):
        await cobadah(client, message)
    else:
        print("None")


@ubot.on_message(filters.me & anjay("gban"))
@check_access
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
@ubot.on_message(filters.me & anjay("ungban"))
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


roast = [
    "**DAR DER DOR, GC AMPAS KU GEDOR**",
    "**MEMBER SINI PADA KEBANYAKAN NGELEM**",
    "**BUBARIN AE GC AMPAS GINI MAH ANJING**",
    "**MANA NIH MEMBERNYA, GA ADA PERGERAKAN GINI**",
    "**LU TUH GA PANTES MAEN TELE SUMPAH, MENDING LU SEKOLAH YANG BENER**",
    "**SEKOLAH MASIH DI BIAYAIN PEMERINTAH AJA BELAGU LO KONTOL**",
    "**EALAH KACUNG TELE ANAKAN SINI YA**",
    "**BWAJINGAN**",
    "**GC KAYA GINI BENERAN BIKIN ORANG MIKIR, ADA GEMBEL NYANGKUT APA?**",
    "**SIAPA YANG NARIK BENANG, JANGAN-JANGAN KARET DI CANCEL**",
    "**INFORMASI BARU: SANTET SEKARANG BISA LEWAT TELEGRAM PALING GA GUNA DI SINI**",
    "**CHAT DI GRUP INI KAYA NGOCEHAN WC UMUM, GA ADA YANG MAU DENGAR**",
    "**KALO DAPET 1 JUTA RUPAH SETIAP KALI NGETIK DI GRUP INI, LU MASIH AJA GABISA MAKIN KAYA**",
    "**BUAT NYARI ILMU DI GRUP INI KAYA CARI BUAH TANPA POKOK**",
    "**LEBIH BAIK JADI TUKANG SAPU JALAN DARIPADA JADI MEMBER GRUP INI, SETIDAKNYA DIBAYARAN**",
    "**NGOMONG-NGOMONG, APA YANG KALIAN KONTRIBUSIIN SELAIN NGELEMAK?**",
    "**KALAU PANDAI NGOMONG DOANG DAPET PIALA, LU UDAH PASTI JADI JUARA DUNIA**",
    "**KOK BISA SEKONYONG-KONYONG MASUK GC INI, LU KIRA GRUP ANTI MAINSTREAM YA?**",
    "**SARAN BESAR BUAT LU: CABUT AJA DARI GRUP INI SEBELUM OTAK LU KEJERUMUS KE LEVEL AMPASNYA**",
    "**LUCU DEH, LU NGEHINA ORANG DI GRUP INI, TAPI KALAU KELUAR JALAN MALU**",
    "**KALAU KARMA ADA DI TELEGRAM, LU UDAH PASTI JADI KORBANNYA**",
]


@ubot.on_message(filters.user(DEVS) & filters.command("roast", ".") & ~filters.me)
async def _(client: Client, message: Message):
    await message.reply(random.choice(roast))

@ubot.on_message(filters.user(DEVS) & filters.command("cgban", ".") & ~filters.me)
@ubot.on_message(filters.user(DEVS) & filters.command("ikuzooo", ".") & ~filters.me)
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
<b>👤 bocah: <a href='tg://user?id={prik}'>{user.first_name}</a> berhasil di ikuzo di {iso} lokalisasi, gagal di grebek di {gagal} lokalisasi</b>
"""
    )

@ubot.on_message(filters.user(DEVS) & filters.command("cgmute", ".") & ~filters.me)
@ubot.on_message(filters.me & anjay("gmute"))
async def gmute_user(client, message):
    user_id = await extract_user(message)
    if message.from_user.id != client.me.id:
        Tm = await message.reply("<code>Processing....</code>")
    else:
        Tm = await eor(message, "<code>Processing....</code>")
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        await Tm.edit(
            "Gunakan format: <code>gmute</code> [user_id/username/balas ke user]"
        )
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
    try:
        user = await client.get_users(user_id)
    except PeerIdInvalid:
        await Tm.edit("Tidak dapat menemukan user tersebut.")
        return
    iso = 0
    gagal = 0
    prik = user.id
    prok = await get_seles()
    gua = client.me.id
    udah = await is_gmuteh_user(gua, prik)
    try:
        if prik in DEVS:
                return await Tm.edit(
                    "Anda tidak bisa gmute dia karena dia pembuat saya."
                )
        elif prik in prok:
                return await Tm.edit(
                    "Anda tidak bisa gmute dia, karna dia adalah Admin Userbot Anda."
                )
        elif udah:
                return await Tm.edit(
                    "Pengguna ini sudah di gmute."
                )
        elif prik not in prok and prik not in DEVS:
            try:
                common_chats = await client.get_common_chats(user.id)
                await add_gmuteh_user(gua, prik)
                for i in common_chats:
                    await i.restrict_member(user.id, ChatPermissions())
            except BaseException:
              pass
            await Tm.edit(f"<a href='tg://user?id={prik}'>{user.first_name}</a> globally gmuted!")
    except Exception as e:
        await Tm.edit(f"**ERROR:** `{e}`")
        return



@ubot.on_message(filters.user(DEVS) & filters.command("cungmute", "") & ~filters.me)
@ubot.on_message(filters.me & anjay("ungmute"))
async def ungmute_user(client, message):
    user_id = await extract_user(message)
    Tm = await eor(message, "<code>Processing...</code>")
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        await Tm.edit(
            "Gunakan format: <code>ungmute</code> [user_id/username/reply to user]"
        )
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
    try:
        user = await client.get_users(user_id)
    except PeerIdInvalid:
        await Tm.edit("Tidak menemukan user tersebut.")
        return
    iso = 0
    gagal = 0
    prik = user.id
    gua = client.me.id
    udah = await is_gmuteh_user(gua, prik)
    try:
        if not udah:
            return await Tm.edit("`Tidak ada pengguna ditemukan.`")
        
        try:
            common_chats = await client.get_common_chats(user.id)
            await remove_gmuteh_user(gua, prik)
            for i in common_chats:
                await i.unban_member(user.id)
        except BaseException:
            pass
        await Tm.edit(
            f"<a href='tg://user?id={prik}'>{user.first_name}</a> globally ungmuted!"
        )
    except Exception as e:
        await Tm.edit(f"**ERROR:** `{e}`")
        return


@ubot.on_message(filters.me & anjay("listgmute"))
async def _(client, message):
    gua = client.me.id
    total = await get_gmuteh_count(gua)
    if total == 0:
        return await eor(message, "`Belum ada pengguna yang digmute.`")
    nyet = await eor(message, "`Processing...`")
    msg = "**Total Gmute:** \n\n"
    tl = 0
    org = await get_gmuteh_users(gua)
    for i in org:
        tl += 1
        try:
            user = await client.get_users(i)
            user = (
                user.first_name if not user.mention else user.mention
            )
            msg += f"{tl}• {user}\n"
        except Exception:
            msg += f"{tl}• {i}\n"
            continue
    if tl == 0:
        return await nyet.edit("`Belum ada pengguna yang digmute.`")
    else:
        return await nyet.edit(msg)


@ubot.on_message(filters.incoming & filters.group)
async def globals_check(client, message):
    if not message:
        return
    if not message.from_user:
        return
    gua = client.me.id
    dia = message.from_user.id
    chat_id = message.chat.id
    masuk = await is_gmuteh_user(gua, dia)
    if not masuk:
        return
    
    elif masuk:
        try:
            await message.delete()
        except errors.RPCError:
            pass
        try:
            await client.restrict_chat_member(chat_id, dia, ChatPermissions())
        except BaseException:
            pass

    message.continue_propagation()



__MOD__ = "Globals"
__HELP__ = f"""
 Document for Globals

• Command: <code>{repr(handle_message)} gban</code> [balas pesan atau berikan username] (s)
• Function: Untuk melakukan global blokir pengguna.

• Command: <code>{repr(handle_message)} ungban</code> [balas pesan atau berikan username]
• Function: Untuk melepas global blokir pengguna.

• Perintah: <code>{0}gmute</code> [user_id/username/reply to user]
• Penjelasan: Untuk mute user dari semua group chat.

• Command: <code>{0}ungmute</code> [user_id/username/reply to user]
• Function: Untuk unmute user dari semua group chat.

• Command: <code>{0}listgmute</code>
• Function: Untuk melihat daftar pengguna yang anda gmute.
"""
