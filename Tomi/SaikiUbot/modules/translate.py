import os
from gc import get_objects

import gtts
from gpytranslate import Translator
from pykeyboard import InlineKeyboard

from .. import *

__MODULE__ = "TRANSLATE"
__HELP__ = f"""
Perintah:
         <code>{PREFIX[0]}tr</code> [reply/text]
Penjelasan:
           Untuk menerjemahkan text

Perintah:
         <code>{PREFIX[0]}tts</code> [reply/text]
Penjelasan:
           Untuk merubah tect menjadi menjadi pesan suara 

Perintah:
         <code>{PREFIX[0]}set_lang</code>
Penjelasan:
           Untuk merubah bahasa translate 
"""

lang_code_translate = {
    "Afrikaans": "af",
    "Arabic": "ar",
    "Chinese": "zh-cn",
    "Czech": "cs",
    "German": "e",
    "Greek": "el",
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "Hindi": "hi",
    "Indonesian": "id",
    "Icelandic": "is",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jw",
    "Korean": "ko",
    "Latin": "la",
    "Myanmar": "my",
    "Nepali": "ne",
    "Dutch": "nl",
    "Portuguese": "pt",
    "Russian": "ru",
    "Sundanese": "su",
    "Swedish": "sv",
    "Thailand": "th",
    "Filipino": "tl",
    "Turkish": "tr",
    "Vietname": "vi",
}


@PY.UBOT("tts", PREFIX)
async def _(client, message):
    if message.reply_to_message:
        language = lang_code[client.me.id]["negara"]
        words_to_say = message.reply_to_message.text or message.reply_to_message.caption
    else:
        if len(message.command) < 2:
            return await message.reply(f"<code>{message.text}</code> ʀᴇᴘʟʏ/ᴛᴇxᴛ")
        else:
            language = lang_code[client.me.id]["negara"]
            words_to_say = message.text.split(None, 1)[1]
    speech = gtts.gTTS(words_to_say, lang=language)
    speech.save("text_to_speech.oog")
    rep = message.reply_to_message or message
    try:
        await client.send_voice(
            chat_id=message.chat.id,
            voice="text_to_speech.oog",
            reply_to_message_id=rep.id,
        )
    except Exception as error:
        await message.reply(error)
    try:
        os.remove("text_to_speech.oog")
    except FileNotFoundError:
        pass


@PY.UBOT(["tr", "tl"], PREFIX)
async def _(client, message):
    trans = Translator()
    if message.reply_to_message:
        dest = lang_code[client.me.id]["negara"]
        to_translate = message.reply_to_message.text or message.reply_to_message.caption
        source = await trans.detect(to_translate)
    else:
        if len(message.command) < 2:
            return await message.reply(f"<code>{message.text}</code> ʀᴇᴘʟʏ/ᴛᴇxᴛ")
        else:
            dest = lang_code[client.me.id]["negara"]
            to_translate = message.text.split(None, 1)[1]
            source = await trans.detect(to_translate)
    translation = await trans(to_translate, sourcelang=source, targetlang=dest)
    reply = f"<code>{translation.text}</code>"
    rep = message.reply_to_message or message
    await client.send_message(message.chat.id, reply, reply_to_message_id=rep.id)


@PY.UBOT("set_lang", PREFIX)
async def _(client, message):
    query = id(message)
    try:
        x = await client.get_inline_bot_results(bot.me.username, f"ubah_bahasa {query}")
        return await message.reply_inline_bot_result(x.query_id, x.results[0].id)
    except Exception as error:
        return await message.reply(error)


@PY.INLINE("^ubah_bahasa")
@Inline.query
async def _(client, inline_query):
    buttons = InlineKeyboard(row_width=3)
    keyboard = []
    for X in lang_code_translate:
        keyboard.append(
            InlineKeyboardButton(
                X, callback_data=f"set_bahasa {int(inline_query.query.split()[1])} {X}"
            )
        )
    buttons.add(*keyboard)
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultArticle(
                    title="get bahasa!",
                    reply_markup=buttons,
                    input_message_content=InputTextMessageContent(
                        "<b>🔄 Silahkan Pilih Bahasa Translate</b>"
                    ),
                )
            )
        ],
    )


@PY.CALLBACK("^set_bahasa")
@Inline.data
async def _(client, callback_query):
    data = callback_query.data.split()
    try:
        m = [obj for obj in get_objects() if id(obj) == int(data[1])][0]
        lang_code[m._client.me.id] = {"negara": lang_code_translate[data[2]]}
        return await callback_query.edit_message_text(
            f"<b>✅ Berhasil Diubah Ke Bahasa {data[2]}"
        )
    except Exception as error:
        return await callback_query.edit_message_text(
            f"<b>❌ ERROR:</b> <code>{error}</code>"
        )
