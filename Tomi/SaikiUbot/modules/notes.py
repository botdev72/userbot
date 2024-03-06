from gc import get_objects

from pykeyboard import InlineKeyboard
from pyrogram.types import (InlineKeyboardButton, InlineQueryResultArticle,
                            InputTextMessageContent)

from .. import *

__MODULE__ = "NOTES"
__HELP__ = f"""
Perintah:
         <code>{PREFIX[0]}addnote</code> [note_name - reply]
Penjelasan:
           Untuk menyimpan sebuah catatan 

Perintah:
         <code>{PREFIX[0]}get</code> [note_name]
Penjelasan:
           Untuk mendapatkan catatan yang disimpan 

Perintah:
         <code>{PREFIX[0]}delnote</code> [note_name]
Penjelasan:
           Untuk menghapus catatan 

Perintah:
         <code>{PREFIX[0]}notes</code>
Penjelasan:
           Untuk melihat daftar catatan yang disimpan 
"""


async def notes_create_button(text):
    buttons = InlineKeyboard(row_width=2)
    keyboard = []
    for X in text.split("|>", 1)[1].split():
        keyboard.append(
            InlineKeyboardButton(X.split(":", 1)[0], url=X.split(":", 1)[1])
        )
    buttons.add(*keyboard)
    text_button = text.split("|>", 1)[0]
    return buttons, text_button


@PY.UBOT("addnote", PREFIX)
async def _(client, message):
    note_name = get_arg(message)
    reply = message.reply_to_message
    if not reply:
        return await message.reply(
            "Balas pesan dan nama pada catatan untuk menyimpan catatan"
        )
    if await get_note(f"{client.me.id}_{note_name}"):
        return await message.reply(f"Catatan {note_name} sudah ada")
    copy = await client.copy_message(client.me.id, message.chat.id, reply.id)
    await save_note(f"{client.me.id}_{note_name}", copy.id)
    await client.send_message(
        client.me.id,
        f"👆🏻 Pesan diatas ini jangan dihapus atau catatan akan hilang\n\n👉🏻 Ketik: <code>{PREFIX[0]}delnote {note_name}</code> untuk menghapus catatan diatas",
    )
    await message.reply("Catatan berhasil di simpan")


@PY.UBOT("get", PREFIX)
async def _(client, message):
    note_name = get_arg(message)
    if not note_name:
        return await message.reply("?")
    note = await get_note(f"{client.me.id}_{note_name}")
    if not note:
        return await message.reply(f"Note {note_name} Tidak ada")
    note_id = await client.get_messages(client.me.id, note)
    if "|>" not in note_id.text or note_id.caption:
        msg = message.reply_to_message or message
        await client.copy_message(
            message.chat.id,
            client.me.id,
            note,
            reply_to_message_id=msg.id,
        )
    else:
        try:
            x = await client.get_inline_bot_results(
                bot.me.username, f"get_notes {id(message)}"
            )
            msg = message.reply_to_message or message
            await client.send_inline_bot_result(
                message.chat.id, x.query_id, x.results[0].id, reply_to_message_id=msg.id
            )
        except Exception as error:
            await message.reply(error)


@PY.INLINE("^get_notes")
@Inline.query
async def _(client, inline_query):
    _id = int(inline_query.query.split()[1])
    m = [obj for obj in get_objects() if id(obj) == _id][0]
    get_note_id = await get_note(f"{m._client.me.id}_{m.text.split()[1]}")
    note_id = await m._client.get_messages(m._client.me.id, get_note_id)
    buttons, text_button = await notes_create_button(note_id.text)
    await client.answer_inline_query(
        inline_query.id,
        cache_time=60,
        results=[
            (
                InlineQueryResultArticle(
                    title="get notes!",
                    reply_markup=buttons,
                    input_message_content=InputTextMessageContent(text_button),
                )
            )
        ],
    )


@PY.UBOT("delnote", PREFIX)
async def _(client, message):
    note_name = get_arg(message)
    if not note_name:
        return await message.reply("Apa yang ingin Anda hapus?")
    note = await get_note(f"{client.me.id}_{note_name}")
    if not note:
        return await message.reply(f"Gagal menghapus catatan {note_name}")
    await rm_note(f"{client.me.id}_{note_name}")
    await message.reply(f"Berhasil menghapus catatan {note_name}")
    await client.delete_messages(client.me.id, [int(note), int(note) + 1])


@PY.UBOT("notes", PREFIX)
async def _(client, message):
    msg = f"Catatan {client.me.first_name} {client.me.last_name or ''}\n\n"
    all = await all_notes()
    for notes in all:
        if client.me.id == int(notes.split("_", 1)[0]):
            msg += f"• {notes.split('_', 1)[1]}\n"
        else:
            msg += ""
    await message.reply(msg)
