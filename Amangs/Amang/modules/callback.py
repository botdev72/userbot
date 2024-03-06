import asyncio
import datetime
import importlib
import sys
from datetime import datetime, timedelta
from os import environ, execle

from pyrogram import filters
from pyrogram.errors import *
from pyrogram.types import *
from pytz import timezone

from Amang import *
from Amang.config import *
from Amang.modules.add_ubot import *
from Amang.modules import *
from Amang.utils import *


SUPPORT = []

@bot.on_callback_query(filters.regex("^support_pmb"))
async def _(client, callback_query):
    user_id = int(callback_query.from_user.id)
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    get = await bot.get_users(user_id)
    await callback_query.message.delete()
    SUPPORT.append(get.id)
    try:
        button = [
            [InlineKeyboardButton("💵Ubah Metode Pembayaran", callback_data="lanjutkan_pembayaran_cb")],
            [InlineKeyboardButton("❌ Batalkan", callback_data=f"batal {user_id}")]
        ]
        pesan = await bot.ask(
            user_id,
            f"<b>Silahkan Kirimkan Bukti Pembayaran Anda dan user_id atau username akun telegram yang ingin dipasang userbot.</b>",
            reply_markup=InlineKeyboardMarkup(button),
            timeout=90,
        )
    except asyncio.TimeoutError as out:
        if get.id not in SUPPORT:
            return
        else:
            SUPPORT.remove(get.id)
            await pesan.delete()
            return await bot.send_message(user_id, "Pembatalan Otomatis")
    text = f"<b>Bukti Pembayaran Anda sudah terkirim {full_name} Silahkan tunggu admin untuk mengecheck pembayaran anda.</b>"
    buttons = [
        [
            InlineKeyboardButton("Pengirim Bukti Pembayaran", callback_data=f"profil {user_id}"),
            InlineKeyboardButton("Kirim Pesan ke pengirim", callback_data=f"jawab_pesan {user_id}"),
        ],
    ]
    if get.id not in SUPPORT:
        return
    else:
        try:
            await pesan.copy(
                SELLER_GROUP,
                OWNER,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            SUPPORT.remove(get.id)
            await bot.edit_message_text(
                user_id,
                pesan.id - 1,
                f"<b>Silahkan Kirimkan Bukti Pembayaran Anda dan user_id atau username akun telegram yang ingin dipasang userbot.</b>",
            )
            await callback_query.message.delete()
            return await bot.send_message(user_id, text)
        except Exception as error:
            return await bot.send_message(user_id, error)



total_bulan = 1  # Jumlah bulan awal
harga_prem_bulan = 25000  # Harga awal per bulan

@bot.on_callback_query(filters.regex("lanjutkan_cb"))
async def lanjutkan_cb(_, query: CallbackQuery):
    keyboard = [
        [
            InlineKeyboardButton("⚙️ Plan", callback_data="button_plan"),
        ],
        [
            InlineKeyboardButton("✔️ Premium", callback_data="lanjutkan_cb"),
            InlineKeyboardButton("Super Premium", callback_data="suprem_cb"),
        ],
        [
            InlineKeyboardButton("⏳ Bulan", callback_data="button_bulan"),
        ],
        [
            InlineKeyboardButton("- 1 Bulan", callback_data="kurangi_bulan"),
            InlineKeyboardButton("+ 1 Bulan", callback_data="tambah_bulan"),
        ],
        [
            InlineKeyboardButton("✅ Lanjutkan", callback_data="lanjutkan_pembayaran_cb"),
            InlineKeyboardButton("❌ Batalkan", callback_data="0_cls"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    total_harga = harga_prem_bulan * total_bulan
    diskon = 0
    if total_bulan > 2:
        diskon = total_harga * 0.08
        total_harga -= diskon

    diskon_teks = f"(-8%)" if total_bulan > 2 else ""

    await query.edit_message_text(
        f"""<b> **Amang Userbot**

🛒 Cart:

• Premium: {total_bulan} bulan {diskon_teks}

• Harga Userbot premium Perbulan: Rp.{harga_prem_bulan}

Total harga: Rp.{total_harga:,}""",
        reply_markup=reply_markup
    )


@bot.on_callback_query(filters.regex("button_plan"))
async def button_plan(_, query: CallbackQuery):
    global total_bulan

    await query.answer("Premium dan super premium")
    await lanjutkan_cb(_, query)


@bot.on_callback_query(filters.regex("button_bulan"))
async def button_bulan(_, query: CallbackQuery):
    global total_bulan

    await query.answer("Kadaluwarsa / Bulan.")
    await lanjutkan_cb(_, query)


@bot.on_callback_query(filters.regex("tambah_bulan"))
async def tambah_bulan_handler(_, query: CallbackQuery):
    global total_bulan

    if total_bulan < 12:
        total_bulan += 1

    await query.answer("Bulan ditambahkan satu.")
    await lanjutkan_cb(_, query)


@bot.on_callback_query(filters.regex("kurangi_bulan"))
async def kurangi_bulan_handler(_, query: CallbackQuery):
    global total_bulan

    if total_bulan > 1:
        total_bulan -= 1

    await query.answer("Bulan dikurangi satu.")
    await lanjutkan_cb(_, query)


harga_suprem_bulan = 30000  # Harga awal per bulan
total_pler = 1

@bot.on_callback_query(filters.regex("suprem_cb"))
async def suprem_cb(_, query: CallbackQuery):
    keyboard = [
        [
            InlineKeyboardButton("⚙️ Plan", callback_data="plan_pler"),
        ],
        [
            InlineKeyboardButton("Premium", callback_data="lanjutkan_cb"),
            InlineKeyboardButton("✔️ Super Premium ", callback_data="suprem_cb"),
        ],
        [
            InlineKeyboardButton("⏳ Bulan", callback_data="buton_pler"),
        ],
        [
            InlineKeyboardButton("- 1 Bulan", callback_data="kurangi_pler"),
            InlineKeyboardButton("+ 1 Bulan", callback_data="tambah_pler"),
        ],
        [
            InlineKeyboardButton("✅ Lanjutkan", callback_data="lanjutkan_pembayaran2_cb"),
            InlineKeyboardButton("❌ Batalkan", callback_data="0_cls"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    total_harga = harga_suprem_bulan * total_pler
    diskon = 0
    if total_pler > 2:
        diskon = total_harga * 0.08
        total_harga -= diskon

    pler_teks = f"(-8%)" if total_pler > 2 else ""

    await query.edit_message_text(
        f"""<b> **Amang Userbot**
        
🛒 Cart:

• Super Premium: {total_pler} bulan {pler_teks}

• Harga Userbot Super premium Perbulan: Rp.{harga_suprem_bulan}

Total harga: Rp.{total_harga:,}""",
        reply_markup=reply_markup
    )


@bot.on_callback_query(filters.regex("plan_pler"))
async def plan_pler(_, query: CallbackQuery):
    global total_pler

    await query.answer("Premium dan super premium!")
    await lanjutkan_cb(_, query)

@bot.on_callback_query(filters.regex("buton_pler"))
async def buton_pler(_, query: CallbackQuery):
    global total_pler

    await query.answer("Kadaluwarsa / Bulan!")
    await suprem_cb(_, query)


@bot.on_callback_query(filters.regex("tambah_pler"))
async def tambah_pler(_, query: CallbackQuery):
    global total_pler

    if total_pler < 12:
        total_pler += 1

    await query.answer("Ditambahkan satu Bulan.")
    await suprem_cb(_, query)


@bot.on_callback_query(filters.regex("kurangi_pler"))
async def kurangi_pler(_, query: CallbackQuery):
    global total_pler

    if total_pler > 1:
        total_pler -= 1

    await query.answer("Dikurangi satu Bulan.")
    await suprem_cb(_, query)



@bot.on_callback_query(filters.regex("lanjutkan_pembayaran_cb"))
async def lanjutkan_pembayaran_cb(_, query: CallbackQuery):
    keyboard = [
        [
            InlineKeyboardButton("DANA", callback_data="dana"),
            InlineKeyboardButton("QRIS", callback_data="qris"),
        ],
        [
            InlineKeyboardButton("🔙Kembali", callback_data="suprem_cb"),
            InlineKeyboardButton("❌Batalkan", callback_data="0_cls"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    total_harga = harga_prem_bulan * total_bulan

    await query.edit_message_text(
        f"<b>Metode Pembayaran:</b>\n\nPilih metode pembayaran yang ingin Anda gunakan.\n\n"
        f"Total harga: Rp{total_harga:,}",
        reply_markup=reply_markup
    )


@bot.on_callback_query(filters.regex("lanjutkan_pembayaran2_cb"))
async def lanjutkan_pembayaran2_cb(_, query: CallbackQuery):
    keyboard = [
        [
            InlineKeyboardButton("DANA", callback_data="dana2"),
            InlineKeyboardButton("QRIS", callback_data="qris2"),
        ],
        [
            InlineKeyboardButton("🔙Kembali", callback_data="suprem_cb"),
            InlineKeyboardButton("❌Batalkan", callback_data="0_cls"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    total_harga = harga_suprem_bulan * total_pler

    await query.edit_message_text(
        f"<b>Metode Pembayaran:</b>\n\nPilih metode pembayaran yang ingin Anda gunakan.\n\n"
        f"Total harga: Rp{total_harga:,}",
        reply_markup=reply_markup
    )
    

@bot.on_callback_query(filters.regex("dana2"))
async def dana2_handler(_, query: CallbackQuery):
    await query.answer("Anda telah memilih metode pembayaran DANA.")
    
    nomor_tujuan = "088226738841"
    atas_nama = "Que Sierra Mentari A"
    total_harga = harga_suprem_bulan * total_pler

    reply_markup = InlineKeyboardMarkup([
        [   
            InlineKeyboardButton("✅Konfirmasi Pembayaran", callback_data="support_pmb"),
        ],
        [
            InlineKeyboardButton("❌Batalkan", callback_data="0_cls"),
        ],
    ])

    await query.message.edit_text(
        f"Untuk mengirim pembayaran melalui DANA gunakan nomor tujuan berikut:\n\n"
        f"Nomor: {nomor_tujuan}\n"
        f"A/N: {atas_nama}\n\n"
        f"Setelah Anda melakukan pembayaran, tekan tombol di bawah ini untuk mengonfirmasinya.\n\n"
        f"Total harga: Rp{total_harga:,}",
        reply_markup=reply_markup
    )


@bot.on_callback_query(filters.regex("qris2"))
async def qris2_handler(_, query: CallbackQuery):
    await query.answer("Anda telah memilih metode pembayaran QRIS.")
    
    qr_code_url = "https://te.legra.ph/file/20897710ec3f3594d354d.jpg"
    atas_nama = "Amang Store"
    total_harga = harga_suprem_bulan * total_pler

    reply_markup = InlineKeyboardMarkup([
        [   
            InlineKeyboardButton("✅Konfirmasi Pembayaran", callback_data="support_pmb"),
        ],
        [
            InlineKeyboardButton("❌Batalkan", callback_data="0_cls"),
        ],
    ])

    await query.message.edit_text(
        f"Untuk mengirim pembayaran melalui QRIS gunakan kode QR berikut:\n\n"
        f"[QR Code]({qr_code_url}) A/N {atas_nama}\n\n"
        f"Setelah Anda melakukan pembayaran, tekan tombol di bawah ini untuk mengonfirmasinya.\n\n"
        f"Total harga: Rp{total_harga:,}",
        reply_markup=reply_markup
    )


@bot.on_callback_query(filters.regex("dana"))
async def dana_handler(_, query: CallbackQuery):
    await query.answer("Anda telah memilih metode pembayaran DANA.")
    
    nomor_tujuan = "088226738841"
    atas_nama = "Que Sierra Mentari A"
    total_harga = harga_prem_bulan * total_bulan

    reply_markup = InlineKeyboardMarkup([
        [   
            InlineKeyboardButton("✅Konfirmasi Pembayaran", callback_data="support_pmb"),
        ],
        [
            InlineKeyboardButton("❌Batalkan", callback_data="0_cls"),
        ],
    ])

    await query.message.edit_text(
        f"Untuk mengirim pembayaran melalui DANA gunakan nomor tujuan berikut:\n\n"
        f"Nomor: {nomor_tujuan}\n"
        f"A/N: {atas_nama}\n\n"
        f"Setelah Anda melakukan pembayaran, tekan tombol di bawah ini untuk mengonfirmasinya.\n\n"
        f"Total harga: Rp{total_harga:,}",
        reply_markup=reply_markup
    )


@bot.on_callback_query(filters.regex("qris"))
async def qris_handler(_, query: CallbackQuery):
    await query.answer("Anda telah memilih metode pembayaran QRIS.")
    
    qr_code_url = "https://te.legra.ph/file/20897710ec3f3594d354d.jpg"
    atas_nama = "Amang Store"
    total_harga = harga_prem_bulan * total_bulan

    reply_markup = InlineKeyboardMarkup([
        [   
            InlineKeyboardButton("✅Konfirmasi Pembayaran", callback_data="support_pmb"),
        ],
        [
            InlineKeyboardButton("❌Batalkan", callback_data="0_cls"),
        ],
    ])

    await query.message.edit_text(
        f"Untuk mengirim pembayaran melalui QRIS gunakan kode QR berikut:\n\n"
        f"[QR Code]({qr_code_url}) A/N {atas_nama}\n\n"
        f"Setelah Anda melakukan pembayaran, tekan tombol di bawah ini untuk mengonfirmasinya.\n\n"
        f"Total harga: Rp{total_harga:,}",
        reply_markup=reply_markup
    )


@bot.on_callback_query(filters.regex("konfirmasi_pembayaran_2"))
async def konfirmasi_pembayaran2_handler(_, query: CallbackQuery):
    keyboard = [
        [
            InlineKeyboardButton("💵Ubah Metode Pembayaran", callback_data="lanjutkan_pembayaran_cb"),
        ],
        [
            InlineKeyboardButton("❌Batalkan", callback_data="0_cls"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.answer("Silakan kirim ID atau tangkapan layar dari transaksi yang Anda lakukan.")
    await query.message.edit_text(
        "📸 Silakan kirim ID atau tangkapan layar dari transaksi yang Anda lakukan.",
        reply_markup=reply_markup
    )



@bot.on_callback_query(filters.regex("start_pmb"))
async def start_admin(_, query: CallbackQuery):
    return await query.edit_message_text(
        f"""<b>» 🤖 Amang Userbot 🤖 «</b>

↪️ Kebijakan Pengembalian

Setelah melakukan pembayaran, jika Anda belum memperoleh/
menerima manfaat dari pembelian, 
Anda dapat menggunakan hak penggantian dalam waktu 2 hari setelah pembelian. Namun, jika 
Anda telah menggunakan/menerima salah satu manfaat dari 
pembelian, termasuk akses ke fitur pembuatan userbot, maka 
Anda tidak lagi berhak atas pengembalian dana.

❓ Tutorial 
Jika anda tidak mengerti cara pembuatanya bisa dilihat 👉 Video Tutorial (https://t.me/amangproject/18)

🆘 Dukungan
Untuk mendapatkan dukungan, Anda dapat:
• Hubungi @amwang
• Menghubungi admin dibawah ini
• Bertanya ke grup support @amwangsupport di Telegram

⚠️ JANGAN menghubungi Dukungan Telegram atau Dukungan Bot untuk meminta dukungan terkait pembayaran yang dilakukan di bot ini.

👉🏻 Tekan tombol Lanjutkan untuk menyatakan bahwa Anda telah 
membaca dan menerima ketentuan ini dan melanjutkan 
pembelian. Jika tidak, tekan tombol Batalkan.
    """,
        reply_markup=InlineKeyboardMarkup(
            [
                [   
                    InlineKeyboardButton(text="➡️ Lanjutkan", callback_data="lanjutkan_cb"),
                ],
                [
                    InlineKeyboardButton(text="👮‍♂ Admin", callback_data="start_admin"),
                    InlineKeyboardButton(text="❌ Batalkan", callback_data="start0"),
                ],
             ]
        ),
        disable_web_page_preview=True
    )


@bot.on_callback_query(filters.regex("start_admin"))
async def start_admin(_, query: CallbackQuery):
    return await query.edit_message_text(
        f"""
    <b>Silakan hubungi Admin dibawah ini,
    Untuk meminta akses membuat userbot.</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="👮‍♂ Amang", user_id=2073506739),
                    InlineKeyboardButton(text="👮‍♂ Nanda", url=f"t.me/ndaaaad"),
                ],
                [
                    InlineKeyboardButton(text="👮‍♂ Rahma", url=f"t.me/xxrahma24"),  
                ],
                [
                    InlineKeyboardButton(text="Kembali", callback_data="start0"),
                    InlineKeyboardButton(text="Tutup", callback_data="0_cls"),
                ],
            ]
        ),
    )
