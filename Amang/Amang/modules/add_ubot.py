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
from Amang.core.functions.plugins import ajg
from Amang.modules import loadModule
from Amang.utils import *


def DATETIMEBOT():
    mydate = datetime.now(timezone("Asia/Jakarta"))
    da = mydate.strftime("🗓️ Tanggal: %d/%m/%Y")
    dt = mydate.strftime("🕕 Jam: %H:%M")
    f_d = f"{da}\n{dt}"
    return f_d


@bot.on_message(filters.command(["tambah"]))
async def clone(bot: bot, msg: Message):
    chat = msg.chat
    text = await msg.reply("Usage:\n\n /tambah session")
    cmd = msg.command
    session = msg.command[1]
    try:
        await text.edit("Booting Your Client")
                   # change this Directry according to ur repo
        ubot = Ubot(name="bot", api_id=API_ID, api_hash=API_HASH, session_string=session, plugins=dict(root="Amang/modules"))
        await bot.start()
        user = await bot.get_me()
        await msg.reply(f"Your Client Has Been Successfully As {user.first_name} ✅.")
    except Exception as e:
        await msg.reply(f"**ERROR:** `{str(e)}`\nPress /start to Start again.")

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
            [InlineKeyboardButton("❌ BATALKAN", callback_data=f"batal {user_id}")]
        ]
        pesan = await bot.ask(
            user_id,
            f"<b>✍️ Silahkan Kirimkan Bukti Pembayaran Anda: {full_name}</b>",
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
    text = f"<b>💬 Bukti Pembayaran Anda sudah terkirim: {full_name} Silahkan tunggu admin untuk mengecheck pembayaran anda.</b>"
    buttons = [
        [
            InlineKeyboardButton("👤 Profil", callback_data=f"profil {user_id}"),
            InlineKeyboardButton("Jawab 💬", callback_data=f"jawab_pesan {user_id}"),
        ],
    ]
    if get.id not in SUPPORT:
        return
    else:
        try:
            await pesan.copy(
                LOGS,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            SUPPORT.remove(get.id)
            await bot.edit_message_text(
                user_id,
                pesan.id - 1,
                f"<b>✍️ Silahkan Kirimkan Bukti Pembayaran Anda {full_name}</b>",
            )
            await callback_query.message.delete()
            return await bot.send_message(user_id, text)
        except Exception as error:
            return await bot.send_message(user_id, error)



total_bulan = 1  # Jumlah bulan awal
harga_per_bulan = 25000  # Harga awal per bulan

@bot.on_callback_query(filters.regex("lanjutkan_cb"))
async def lanjutkan_cb(_, query: CallbackQuery):
    keyboard = [
        [   InlineKeyboardButton("⏳Bulan", callback_data="button_bulan"),
        ],
        [
            InlineKeyboardButton("- 1 Bulan", callback_data="kurangi_bulan"),
            InlineKeyboardButton("+ 1 Bulan", callback_data="tambah_bulan"),
        ],
        [   InlineKeyboardButton("✅Lanjutkan", callback_data="lanjutkan_pembayaran_cb"),
            InlineKeyboardButton("❌Batalkan", callback_data="0_cls"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    total_harga = harga_per_bulan * total_bulan

    await query.edit_message_text(
        f"""<b> **Amang Userbot**

•  Premium : {total_bulan} bulan

• Harga Userbot Perbulan : Rp.{harga_per_bulan}


Total harga: Rp.{total_harga:,}""",
        reply_markup=reply_markup
    )

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


@bot.on_callback_query(filters.regex("lanjutkan_pembayaran_cb"))
async def lanjutkan_pembayaran_cb(_, query: CallbackQuery):
    keyboard = [
        [
            InlineKeyboardButton("DANA", callback_data="dana"),
            InlineKeyboardButton("QRIS", callback_data="qris"),
        ],
        [
            InlineKeyboardButton("🔙Kembali", callback_data="lanjutkan_cb"),
            InlineKeyboardButton("❌Batalkan", callback_data="0_cls"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    total_harga = harga_per_bulan * total_bulan

    await query.edit_message_text(
        f"<b>Metode Pembayaran:</b>\n\nPilih metode pembayaran yang ingin Anda gunakan.\n\n"
        f"Total harga: Rp{total_harga:,}",
        reply_markup=reply_markup
    )


@bot.on_callback_query(filters.regex("dana"))
async def dana_handler(_, query: CallbackQuery):
    await query.answer("Anda telah memilih metode pembayaran DANA.")
    
    nomor_tujuan = "088226738841"
    atas_nama = "Que Sierra Mentari A"
    total_harga = harga_per_bulan * total_bulan

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
    total_harga = harga_per_bulan * total_bulan

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
Jika anda tidak mengerti cara pembuatanya bisa dilihat 👉 comingsoon...

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


@bot.on_callback_query(filters.regex("buat_bot"))
async def _(_, callback_query):
    user_id = callback_query.from_user.id
    PREM_ID = await get_prem()
    ID_SELES = await get_seles()
    if not bot.me.id == OWNER:
        MAX_UBOT = 23
    else:
        MAX_UBOT = 23
    if len(ubot._ubot) == MAX_UBOT:
        buttons = [
            [InlineKeyboardButton(text="👮‍♂ Admin", callback_data="start_admin")],
            [InlineKeyboardButton("Tutup", callback_data="0_cls")],
        ]
        await callback_query.message.delete()
        return await bot.send_message(
            user_id,
            f"""
<b>Peringatan ⚠️ </b>

<b>AmangPyrobot Sudah Full User</b>
<b>Silahkan membuat userbot di @amwang2_bot </b>

""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if user_id not in PREM_ID:
        buttons = [
            [   InlineKeyboardButton(text="💰 Beli Userbot", callback_data="start_pmb"),
                InlineKeyboardButton(text="👮🏻‍♀️ Daftar Admin", callback_data="start_admin"),
            ],
            [
               InlineKeyboardButton(text="❌ Tutup", callback_data="0_cls")
            ],
        ]
        await callback_query.message.delete()
        return await bot.send_message(
            user_id,
            f"""
<b>🤖 Buat userbot</b>\n\n<b>Untuk mengakses fitur premium ini, Anda perlu melakukan pembelian.</b>\n<b>Beli sekarang untuk bisa membuat userbot premium!</b>
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    try:
        await callback_query.message.delete()
        phone = await bot.ask(
            user_id,
            (
                "<b>Silahkan Masukkan Nomor Telepon Telegram Anda Dengan Format Kode Negara.\nContoh: +628xnxx</b>\n"
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
        in_memory=False,
    )
    get_otp = await bot.send_message(user_id, "<b>Sedang Mengirim Kode OTP di Akun Telegram Anda.</b>")
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
        importlib.reload(importlib.import_module(f"Amang.modules.{mod}"))
    mydate = datetime.now(timezone("Asia/Jakarta")) + timedelta(days=30)
    get_date = mydate.strftime("%d-%m-%Y")
    text_done = f"<b>Terima kasih telah berlangganan {bot.me.mention}\nAkun: <a href=tg://openmessage?user_id={new_client.me.id}-{new_client.me.first_name} {new_client.me.last_name or ''}</a> > <code>{new_client.me.id}</code></b>\n<b>📅 Expired on :</b><code>{get_date}</code>"
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
    await bot.send_message(
        LOGS,
        text_done,
        disable_web_page_preview=True,
    )
    buttons = [
        [
            InlineKeyboardButton(
                "🧑‍💻 Pembuat Userbot 🧑‍💻",
                url=f"tg://openmessage?user_id={callback_query.from_user.id}",
            )
        ],
    ]
    await bot.send_message(
        LOGS,
        f"{text_done}\n<b>{date}</b>",
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True,
    )
    try:
        await new_client.join_chat("amangproject")
        await new_client.join_chat("amwangs")
        await new_client.join_chat("amwangsupport")
    except UserAlreadyParticipant:
        pass
    if callback_query.from_user.id in ID_SELES:
        return
    else:
        await remove_prem(callback_query.from_user.id)


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
            "❌ Anda tidak bisa menggunakan perintah ini\n\n✅ hanya pengguna yang memiliki akses bisa menggunakan perintah ini"
        )
    count = 0
    user = ""
    for X in ubot._ubot:
        try:
            count += 1
            user += f"""
❏ USERBOT KE {count}
 ├ AKUN: <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a> 
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


@bot.on_message(filters.command("getubot"))
async def _(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    seles = await get_seles()
    if user_id not in DEVS and user_id not in seles:
        return await message.reply(
            "❌ Anda tidak bisa menggunakan perintah ini\n\n✅ hanya pengguna yang memiliki akses bisa menggunakan perintah ini"
        )
    count = 0
    for ub in ubot._ubot:
        count += 1
        get_exp = await get_expired_date(ub.me.id)
        exp = get_exp.strftime("%d-%m-%Y") if get_exp is not None else "Tidak diketahui"
        list_ubot = f"""
<b>❏ USERBOT KE {count}</b>
<b> ├ AKUN:</b> <a href=tg://openmessage?user_id={ub.me.id}>{ub.me.first_name} {ub.me.last_name or ''}</a> 
<b> ├ EXPIRED: {exp}</b>
<b> ╰ ID: </b> <code>{ub.me.id}</code>
"""
        await bot.send_message(
            chat_id,
            list_ubot,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "👤 Info", callback_data=f"profil {ub.me.id}"
                        ),
                    ],
                ]
            ),
        )
        await asyncio.sleep(1.5)


@ubot.on_message(filters.command("delubot", cmd) & filters.me)
async def _(client, message):
    user_id = message.from_user.id
    if user_id not in DEVS:
        await eor(message, "<b> Tidak punya akses</b>.")
        return
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        text = message.text.split()
        if len(text) < 2:
            await eor(
                message,
                "<code>Maaf, format yang Anda berikan salah. Mohon balas ke pengguna atau berikan username/user ID.</code>",
            )
            return
        username = text[1]
        try:
            user = await client.get_users(username)
        except ValueError:
            user = None
        if user is None:
            await eor(
                message, f"<code>Maaf, pengguna {username} tidak ditemukan.</code>"
            )
            return
        user_id = user.id

    await remove_ubot(user_id)
    await eor(message, f"<b> ✅ Done.</b>")


@bot.on_message(filters.command("delubot"))
async def _(client, message):
    user_id = message.from_user.id
    if user_id not in DEVS:
        return
    if len(message.command) < 2:
        return await message.reply("Ketik /delubot user_id Untuk Mematikan Userbot")
    else:
        for X in ubot._ubot:
            try:
                user = await bot.get_users(message.text.split()[1])
                await remove_ubot(user.id)
                await message.reply(
                    f"<b> ✅ {user.mention} Berhasil Dihapus Dari Database</b>"
                )
                return await bot.send_message(
                    user.id, "<b>MASA AKTIF ANDA TELAH BERAKHIR"
                )
            except Exception as e:
                return await message.reply(f"<b>❌ {e} </b>")


@bot.on_message(filters.command(["restart"]))
async def restart(_, message):
    user_id = message.from_user.id
    my_id = []
    for _ubot_ in ubot._ubot:
        my_id.append(_ubot_.me.id)
    if user_id not in my_id:
        return await message.reply(
            "<b>❌ Anda tidak bisa menggunakan perintah ini\n\n✅ Anda jelek, belom mandi, dekil bau, jijik gue sama lo, dan anda bukanlah pengguna @amanguserbot.</b>"
        )
    buttons = [
        [
            InlineKeyboardButton(text="✅ Restart", callback_data=f"ress {user_id}"),
        ],
        [
            InlineKeyboardButton("❌ Batalkan", callback_data="0_cls"),
        ],
    ]
    await bot.send_message(
        message.chat.id,
        f"<b>Restart Ubot?</b>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def reboot():
    for _ubot in await get_userbots():
        ubot_ = Ubot(**_ubot)
        try:
            if ubot_.is_connected:
                await ubot_.stop()
                await ubot_.start()
            else:
                await ubot_.start()
        except Exception as e:
            print(f"{e}")


async def restart_all():
    asyncio.get_event_loop().create_task(reboot())


async def restart_bot(ubot_):
    for _ubot in await get_userbots():
        ubot_ = Ubot(**_ubot)
    try:
        if ubot_.is_connected:
            await ubot_.disconnect()
        else:
            ubot_.in_memory = False
            await ubot_.start()
            for mod in loadModule():
                importlib.reload(importlib.import_module(f"Amang.modules.{mod}"))
            await ajg()
            print("BOT SERVER RESTARTED !!")
    except Exception as e:
        print(f"{e}")


@bot.on_callback_query(filters.regex("ress"))
async def is_restart(_, callback_query):
    for _ubot in await get_userbots():
        if int(_ubot["name"]) == int(callback_query.data.split()[1]):
            ubot_ = Ubot(**_ubot)
            try:
                await callback_query.edit_message_text("<b>Processing...</b>")
                await restart_bot(ubot_)
                await asyncio.sleep(2)
                await callback_query.edit_message_text(
                    "✅ <b>UserBot was restarted!</b>"
                )
            except Exception as err:
                await callback_query.edit_message_text(f"{err}")


@bot.on_message(filters.command(["control"]))
async def restart(_, message):
    user_id = message.from_user.id
    if user_id not in DEVS:
        return await message.reply("<b>❌ Only Amang can use this command</b>")
    buttons = [
        [
            InlineKeyboardButton(text="✅", callback_data="restart_semua"),
            InlineKeyboardButton("❌", callback_data="0_cls"),
        ],
    ]
    await bot.send_message(
        message.chat.id,
        f"<b>Restart Server</b>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@bot.on_callback_query(filters.regex("restart_semua"))
async def is_restart(_, callback_query):
    try:
        await callback_query.edit_message_text("<b>Processing...</b>")
        LOGGER(__name__).info("BOT SERVER RESTARTED !!")
    except BaseException as err:
        LOGGER(__name__).info(f"{err}")
        return
    await asyncio.sleep(2)
    await callback_query.edit_message_text("✅ <b>AmangUbot Berhasil Di Restart.</b>")
    args = [sys.executable, "-m", "Amang"]
    execle(sys.executable, *args, environ)


async def is_cancel(callback_query, text):
    if text.startswith("/cancel"):
        user_id = callback_query.from_user.id
        await bot.send_message(user_id, "<b>Membatalkan Proses Pembuatan Userbot!</b>")
        return True
    return False
