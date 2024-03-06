from pyrogram.errors import MessageNotModified
from pyrogram.types import (InlineKeyboardButton, InlineQueryResultArticle,
                            InputTextMessageContent)

from SaikiUbot import bot, get_my_id


class Button:
    def admin():
        menu_button = [
            [
                InlineKeyboardButton("GLOBAL", callback_data="menu_help admin_gban"),
                InlineKeyboardButton(
                    "RESTRICT", callback_data="menu_help admin_restrict"
                ),
            ],
            [InlineKeyboardButton("• KEMBALI •", callback_data="help_back")],
        ]
        back_button = [
            [InlineKeyboardButton("• KEMBALI •", callback_data="menu_help admin_back")]
        ]
        return [menu_button, back_button]

    def alive(get_id):
        button_owner = [
            [
                InlineKeyboardButton(
                    text="🗑️ close",
                    callback_data=f"alv_cls {int(get_id[1])} {int(get_id[2])}",
                ),
                InlineKeyboardButton(text="stats 📊", callback_data="stats"),
            ],
        ]
        button_ubot = [
            [
                InlineKeyboardButton(
                    text="🗑️ close",
                    callback_data=f"alv_cls {int(get_id[1])} {int(get_id[2])}",
                )
            ]
        ]
        return [button_owner, button_ubot]

    def download(message, query):
        button = [
            [
                InlineKeyboardButton(
                    text="🔈 Audio ",
                    callback_data=f"ytdl_{query}_Audio {message.from_user.id}",
                ),
                InlineKeyboardButton(
                    text="Video 🎥",
                    callback_data=f"ytdl_{query}_Video {message.from_user.id}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🗑 Tutup 🗑",
                    callback_data=f"1_cls {message.id} {message.from_user.id}",
                ),
            ],
        ]
        return button

    def sticker():
        menu_button = [
            [
                InlineKeyboardButton("KANG", callback_data="menu_help sticker_kang"),
                InlineKeyboardButton(
                    "MEMIFY", callback_data="menu_help sticker_memify"
                ),
            ],
            [
                InlineKeyboardButton("MAMES", callback_data="menu_help sticker_memes"),
                InlineKeyboardButton(
                    "QUOTLY", callback_data="menu_help sticker_quotly"
                ),
            ],
            [
                InlineKeyboardButton("TINY", callback_data="menu_help sticker_tiny"),
            ],
            [InlineKeyboardButton("• KEMBALI •", callback_data="help_back")],
        ]
        back_button = [
            [
                InlineKeyboardButton(
                    "• KEMBALI •", callback_data="menu_help sticker_back"
                )
            ]
        ]
        return [menu_button, back_button]

    def start():
        button = [
            [InlineKeyboardButton("🔥 BUAT USERBOT 🔥", callback_data="add_ubot")],
            [
                InlineKeyboardButton("💬 BANTUAN", callback_data="help_back"),
                InlineKeyboardButton("SUPPORT 💬", callback_data="support"),
            ],
        ]
        return button

    def translate():
        button = [
            [
                InlineKeyboardButton(
                    "• LANG_CODE •", url="https://graph.org/LANG-CODE-11-26"
                )
            ],
            [
                InlineKeyboardButton("• KEMBALI •", callback_data="help_back"),
            ],
        ]
        return button


class Inline:
    def query(func):
        async def wrapper(client, inline_query):
            users = get_my_id
            if inline_query.from_user.id not in users:
                await client.answer_inline_query(
                    inline_query.id,
                    cache_time=1,
                    results=[
                        (
                            InlineQueryResultArticle(
                                title=f"Anda belum order @{bot.me.username}",
                                input_message_content=InputTextMessageContent(
                                    f"Silahkan Order Di @{bot.me.username} Dulu Biar Bisa Menggunakan Inline Ini"
                                ),
                            )
                        )
                    ],
                )
            else:
                await func(client, inline_query)

        return wrapper

    def data(func):
        async def wrapper(client, callback_query):
            users = get_my_id
            if callback_query.from_user.id not in users:
                await callback_query.answer(
                    f"Makanya Order Userbot @{bot.me.username} Dulu Biar Bisa Klik Tombol Ini",
                    True,
                )
            else:
                try:
                    await func(client, callback_query)
                except MessageNotModified:
                    await callback_query.answer("❌ ERROR")

        return wrapper
