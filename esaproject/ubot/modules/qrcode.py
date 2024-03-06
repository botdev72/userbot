import asyncio
import os

from bs4 import BeautifulSoup
from pyrogram import filters

from . import bot, ubot, anjay, cobadah
from ubot.config import *
from ubot.utils import eor

DOWN_PATH = "ubot/resources/"


__MODULE__ = "QrCode"
__HELP__ = """
Bantuan Untuk QrCode

• Perintah: <code>{0}qrGen</code> [text QRcode]
• Penjelasan: Untuk merubah QRcode text menjadi gambar.

• Perintah: <code>{0}qrRead</code> [reply to media]
• Penjelasan: Untuk merubah QRcode menjadi text.
"""


@ubot.on_message(anjay("qrgen") & filters.me)
async def _(client, message):
    ID = message.reply_to_message or message
    if message.reply_to_message:
        texts = message.reply_to_message.text
    else:
        if len(message.command) < 2:
            return await message.delete()
        else:
            texts = message.text.split(None, 1)[1]
    Tm = await message.edit("Sedang Memproses Buat QRcode....")
    text = texts.replace(" ", "%20")
    QRcode = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={text}"
    await client.send_photo(message.chat.id, QRcode, reply_to_message_id=ID.id)
    await Tm.delete()


@ubot.on_message(anjay("qrread") & filters.me)
async def _(client, message):
    replied = message.reply_to_message
    if not (replied and replied.media and (replied.photo or replied.sticker)):
        TM = await message.edit("Balas kode qr untuk mendapatkan data...")
        return
    if not os.path.isdir(DOWN_PATH):
        os.makedirs(DOWN_PATH)
    AM = await message.edit("Mengunduh media...")
    down_load = await client.download_media(message=replied, file_name=DOWN_PATH)
    await AM.edit("Memproses Kode QR Anda...")
    cmd = [
        "curl",
        "-X",
        "POST",
        "-F",
        "f=@" + down_load + "",
        "https://zxing.org/w/decode",
    ]
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    out_response = stdout.decode().strip()
    err_response = stderr.decode().strip()
    os.remove(down_load)
    if not (out_response or err_response):
        await AM.edit("Tidak bisa mendapatkan data Kode QR ini...")
        return
    try:
        soup = BeautifulSoup(out_response, "html.parser")
        qr_contents = soup.find_all("pre")[0].text
    except IndexError:
        await TM.edit("Indeks Daftar Di Luar Jangkauan")
        return
    await AM.edit(f"<b>Data QRCode:</b>\n<code>{qr_contents}</code>")
