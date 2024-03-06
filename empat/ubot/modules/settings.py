from asyncio import sleep

from pyrogram import *
from pyrogram.types import *

from ubot import KY, Emo
from ubot.utils import get_arg
from ubot.utils.dbfunctions import *

__MODULE__ = "Settings"
__HELP__ = """
Bantuan Untuk Settings

• Perintah: <code>{0}setprefix</code> [trigger]
• Penjelasan: Untuk mengatur handler userbot anda.

• Perintah: <code>{0}setdb</code> [variable] [value]
• Penjelasan: Untuk mengubah tampilan emoji.

• Perintah: <code>{0}emoid</code> [reply emoji]
• Penjelasan: Untuk mengubah tampilan emoji.

• Perintah: <code>{0}getemo</code>
• Penjelasan: Untuk melihat tampilan emoji.

• Contoh pengunaan set emoji dan setprefix :

`{0}setdb ping 😎`
`{0}setdb pong 🚊`
`{0}setdb proses ⏳`
`{0}setdb sukses ✅`
`{0}setdb gagal ❌`
`{0}setdb profil 👋`
`{0}setdb anu 🤖`
`{0}setdb notepic link or off`


`{0}setprefix 1 - ( + ) none`

Untuk akun premium bisa menggunakan emoji premium.
"""


@KY.UBOT("setprefix")
async def _(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    Tm = await message.edit(f"{emo.proses} **Processing...**")
    if len(message.command) < 2:
        return await Tm.edit(f"{emo.gagal} **Prefix harus berupa trigger.**")
    else:
        ub_prefix = []
        for prefix in message.command[1:]:
            if prefix.lower() == "none":
                ub_prefix.append("")
            else:
                ub_prefix.append(prefix)
        try:
            client.set_prefix(client.me.id, ub_prefix)
            await set_pref(client.me.id, ub_prefix)
            parsed_prefix = " ".join(f"{prefix}" for prefix in ub_prefix)
            return await Tm.edit(f"{emo.sukses} Prefix diatur ke : {parsed_prefix}")
        except Exception as error:
            await Tm.edit(str(error))


@KY.UBOT("emoid")
async def emoid(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    Tm = await message.edit(f"{emo.proses} **Processing...**")
    emoji = message.reply_to_message
    if emoji.entities:
        for entot in emoji.entities:
            if entot.custom_emoji_id:
                emoid = entot.custom_emoji_id
                await Tm.edit(f"{emo.sukses} **Custom Emoji ID : `{emoid}`.**")
            else:
                await Tm.edit(f"{emo.gagal} **Reply ke Custom Emoji.**")


@KY.UBOT("setdb")
async def set_emoji(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    gua = client.me.is_premium
    jing = await message.reply(f"{emo.proses} **Processing...**")
    if len(message.command) < 3:
        return await jing.edit(
            f"{emo.gagal} **Gunakan Format : `setdb variable value`.**"
        )
    command, variable, value = message.command[:3]
    emoji_id = None
    get_arg(message)
    if variable.lower() == "ping":
        if gua == True:
            if message.entities:
                for entity in message.entities:
                    if entity.custom_emoji_id:
                        emoji_id = entity.custom_emoji_id
                        break
                if emoji_id:
                    await set_var(client.me.id, "emo_ping", emoji_id)
                    await jing.edit(
                        f"{emo.sukses} <b>Emoji ping diset ke :</b> <emoji id={emoji_id}>{value}</emoji>"
                    )
        elif gua == False:
            await set_var(client.me.id, "emo_ping", value)
            await jing.edit(f"{emo.sukses} <b>Emoji ping diset ke :</b> {value}")
    elif variable.lower() == "pong":
        if gua == True:
            if message.entities:
                for entity in message.entities:
                    if entity.custom_emoji_id:
                        emoji_id = entity.custom_emoji_id
                        break
                if emoji_id:
                    await set_var(client.me.id, "emo_pong", emoji_id)
                    await jing.edit(
                        f"{emo.sukses} <b>Emoji pong diset ke :</b> <emoji id={emoji_id}>{value}</emoji>"
                    )
        elif gua == False:
            await set_var(client.me.id, "emo_pong", value)
            await jing.edit(f"{emo.sukses} <b>Emoji pong diset ke :</b> {value}")
    elif variable.lower() == "proses":
        if gua == True:
            if message.entities:
                for entity in message.entities:
                    if entity.custom_emoji_id:
                        emoji_id = entity.custom_emoji_id
                        break
                if emoji_id:
                    await set_var(client.me.id, "emo_proses", emoji_id)
                    await jing.edit(
                        f"{emo.sukses} <b>Emoji proses diset ke :</b> <emoji id={emoji_id}>{value}</emoji>"
                    )
        elif gua == False:
            await set_var(client.me.id, "emo_proses", value)
            await jing.edit(f"{emo.sukses} <b>Emoji proses diset ke :</b> {value}")
    elif variable.lower() == "gagal":
        if gua == True:
            if message.entities:
                for entity in message.entities:
                    if entity.custom_emoji_id:
                        emoji_id = entity.custom_emoji_id
                        break
                if emoji_id:
                    await set_var(client.me.id, "emo_gagal", emoji_id)
                    await jing.edit(
                        f"{emo.sukses} <b>Emoji gagal diset ke :</b> <emoji id={emoji_id}>{value}</emoji>"
                    )
        elif gua == False:
            await set_var(client.me.id, "emo_gagal", value)
            await jing.edit(f"{emo.sukses} <b>Emoji gagal diset ke :</b> {value}")
    elif variable.lower() == "sukses":
        if gua == True:
            if message.entities:
                for entity in message.entities:
                    if entity.custom_emoji_id:
                        emoji_id = entity.custom_emoji_id
                        break
                if emoji_id:
                    await set_var(client.me.id, "emo_sukses", emoji_id)
                    await jing.edit(
                        f"{emo.sukses} <b>Emoji sukses diset ke :</b> <emoji id={emoji_id}>{value}</emoji>"
                    )
        elif gua == False:
            await set_var(client.me.id, "emo_sukses", value)
            await jing.edit(f"{emo.sukses} <b>Emoji sukses diset ke :</b> {value}")
    elif variable.lower() == "profil":
        if gua == True:
            if message.entities:
                for entity in message.entities:
                    if entity.custom_emoji_id:
                        emoji_id = entity.custom_emoji_id
                        break
                if emoji_id:
                    await set_var(client.me.id, "emo_profil", emoji_id)
                    await jing.edit(
                        f"{emo.sukses} <b>Emoji profil diset ke :</b> <emoji id={emoji_id}>{value}</emoji>"
                    )
        elif gua == False:
            await set_var(client.me.id, "emo_profil", value)
            await jing.edit(f"{emo.sukses} <b>Emoji profil diset ke :</b> {value}")
    elif variable.lower() == "anu":
        if gua == True:
            if message.entities:
                for entity in message.entities:
                    if entity.custom_emoji_id:
                        emoji_id = entity.custom_emoji_id
                        break
                if emoji_id:
                    await set_var(client.me.id, "emo_anu", emoji_id)
                    await jing.edit(
                        f"{emo.sukses} <b>Emoji anu diset ke :</b> <emoji id={emoji_id}>{value}</emoji>"
                    )
        elif gua == False:
            await set_var(client.me.id, "emo_anu", value)
            await jing.edit(f"{emo.sukses} <b>Emoji anu diset ke :</b> {value}")
    elif variable.lower() == "notepic":
        if value.lower() == "off":
            await del_var(client.me.id, "note_pic")
            await jing.edit(f"{emo.sukses} <b>{variable} Berhasil Dihapus.</b>")
        else:
            await set_var(client.me.id, "note_pic", value)
            await jing.edit(
                f"{emo.sukses} <b>Notes Pic Berhasil Diset ke {value}.</b>",
                disable_web_page_preview=True,
            )
    elif variable.lower() == "antipm":
        if value.lower() == "off":
            await del_var(client.me.id, "ENABLE_PM_GUARD")
            await jing.edit(f"{emo.sukses} <b>AntiPM Dimatikan.</b>")
        else:
            await set_var(client.me.id, "ENABLE_PM_GUARD", True)
            await jing.edit(f"{emo.sukses} <b>AntiPM Dihidupkan.</b>")
    else:
        await jing.edit(f"{emo.gagal} **Silakan ketik `help {message.text}`.**")


@KY.UBOT("getemo")
async def getemoji(client, message):
    emo = Emo(client.me.id)
    await emo.initialize()
    xx = await message.reply(f"{emo.proses} **Processing...**")
    await xx.edit(f"{emo.sukses} <b>๏ Emoji kamu :</b>\n\n PING : {emo.ping}\n PONG : {emo.pong}\n PROSES : {emo.proses}\n SUKSES : {emo.sukses}\n GAGAL : {emo.gagal}\n PROFIL : {emo.profil}\n ANU : {emo.anu}")
    
