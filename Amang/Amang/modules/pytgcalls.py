
from asyncio import QueueEmpty

from pytgcalls.exceptions import NoActiveGroupCall, NotInGroupCallError
from pytgcalls.types import StreamAudioEnded, Update

from Amang import ubot
from Amang.core.pytgcalls import queues


@ubot.pytgcalls_decorator()
async def _(_, chat_id: int):
    try:
        queues.clear(chat_id)
    except QueueEmpty:
        pass


@ubot.pytgcalls_decorator()
async def stream_end(client, update: Update):
    if isinstance(update, StreamAudioEnded):
        queues.task_done(update.chat_id)
        if queues.is_empty(update.chat_id):
            try:
                await client.leave_group_call(update.chat_id)
            except (NotInGroupCallError, NoActiveGroupCall):
                pass
        else:
            await client.change_stream(
                update.chat_id, queues.get(update.chat_id)["file"]
            )
