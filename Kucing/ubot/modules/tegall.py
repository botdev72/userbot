
from . import bot, ubot, anjay, cobadah
from ubot.utils import eor

from asyncio import sleep

from . import *

spam_chats = []

stopProcess = False

__MODULE__ = "Mention"
__HELP__ = """
Bantuan Untuk Mention

• Perintah: <code>{0}all</code> [type message/reply message]
• Penjelasan: Untuk memention semua anggota grup dengan pesan yang anda inginkan.

• Perintah: <code>{0}stop</code>
• Penjelasan: Untuk membatalkan memention anggota grup.
"""



@ubot.on_message(anjay("all") & filters.me)
async def mentionall(client: Client, message: Message):
    await message.delete()
    chat_id = message.chat.id
    direp = message.reply_to_message.text
    args = get_arg(message)
    if not direp and not args:
        return await message.edit("**Berikan saya pesan atau balas ke pesan!**")

    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        elif usr.user.is_bot == True:
            pass
        elif usr.user.is_deleted == True:
            pass
        usrnum += 1
        usrtxt += f"**👤 [{usr.user.first_name}](tg://user?id={usr.user.id})**\n"
        if usrnum == 5:
            if direp:
                txt = f"**{direp}**\n\n{usrtxt}\n"
                await client.send_message(chat_id, txt)
            await sleep(2)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@ubot.on_message(anjay("stop") & filters.me)
async def cancel_spam(client, message):
    if not message.chat.id in spam_chats:
        return await message.edit("**Sepertinya tidak ada tagall disini.**")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.edit("**Memberhentikan Mention.**")
