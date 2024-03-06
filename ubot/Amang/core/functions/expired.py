import asyncio
import sys
from datetime import datetime
from os import environ, execle

from pytz import timezone

from Amang import LOGGER
from Amang import bot, ubot
from Amang.config import LOGS
from Amang.utils.dbfunctions import (get_expired_date, rem_expired_date,
                                    remove_ubot)

SELLER_GROUP = -1001953239597

async def expired_date():
    while True:
        now = datetime.now(timezone("Asia/Jakarta"))
        time = now.strftime("%d-%m-%Y")
        clock = now.strftime("%H:%M:%S")
        for X in ubot._ubot:
            try:
                exp = (await get_expired_date(X.me.id)).strftime("%d-%m-%Y")
                if time == exp:
                    await X.log_out()
                    await rem_expired_date(X.me.id)
                    await remove_ubot(X.me.id)
                    ubot._ubot.remove(X)
                    await bot.send_message(
                        LOGS, SELLER_GROUP,
                        f"<b>{X.me.first_name} {X.me.last_name or ''} | <code>{X.me.id}</code> masa aktif telah habis</b>",
                    )
            except:
                pass
        text = await bot.send_message(
            LOGS,
            f"<b>🗓️ Tanggal:</b> <code>{time}</code>\n<b>🕕 Jam:</b> <code>{clock}</code>",
        )
        await asyncio.sleep(3600)
        await text.delete()


async def rebot():
    while True:
        await asyncio.sleep(600)
        try:
            await bot.send_message(LOGS, "<b>Auto Restart On...</b>")
            LOGGER(__name__).info("BOT SERVER RESTARTED !!")
        except Exception as err:
            LOGGER(__name__).info(f"{err}")
        await asyncio.sleep(2)
        await bot.send_message(LOGS, "✅ <b>Bot Berhasil Di Restart.</b>")
        args = [sys.executable, "-m", "Amang"]
        execle(sys.executable, *args, environ)


async def restart_all():
    asyncio.get_event_loop().create_task(rebot())
