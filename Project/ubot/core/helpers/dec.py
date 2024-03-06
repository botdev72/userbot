from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ubot import OWNER_ID, bot, ubot


async def load_user_allchats(client):
    pcnya = []
    gcnya = []
    async for dialog in client.get_dialogs(limit=None):
        try:
            if dialog.chat.type == ChatType.PRIVATE:
                pcnya.append(dialog.chat.id)
            elif dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
                gcnya.append(dialog.chat.id)
        except Exception as e:
            print(f"Error: {e}")

    return pcnya, gcnya


async def installing_user(client):
    pcnya, gcnya = await load_user_allchats(client)
    client_id = client.me.id
    client._get_my_peer[client_id] = {"pm": pcnya, "gc": gcnya}


async def installPeer():
    try:
        for client in ubot._ubot:
            await installing_user(client)
    except Exception:
        pass
    await bot.send_message(OWNER_ID, "✅ Sukses Install Data Pengguna.")


async def sending_user(user_id):
    await bot.send_message(
        user_id,
        "Silakan Buat Userbot Ulang Anda",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Buat Userbot",
                        callback_data="bahan",
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )
