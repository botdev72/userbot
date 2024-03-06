from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.types import *
from pytz import timezone

from ubot import KY, add_offi, bot, get_offi
from ubot.config import *
from ubot.utils.dbfunctions import *
from ubot.utils.utils import *


@KY.BOT("unof")
@KY.UBOT("unof", sudo=False)
async def prem_user(client, message):
    if message.from_user.id not in await get_seles():
        return
    user_id, get_bulan = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply(f"<b>{message.text} [user_id/username - bulan]</b>")
    try:
        get_id = (await client.get_users(user_id)).id
    except Exception as error:
        return await message.reply(str(error))
    if not get_bulan:
        get_bulan = 1
    premium = await get_prem()
    if get_id in premium:
        return await message.reply(
            f"Pengguna denga ID : `{get_id}` sudah memiliki akses !"
        )
    added = await add_prem(get_id)
    if added:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(get_bulan))
        expired_formatted = expired.strftime("%d %b %Y")
        await set_expired_date(get_id, expired)
        await message.reply(
            f"✅ {get_id} Berhasil diaktifkan selama `{get_bulan}` bulan. Silakan buka {bot.me.mention}. \n\nKadaluwarsa pada : `{expired_formatted}`.",
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
        await message.delete()
        await message.reply_text("Error")


@KY.BOT("delunof")
@KY.UBOT("delunof", sudo=False)
async def unprem_user(client, message):
    user_id = await extract_user(message)
    if message.from_user.id not in await get_seles():
        return
    if not user_id:
        return await message.reply("Balas pesan pengguna atau berikan user_id/username")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        await message.reply(str(error))
    delpremium = await get_prem()
    if user.id not in delpremium:
        return await message.reply("Tidak ditemukan")
    removed = await remove_prem(user.id)
    if removed:
        await message.reply(f" ✅ {user.mention} berhasil dihapus")
    else:
        await message.delete()
        await message.reply_text("Terjadi kesalahan yang tidak diketahui")


@KY.BOT("getunof")
@KY.UBOT("getunof", sudo=False)
async def get_prem_user(client, message):
    if message.from_user.id not in KYNAN:
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


@KY.BOT("seles")
@KY.UBOT("seles", sudo=False)
async def seles_user(client, message):
    if message.from_user.id not in KYNAN:
        return
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply("Balas pesan pengguna atau berikan user_id/username")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        await message.reply(str(error))
    reseller = await get_seles()
    if user.id in reseller:
        return await message.reply("Sudah menjadi reseller.")
    added = await add_seles(user.id)
    if added:
        await add_prem(user.id)
        await message.reply(f"✅ {user.mention} telah menjadi reseller")
    else:
        await message.delete()
        await message.reply_text("Terjadi kesalahan yang tidak diketahui")


@KY.BOT("delseles")
@KY.UBOT("delseles", sudo=False)
async def unseles_user(client, message):
    user_id = await extract_user(message)
    if message.from_user.id not in KYNAN:
        return
    if not user_id:
        return await message.reply("Balas pesan pengguna atau berikan user_id/username")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        await message.reply(str(error))
    delreseller = await get_seles()
    if user.id not in delreseller:
        return await message.reply("Tidak ditemukan")
    removed = await remove_seles(user.id)
    if removed:
        await remove_prem(user.id)
        await message.reply(f"{user.mention} berhasil dihapus")
    else:
        await message.delete()
        await message.reply_text("Terjadi kesalahan yang tidak diketahui")


@KY.BOT("getseles")
@KY.UBOT("getseles", sudo=False)
async def get_seles_user(client, message):
    if message.from_user.id not in KYNAN:
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
@KY.UBOT("setexp", sudo=False)
async def expired_add(client, message):
    if message.from_user.id not in KYNAN:
        return
    user_id, get_day = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply(f"{message.text} user_id/username - hari")
    try:
        get_id = (await client.get_users(user_id)).id
    except Exception as error:
        return await message.reply(str(error))
    if not get_day:
        get_day = 30
    now = datetime.now(timezone("Asia/Jakarta"))
    expire_date = now + timedelta(days=int(get_day))
    await set_expired_date(user_id, expire_date)
    await message.reply(f"{get_id} telah diaktifkan selama {get_day} hari.")


@KY.BOT("cek")
@KY.UBOT("cek", sudo=False)
async def expired_cek(client, message):
    if message.from_user.id not in await get_seles():
        return
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply("Pengguna tidak ditemukan")
    expired_date = await get_expired_date(user_id)
    if expired_date is None:
        await message.reply(f"{user_id} belum diaktifkan.")
    else:
        remaining_days = (expired_date - datetime.now()).days
        await message.reply(
            f"{user_id} aktif hingga {expired_date.strftime('%d-%m-%Y %H:%M:%S')}. Sisa waktu aktif {remaining_days} hari.",
        )


@KY.BOT("delexp")
@KY.UBOT("delexp", sudo=False)
async def un_expired(client, message):
    user_id = await extract_user(message)
    if message.from_user.id not in KYNAN:
        return
    if not user_id:
        return await message.reply("User tidak ditemukan")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await message.reply(str(error))
    await rem_expired_date(user.id)
    return await message.reply(f"✅ {user.id} expired telah dihapus")


@KY.BOT("bcast")
async def bacotan(_, message: Message):
    await message.delete()
    if message.from_user.id not in KYNAN:
        return
    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
    if len(message.command) > 1:
        return await message.reply(
            "<b>Silakan sertakan pesan atau balas pesan yang ingin disiarkan.</b>",
        )

    kntl = 0
    mmk = []
    jmbt = len(await get_served_users())
    babi = await get_served_users()
    for xx in babi:
        mmk.append(int(xx["user_id"]))
    if OWNER_ID in mmk:
        mmk.remove(OWNER_ID)
    for i in mmk:
        try:
            m = (
                await bot.forward_messages(i, y, x)
                if message.reply_to_message
                else await bot.send_message(i, y, x)
            )
            # await bot.send_message(i, text)
            kntl += 1
        except:
            pass
    return await message.reply(
        f"**Berhasil mengirim pesan ke `{kntl}` pengguna, dari `{jmbt}` pengguna.**",
    )


@KY.UBOT("getubot", sudo=False)
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


@KY.BOT("offi")
@KY.UBOT("offi", sudo=False)
async def offi_user(client, message):
    if message.from_user.id not in await get_seles():
        return
    user_id, get_bulan = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply(f"<b>{message.text} [user_id/username - bulan]</b>")
    try:
        get_id = (await client.get_users(user_id)).id
    except Exception as error:
        return await message.reply(str(error))
    if not get_bulan:
        get_bulan = 1
    offi = await get_offi()

    if get_id in offi:
        return await message.reply(
            f"Pengguna denga ID : `{get_id}` sudah memiliki akses !"
        )
    try:
        await add_prem(get_id)
        await add_offi(get_id)
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(get_bulan))
        expired_formatted = expired.strftime("%d %b %Y")
        await set_expired_date(get_id, expired)
        await message.reply(
            f"✅ {get_id} Berhasil diaktifkan selama `{get_bulan}` bulan. Silakan buka {bot.me.mention}. \n\nKadaluwarsa pada : `{expired_formatted}`.",
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
        await message.delete()
        await message.reply_text(f"Error {e}")
