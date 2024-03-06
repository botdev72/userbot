import asyncio
import logging
import os
import sys
import time
from datetime import datetime
from logging import *
from typing import Any, Dict
import logging
from logging.handlers import RotatingFileHandler
from aiohttp import ClientSession
from pyrogram import Client, __version__, enums, filters
from pyrogram.handlers import MessageHandler
from pyromod import listen
from pytgcalls import PyTgCalls


from .config import *

StartTime = time.time()
START_TIME = datetime.now()

aiosession = ClientSession()

cmd = cmd



logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("logs.txt", maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)

LOG = logging.getLogger(__name__)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            "logs.txt", maxBytes=5000000, backupCount=10
        ),
        logging.StreamHandler(),
    ],
)



logging.getLogger("asyncio").setLevel(logging.CRITICAL)
logging.getLogger("pytgcalls").setLevel(logging.WARNING)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pyrogram.client").setLevel(logging.WARNING)
logging.getLogger("pyrogram.session.auth").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram.session.session").setLevel(logging.CRITICAL)
logging.basicConfig(level=logging.INFO)

LOG = logging.getLogger(__name__)



def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)



bot = Client(
    name="ubot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    )


class Ubot(Client):
    __module__ = "pyrogram.client"
    _ubot = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_py = PyTgCalls(self)

    def on_message(self, filters=filters.Filter, group=-1):
        def decorator(func):
            for ub in self._ubot:
                ub.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator
        
    def pytgcalls_decorator(self):
        def decorator(func):
            for ub in self._ubot:
                try:
                    if func.__name__ != "stream_end":
                        ub.call_py.on_kicked()(func)
                        ub.call_py.on_closed_voice_chat()(func)
                        ub.call_py.on_left()(func)
                    else:
                        ub.call_py.on_stream_end()(func)
                except:
                    pass
            return func

        return decorator

    async def start(self):
        await super().start()
        await self.call_py.start()
        if self not in self._ubot:
            self._ubot.append(self)


ubot = Ubot(
    name="bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION, in_memory=True
)
