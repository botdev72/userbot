import asyncio

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .. import *

CONFIRM_PAYMENT = []


@PY.CALLBACK("^confirm")
async def _(client, callback_query):
    user_id = int(callback_query.from_user.id)
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    get = await bot.get_users(user_id)
    CONFIRM_PAYMENT.append(get.id)
    try:
        button = [[InlineKeyboardButton("❌ BATALKAN", callback_data=f"home {user_id}")]]
        await callback_query.message.delete()
        pesan = await bot.ask(
            user_id,
            f"<b>💬 SILAHKAN KIRIMKAN SCREENSHOT BUKTI PEMBAYARAN ANDA: {full_name}</b>",
            reply_markup=InlineKeyboardMarkup(button),
            timeout=300,
        )
    except asyncio.TimeoutError as out:
        if get.id not in CONFIRM_PAYMENT:
            return
        else:
            CONFIRM_PAYMENT.remove(get.id)
            await pesan.request.delete()
            return await bot.send_message(user_id, "Pembatalan Otomatis")
    if get.id not in CONFIRM_PAYMENT:
        return
    else:
        if not pesan.photo:
            CONFIRM_PAYMENT.remove(get.id)
            await pesan.request.edit(
                f"<b>💬 SILAHKAN KIRIMKAN SCREENSHOT BUKTI PEMBAYARAN ANDA: {full_name}</b>",
            )
            buttons = [[InlineKeyboardButton("✅ KONFIRMASI", callback_data="confirm")]]
            return await bot.send_message(
                user_id,
                """
<b>❌ TIDAK DAPAT DIPROSES</b>

<b>💬 HARAP KIRIMKAN SCREENSHOT BUKTI PEMBAYARAN ANDA YANG VALID</b>

<b>✅ SILAHKAN KONFIRMASI ULANG PEMBAYARAN ANDA</b>
""",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        elif pesan.photo:
            buttons = [
                [
                    InlineKeyboardButton("✅ YES ", callback_data=f"success {user_id}"),
                    InlineKeyboardButton("NOT ❌", callback_data=f"failed {user_id}"),
                ],
                [
                    InlineKeyboardButton(
                        "👤 DAPATKAN PROFIL 👤", callback_data=f"profil {user_id}"
                    )
                ],
            ]
            await pesan.copy(
                OWNER_ID,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            CONFIRM_PAYMENT.remove(get.id)
            await pesan.request.edit(
                f"<b>💬 SILAHKAN KIRIMKAN SCREENSHOT BUKTI PEMBAYARAN ANDA: {full_name}</b>",
            )
            return await bot.send_message(
                user_id,
                f"""
<b>💬 BAIK {full_name} SILAHKAN DITUNGGU DAN JANGAN SPAM YA</b>

<b>🏦 PEMBAYARAN ANDA AKAN DIKONFIRMASI SETELAH 1-12 JAM KERJA</b>
""",
            )


@PY.CALLBACK("^(success|failed|home)")
async def _(client, callback_query):
    query = callback_query.data.split()
    get_user = await bot.get_users(query[1])
    await callback_query.message.delete()
    if query[0] == "success":
        buttons = [
            [InlineKeyboardButton("🔥 BUAT USERBOT 🔥", callback_data="add_ubot")],
        ]
        await bot.send_message(
            get_user.id,
            """
<b>✅ PEMBAYARAN ANDA BERHASIL DIKONFIRMASI</b>

<b>💬 SEKARANG ANDA BISA MEMBUAT USERBOT</b>
""",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        buttons_success = [
            [
                InlineKeyboardButton(
                    "👤 DAPATKAN PROFIL 👤", callback_data=f"profil {get_user.id}"
                )
            ],
        ]
        await add_prem(get_user.id)
        return await bot.send_message(
            OWNER_ID,
            f"""
<b>✅ {get_user.first_name} {get_user.last_name or ''} DITAMBAHKAN KE ANGGOTA PREMIUM</b>
""",
            reply_markup=InlineKeyboardMarkup(buttons_success),
        )
    if query[0] == "failed":
        buttons = [
            [InlineKeyboardButton("💳 LAKUKAN PEMBAYARAN 💳", callback_data="add_ubot")],
        ]
        await bot.send_message(
            get_user.id,
            """
<b>❌ PEMBAYARAN ANDA TIDAK BISA DIKONFIRMASI</b>

<b>💬 SILAHKAN LAKUKAN PEMBAYARAN DENGAN BENAR</b>
""",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        buttons_failed = [
            [
                InlineKeyboardButton(
                    "👤 DAPATKAN PROFIL 👤", callback_data=f"profil {get_user.id}"
                )
            ],
        ]
        return await bot.send_message(
            OWNER_ID,
            f"""
<b>❌ {get_user.first_name} {get_user.last_name or ''} TIDAK DITAMBAHKAN KE ANGGOTA PREMIUM</b>
""",
            reply_markup=InlineKeyboardMarkup(buttons_failed),
        )
    if query[0] == "home":
        if get_user.id in CONFIRM_PAYMENT:
            CONFIRM_PAYMENT.remove(get_user.id)
            buttons_home = Button.start()
            return await bot.send_message(
                get_user.id,
                f"""
<b>👋🏻 HALO <a href=tg://user?id={callback_query.from_user.id}>{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}</a>!

💬 @{bot.me.username} ADALAH BOT YANG DAPAT MEMBUAT USERBOT DENGAN MUDAH

👉🏻 KLIK TOMBOL DIBAWAH UNTUK MEMBUAT USERBOT 
""",
                reply_markup=InlineKeyboardMarkup(buttons_home),
            )
