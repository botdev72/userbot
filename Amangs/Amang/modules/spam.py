import asyncio

from pyrogram import filters

from Amang import *
from Amang.config import *
from Amang.utils import eor

__MOD__ = "Spam"
__HELP__ = f"""
 Document for Spam

• Command: <code>{cmd[0]}spam</code> [number_messages - message_text]
• Function: Untuk spam pesan.

• Command: <code>{cmd[0]}spam</code> [reply_user - number_messages - message_text]
• Function: Untuk spam pesan ke user yang di reply.

• Command: <code>{cmd[0]}delayspam</code> [waktu] [jumlah] [balas pesan]
• Function: Untuk melakukan delay spam.
"""


"""
async def _(client, message):
    if message.reply_to_message:
        spam = await eor(message, "Processing...")
        reply_id = message.reply_to_message.id
        quantity = int(message.text.split(None, 2)[1])
        spam_text = message.text.split(None, 2)[2]
        await asyncio.sleep(1)
        await message.delete()
        await spam.delete()
        for i in range(quantity):
            await client.send_message(
                message.chat.id, spam_text, reply_to_message_id=reply_id
            )
            await asyncio.sleep(0.1)
    else:
        if len(message.text.split()) < 2:
            await eor(message, "Gunakan format:\n spam jumlah spam, text spam...")
        else:
            spam = await eor(message, "Processing...")
            quantity = int(message.text.split(None, 2)[1])
            spam_text = message.text.split(None, 2)[2]
            await asyncio.sleep(1)
            await message.delete()
            await spam.delete()
            for i in range(quantity):
                await client.send_message(message.chat.id, spam_text)
                await asyncio.sleep(0.1)


@ubot.on_message(filters.me & anjay("delayspam"))
async def delayspammer(client, message):
    try:
        args = message.text.split(" ", 3)
        delay = float(args[1])
        count = int(args[2])
        if message.reply_to_message:
            msg = await message.reply_to_message.text
        else:
            msg = str(args[3])
    except BaseException:
        return await message.edit(
            f"**Penggunaan :** {cmd[0]}dspam [waktu] [jumlah] [balas pesan]"
        )
    await message.delete()
    try:
        for i in range(count):
            await client.send_message(message.chat.id, msg)
            await asyncio.sleep(delay)
    except Exception as u:
        await client.send_message(message.chat.id, f"**Error :** `{u}`")
"""

@ubot.on_message(filters.me & anjay("spam"))
async def spam_cmd(client, message):
    reply = message.reply_to_message
    msg = await message.reply("processing...", quote=False)
    if reply:
        try:
            count_message = int(message.command[1])
            for i in range(count_message):
                await reply.copy(message.chat.id)
                await asyncio.sleep(0.1)
        except Exception as error:
            return await msg.edit(error)
    else:
        if len(message.command) < 2:
            return await msg.edit(
                "Gunakan format:\n {cmd[0]}spam jumlah spam, text spam."
            )
        else:
            try:
                count_message = int(message.command[1])
                for i in range(count_message):
                    await message.reply(message.text.split(None, 2)[2], quote=False)
                    await asyncio.sleep(0.1)
            except Exception as error:
                return await msg.edit(error)
    await msg.delete()
    await message.delete()


@ubot.on_message(filters.me & anjay("delayspam"))
async def dspam_cmd(client, message):
    reply = message.reply_to_message
    msg = await message.reply("processing...", quote=False)
    if reply:
        try:
            count_message = int(message.command[1])
            count_delay = int(message.command[2])
            for i in range(count_message):
                await reply.copy(message.chat.id)
                await asyncio.sleep(count_delay)
        except Exception as error:
            return await msg.edit(error)
    else:
        if len(message.command) < 4:
            return await msg.edit(
                "**Penggunaan :** {cmd[0]}delayspam [jumlah] [waktu] [pesan/reply"
            )
        else:
            try:
                count_message = int(message.command[1])
                count_delay = int(message.command[2])
                for i in range(count_message):
                    await message.reply(message.text.split(None, 3)[3], quote=False)
                    await asyncio.sleep(count_delay)
            except Exception as error:
                return await msg.edit(error)
    await msg.delete()
    await message.delete()