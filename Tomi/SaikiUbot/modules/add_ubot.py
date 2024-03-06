import asyncio
import importlib
from datetime import datetime, timedelta
from io import BytesIO

from pyrogram import filters
from pyrogram.enums import ChatType, SentCodeType
from pyrogram.errors import *
from pyrogram.types import *
from pytz import timezone

from SaikiUbot.modules import loadModule

from .. import *


@bot.on_callback_query(filters.regex("add_ubot"))
async def _(_, callback_query):
    user_id = callback_query.from_user.id
    PREM_ID = await get_prem()
    ID_SELES = await get_seles()
    if not bot.me.id == 5812805818:
        MAX_UBOT = 10
    else:
        MAX_UBOT = 99
    if len(ubot._ubot) == MAX_UBOT:
        buttons = [
            [InlineKeyboardButton("🗑️ Tutup 🗑️", callback_data="0_cls")],
        ]
        await callback_query.message.delete()
        return await bot.send_message(
            user_id,
            f"""
<b>❌ TIDAK BISA MEMBUAT USERBOT!</b>

<b>📚 KARENA MAKSIMAL USERBOT ADALAH {MAX_UBOT} TELAH TERCAPAI</b>

<b>☎️ SILAHKAN HUBUNGI: <a href=t.me/T0M1_X>ADMIN</a> JIKA MAU DIBUATKAN BOT SEPERTI SAYA</b>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    elif user_id not in PREM_ID:
        buttons = [[InlineKeyboardButton("✅ KONFIRMASI", callback_data="confirm")]]
        await callback_query.message.delete()
        return await bot.send_message(
            user_id,
            TEXT_PAYMENT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    try:
        await callback_query.message.delete()
        phone = await bot.ask(
            user_id,
            (
                "<b>Silahkan Masukkan Nomor Telepon Telegram Anda Dengan Format Kode Negara.\nContoh: +628xxxxxxx</b>\n"
                "\n<b>Gunakan /cancel untuk Membatalkan Proses Membuat Userbot</b>"
            ),
            timeout=300,
        )
    except asyncio.TimeoutError:
        return await bot.send_message(user_id, "waktu Telah Habis")
    if await is_cancel(callback_query, phone.text):
        return
    phone_number = phone.text
    new_client = Ubot(
        name=str(callback_query.id),
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=False,
    )
    get_otp = await bot.send_message(user_id, "<b>Mengirim Kode OTP...</b>")
    await new_client.connect()
    try:
        code = await new_client.send_code(phone_number.strip())
    except PhoneNumberInvalid as PNI:
        await get_otp.delete()
        return await bot.send_message(user_id, PNI)
    except PhoneNumberFlood as PNF:
        await get_otp.delete()
        return await bot.send_message(user_id, PNF)
    except PhoneNumberBanned as PNB:
        await get_otp.delete()
        return await bot.send_message(user_id, PNB)
    except PhoneNumberUnoccupied as PNU:
        await get_otp.delete()
        return await bot.send_message(user_id, PNU)
    except Exception as error:
        await get_otp.delete()
        return await bot.send_message(user_id, f"<b>ERROR:</b> {error}")
    try:
        sent_code = {
            SentCodeType.APP: "<a href=tg://openmessage?user_id=777000>Akun Telegram</a> Resmi",
            SentCodeType.SMS: "SMS Anda",
            SentCodeType.CALL: "Panggilan Telpon",
            SentCodeType.FLASH_CALL: "panggilan kilat telepon",
            SentCodeType.FRAGMENT_SMS: "Fragment SMS",
            SentCodeType.EMAIL_CODE: "Email Anda",
        }
        await get_otp.delete()
        otp = await bot.ask(
            user_id,
            (
                f"<b>Silakan Periksa Kode OTP Dari {sent_code[code.type]}. Kirim Kode OTP Ke Sini Setelah Membaca Format Di Bawah Ini.</b>\n"
                "\nJika Kode OTP Adalah <code>12345</code> Tolong <b>[ TAMBAHKAN SPASI ]</b> kirimkan Seperti ini <code>1 2 3 4 5</code>\n"
                "\n<b>Gunakan /cancel Untuk Membatalkan Proses Membuat Userbot</b>"
            ),
            timeout=300,
        )
    except asyncio.TimeoutError:
        return await bot.send_message(user_id, "waktu Telah Habis")
    if await is_cancel(callback_query, otp.text):
        return
    otp_code = otp.text
    try:
        await new_client.sign_in(
            phone_number.strip(),
            code.phone_code_hash,
            phone_code=" ".join(str(otp_code)),
        )
    except PhoneCodeInvalid as PCI:
        return await bot.send_message(user_id, PCI)
    except PhoneCodeExpired as PCE:
        return await bot.send_message(user_id, PCE)
    except BadRequest as error:
        return await bot.send_message(user_id, f"<b>ERROR:</b> {error}")
    except SessionPasswordNeeded:
        try:
            two_step_code = await bot.ask(
                user_id,
                "<b>Akun anda Telah mengaktifkan Verifikasi Dua Langkah. Silahkan Kirimkan Passwordnya.\n\nGunakan /cancel untuk Membatalkan Proses Membuat Userbot</b>",
                timeout=300,
            )
        except asyncio.TimeoutError:
            return await bot.send_message(user_id, "Batas waktu tercapai 5 menit.")
        if await is_cancel(callback_query, two_step_code.text):
            return
        new_code = two_step_code.text
        try:
            await new_client.check_password(new_code)
        except Exception as error:
            return await bot.send_message(user_id, f"<b>ERROR:</b> {error}")
    session_string = await new_client.export_session_string()
    await new_client.disconnect()
    new_client.storage.session_string = session_string
    new_client.in_memory = False
    await new_client.start()
    await add_ubot(
        user_id=int(new_client.me.id),
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string,
    )
    for mod in loadModule():
        importlib.reload(importlib.import_module(f"userbot.modules.{mod}"))
    text_done = f"<b>🔥 {bot.me.mention} Berhasil Diaktifkan Di Akun: <a href=tg://openmessage?user_id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a> > <code>{new_client.me.id}</code></b> "
    await bot.send_message(
        user_id,
        text_done,
        disable_web_page_preview=True,
    )
    now = datetime.now(timezone("Asia/Jakarta"))
    date = now.strftime("%d-%m-%Y")
    expire_date = now + timedelta(days=30)
    await set_expired_date(new_client.me.id, expire_date)
    get_exp = await get_expired_date(new_client.me.id)
    exp = get_exp.strftime("%d-%m-%Y")
    buttons = [
        [
            InlineKeyboardButton(
                "🧑‍💻 Pembuat Userbot 🧑‍💻",
                url=f"tg://openmessage?user_id={callback_query.from_user.id}",
            )
        ],
        [
            InlineKeyboardButton(
                "📁 Hapus Dari Database 📁",
                callback_data=f"del_ubot {new_client.me.id}",
            )
        ],
    ]
    await bot.send_message(
        LOGS_MAKER_UBOT,
        f"{text_done}\n<b>🗓️ Mulai: {date}</b>\n<b>🗓️ Akhir: {exp}</b>",
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True,
    )
    get_my_id.append(new_client.me.id)
    users = 0
    group = 0
    async for dialog in new_client.get_dialogs():
        if dialog.chat.type == ChatType.PRIVATE:
            users += 1
        elif dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
            group += 1
    get_my_peer[new_client.me.id] = {"group": group, "users": users}
    try:
        await new_client.join_chat("SaikiSupport")
    except UserAlreadyParticipant:
        pass
    if callback_query.from_user.id in ID_SELES:
        return
    else:
        await remove_prem(callback_query.from_user.id)


@bot.on_message(filters.command("getubot"))
async def _(client, message):
    if not message.from_user.id == OWNER_ID:
        return
    count = 0
    user = ""
    for X in ubot._ubot:
        count += 1
        user += f"""
❏ USERBOT KE {count}
 ├ AKUN: <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a> 
 ╰ ID: <code>{X.me.id}</code>
"""
    if int(len(str(user))) > 4096:
        with BytesIO(str.encode(str(user))) as out_file:
            out_file.name = "userbot.txt"
            await message.reply_document(
                document=out_file,
            )
    else:
        await message.reply(f"<b>{user}</b>")


@bot.on_message(filters.command("delubot"))
async def _(client, message):
    user_id = message.from_user.id
    if not user_id == OWNER_ID:
        return
    if len(message.command) < 2:
        return await message.reply("Ketik /delubot user_id Untuk Mematikan Userbot")
    else:
        try:
            show = await bot.get_users(int(message.text.split()[1]))
            get_id = show.id
            get_mention = f"<a href=tg://user?id={get_id}>{show.first_name} {show.last_name or ''}</a>"
        except BadRequest:
            get_id = int(message.text.split()[1])
            get_mention = f"<a href=tg://user?id={get_id}>Userbot</a>"
        for X in ubot._ubot:
            if get_id == X.me.id:
                await remove_ubot(get_id)
                ubot._ubot.remove(X)
                get_my_id.remove(get_id)
                await message.reply(
                    f"<b> ✅ {get_mention} Berhasil Dihapus Dari Database</b>"
                )
                await bot.send_message(get_id, "<b>💬 MASA AKTIF ANDA TELAH BERAKHIR")
                return await rem_expired_date(get_id)


@bot.on_callback_query(filters.regex("del_ubot"))
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if not user_id == OWNER_ID:
        return
    try:
        show = await bot.get_users(callback_query.data.split()[1])
        get_id = show.id
        get_mention = f"<a href=tg://user?id={get_id}>{show.first_name} {show.last_name or ''}</a>"
    except BadRequest:
        get_id = int(callback_query.data.split()[1])
        get_mention = f"<a href=tg://user?id={get_id}>Userbot</a>"
    for X in ubot._ubot:
        if get_id == X.me.id:
            await X.log_out()
            await remove_ubot(get_id)
            ubot._ubot.remove(X)
            get_my_id.remove(get_id)
            await bot.send_message(
                OWNER_ID, f"<b> ✅ {get_mention} Berhasil Dihapus Dari Database</b>"
            )
            await bot.send_message(get_id, "<b>💬 MASA AKTIF ANDA TELAH BERAKHIR")
            return await rem_expired_date(get_id)


async def is_cancel(callback_query, text):
    if text.startswith("/cancel"):
        await bot.send_message(
            callback_query.from_user.id, "<b>Membatalkan Proses!</b>"
        )
        return True
    return False
