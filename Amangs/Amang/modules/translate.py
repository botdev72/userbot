import os

import gtts
from gpytranslate import Translator
from pyrogram import filters

from Amang import *
from Amang.config import *
from Amang.utils import eor

__MOD__ = "Translate"
__HELP__ = f"""
 Document for Translate

• Command: <code>{cmd[0]}tr</code> [lang_code - reply/text]
• Function: Untuk menerjemahkan text dengan kode negara yang diinginkan.

• Command: <code>{cmd[0]}tts</code> [lang_code - reply/text]
• Function: Untuk menerjemahkan text dengan kode negara yang diinginkan serta merubahnya menjadi pesan suara.
"""


@ubot.on_message(filters.me & anjay("tts"))
async def _(_, message):
    if message.reply_to_message:
        if len(message.command) < 2:
            language = "id"
            words_to_say = (
                message.reply_to_message.text or message.reply_to_message.caption
            )
        else:
            language = message.text.split(None, 2)[1]
            words_to_say = (
                message.reply_to_message.text or message.reply_to_message.caption
            )
    else:
        if len(message.command) < 3:
            return
        else:
            language = message.text.split(None, 2)[1]
            words_to_say = message.text.split(None, 2)[2]
    speech = gtts.gTTS(words_to_say, lang=language)
    speech.save("text_to_speech.oog")
    reply_me_or_user = message.reply_to_message or message
    try:
        await _.send_voice(
            chat_id=message.chat.id,
            voice="text_to_speech.oog",
            reply_to_message_id=reply_me_or_user.id,
        )
    except:
        ABC = await eor(
            message,
            "Pesan Suara tidak diizinkan di sini.\nSalin yang dikirim ke Pesan Tersimpan.",
        )
        await _.send_voice(_.me.id, "text_to_speech.oog")
        await message.delete()
        await ABC.delete()
        await asyncio.sleep(2)
    try:
        os.remove("text_to_speech.oog")
    except FileNotFoundError:
        pass


@ubot.on_message(filters.me & anjay(["tr", "tl"]))
async def _(client, message):
    trans = Translator()
    if message.reply_to_message:
        if len(message.command) < 2:
            dest = "id"
            to_translate = (
                message.reply_to_message.text or message.reply_to_message.caption
            )
            source = await trans.detect(to_translate)
        else:
            dest = message.text.split(None, 2)[1]
            to_translate = (
                message.reply_to_message.text or message.reply_to_message.caption
            )
            source = await trans.detect(to_translate)
    else:
        if len(message.command) < 3:
            return
        else:
            dest = message.text.split(None, 2)[1]
            to_translate = message.text.split(None, 2)[2]
            source = await trans.detect(to_translate)
    translation = await trans(to_translate, sourcelang=source, targetlang=dest)
    reply = f"<b>Bahasa {source} Ke Bahasa {dest}</b>:\n<code>{translation.text}</code>"
    reply_me_or_user = message.reply_to_message or message
    await client.send_message(
        message.chat.id, reply, reply_to_message_id=reply_me_or_user.id
    )
