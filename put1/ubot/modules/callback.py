import asyncio
import importlib
from datetime import datetime

import random
from time import time

from pyrogram.raw.functions import Ping

from pyrogram.enums import SentCodeType
from pyrogram.errors import *
from pyrogram.types import *

from pytz import timezone

from ubot import *
from .add_ubot import bikin_ubot
from ubot.utils.dbfunctions import *
from ubot.utils.unpack import unpackInlineMessage
from .eval import restart

CONFIRM_PAYMENT = []


async def cek_ubot(client, callback_query):
    await bot.send_message(
        callback_query.from_user.id,
        await MSG.USERBOT(0),
        reply_markup=InlineKeyboardMarkup(Button.userbot(ubot._ubot[0].me.id, 0)),
    )


@bot.on_callback_query(filters.regex("^close_user"))
async def close_usernya(client, cq):
    unPacked = unpackInlineMessage(cq.inline_message_id)
    for x in ubot._ubot:
        if cq.from_user.id == OWNER_ID:
            await x.delete_messages(
                unPacked.chat_id, cq.from_user.id, unPacked.message_id
            )


@bot.on_inline_query(filters.regex("^ambil_ubot"))
async def getubot_query(client, inline_query):
    msg = await MSG.USERBOT(0)
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultArticle(
                    title="bijinya",
                    reply_markup=InlineKeyboardMarkup(Button.ambil_akun(ubot._ubot[0].me.id, 0)),
                    input_message_content=InputTextMessageContent(msg),
                )
            )
        ],
    )

@bot.on_callback_query(filters.regex("^bayar_dulu"))
async def payment_userbot(client, callback_query):
    user_id = callback_query.from_user.id
    buttons = Button.plus_minus(1, user_id)
    await callback_query.message.delete()
    return await bot.send_message(
        user_id,
        MSG.TEXT_PAYMENT(25, 25, 1),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons),
    )

@bot.on_callback_query(filters.regex("^bahan"))
async def need_api(client, callback_query):
    user_id = callback_query.from_user.id
    if len(ubot._ubot) > MAX_BOT:
        buttons = [
            [InlineKeyboardButton("Tutup", callback_data="0_cls")],
        ]
        await callback_query.message.delete()
        return await bot.send_message(
            user_id,
            f"""
<b>❌ Tidak Dapat Membuat Userbot !</b>

<b>📚 Karena Telah Mencapai Yang Telah Di Tentukan : {len(ubot._ubot)}</b>

<b>👮‍♂ Silakan Hubungi Admin . </b>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if user_id not in await get_prem():
        buttons = [
            [InlineKeyboardButton("➡️ Lanjutkan", callback_data="bayar_dulu")],
            [InlineKeyboardButton("❌ Batalkan", callback_data=f"home {user_id}")],
        ]
        await callback_query.message.delete()
        return await bot.send_message(
            user_id,
            MSG.POLICY(),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        await bikin_ubot(client, callback_query)
        
        
@bot.on_callback_query(filters.regex("^cek_masa_aktif"))
async def cek_userbot_expired(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    expired = await get_expired_date(user_id)
    try:
        xxxx = (expired - datetime.now()).days
        return await callback_query.answer(f"⏳ Tinggal {xxxx} hari lagi", True)
    except:
        return await callback_query.answer("✅ Sudah tidak aktif", True)
        


@bot.on_callback_query(filters.regex("^cek_ubot"))
@bot.on_message(filters.command("getubot"))
async def _(client, message):
    await cek_ubot(client, message)
    

@bot.on_callback_query(filters.regex("^del_ubot"))
async def hapus_ubot(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in USER_ID:
        return await callback_query.answer(
            f"❌ Jangan Diklik Boss {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
            True,
        )
    try:
        show = await bot.get_users(callback_query.data.split()[1])
        get_id = show.id
        get_mention = f"<a href=tg://user?id={get_id}>{show.first_name} {show.last_name or ''}</a>"
    except Exception:
        get_id = int(callback_query.data.split()[1])
        get_mention = f"<a href=tg://user?id={get_id}>Userbot</a>"
    for X in ubot._ubot:
        if get_id == X.me.id:
            await X.unblock_user(bot.me.username)
            for chat in await get_chat(X.me.id):
                await remove_chat(X.me.id, chat)
            await rm_all(X.me.id)
            await remove_ubot(X.me.id)
            await rem_expired_date(X.me.id)
            await rem_uptime(X.me.id)
            await rem_pref(X.me.id)
            ubot._get_my_id.remove(X.me.id)
            ubot._ubot.remove(X)
            await X.log_out()
            return await bot.send_message(OWNER_ID, f"<b> ✅ {get_mention} Berhasil Di Hapus Dari Database</b>")
            #return await bot.send_message(X.me.id, "<b>💬 Masa Aktif Anda Telah Habis")
            
@bot.on_callback_query(filters.regex("^(get_otp|get_phone|get_faktor|ub_deak|deak_akun)"))
async def tools_userbot(client, callback_query):
    user_id = callback_query.from_user.id
    query = callback_query.data.split()
    if user_id not in USER_ID:
        return await callback_query.answer(
            f"❌ Jangan Di Klik Mas {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
            True,
        )
    X = ubot._ubot[int(query[1])]
    if query[0] == "get_otp":
        async for otp in X.search_messages(777000, limit=1):
            try:
                if not otp.text:
                    await callback_query.answer("❌ Kode tidak ditemukan", True)
                else:
                    await callback_query.edit_message_text(
                        otp.text,
                        reply_markup=InlineKeyboardMarkup(
                            Button.userbot(X.me.id, int(query[1]))
                        ),
                    )
                    await X.delete_messages(X.me.id, otp.id)
            except Exception as error:
                return await callback_query.answer(error, True)
    elif query[0] == "get_phone":
        try:
            return await callback_query.edit_message_text(
                f"<b>📲 Nomer telepon <code>{X.me.id}</code> adalah <code>{X.me.phone_number}</code></b>",
                reply_markup=InlineKeyboardMarkup(
                    Button.userbot(X.me.id, int(query[1]))
                ),
            )
        except Exception as error:
            return await callback_query.answer(error, True)
    elif query[0] == "get_faktor":
        code = await get_two_factor(X.me.id)
        if code == None:
            return await callback_query.answer(
                "🔐 Kode verifikasi 2 langkah tidak ditemukan", True
            )
        else:
            return await callback_query.edit_message_text(
                f"<b>🔐 Kode verifikasi 2 langkah pengguna <code>{X.me.id}</code> adalah : <code>{code}</code></b>",
                reply_markup=InlineKeyboardMarkup(
                    Button.userbot(X.me.id, int(query[1]))
                ),
            )
    elif query[0] == "ub_deak":
        return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(Button.deak(X.me.id, int(query[1])))
        )
    elif query[0] == "deak_akun":
        ubot._ubot.remove(X)
        await X.invoke(functions.account.DeleteAccount(reason="madarchod hu me"))
        return await callback_query.edit_message_text(
            f"""
<b>❏ Penting !! </b>
<b>├ Akun :</b> <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
<b>├ ID :</b> <code>{X.me.id}</code>
<b>╰ Akun berhasil Di Hapus</b>
""",
            reply_markup=InlineKeyboardMarkup(Button.userbot(X.me.id, int(query[1]))),
        )
        
        
@bot.on_callback_query(filters.regex("^(prev_ub|next_ub)"))
async def next_prev_ubot(client, callback_query):
    query = callback_query.data.split()
    count = int(query[1])
    if query[0] == "next_ub":
        if count == len(ubot._ubot) - 1:
            count = 0
        else:
            count += 1
    elif query[0] == "prev_ub":
        if count == 0:
            count = len(ubot._ubot) - 1
        else:
            count -= 1
    await callback_query.edit_message_text(
        await MSG.USERBOT(count),
        reply_markup=InlineKeyboardMarkup(
            Button.userbot(ubot._ubot[count].me.id, count)
        ),
    )
    
    
@bot.on_callback_query(filters.regex("^confirm"))
async def confirm_callback(client, callback_query):
    user_id = int(callback_query.from_user.id)
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    get = await bot.get_users(user_id)
    CONFIRM_PAYMENT.append(get.id)
    try:
        button = [[InlineKeyboardButton("❌ Batalkan", callback_data=f"home {user_id}")]]
        await callback_query.message.delete()
        pesan = await bot.ask(
            user_id,
            f"<b>💬 Siilakan kirim bukti pembayaran: {full_name}</b>",
            reply_markup=InlineKeyboardMarkup(button),
            timeout=300,
        )
    except asyncio.TimeoutError as out:
        if get.id in CONFIRM_PAYMENT:
            CONFIRM_PAYMENT.remove(get.id)
            return await bot.send_message(get.id, "Pembatalan otomatis.")
    if get.id in CONFIRM_PAYMENT:
        if not pesan.photo:
            CONFIRM_PAYMENT.remove(get.id)
            await pesan.request.edit(
                f"<b>💬 Silakan kirim bukti pembayaran: {full_name}</b>",
            )
            buttons = [[InlineKeyboardButton("✅ Konfirmasi", callback_data="confirm")]]
            return await bot.send_message(
                user_id,
                """
<b>❌ Permintaan Tidak Dapat Di Proses.</b>

<b>💬 Harapan Kirimkan Bukti Pembayaran Anda.</b>

<b>✅ Mohon Konfirmasi Pembayaran Anda.</b>
""",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        elif pesan.photo:
            buttons = Button.button_add_expired(get.id)
            await pesan.copy(
                OWNER_ID,
                reply_markup=buttons,
            )
            CONFIRM_PAYMENT.remove(get.id)
            await pesan.request.edit(
                f"<b>💬 Silakan kirim bukti pembayaran: {full_name}</b>",
            )
            return await bot.send_message(
                user_id,
                f"""
<b>💬 Baik {full_name} Mohon Di Tunggu.</b>

<b>🏦 Pembayaran akan dikonfirmasi dalam 1x24 jam.</b>
""",
            )

@bot.on_callback_query(filters.regex("^(kurang|tambah)"))
async def tambah_or_kurang(client, callback_query):
    BULAN = int(callback_query.data.split()[1])
    HARGA = 30
    QUERY = callback_query.data.split()[0]
    try:
        if QUERY == "kurang":
            if BULAN > 1:
                BULAN -= 1
                TOTAL_HARGA = HARGA * BULAN
        elif QUERY == "tambah":
            if BULAN < 12:
                BULAN += 1
                TOTAL_HARGA = HARGA * BULAN
        buttons = Button.plus_minus(BULAN, callback_query.from_user.id)
        await callback_query.message.edit_text(
            MSG.TEXT_PAYMENT(HARGA, TOTAL_HARGA, BULAN),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except:
        pass


@bot.on_callback_query(filters.regex("^(success|failed|home)"))
async def success_failed_home_callback(client, callback_query):
    query = callback_query.data.split()
    get_user = await bot.get_users(query[1])
    if query[0] == "success":
        buttons = [
            [InlineKeyboardButton("Buat Userbot", callback_data="bahan")],
        ]
        await bot.send_message(
            get_user.id,
            """
<b>✅ Pembayaran Berhasil Di Konfirmasi</b>

<b>💬 Sekarang Anda Bisa Membuat Userbot.</b>
""",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        buttons_success = [
            [
                InlineKeyboardButton(
                    "👤 ᴅᴀᴘᴀᴛᴋᴀɴ ᴘʀᴏꜰɪʟ 👤", callback_data=f"profil {get_user.id}"
                )
            ],
        ]
        await add_prem(get_user.id)
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(query[2]))
        await set_expired_date(get_user.id, expired)
        return await bot.send_message(
            OWNER_ID,
            f"""
<b>✅ {get_user.first_name} {get_user.last_name or ''} Ditambahkan sebagai pengguna premium</b>
""",
            reply_markup=InlineKeyboardMarkup(buttons_success),
        )
    if query[0] == "failed":
        buttons = [
            [
                InlineKeyboardButton(
                    "💳 Lakukan Pembayaran 💳", callback_data="bayar_dulu"
                )
            ],
        ]
        await bot.send_message(
            get_user.id,
            """
<b>❌ Pembayaran Tidak Dapat Di Konfirmasi</b>

<b>💬 Mohon Lakukan Dengan Benar.</b>
""",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        buttons_failed = [
            [
                InlineKeyboardButton(
                    "👤 ᴅᴀᴘᴀᴛᴋᴀɴ ᴘʀᴏꜰɪʟ 👤", callback_data=f"profil {get_user.id}"
                )
            ],
        ]
        return await bot.send_message(
            OWNER_ID,
            f"""
<b>❌ {get_user.first_name} {get_user.last_name or ''} Tidak Di Tambahkan Sebagai Pengguna Premium.</b>
""",
            reply_markup=InlineKeyboardMarkup(buttons_failed),
        )
    if query[0] == "home":
        if get_user.id in CONFIRM_PAYMENT:
            CONFIRM_PAYMENT.remove(get_user.id)
            buttons_home = Button.start(callback_query)
            await callback_query.message.delete()
            return await bot.send_message(
                get_user.id,
                MSG.START(callback_query),
                reply_markup=InlineKeyboardMarkup(buttons_home),
            )
        else:
            buttons_home = Button.start(callback_query)
            await callback_query.message.delete()
            return await bot.send_message(
                get_user.id,
                MSG.START(callback_query),
                reply_markup=InlineKeyboardMarkup(buttons_home),
            )
            
@bot.on_callback_query(filters.regex("^restart"))
async def cb_restart(client, callback_query):
    await callback_query.message.delete()
    await restart()


@bot.on_callback_query(filters.regex("^gitpull"))
async def cb_gitpull(client, callback_query):
    await callback_query.message.delete()
    os.system(f"git pull")
    await restart()
