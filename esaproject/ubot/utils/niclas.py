
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pykeyboard import InlineKeyboard
from pyrogram.errors import MessageNotModified
from pyrogram.types import (InlineKeyboardButton, InlineQueryResultArticle,
                            InputTextMessageContent)

from .dbfunctions import *

class MSG:
    async def USERBOT(count):
        expired_date = await get_expired_date(ubot._ubot[int(count)].me.id)
        return f"""
<b>❏ ᴜsᴇʀʙᴏᴛ ᴋᴇ</b> <code>{int(count) + 1}/{len(ubot._ubot)}</code>
<b> ├ ᴀᴋᴜɴ:</b> <a href=tg://user?id={ubot._ubot[int(count)].me.id}>{ubot._ubot[int(count)].me.first_name} {ubot._ubot[int(count)].me.last_name or ''}</a> 
<b> ├ ɪᴅ:</b> <code>{ubot._ubot[int(count)].me.id}</code>
<b> ╰ ᴇxᴘɪʀᴇᴅ</b> <code>{expired_date.strftime('%d-%m-%Y')}</code>
"""

class Button:
    def deak(user_id, count):
        button = [
            [
                InlineKeyboardButton(
                    "⬅️ Kembali ",
                    callback_data=f"prev_ub {int(count)}",
                ),
                InlineKeyboardButton(
                    "Setujui ✅", callback_data=f"deak_akun {int(count)}"
                ),
            ],
        ]
        return button

    def expired_button_bot():
        button = [
            [
                InlineKeyboardButton(
                    text=f"{bot.me.first_name}",
                    url=f"https://t.me/{bot.me.username}",
                )
            ]
        ]
        return button
        
    def userbot(user_id, count):
        button = [
            [
                InlineKeyboardButton(
                    "Hapus Dari Database",
                    callback_data=f"del_ubot {int(user_id)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "Cek Nomor",
                    callback_data=f"get_phone {int(count)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "Cek Kadaluarsa",
                    callback_data=f"cek_masa_aktif {int(user_id)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "Cek Otp",
                    callback_data=f"get_otp {int(count)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "Cek Verifikasi 2L",
                    callback_data=f"get_faktor {int(count)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "Musnah", callback_data=f"ub_deak {int(count)}"
                )
            ],
            [
                InlineKeyboardButton("❮", callback_data=f"prev_ub {int(count)}"),
                InlineKeyboardButton("❯", callback_data=f"next_ub {int(count)}"),
            ],
            [
                InlineKeyboardButton("Tutup", callback_data=f"0_cls"),
            ],
        ]
        return button

    def ambil_akun(user_id, count):
        button = [
            [
                InlineKeyboardButton(
                    "Hapus Dari Database",
                    callback_data=f"del_ubot {int(user_id)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "Cek Nomor",
                    callback_data=f"get_phone {int(count)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "Cek Kadaluarsa",
                    callback_data=f"cek_masa_aktif {int(user_id)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "Cek Otp",
                    callback_data=f"get_otp {int(count)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "Cek Verifikasi 2L",
                    callback_data=f"get_faktor {int(count)}",
                )
            ],
            [
                InlineKeyboardButton(
                    "Musnah", callback_data=f"ub_deak {int(count)}"
                )
            ],
            [
                InlineKeyboardButton("❮", callback_data=f"prev_ub {int(count)}"),
                InlineKeyboardButton("❯", callback_data=f"next_ub {int(count)}"),
            ],
            [
                InlineKeyboardButton("Tutup", callback_data=f"close_user")
            ],
        ]
        return button
