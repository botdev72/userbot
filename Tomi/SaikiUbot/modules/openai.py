import io
import os

from .. import *

__MODULE__ = "OPENAI"
__HELP__ = f"""
Perintah:
          <code>{PREFIX[0]}ai</code> or <code>{PREFIX[0]}ask</code> [query]
Penjelasan:
           Untuk mengajukan pertanyaan ke AI

Perintah:
          <code>{PREFIX[0]}dalle</code> or <code>{PREFIX[0]}photo</code> [query]
Penjelasan:
           Untuk membuat sebuah photo 

Perintah:
          <code>{PREFIX[0]}stt</code> [reply voice note]
Penjelasan:
           Untuk merubah pesan suara ke text 
"""


@PY.UBOT(["ai", "ask"], PREFIX)
async def _(client, message):
    Tm = await message.reply("<code>Memproses...</code>")
    if len(message.command) < 2:
        return await Tm.edit(f"<b><code>{message.text}</code> [pertanyaan]</b>")
    try:
        response = OpenAi.ChatGPT(message.text.split(None, 1)[1])
        if int(len(str(response))) > 4096:
            with io.BytesIO(str.encode(str(response))) as out_file:
                out_file.name = "openAi.txt"
                await message.reply_document(
                    document=out_file,
                )
                return await Tm.delete()
        else:
            msg = message.reply_to_message or message
            await client.send_message(
                message.chat.id, response, reply_to_message_id=msg.id
            )
            return await Tm.delete()
    except Exception as error:
        await message.reply(error)
        return await Tm.delete()


@PY.UBOT(["dalle", "photo"], PREFIX)
async def _(client, message):
    Tm = await message.reply("<code>Memproses...</code>")
    if len(message.command) < 2:
        return await Tm.edit(f"<b><code>{message.text}</code> [query]</b>")
    try:
        response = OpenAi.ImageDalle(message.text.split(None, 1)[1])
        msg = message.reply_to_message or message
        await client.send_photo(message.chat.id, response, reply_to_message_id=msg.id)
        return await Tm.delete()
    except Exception as error:
        await message.reply(error)
        return await Tm.delete()


@PY.UBOT("stt", PREFIX)
async def _(client, message):
    Tm = await message.reply("<code>Memproses...</code>")
    reply = message.reply_to_message
    if reply:
        if reply.voice or reply.audio or reply.video:
            file = await client.download_media(
                message=message.reply_to_message,
                file_name=f"sst_{message.reply_to_message.id}",
            )
            audio_file = f"{file}.mp3"
            cmd = f"ffmpeg -i {file} -q:a 0 -map a {audio_file}"
            await run_cmd(cmd)
            os.remove(file)
            try:
                response = OpenAi.SpeechToText(audio_file)
            except Exception as error:
                await message.reply(error)
                return await Tm.delete()
            if int(len(str(response))) > 4096:
                with io.BytesIO(str.encode(str(response))) as out_file:
                    out_file.name = "openAi.txt"
                    await message.reply_document(
                        document=out_file,
                    )
                    return await Tm.delete()
            else:
                msg = message.reply_to_message or message
                await client.send_message(
                    message.chat.id, response, reply_to_message_id=msg.id
                )
                return await Tm.delete()
        else:
            return await Tm.edit(
                f"<b><code>{message.text}</code> [reply voice_chat/audio/video]</b>"
            )
