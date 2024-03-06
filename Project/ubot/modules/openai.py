import io
import os
import subprocess

from ubot import KY, Emo, OpenBO
from ubot.utils import get_text

__MODULE__ = "OpenAi"
__HELP__ = """
Bantuan Untuk OpenAi

• Perintah: <code>{0}ai</code> [query]
• Penjelasan: Untuk mengajukan pertanyaan ke AI

• Perintah: <code>{0}img</code> [query]
• Penjelasan: Untuk mencari gambar ke AI

• Perintah : <code>{0}stt</code> [balas audio]
• Penjelasan : Untuk merubah pesan suara ke teks.
"""


@KY.UBOT("ai", sudo=True)
async def ai_cmd(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    Tm = await message.reply(f"{emo.proses} <b>Processing...</b>")
    args = get_text(message)
    if not args:
        return await Tm.edit(
            f"{emo.gagal} <b><code>{message.text}</code> [pertanyaan]</b>"
        )
    try:
        response = OpenBO.ChatGPT(args)
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


@KY.UBOT("img", sudo=True)
async def dalle_cmd(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    Tm = await message.reply(f"{emo.proses} <b>Processing...</b>")
    if len(message.command) < 2:
        return await Tm.edit(f"{emo.gagal} <b><code>{message.text}</code> [query]</b>")
    try:
        response = OpenBO.ImageDalle(message.text.split(None, 1)[1])
        msg = message.reply_to_message or message
        await client.send_photo(message.chat.id, response, reply_to_message_id=msg.id)
        return await Tm.delete()
    except Exception as error:
        await message.reply(error)
        return await Tm.delete()


@KY.UBOT("stt", sudo=True)
async def stt_cmd(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    Tm = await message.reply(f"{emo.proses} <b>Processing...</b>")
    reply = message.reply_to_message
    if reply:
        if reply.voice or reply.audio or reply.video:
            file = await client.download_media(
                message=message.reply_to_message,
                file_name=f"sst_{message.reply_to_message.id}",
            )
            audio_file = f"{file}.mp3"
            cmd = f"ffmpeg -i {file} -q:a 0 -map a {audio_file}"
            subprocess.run(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            os.remove(file)
            try:
                response = OpenBO.SpeechToText(audio_file)
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
                f"{emo.gagal} <b><code>{message.text}</code> [balas media].</b>"
            )
