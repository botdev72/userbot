"""
CREDITS TOMI SETIAWAN
BABANG GANTENG
"""


import re
from gc import get_objects

from pykeyboard import InlineKeyboard
from pyrogram import *
from pyrogram.types import *

from ubot import *

from ubot.config import *
from ubot.utils import *

__MODULE__ = "Notes"
__HELP__ = """
Bantuan Untuk Notes


• Perintah: <code>{0}save</code> [nama catatan] [balas pesan]
• Penjelasan: Untuk menyimpan catatan.

• Perintah: <code>{0}get</code> [nama catatan]
• Penjelasan: Untuk mengambil catatan.

• Perintah: <code>{0}rm</code> [nama catatan]
• Penjelasan: Untuk menghapus catatan.

• Perintah: <code>{0}notes</code>
• Penjelasan: Untuk melihat semua catatan.


• Note: Untuk menggunakan button, Gunakan Format :
<code>Mbah google [google|google.com]</code>
"""


@ubot.on_message(anjay("save") & filters.me)
async def addnote_cmd(client, message):
    note_name = get_arg(message)
    reply = message.reply_to_message
    if not reply:
        return await message.reply(
            "<b>Gunakan format :</b> <code>save</code> [nama catatan] [balas ke pesan].",
        )
    if await get_note(client.me.id, note_name):
        return await message.reply(f"<b>Catatan <code>{note_name}</code> sudah ada.</b>")
    bjir = await reply.forward(client.me.id)
    copy = bjir.id
    #copy = await client.send_message(client.me.id, message.chat.id, reply.id)
    await save_note(client.me.id, note_name, copy)
    await message.reply(f"<b>Catatan <code>{note_name}</code> berhasil disimpan.</b>")


@ubot.on_message(anjay("get") & filters.me)
async def get_cmd(client, message):
    note_name = get_arg(message)
    if not note_name:
        return await message.reply(
            "<b>Gunakan format :</b> <code>get</code> [nama catatan].",
        )
    note = await get_note(client.me.id, note_name)
    if not note:
        return await message.reply(
            f"<b>Catatan dengan nama <code>{note_name}</code> tidak ditemukan.</b>",
        )
    msg_o = await client.get_messages(client.me.id, note)
    note_id = await client.get_messages(client.me.id, note)
    if note_id.text:
        if "|" in note_id.text:
            try:
                x = await client.get_inline_bot_results(
                    bot.me.username, f"get_notes {id(message)}"
                )
                #msg = message.reply_to_message or message
                await client.send_inline_bot_result(
                    message.chat.id,
                    x.query_id,
                    x.results[0].id,
                    reply_to_message_id=message.id,
                )
            except Exception as error:
                return await message.reply(error)
        else:
            await msg_o.copy(message.chat.id, reply_to_message_id=message.id)
    else:
        await msg_o.copy(message.chat.id, reply_to_message_id=message.id)


async def notes_create_button(text):
    buttons = InlineKeyboard(row_width=2)
    keyboard = []
    for button_text in re.findall(r"\[(.*?)\]", text):
        button_label, button_url = button_text.split("|")
        keyboard.append(InlineKeyboardButton(button_label, url=button_url))
    buttons.add(*keyboard)
    text_button = re.sub(r"\[(.*?)\]", "", text)
    return buttons, text_button


@bot.on_inline_query(filters.regex("^get_notes"))
async def get_notes_button(client, inline_query):
    _id = int(inline_query.query.split()[1])
    m = [obj for obj in get_objects() if id(obj) == _id][0]
    get_note_id = await get_note(m._client.me.id, m.text.split()[1])
    note_id = await m._client.get_messages(m._client.me.id, get_note_id)
    keyboard, text_button = await notes_create_button(note_id.text)
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultArticle(
                    title="get notes!",
                    reply_markup=keyboard,
                    input_message_content=InputTextMessageContent(text_button),
                )
            )
        ],
    )


@ubot.on_message(anjay("rm") & filters.me)
async def delnote_cmd(client, message):
    note_name = get_arg(message)
    if not note_name:
        return await message.reply(
            "<b>Gunakan format :</b> <code>rm</code> [nama catatan]",
        )
    note = await get_note(client.me.id, note_name)
    if not note:
        return await message.reply(
            f"<b>Catatan dengan nama <code>{note_name}</code> tidak ditemukan.</b>",
        )
    await rm_note(client.me.id, note_name)
    await message.reply(f"<b>Catatan <code>{note_name}</code> berhasil dihapus.</b>")

    await client.delete_messages(client.me.id, [int(note), int(note) + 1])


@ubot.on_message(anjay("notes") & filters.me)
async def notes_cmd(client, message):
    msg = f"<b>๏ Daftar Catatan :</b>\n\n"
    semua = await all_notes(client.me.id)
    if not semua:
        return await message.reply("Tidak ada catatan tersimpan .")
    else:
        for notes in semua:
            msg += f"• <code>{notes}</code>\n"
        await message.reply(msg)
