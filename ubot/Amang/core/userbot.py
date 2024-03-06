import sys
from pyrogram import *
from pyrogram.handlers import *
from pyrogram.types import *
from Amang.config import *
import pytgcalls
from ..logging import LOGGER

CLIENT_TYPE = pytgcalls.GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM
PLAYOUT_FILE = "/Amang/resources/vc.mp3"
OUTGOING_AUDIO_BITRATE_KBIT = 512

class Ubot(Client):
    _ubot = []
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vc = pytgcalls.GroupCallFactory(
        self, CLIENT_TYPE, OUTGOING_AUDIO_BITRATE_KBIT
    ).get_file_group_call(PLAYOUT_FILE)

    def on_message(self, filters=filters.Filter):
        def decorator(func):
            for ub in self._ubot:
                ub.add_handler(MessageHandler(func, filters))
            return func

        return decorator

    async def start(self):
        await super().start()
        if self not in self._ubot:
            self._ubot.append(self)
            
    async def stop(self):
        await super().stop()
        if self not in self._ubot:
            self._ubot.append(self)
