import asyncio
import os

import cv2

from ubot import *

__MODULE__ = "Image"
__HELP__ = """
 Bantuan Untuk Image

• Perintah : <code>{0}blur</code> [balas foto]
• Penjelasan : Untuk memberikan efek blur ke gambar.

• Perintah : <code>{0}mirror</code> [balas foto]
• Penjelasan : Untuk memberikan efek cermin ke gambar.

• Perintah : <code>{0}negative</code> [balas foto]
• Penjelasan : Untuk memberikan efek negative ke gambar.
"""


@KY.UBOT("blur", sudo=True)
async def blur_cmd(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    ureply = message.reply_to_message
    xd = await message.reply(f"{emo.proses} <b>Processing...</b>")
    await asyncio.sleep(2)
    if not ureply:
        return await xd.edit(f"{emo.gagal} **Silakan balas ke gambar.**")
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


@KY.UBOT("negative", sudo=True)
async def negative_cmd(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    ureply = message.reply_to_message
    ayiin = await message.reply(f"{emo.proses} **Processing...**")
    await asyncio.sleep(2)
    if not ureply:
        return await ayiin.edit(f"{emo.gagal} **Silakan balas ke gambar.**")
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


@KY.UBOT("mirror", sudo=True)
async def miror_cmd(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    ureply = message.reply_to_message
    kentu = await message.reply(f"{emo.proses} <b>Processing...</b>")
    await asyncio.sleep(2)
    if not ureply:
        return await kentu.edit(f"{emo.gagal} **Silakan balas ke gambar.**")
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
