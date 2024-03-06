# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

import base64

from ubot import *


@KY.UBOT("encode|en", FIL.SUDO)
async def encod(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    xx = await message.reply(f"{emo.proses} **Processing...**")
    tex = get_text(message)
    if not tex:
        return await xx.edit(f"{emo.gagal} **Berikan teks atau balas pesan.**")
    else:
        try:
            byt = tex.encode("ascii")
            et = base64.b64encode(byt)
            atc = et.decode("ascii")
            await xx.edit(
                f"{emo.sukses} **Encoded Text:** `{tex}`\n{emo.sukses} **OUTPUT :** `{atc}`"
            )
        except Exception as p:
            await xx.edit(f"{emo.gagal} **ERROR :** {str(p)}")


@KY.UBOT("decode|de", FIL.SUDO)
async def dencod(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    xx = await message.reply(f"{emo.proses} **Processing...**")
    tex = get_text(message)
    if not tex:
        return await xx.edit(f"{emo.gagal} **Berikan teks atau balas pesan.**")
    else:
        try:
            byt = tex.encode("ascii")
            et = base64.b64decode(byt)
            atc = et.decode("ascii")
            await xx.edit(
                f"{emo.sukses} **Decode Text:** `{tex}`\n{emo.sukses} **OUTPUT :** `{atc}`"
            )
        except Exception as p:
            await xx.edit(f"{emo.gagal} **ERROR :** {str(p)}")
