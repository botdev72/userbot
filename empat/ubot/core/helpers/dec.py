import asyncio

from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ubot import OWNER_ID, bot, ubot


async def install_my_peer(client):
    users = []
    groups = []
    async for dialog in client.get_dialogs(limit=None):
        if dialog.chat.type == ChatType.PRIVATE:
            users.append(dialog.chat.id)
            await asyncio.sleep(5)
        elif dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
            groups.append(dialog.chat.id)
            await asyncio.sleep(5)
        client._get_my_peer[client.me.id] = {"pm": users, "gc": groups}


async def installPeer():
    tasks = [install_my_peer(client) for client in ubot._ubot]
    await asyncio.gather(*tasks, return_exceptions=True)
    await bot.send_message(OWNER_ID, "✅ Done Banh !!")


# asyncio.create_task(installPeer())


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
