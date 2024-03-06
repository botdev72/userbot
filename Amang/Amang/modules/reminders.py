"""
CREDIT
KODE BY [AMANG] <https://t.me/amwang> <https://github.com/amanqs>

HAPUS CREDIT?, WAH KEBANGETAN SIH.
"""



from datetime import datetime, timedelta
from pyrogram import Client, filters
from pytimeparse import parse
from pytz import timezone

from Amang import *
from Amang.config import *

# Daftar pengingat yang tersimpan
reminders = []

@ubot.on_message(filters.me & filters.command("remind", cmd))
async def remind(client, message):
    if len(message.command) == 1 or len(message.command) == 2:
        await message.reply("Penggunaan: `remind <waktu> <pesan>`\n\nContoh:\n`{cmd[0]}remind 1j30m Beli susu`\n`{cmd[0]}remind 1h30m Cek email`", parse_mode=enums.ParseMode.MARKDOWN)
    else:
        time_from_now = message.command[1]
        text_to_remind = message.text[1+6+1 + len(time_from_now) + 1:]

        now = datetime.now(timezone("Asia/Jakarta"))
        delay = parse(time_from_now)
        t = now + timedelta(seconds=delay)

        # Menyimpan pengingat ke dalam daftar
        reminders.append((t, text_to_remind))

        await client.send_message(message.chat.id, text_to_remind, schedule_date=t)

        await message.reply(f"Pengingat disimpan, akan dikirim pada {t.strftime('%d/%m/%Y')} pukul {t.strftime('%H:%M:%S')}.")

@ubot.on_message(filters.me & filters.command("listremind", cmd))
async def list_reminders(client, message):
    if len(reminders) == 0:
        await message.reply("Tidak ada pengingat yang tersimpan.")
    else:
        response = "Daftar Pengingat:\n\n"
        for i, reminder in enumerate(reminders, start=1):
            t, text = reminder
            response += f"{i}. {text} - {t.strftime('%d/%m/%Y %H:%M:%S')}\n"
        await message.reply(response)


__MOD__ = "reminder"
__HELP__ = f"""
Modul ini memungkinkan pengguna untuk mengatur pengingat.

• Command: `{cmd[0]}remind`
• Function: Mengatur pengingat untuk waktu tertentu di masa depan.

Penggunaan: `{cmd[0]}remind <waktu> <pesan>`

Contoh:
`{cmd[0]}remind 1j30m Beli susu`
`{cmd[0]}remind 1h30m Cek email`

Catatan: Argumen waktu mendukung berbagai format seperti jam (j), menit (m), dan hari (h).

• Command: `{cmd[0]}listremind`
• Function: Menampilkan daftar pengingat yang tersimpan.

Penggunaan: `{cmd[0]}listremind`

Untuk mengatur pengingat, gunakan perintah `{cmd[0]}remind` diikuti oleh waktu dan pesan yang diinginkan. Argumen waktu harus disediakan dalam format yang disebutkan di atas. Pengingat akan dikirim pada waktu yang ditentukan dengan pesan yang diberikan.

Untuk melihat daftar pengingat yang tersimpan, gunakan perintah `{cmd[0]}daftarpengingat`.
"""