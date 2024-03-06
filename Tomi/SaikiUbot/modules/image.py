import asyncio
import io
import os

import cv2
import requests
from pyrogram import raw

from .. import *

__MODULE__ = "IMAGE"
__HELP__ = f"""
Perintah:
         <code>{PREFIX[0]}rbg</code> [reply to photo]
Penjelasan:
           Untuk menghapus Latar Belakang Gambar

Perintah:
         <code>{PREFIX[0]}blur</code> [reply to photo]
Penjelasan:
           Untuk memberika Efek Blur Ke Gambar

Perintah:
         <code>{PREFIX[0]}miror</code> [reply to photo]
Penjelasan:
           Untuk memberikan efek cermin ke gambar

Perintah:
         <code>{PREFIX[0]}negative</code> [reply to photo]
Penjelasan:
           Untuk memberikan efek negative ke gambar
"""


async def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": RMBG_API,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True,
    )


@PY.UBOT("rbg", PREFIX)
async def _(client, message):
    if RMBG_API is None:
        return
    if message.reply_to_message:
        reply_message = message.reply_to_message
        xx = await message.reply("<i>Memproses...</i>")
        try:
            if (
                isinstance(reply_message.media, raw.types.MessageMediaPhoto)
                or reply_message.media
            ):
                downloaded_file_name = await client.download_media(
                    reply_message, "./downloads/"
                )
                await xx.edit("<i>Menghapus latar belakang dari gambar ini...</i>")
                output_file_name = await ReTrieveFile(downloaded_file_name)
                os.remove(downloaded_file_name)
            else:
                await xx.edit("<i>Bagaimana cara menghapus latar belakang ini ?</i>")
        except Exception as e:
            await xx.edit(f"ERROR: {(str(e))}")
            return
        contentType = output_file_name.headers.get("content-type")
        if "image" in contentType:
            with io.BytesIO(output_file_name.content) as remove_bg_image:
                remove_bg_image.name = "rbg.png"
                await client.send_document(
                    message.chat.id,
                    document=remove_bg_image,
                    force_document=True,
                    reply_to_message_id=message.id,
                )
                await xx.delete()
        else:
            await xx.edit(
                "<b>Kesalahan (Kunci API tidak valid, saya kira ?)</b>\n<i>{}</i>".format(
                    output_file_name.content.decode("UTF-8")
                ),
            )
    else:
        return await message.reply("Silahkan Balas Ke Gambar")


@PY.UBOT("blur", PREFIX)
async def _(client, message):
    ureply = message.reply_to_message
    xd = await message.reply("<i>Memproses...</i>")
    if not ureply:
        return await xd.edit("Balas Ke Gambae")
    yinsxd = await client.download_media(ureply, "./downloads/")
    if yinsxd.endswith(".tgs"):
        cmd = ["lottie_convert.py", yinsxd, "yin.png"]
        file = "yin.png"
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    else:
        img = cv2.VideoCapture(yinsxd)
        heh, lol = img.read()
        cv2.imwrite("yin.png", lol)
        file = "yin.png"
    yin = cv2.imread(file)
    ayiinxd = cv2.GaussianBlur(yin, (35, 35), 0)
    cv2.imwrite("yin.jpg", ayiinxd)
    await client.send_photo(
        message.chat.id,
        "yin.jpg",
        reply_to_message_id=message.id,
    )
    await xd.delete()
    os.remove("yin.png")
    os.remove("yin.jpg")
    os.remove(yinsxd)


@PY.UBOT("negative", PREFIX)
async def _(client, message):
    ureply = message.reply_to_message
    ayiin = await message.reply("Memproses...")
    if not ureply:
        return await ayiin.edit("Balas Ke Gambar")
    ayiinxd = await client.download_media(ureply, "./downloads/")
    if ayiinxd.endswith(".tgs"):
        cmd = ["lottie_convert.py", ayiinxd, "yin.png"]
        file = "yin.png"
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    else:
        img = cv2.VideoCapture(ayiinxd)
        heh, lol = img.read()
        cv2.imwrite("yin.png", lol)
        file = "yin.png"
    yinsex = cv2.imread(file)
    kntlxd = cv2.bitwise_not(yinsex)
    cv2.imwrite("yin.jpg", kntlxd)
    await client.send_photo(
        message.chat.id,
        "yin.jpg",
        reply_to_message_id=message.id,
    )
    await ayiin.delete()
    os.remove("yin.png")
    os.remove("yin.jpg")
    os.remove(ayiinxd)


@PY.UBOT("miror", PREFIX)
async def _(client, message):
    ureply = message.reply_to_message
    kentu = await message.reply("<i>Memproses</i>")
    if not ureply:
        return await kentu.edit("Balas Ke Gambar")
    xnxx = await client.download_media(ureply, "./downloads/")
    if xnxx.endswith(".tgs"):
        cmd = ["lottie_convert.py", xnxx, "yin.png"]
        file = "yin.png"
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    else:
        img = cv2.VideoCapture(xnxx)
        kont, tol = img.read()
        cv2.imwrite("yin.png", tol)
        file = "yin.png"
    yin = cv2.imread(file)
    mmk = cv2.flip(yin, 1)
    ayiinxd = cv2.hconcat([yin, mmk])
    cv2.imwrite("yin.jpg", ayiinxd)
    await client.send_photo(
        message.chat.id,
        "yin.jpg",
        reply_to_message_id=message.id,
    )
    await kentu.delete()
    os.remove("yin.png")
    os.remove("yin.jpg")
    os.remove(xnxx)
