"""
CREDIT
KODE BY [AMANG] <https://t.me/amwang> <https://github.com/amanqs>
HAPUS CREDIT?, WAH KEBANGETAN SIH.
"""


from datetime import datetime, timedelta

from pytimeparse import parse
from pytz import timezone

from ubot import KY

# Daftar pengingat yang tersimpan

reminders = []


@KY.UBOT("remind", sudo=True)
async def remind(client, message):
    if len(message.command) == 1 or len(message.command) == 2:
        await message.reply_text(
            f"Penggunaan: `remind <waktu> <pesan>`\n\nContoh:\n`{message.text} 1j30m Beli susu`\n`{message.text} 1h30m Cek email`",
        )
    else:
        time_from_now = message.command[1]
        text_to_remind = message.text.split(" ", 2)[2]
        now = datetime.now(timezone("Asia/Jakarta"))
        delay = parse(time_from_now)
        t = now + timedelta(seconds=delay)

        reminders.append((t, text_to_remind))
        await client.send_message(message.chat.id, text_to_remind, schedule_date=t)
        await message.reply_text(
            f"Pengingat disimpan, akan dikirim pada {t.strftime('%d/%m/%Y')} pukul {t.strftime('%H:%M:%S')}.",
        )


@KY.UBOT("listremind", sudo=True)
async def list_reminders(client, message):
    if len(reminders) == 0:
        await message.reply("Tidak ada pengingat yang tersimpan.")
    else:
        response = "Daftar Pengingat:\n\n"
        for i, reminder in enumerate(reminders, start=1):
            t, text = reminder
            response += f"{i}. {text} - {t.strftime('%d/%m/%Y %H:%M:%S')}\n"
        await message.reply(response)


__MODULE__ = "Reminders"
__HELP__ = """
Modul ini memungkinkan pengguna untuk mengatur pengingat.

• Perintah: `{0}remind`
• Penjelasan: Mengatur pengingat untuk waktu tertentu di masa depan.

Penggunaan: `{0}remind <waktu> <pesan>`
Contoh:
`{0}remind 1j30m Beli susu`

`{0}remind 1h30m Cek email`

Catatan: Argumen waktu mendukung berbagai format seperti jam (j), menit (m), dan hari (h).

• Perintah: `{0}listremind`
• Penjelasan: Menampilkan daftar pengingat yang tersimpan.

Penggunaan: `{0}listremind`
Untuk mengatur pengingat, gunakan perintah `{0}remind` diikuti oleh waktu dan pesan yang diinginkan. Argumen waktu harus disediakan dalam format yang disebutkan di atas. Pengingat akan dikirim pada waktu yang ditentukan dengan pesan yang diberikan.

Untuk melihat daftar pengingat yang tersimpan, gunakan perintah `{0}listremind`.
"""
