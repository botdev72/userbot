import openai
from pyrogram import filters

from Amang import *
from Amang.config import *
from Amang.utils import eor

__MODULE__ = "openai"
__HELP__ = f"""
 Document for OpenAI

• Command: <code>{cmd[0]}ai</code> [query]
• Function: Untuk mengajukan pertanyaan ke AI

• Command: <code>{cmd[0]}img</code> [query]
• Function: Untuk mencari gambar ke AI
"""


class OpenAi:
    def text(question):
        openai.api_key = "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"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Q: {question}\nA:",
            temperature=0,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        return response.choices[0].text

    def photo(question):
        openai.api_key = "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"
        response = openai.Image.create(prompt=question, n=1, size="1024x1024")
        return response["data"][0]["url"]


@ubot.on_message(filters.me & filters.command(["ai", "ask"], cmd))
async def _(client, message):
    Tm = await eor(message, "<code>Processing...</code>")
    if len(message.command) < 2:
        return await Tm.edit(f"<b>Gunakan format :<code>ai</code> [pertanyaan]</b>")
    try:
        response = OpenAi.text(message.text.split(None, 1)[1])
        await message.reply(response)
        await Tm.delete()
    except Exception as error:
        await message.reply(error)
        await Tm.delete()


@ubot.on_message(filters.me & filters.command(["img"], cmd))
async def _(client, message):
    Tm = await eor(message, "<code>Processing...</code>")
    if len(message.command) < 2:
        return await Tm.edit(f"<b>Gunakan format<code>img</code> [pertanyaan]</b>")
    try:
        response = OpenAi.photo(message.text.split(None, 1)[1])
        msg = message.reply_to_message or message
        await client.send_photo(message.chat.id, response, reply_to_message_id=msg.id)
        return await Tm.delete()
    except Exception as error:
        await message.reply(error)
        return await Tm.delete()
