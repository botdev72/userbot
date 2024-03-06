import asyncio
import os

from ubot import *
from ubot.utils import *

__MODULE__ = "Sounds"
__HELP__ = """
Bantuan Untuk Sounds

• Perintah: <b>{0}efek</b> [efek_code - reply to voice note]
• Penjelasan: Untuk mengubah suara voice note.

<b>efek_code:</b>  <b>bengek</b> <b>robot</b> <b>jedug</b> <b>fast</b> <b>echo</b>
"""


@KY.UBOT("efek")
async def convert_efek(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    helo = get_arg(message)
    rep = message.reply_to_message
    Tm = await message.reply(f"{emo.proses} **Processing...**")
    await asyncio.sleep(3)
    if rep and helo:
        tau = ["bengek", "robot", "jedug", "fast", "echo"]
        if helo in tau:
            indir = await client.download_media(rep)
            KOMUT = {
                "bengek": '-filter_complex "rubberband=pitch=1.5"',
                "robot": "-filter_complex \"afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=512:overlap=0.75\"",
                "jedug": '-filter_complex "acrusher=level_in=8:level_out=18:bits=8:mode=log:aa=1"',
                "fast": "-filter_complex \"afftfilt=real='hypot(re,im)*cos((random(0)*2-1)*2*3.14)':imag='hypot(re,im)*sin((random(1)*2-1)*2*3.14)':win_size=128:overlap=0.8\"",
                "echo": '-filter_complex "aecho=0.8:0.9:500|1000:0.2|0.1"',
            }
            ses = await asyncio.create_subprocess_shell(
                f"ffmpeg -i '{indir}' {KOMUT[helo]} audio.mp3"
            )
            await ses.communicate()
            await Tm.delete()
            await rep.reply_voice("audio.mp3", caption=f"{emo.sukses} **Efek {helo}**")
            os.remove("audio.mp3")
        else:
            await message.reply(f"{emo.gagal} **Silakan masukkan efek : `{tau}`**")
    else:
        await Tm.edit(
            f"{emo.gagal} **Silakan balas audio.\n\nContoh : <code>{0}efek bengek</code>[balas audio]**"
        )
