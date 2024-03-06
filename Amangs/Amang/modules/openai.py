import openai
from pyrogram import filters

from Amang import *
from Amang.config import *
from Amang.utils import *

__MOD__ = "OpenAI"
__HELP__ = f"""
 Document for OpenAI

• Command: <code>{cmd[0]}ai</code> [query] (s)
• Function: Untuk mengajukan pertanyaan ke AI

• Command: <code>{cmd[0]}img</code> [query] (s)
• Function: Untuk mencari gambar ke AI
"""


openai.api_key = OPENAI_API

class OpenAi:
    @staticmethod
    async def ChatGPT(question):
        response = await asyncio.to_thread(
            openai.ChatCompletion.create,
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}],
        )
        return response.choices[0].message["content"].strip()

    @staticmethod
    async def ImageDalle(question):
        response = await asyncio.to_thread(
            openai.Image.create,
            prompt=question,
            n=1,
        )
        return response["data"][0]["url"]

    @staticmethod
    async def SpeechToText(file):
        audio_file = open(file, "rb")
        response = await asyncio.to_thread(
            openai.Audio.transcribe, "whisper-1", audio_file
        )
        return response["text"]



@ubot.on_message(filters.me & anjay("ai"))
@check_access
async def _(client, message):
    Tm = await message.reply_text("<code>Memproses...</code>")
    if len(message.command) < 2:
        return await Tm.edit(f"<b>Gunakan format :<code>ai</code> [pertanyaan]</b>")
    try:
        response = await OpenAi.ChatGPT(message.text.split(None, 1)[1])
        await message.reply(response)
        await Tm.delete()
    except Exception as error:
        await message.reply(error)
        await Tm.delete()


@ubot.on_message(filters.me & anjay("img"))
@check_access
async def _(client, message):
    Tm = await message.reply_text("<code>Memproses...</code>")
    if len(message.command) < 2:
        return await Tm.edit(f"<b>Gunakan format<code>img</code> [pertanyaan]</b>")
    try:
        response = await OpenAi.ImageDalle(message.text.split(None, 1)[1])
        msg = message.reply_to_message or message
        await client.send_photo(message.chat.id, response, reply_to_message_id=msg.id)
        return await Tm.delete()
    except Exception as error:
        await message.reply(error)
        return await Tm.delete()
