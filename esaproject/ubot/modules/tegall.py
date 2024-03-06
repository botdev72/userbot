
from . import bot, ubot, anjay, cobadah
from ubot.utils import eor

from asyncio import sleep

from . import *

tagallgcid = []

emoji = "😀 😃 😄 😁 😆 😅 😂 🤣 😭 😗 😙 😚 😘 🥰 😍 🤩 🥳 🤗 🙃 🙂 ☺️ 😊 😏 😌 😉 🤭 😶 😐 😑 😔 😋 😛 😝 😜 🤪 🤔 🤨 🧐 🙄 😒 😤 😠 🤬 ☹️ 🙁 😕 😟 🥺 😳 😬 🤐 🤫 😰 😨 😧 😦 😮 😯 😲 😱 🤯 😢 😥 😓 😞 😖 😣 😩 😫 🤤 🥱 😴 😪 🌛 🌜 🌚 🌝 🎲 🧩 ♟ 🎯 🎳 🎭💕 💞 💓 💗 💖 ❤️‍🔥 💔 🤎 🤍 🖤 ❤️ 🧡 💛 💚 💙 💜 💘 💝 🐵 🦁 🐯 🐱 🐶 🐺 🐻 🐨 🐼 🐹 🐭 🐰 🦊 🦝 🐮 🐷 🐽 🐗 🦓 🦄 🐴 🐸 🐲 🦎 🐉 🦖 🦕 🐢 🐊 🐍 🐁 🐀 🐇 🐈 🐩 🐕 🦮 🐕‍🦺 🐅 🐆 🐎 🐖 🐄 🐂 🐃 🐏 🐑 🐐 🦌 🦙 🦥 🦘 🐘 🦏 🦛 🦒 🐒 🦍 🦧 🐪 🐫 🐿️ 🦨 🦡 🦔 🦦 🦇 🐓 🐔 🐣 🐤 🐥 🐦 🦉 🦅 🦜 🕊️ 🦢 🦩 🦚 🦃 🦆 🐧 🦈 🐬 🐋 🐳 🐟 🐠 🐡 🦐 🦞 🦀 🦑 🐙 🦪 🦂 🕷️ 🦋 🐞 🐝 🦟 🦗 🐜 🐌 🐚 🕸️ 🐛 🐾 🌞 🤢 🤮 🤧 🤒 🍓 🍒 🍎 🍉 🍑 🍊 🥭 🍍 🍌 🌶 🍇 🥝 🍐 🍏 🍈 🍋 🍄 🥕 🍠 🧅 🌽 🥦 🥒 🥬 🥑 🥯 🥖 🥐 🍞 🥜 🌰 🥔 🧄 🍆 🧇 🥞 🥚 🧀 🥓 🥩 🍗 🍖 🥙 🌯 🌮 🍕 🍟 🥨 🥪 🌭 🍔 🧆 🥘 🍝 🥫 🥣 🥗 🍲 🍛 🍜 🍢 🥟 🍱 🍚 🥡 🍤 🍣 🦞 🦪 🍘 🍡 🥠 🥮 🍧 🍨".split(
    " "
)

__MODULE__ = "Mention"
__HELP__ = """
Bantuan Untuk Mention

• Perintah: <code>{0}all</code> [type message/reply message]
• Penjelasan: Untuk memention semua anggota grup dengan pesan yang anda inginkan.

• Perintah: <code>{0}stop</code>
• Penjelasan: Untuk membatalkan memention anggota grup.
"""



@ubot.on_message(anjay("all") & filters.me)
async def tagmentions(client, message):
    text = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if not text:
        await message.reply("<b>Give me text!</b>")
    else:     
        Spam = tagallgcid.append(message.chat.id)
        usrnum = 0
        usrtxt = ""
        async for usr in client.get_chat_members(message.chat.id):
            if not message.chat.id in tagallgcid:
                break
            usrnum += 1
            usrtxt += f"<a href=tg://user?id={usr.user.id}>{random.choice(emoji)}</a>"
            if usrnum == 5:
                if text:
                    txt = f"{usrtxt}\n\n{text}"
                    await client.send_message(message.chat.id, txt)
                await asyncio.sleep(1.5)
                usrnum = 0
                usrtxt = ""
        try:
            tagallgcid.remove(message.chat.id)
        except:
            pass