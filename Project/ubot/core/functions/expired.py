import asyncio
from datetime import datetime

from pyrogram.types import InlineKeyboardMarkup
from pytz import timezone

from ubot import SKY, bot, remove_offi, ubot
from ubot.core.helpers import MSG, Button
from ubot.utils.dbfunctions import *


async def expiredUserbots():
    while not await asyncio.sleep(120):
        for X in ubot._ubot:
            try:
                time = datetime.now(timezone("Asia/Jakarta")).strftime("%d-%m-%Y")
                exp = (await get_expired_date(X.me.id)).strftime("%d-%m-%Y")
                if time == exp:
                    await X.unblock_user(bot.me.username)
                    for chat in await get_chat(X.me.id):
                        await remove_chat(X.me.id, chat)
                    await rm_all(X.me.id)
                    await remove_ubot(X.me.id)
                    await rem_expired_date(X.me.id)
                    await rem_uptime(X.me.id)
                    await remove_offi(X.me.id)
                    await rem_pref(X.me.id)
                    await rmall_var(X.me.id)
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
                print(f"Error: - {X.me.id} - :{str(e)}")


# asyncio.create_task(expiredUserbots())
