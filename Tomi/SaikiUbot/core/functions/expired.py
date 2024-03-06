import asyncio
from datetime import datetime

from pytz import timezone

from SaikiUbot import bot, ubot
from SaikiUbot.utils import get_expired_date, rem_expired_date, remove_ubot


async def premium():
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
                        -1001880331689,
                        f"<b>{X.me.first_name} {X.me.last_name or ''} | <code>{X.me.id}</code> masa aktif telah habis</b>",
                    )
            except:
                pass
        text = await bot.send_message(
            -1001880331689,
            f"<b>🗓️ Tanggal:</b> <code>{time}</code>\n<b>🕕 Jam:</b> <code>{clock}</code>",
        )
        await asyncio.sleep(3600)
        await text.delete()
