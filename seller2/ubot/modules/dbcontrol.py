from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.types import *
from pytz import timezone

from ubot import FIL, KY, add_offi, bot, get_offi
from ubot.config import *
from ubot.utils.dbfunctions import *
from ubot.utils.utils import *


@KY.BOT("prem", FIL.GROUP)
@KY.UBOT("prem")
async def prem_user(client, message):
    Tm = await message.reply("<b>Processing...</b>")
    # if message.chat.id != LOG_SELLER:
    # return await Tm.edit("Perintah ini hanya dapat digunakan di grup resmi seller [ubot]."
    # )
    #chat_type = message.chat.type
    #if chat_type == enums.ChatType.PRIVATE:
        #return await Tm.edit("<b>Mau ngapain ? ketik ini di gc seles</b>")
    if message.from_user.id not in await get_seles():
        return await Tm.edit(
            "Untuk menggunakan perintah ini, anda harus menjadi Reseller"
        )
    user_id, get_bulan = await extract_user_and_reason(message)
    if not user_id:
        return await Tm.edit(f"<b>{message.text} [user_id/username - bulan]</b>")
    try:
        get_id = (await client.get_users(user_id)).id
    except Exception as error:
        return await Tm.edit(str(error))
    if not get_bulan:
        get_bulan = 1
    premium = await get_prem()
    if get_id in premium:
        return await Tm.edit(f"Pengguna denga ID : `{get_id}` sudah memiliki akses !")
    added = await add_prem(get_id)
    if added:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(get_bulan))
        expired_formatted = expired.strftime("%d %b %Y")
        await set_expired_date(get_id, expired)
        await Tm.edit(
            f"✅ {get_id} Berhasil diaktifkan selama `{get_bulan}` bulan. Silakan buka @{bot.me.username}. \n\nKadaluwarsa pada : `{expired_formatted}`."
        )
        await bot.send_message(
            OWNER_ID,
            f"• {message.from_user.id} ─> {get_id} •",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "👤 ᴘʀᴏғɪʟ",
                            callback_data=f"profil {message.from_user.id}",
                        ),
                        InlineKeyboardButton(
                            "ᴘʀᴏғɪʟ 👤", callback_data=f"profil {get_id}"
                        ),
                    ],
                ]
            ),
        )
        await bot.send_message(
            get_id,
            f"Selamat ! Akun anda sudah memiliki akses untuk pembuatan userbot\nKadaluwarsa pada : {expired_formatted}.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Lanjutkan Pembuatan Userbot", callback_data="bahan"
                        )
                    ],
                ]
            ),
        )
    else:
        await Tm.delete()
        await message.reply_text("Error")


@KY.BOT("delprem", FIL.GROUP)
@KY.UBOT("delprem")
async def unprem_user(client, message):
    user_id = await extract_user(message)
    Tm = await message.reply("Processing...")
    if message.from_user.id != OWNER_ID:
        return
    if not user_id:
        return await Tm.edit("Balas pesan pengguna atau berikan user_id/username")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        await Tm.edit(str(error))
    delpremium = await get_prem()
    if user.id not in delpremium:
        return await Tm.edit("Tidak ditemukan")
    removed = await remove_prem(user.id)
    if removed:
        await Tm.edit(f" ✅ {user.mention} berhasil dihapus")
    else:
        await Tm.delete()
        await message.reply_text("Terjadi kesalahan yang tidak diketahui")


@KY.BOT("getprem", FIL.GROUP)
@KY.UBOT("getprem")
async def get_prem_user(client, message):
    if message.from_user.id != OWNER_ID:
        return
    text = ""
    count = 0
    for user_id in await get_prem():
        try:
            user = await bot.get_users(user_id)
            count += 1
            userlist = f"• {count}: <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> > <code>{user.id}</code>"
        except Exception:
            continue
        text += f"{userlist}\n"
    if not text:
        await message.reply_text("Tidak ada pengguna yang ditemukan")
    else:
        await message.reply_text(text)


@KY.BOT("seles", FIL.SUDO)
@KY.UBOT("seles", FIL.ME_USER)
async def seles_user(client, message):
    user_id = await extract_user(message)
    Tm = await message.reply("Tunggu Sebentar...")
    if not user_id:
        return await Tm.edit("Balas pesan pengguna atau berikan user_id/username")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        await Tm.edit(str(error))
    reseller = await get_seles()
    if user.id in reseller:
        return await Tm.edit("Sudah menjadi reseller.")
    added = await add_seles(user.id)
    if added:
        await add_prem(user.id)
        await Tm.edit(f"✅ {user.mention} telah menjadi reseller")
    else:
        await Tm.delete()
        await message.reply_text("Terjadi kesalahan yang tidak diketahui")


@KY.BOT("delseles", FIL.SUDO)
@KY.UBOT("delseles", FIL.ME_USER)
async def unseles_user(client, message):
    user_id = await extract_user(message)
    if message.from_user.id != OWNER_ID:
        return
    Tm = await message.reply("Tunggu Sebentar...")
    if not user_id:
        return await Tm.edit("Balas pesan pengguna atau berikan user_id/username")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        await Tm.edit(str(error))
    delreseller = await get_seles()
    if user.id not in delreseller:
        return await Tm.edit("Tidak ditemukan")
    removed = await remove_seles(user.id)
    if removed:
        await remove_prem(user.id)
        await Tm.edit(f"{user.mention} berhasil dihapus")
    else:
        await Tm.delete()
        await message.reply_text("Terjadi kesalahan yang tidak diketahui")


@KY.BOT("getseles", FIL.SUDO)
@KY.UBOT("getseles")
async def get_seles_user(client, message):
    if message.from_user.id != OWNER_ID:
        return
    text = ""
    count = 0
    for user_id in await get_seles():
        try:
            user = await bot.get_users(user_id)
            count += 1
            userlist = f"• {count}: <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> > <code>{user.id}</code>"
        except Exception:
            continue
        text += f"{userlist}\n"
    if not text:
        await message.reply_text("Tidak ada pengguna yang ditemukan")
    else:
        await message.reply_text(text)


@KY.BOT("setexp")
@KY.UBOT("setexp")
async def expired_add(client, message):
    Tm = await message.reply("Processing...")
    if message.from_user.id != OWNER_ID:
        return await Tm.edit("Lu siapa ngentod.")
    #if message.chat.id != LOG_SELLER:
        #return await Tm.edit(
            #"Perintah ini hanya dapat digunakan di grup resmi seller [ubot]."
        #)
    user_id, get_day = await extract_user_and_reason(message)
    if not user_id:
        return await Tm.edit(f"{message.text} user_id/username - hari")
    try:
        get_id = (await client.get_users(user_id)).id
    except Exception as error:
        return await Tm.edit(str(error))
    if not get_day:
        get_day = 30
    now = datetime.now(timezone("Asia/Jakarta"))
    expire_date = now + timedelta(days=int(get_day))
    await set_expired_date(user_id, expire_date)
    await Tm.edit(f"{get_id} telah diaktifkan selama {get_day} hari.")


@KY.BOT("cek", FIL.SUDO)
@KY.UBOT("cek", FIL.ME_USER)
async def expired_cek(client, message):
    user_id = await extract_user(message)
    Tm = await message.reply("Processing...")
    if message.chat.id != LOG_SELLER:
        return await Tm.edit(
            "Perintah ini hanya dapat digunakan di grup resmi seller [ubot]."
        )
    if not user_id:
        return await Tm.edit("Pengguna tidak ditemukan")
    expired_date = await get_expired_date(user_id)
    if expired_date is None:
        await Tm.edit(f"{user_id} belum diaktifkan.")
    else:
        remaining_days = (expired_date - datetime.now()).days
        await Tm.edit(
            f"{user_id} aktif hingga {expired_date.strftime('%d-%m-%Y %H:%M:%S')}. Sisa waktu aktif {remaining_days} hari."
        )


@KY.BOT("delexp", FIL.SUDO)
@KY.UBOT("delexp", FIL.ME_USER)
async def un_expired(client, message):
    user_id = await extract_user(message)
    Tm = await message.reply("Processing...")
    if message.from_user.id != OWNER_ID:
        return
    #if message.chat.id != LOG_SELLER:
        #return await Tm.edit(
            #"Perintah ini hanya dapat digunakan di grup resmi seller [ubot]."
        #)
    if not user_id:
        return await Tm.edit("User tidak ditemukan")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(str(error))
    await rem_expired_date(user.id)
    return await Tm.edit(f"✅ {user.id} expired telah dihapus")


@KY.BOT("bcast")
async def bacotan(_, message: Message):
    await message.delete()
    if message.from_user.id != OWNER_ID:
        return
    message.from_user.id
    if len(message.command) > 1:
        text = " ".join(message.command[1:])
    elif message.reply_to_message is not None:
        text = message.reply_to_message.text
    else:
        return await eor(
            message,
            "<code>Silakan sertakan pesan atau balas pesan yang ingin disiarkan.</code>",
        )
    kntl = 0
    mmk = []
    jmbt = len(await get_served_users())
    babi = await get_served_users()
    for x in babi:
        mmk.append(int(x["user_id"]))
    if OWNER_ID in mmk:
        mmk.remove(OWNER_ID)
    for i in mmk:
        try:
            await bot.send_message(i, text)
            kntl += 1
        except:
            pass
    return await eor(
        message,
        f"**Berhasil mengirim pesan ke `{kntl}` pengguna, dari `{jmbt}` pengguna.**",
    )


@KY.UBOT("getubot")
async def getubot_cmd(client, message):
    if message.from_user.id != OWNER_ID:
        return
    msg = await message.reply("<b>Procesing...</b>", quote=True)
    try:
        x = await client.get_inline_bot_results(bot.me.username, f"ambil_ubot")
        await message.reply_inline_bot_result(x.query_id, x.results[0].id, quote=True)
        await msg.delete()
    except Exception as error:
        await msg.edit(error)


###################### AKSES JOINVC #######################


@KY.BOT("fullakses")
@KY.UBOT("fullakses")
async def offi_user(client, message):
    Tm = await message.reply("<b>Processing... .</b>")
    # if message.chat.id != LOG_SELLER:
    # return await Tm.edit("Perintah ini hanya dapat digunakan di grup resmi seller [ubot]."
    # )
    if message.from_user.id not in await get_seles():
        return await Tm.edit(
            "Untuk menggunakan perintah ini, anda harus menjadi Reseller"
        )
    user_id, get_bulan = await extract_user_and_reason(message)
    if not user_id:
        return await Tm.edit(f"<b>{message.text} [user_id/username - bulan]</b>")
    try:
        get_id = (await client.get_users(user_id)).id
    except Exception as error:
        return await Tm.edit(str(error))
    if not get_bulan:
        get_bulan = 1
    offi = await get_offi()

    if get_id in offi:
        return await Tm.edit(f"Pengguna denga ID : `{get_id}` sudah memiliki akses !")
    try:
        await add_prem(get_id)
        await add_offi(get_id)
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(get_bulan))
        expired_formatted = expired.strftime("%d %b %Y")
        await set_expired_date(get_id, expired)
        await Tm.edit(
            f"✅ {get_id} Berhasil diaktifkan selama `{get_bulan}` bulan. Silakan buka {bot.me.mention}. \n\nKadaluwarsa pada : `{expired_formatted}`."
        )
        await bot.send_message(
            OWNER_ID,
            f"• {message.from_user.id} ─> {get_id} •",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "👤 ᴘʀᴏғɪʟ",
                            callback_data=f"profil {message.from_user.id}",
                        ),
                        InlineKeyboardButton(
                            "ᴘʀᴏғɪʟ 👤", callback_data=f"profil {get_id}"
                        ),
                    ],
                ]
            ),
        )
        await bot.send_message(
            get_id,
            f"Selamat ! Akun anda sudah memiliki akses untuk pembuatan userbot\nKadaluwarsa pada : {expired_formatted}.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Lanjutkan Pembuatan Userbot", callback_data="bahan"
                        )
                    ],
                ]
            ),
        )
    except Exception as e:
        await Tm.delete()
        await message.reply_text(f"Error {e}")
