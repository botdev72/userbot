import asyncio

from pyrogram import filters

from ubot import *

berenti = False

@ubot.on_message(anjay("dspam") & filters.me)
async def dspam_cmd(client, message):
    global berenti
    
    reply = message.reply_to_message
    msg = await message.reply("Processing...", quote=False)
    berenti = True
    if reply:
        try:
            count_message = int(message.command[1])
            count_delay = int(message.command[2])
        except Exception as error:
            return await msg.edit(str(error))
        for i in range(count_message):
            if not berenti:
              break
            try:
                await reply.copy(message.chat.id)
                await asyncio.sleep(count_delay)
            except:
                pass
    else:
        if len(message.command) < 4:
            return await msg.edit(
                f"Silakan ketik <code>{message.command}</code> untuk bantuan perintah."
            )
        else:
            try:
                count_message = int(message.command[1])
                count_delay = int(message.command[2])
            except Exception as error:
                return await msg.edit(str(error))
            for i in range(count_message):
                if not berenti:
                    break
                try:
                    
                    await message.reply(message.text.split(None, 3)[3], quote=False)
                    await asyncio.sleep(count_delay)
                except:
                    pass
                  
    berenti = False
    
    await msg.delete()
    await message.delete()


@ubot.on_message(anjay("spam") & filters.me)
async def spam_cmd(client, message):
    global berenti
    
    reply = message.reply_to_message
    msg = await message.reply("Processing...", quote=False)
    berenti = True
    
    if reply:
        try:
            count_message = int(message.command[1])
            for i in range(count_message):
                if not berenti:
                    break
                await reply.copy(message.chat.id)
                await asyncio.sleep(0.1)
        except Exception as error:
            return await msg.edit(str(error))
        #berenti = False
    else:
        if len(message.command) < 2:
            return await msg.edit(
                f"Silakan ketik <code>{message.command}</code> untuk bantuan perintah."
            )
        else:
            try:
                
                count_message = int(message.command[1])
                for i in range(count_message):
                    if not berenti:
                        break
                    await message.reply(message.text.split(None, 2)[2], quote=False)
                    await asyncio.sleep(0.1)
            except Exception as error:
                return await msg.edit(str(error))
    berenti = False

    await msg.delete()
    await message.delete()
    

@ubot.on_message(anjay("cspam") & filters.me)
async def capek_dah(client, message):
    global berenti
    
    if not berenti:
        return await message.reply("Sedang tidak ada perintah spam disini.")
    berenti = False
    await message.reply("Ok spam berhasil dihentikan.")
    
    

__MODULE__ = "Spam"
__HELP__ = """
Bantuan Untuk Spam

• Perintah: <code>{0}dspam</code> [jumlah] [waktu delay] [balas pesan]
• Penjelasan: Untuk melakukan delay spam.

• Perintah: <code>{0}spam</code> [jumlah] [kata]
• Penjelasan: Untuk melakukan spam.

• Perintah: <code>{0}cspam</code>
• Penjelasan: Untuk stop spam.
"""
