import asyncio
from datetime import datetime

from pyrogram.types import InlineKeyboardMarkup
from pytz import timezone


from ubot import bot, ubot, SKY
from ubot.utils.dbfunctions import rm_all, remove_ubot, rem_expired_date, get_expired_date
from ubot.core.helpers import MSG, Button


async def expired_userbot(X):
    try:
        time = datetime.now(timezone("Asia/Jakarta")).strftime("%d-%m-%Y")
        exp = (await get_expired_date(X.me.id)).strftime("%d-%m-%Y")
        if time == exp:
            for chat in await get_chat(X.me.id):
                await remove_chat(X.me.id, chat)
            await rm_all(X.me.id)
            await remove_ubot(X.me.id)
            await rem_expired_date(X.me.id)
            ubot._get_my_id.remove(X.me.id)
            ubot._ubot.remove(X)
            await X.log_out()
            expired_text = MSG.EXPIRED_MSG_BOT(X)
            expired_button = Button.expired_button_bot()
            await bot.send_message(
                SKY,
                expired_text,
                reply_markup=InlineKeyboardMarkup(expired_button),
            )
    except Exception as e:
        print(f"Error: {str(e)}")


async def expiredUserbots():
    while True:
        tasks = [expired_userbot(X) for X in ubot._ubot]
        await asyncio.gather(*tasks)
        await asyncio.sleep(60)