from asyncio import QueueEmpty
from contextlib import suppress
from pytgcalls.exceptions import NoActiveGroupCall, NotInGroupCallError
from pytgcalls.types import StreamAudioEnded, Update

from ubot import ubot
from ubot.core.pytgcalls import queues
from .vctls import turun_dewek, daftar_join


@ubot.pytgcalls_decorator()
async def _(_, chat_id: int):
    global turun_dewek
    if chat_id in daftar_join:
        turun_dewek = False
    else:
        try:
            queues.clear(chat_id)
            turun_dewek = True
        except QueueEmpty:
            pass


@ubot.pytgcalls_decorator()
async def stream_end(client, update: Update):
    global turun_dewek
    if isinstance(update, StreamAudioEnded):
        queues.task_done(update.chat_id)
        if update.chat_id in daftar_join:
            turun_dewek = False
        elif queues.is_empty(update.chat_id):
            try:
                await client.leave_group_call(update.chat_id)
                turun_dewek = True
            except (NotInGroupCallError, NoActiveGroupCall):
                pass
        else:
            await client.change_stream(
                update.chat_id, queues.get(update.chat_id)["file"]
            )
