import asyncio

from .. import *

__MODULE__ = "SPAM"
__HELP__ = f"""
Perintah:
         <code>{PREFIX[0]}spam</code> [jumlah_pesan - pesan_spam]
Penjelasan:
           Untuk spam pesan

Perintah:
         <code>{PREFIX[0]}dspam</code> [jumlah_pesan - jumlah_delay_detik - pesan_spam]
Penjelasan:
           Untuk spam pesan delay 
"""


@PY.UBOT(["spam", "dspam"], PREFIX)
async def _(client, message):
    if message.command[0] == "spam":
        if message.reply_to_message:
            spam = await message.reply("Diproses")
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
            if len(message.text.split()) < 3:
                await message.reply_text("⚡ Usage:\n spam jumlah spam, text spam")
            else:
                spam = await message.reply("Diproses")
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
        if len(message.text.split()) < 4:
            await message.reply_text(
                "⚡ Usage:\n dspam jumlah spam, jumlah delay detik, text spam"
            )
        else:
            spam = await message.reply("Diproses")
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
