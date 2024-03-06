import string
from gc import get_objects

from pykeyboard import InlineKeyboard
from pyrogram.types import (InlineKeyboardButton, InlineQueryResultArticle,
                            InputTextMessageContent)

from SaikiUbot import PREFIX, PY, Inline, bot

font = {
    "sᴍᴀʟʟᴄᴀᴘs": "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘϙʀsᴛᴜᴠᴡxʏᴢABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "𝚃𝚈𝙿𝙴𝚆𝚁𝙸𝚃𝙴𝚁": "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉",
    "𝕆𝕌𝕋𝕃𝕀ℕ𝔼": "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ",
    "𝒟ℰℛℐℋℒ": "𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵",
    "Ⓥ︎Ⓘ︎Ⓡ︎Ⓒ︎Ⓛ︎Ⓔ︎Ⓢ︎": "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ",
    "𝗦𝗔𝗡𝗦": "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭",
    "ᵗⁱⁿʸ": "ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖʳˢᵗᵘᵛʷˣʸᶻ",
    "𝐒𝐄𝐑𝐈𝐅": "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙",
    "꒒ꍏꀷꌩꌃꀎꁅ": "ꍏꌃꏳꀷꏂꎇꁅꀍꀤ꒻ꀘ꒒ꎭꈤꂦᖘꆰꋪꌚ꓄ꀎ꒦ꅐꉧꌩꁴ",
    "爪卂几ᘜ卂": "卂乃匚ᗪ乇千ᘜ卄|ﾌҜㄥ爪几ㄖ卩尺丂ㄒㄩᐯ山乂ㄚ乙",
}
basic = string.ascii_letters

__MODULE__ = "FONT"
__HELP__ = f"""
Perintah:
         <code>{PREFIX[0]}font</code> [reply/text]
Penjelasan:
           Untuk merubah text font dengan tampilan yang berbeda 
"""


def gen_font(text, new_font):
    new_font = " ".join(new_font).split()
    for q in text:
        if q in basic:
            new = new_font[basic.index(q)]
            text = text.replace(q, new)
    return text


@PY.UBOT("font", PREFIX)
async def _(client, message):
    if message.reply_to_message:
        if message.reply_to_message.text:
            query = id(message)
        else:
            return await message.reply("harap reply ke text")
    else:
        if len(message.command) < 2:
            return await message.reply(f"{message.text} [reply/text]")
        else:
            query = id(message)
    try:
        x = await client.get_inline_bot_results(bot.me.username, f"get_font {query}")
        return await message.reply_inline_bot_result(x.query_id, x.results[0].id)
    except Exception as error:
        return await message.reply(error)


@PY.INLINE("^get_font")
@Inline.query
async def _(client, inline_query):
    get_id = int(inline_query.query.split(None, 1)[1])
    buttons = InlineKeyboard(row_width=2)
    keyboard = []
    for X in font:
        keyboard.append(InlineKeyboardButton(X, callback_data=f"get {get_id} {X}"))
    buttons.add(*keyboard)
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultArticle(
                    title="get font!",
                    reply_markup=buttons,
                    input_message_content=InputTextMessageContent(
                        "<b>👇 Silahkan Pilih Salah Satu Font Dibawah</b>"
                    ),
                )
            )
        ],
    )


@PY.CALLBACK("^get")
@Inline.data
async def _(client, callback_query):
    try:
        q = int(callback_query.data.split()[1])
        m = [obj for obj in get_objects() if id(obj) == q][0]
        new = str(callback_query.data.split()[2])
        if m.reply_to_message:
            text = m.reply_to_message.text
        else:
            text = m.text.split(None, 1)[1]
        get_new_font = gen_font(text, font[new])
        buttons = InlineKeyboard(row_width=2)
        keyboard = []
        for X in font:
            keyboard.append(InlineKeyboardButton(X, callback_data=f"get {q} {X}"))
        buttons.add(*keyboard)
        return await callback_query.edit_message_text(
            get_new_font, reply_markup=buttons
        )
    except Exception as error:
        return await callback_query.edit_message_text(
            f"<b>❌ ERROR:</b> <code>{error}</code>"
        )
