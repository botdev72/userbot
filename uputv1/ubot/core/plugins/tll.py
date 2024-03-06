from asyncio import sleep

from ubot import *

spam_chats = []

stopProcess = False


def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])
    

async def mentionall(client: Client, message: Message):
    await message.delete()
    chat_id = message.chat.id
    direp = message.reply_to_message.text
    args = get_arg(message)
    if not direp and not args:
        return await message.reply("`Berikan saya pesan atau balas ke pesan !`")

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
        usrtxt += f"**🦄 [{usr.user.first_name}](tg://user?id={usr.user.id})**\n"
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



async def batal_tag(client, message):
    if not message.chat.id in spam_chats:
        return await message.reply("`Sepertinya tidak ada tagall disini.`")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("`Tag All Diberhentikan.`")
