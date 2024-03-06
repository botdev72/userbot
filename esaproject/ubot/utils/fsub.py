from os import getenv

from pykeyboard import InlineKeyboard
from pyrogram.enums import ChatType
from pyrogram.errors import (ChatAdminRequired, ChatWriteForbidden,
                             UserNotParticipant)
from pyrogram.types import InlineKeyboardButton

from ubot import bot

FORCE_SUBCRIBE = list(
    map(
        int,
        getenv(
            "FORCE_SUBCRIBE", "-1001825363971 -1001812143750 -1001982790377"
        ).split(),
    )
)


def MULTI_SUBSCRIBE(func):
    async def subscribe(client, message):
        user_id = message.from_user.id
        user_name = (
            f"{message.from_user.first_name} {message.from_user.last_name or ''}"
        )
        rpk = f"<a href=tg://user?id={user_id}>{user_name}</a>"
        if not FORCE_SUBCRIBE:
            return
        try:
            try:
                for i in range(min(len(FORCE_SUBCRIBE), len(FORCE_SUBCRIBE))):
                    await bot.get_chat_member(FORCE_SUBCRIBE[i], user_id)
            except UserNotParticipant:
                buttons = InlineKeyboard(row_width=2)
                keyboard: List[InlineKeyboardButton] = []
                for i in range(min(len(FORCE_SUBCRIBE), len(FORCE_SUBCRIBE))):
                    get = await bot.get_chat(FORCE_SUBCRIBE[i])
                    FSubLink = f"{get.invite_link}"
                    if get.type == ChatType.GROUP:
                        FSubName = "• Join Group •"
                    elif get.type == ChatType.SUPERGROUP:
                        FSubName = "• Join Group •"
                    elif get.type == ChatType.CHANNEL:
                        FSubName = "• Join Channel •"
                    keyboard.append(
                        InlineKeyboardButton(
                            text=FSubName,
                            url=FSubLink,
                        )
                    )
                buttons.add(*keyboard)
                try:
                    await message.reply(
                        f"""
<b>🙋🏻‍♂️ Halo {rpk} Apa kabar?

💡 Untuk Menggunakan Bot, 

📣 Anda Harus Bergabung Dengan Group/Channel Terlebih Dahulu,

✅ Jika Sudah Bergabung Silahkan Klik Kembali: {message.text}</b>
""",
                        disable_web_page_preview=True,
                        reply_markup=buttons,
                    )
                    await message.stop_propagation()
                except ChatWriteForbidden:
                    pass
        except ChatAdminRequired:
            await message.reply(f"Saya bukan admin di : {FORCE_SUBCRIBE} !")
        return await func(bot, message)

    return subscribe
