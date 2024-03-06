import asyncio

from pyrogram import filters

from ubot import *
from ubot.utils import *

@ubot.on_message(anjay("dspam") & filters.me)
@ubot.on_message(anjay("spam") & filters.me)
async def spam_PREFIX(client, message):
    if message.command[0] == "spam":
        if message.reply_to_message:
            spam = await message.reply("`Processing...`")
            try:
                quantity = int(message.text.split(None, 2)[1])
                spam_text = message.text.split(None, 2)[2]
            except Exception as error:
                return await spam.edit(error)
            await asyncio.sleep(1)
            await message.delete()
            await spam.delete()
            for i in range(quantity):
                await client.send_message(
                    message.chat.id,
                    spam_text,
                    reply_to_message_id=message.reply_to_message.id,
                )
                await asyncio.sleep(0.3)
        else:
            if len(message.command) < 3:
                await eor(
                    message, f"**Gunakan format:\n`{cobadah}spam [jumlah] [pesan]`**"
                )
            else:
                spam = await message.reply("`Processing...`")
                try:
                    quantity = int(message.text.split(None, 2)[1])
                    spam_text = message.text.split(None, 2)[2]
                except Exception as error:
                    return await spam.edit(error)
                await asyncio.sleep(1)
                await message.delete()
                await spam.delete()
                for i in range(quantity):
                    await client.send_message(message.chat.id, spam_text)
                    await asyncio.sleep(0.3)
    elif message.command[0] == "dspam":
        if message.reply_to_message:
            if len(message.command) < 3:
                return await eor(
                    message,
                    f"**Gunakan format:\n`{cobadah}dspam[jumlah] [waktu delay] [balas pesan]`**",
                )
            spam = await message.reply("`Processing...`")
            try:
                quantity = int(message.text.split(None, 3)[1])
                delay_msg = int(message.text.split(None, 3)[2])
            except Exception as error:
                return await spam.edit(error)
            await asyncio.sleep(1)
            await message.delete()
            await spam.delete()
            for i in range(quantity):
                await message.reply_to_message.copy(message.chat.id)
                await asyncio.sleep(delay_msg)
        else:
            if len(message.command) < 4:
                return await eor(
                    message,
                    f"**Gunakan format:\n`{cobadah}dspam[jumlah] [waktu delay] [balas pesan]`**",
                )
            else:
                spam = await message.reply("`Processing...`")
                try:
                    quantity = int(message.text.split(None, 3)[1])
                    delay_msg = int(message.text.split(None, 3)[2])
                    spam_text = message.text.split(None, 3)[3]
                except Exception as error:
                    return await spam.edit(error)
                await asyncio.sleep(1)
                await message.delete()
                await spam.delete()
                for i in range(quantity):
                    await client.send_message(message.chat.id, spam_text)
                    await asyncio.sleep(delay_msg)


@ubot.on_message(filters.me & anjay("bspam"))
async def bigspam(client, message):
    text = message.text
    if message.reply_to_message:
        if not len(text.split()) >= 2:
            return await message.reply(
                "`Gunakan dalam Format yang Tepat` **Contoh** : bspam [jumlah] [kata]"
            )
        spam_message = message.reply_to_message
    else:
        if not len(text.split()) >= 3:
            return await message.reply(
                "`Membalas Pesan atau Memberikan beberapa Teks ..`"
            )
        spam_message = text.split(maxsplit=2)[2]
    counter = text.split()[1]
    try:
        counter = int(counter)
    except BaseException:
        return await message.reply("`Gunakan dalam Format yang Tepat`")
    await asyncio.wait(
        [client.send_message(message.chat.id, spam_message) for i in range(counter)]
    )
    await message.delete()


__MODULE__ = "Spam"
__HELP__ = """
Bantuan Untuk Spam

• Perintah: <code>{0}dspam</code> [jumlah] [waktu delay] [balas pesan]
• Penjelasan: Untuk melakukan delay spam.

• Perintah: <code>{0}spam</code> [jumlah] [kata]
• Penjelasan: Untuk melakukan spam.

• Perintah: <code>{0}bspam</code> [jumlah] [kata]
• Penjelasan: Untuk melakukan bigspam.
"""
