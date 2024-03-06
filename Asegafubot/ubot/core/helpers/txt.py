from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ubot import *
from ubot.utils.dbfunctions import *


class MSG:
    def EXPIRED_MSG_BOT(X):
        return f"""
<b>❏ Pemberitahuan</b>
<b>├ Akun :</b> <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
<b>├ ID:</b> <code>{X.me.id}</code>
<b>╰ Masa Aktif Habis</b>
"""

    def START(message):
        if not message.from_user.id == USER_ID:
            msg = f"""
<b>👋 Halo {message.from_user.first_name} !! Saya adalah bot yang dapat membuat userbot dengan mudah . Jika anda ingin melakukan pembuatan userbot silakan siapkan nomor akun telegram anda karena itu akan diperlukan nanti .

Atau anda bisa tonton tutorial yang sudah saya sediakan dibawah.</b>
"""
        else:
            msg = f"""
🧑‍💻 Developer <a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>

✅ Gunakan Dengan Bijak !!!
"""
        return msg

    def TEXT_PAYMENT(harga, total, bulan):
        return f"""
<b>Silakan Lakukan Pembayaran Terlebih Dahulu</b>

<b>Harga Perbulan: {harga}.000</b>

<b>💳 Metode Pembayaran:</b>
 <b>├──• Dana </b>
 <b>├─• <code>08XXXXXXXX</code></b>


<b>🔖 Total Harga: Rp. {total}.000</b>
<b>🗓️ Total Bulan: {bulan}</b> 

<b>✅ Klik Tombol Di Bawah Ini Untuk Mengirimkan Bukti Pembayaran</b>
"""

    async def USERBOT(count):
        expired_date = await get_expired_date(ubot._ubot[int(count)].me.id)
        return f"""
<b>❏ Userbot</b> <code>{int(count) + 1}/{len(ubot._ubot)}</code>
<b>├ Akun :</b> <a href=tg://user?id={ubot._ubot[int(count)].me.id}>{ubot._ubot[int(count)].me.first_name} {ubot._ubot[int(count)].me.last_name or ''}</a> 
<b>├ ID:</b> <code>{ubot._ubot[int(count)].me.id}</code>
<b>╰ Expires</b> <code>{expired_date.strftime('%d-%m-%Y')}</code>
"""

    def POLICY():
        return """
↪️ Kebijakan Pengembalian

Setelah melakukan pembayaran, jika Anda belum memperoleh/
menerima manfaat dari pembelian,
Anda dapat menggunakan hak penggantian dalam waktu 2 hari setelah pembelian. Namun, jika
Anda telah menggunakan/menerima salah satu manfaat dari
pembelian, termasuk akses ke fitur pembuatan userbot, maka
Anda tidak lagi berhak atas pengembalian dana.

🆘 Dukungan
Untuk mendapatkan dukungan, Anda dapat:
• Menghubungi admin dibawah ini
• Support @KynanSupport di Telegram
⚠️ JANGAN menghubungi Dukungan Telegram atau Dukungan Bot untuk meminta dukungan terkait pembayaran yang dilakukan di bot ini.
👉🏻 Tekan tombol Lanjutkan untuk menyatakan bahwa Anda telah
membaca dan menerima ketentuan ini dan melanjutkan
pembelian. Jika tidak, tekan tombol Batalkan
"""


async def sending_user(user_id):
    await bot.send_message(
        user_id,
        "Silakan Buat Userbot Ulang Anda",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Buat Userbot",
                        callback_data="bahan",
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )
