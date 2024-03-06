import asyncio
import re
import os
import sys
import time
from os import environ, execle
from datetime import datetime
from pyrogram import *

from pyrogram.handlers import *
from pyrogram.types import *
from ubot.utils.dbfunctions import get_pref
import pytgcalls

from aiohttp import ClientSession
from .config import *
from .logging import LOGGER
from pyromod import listen
StartTime = time.time()
START_TIME = datetime.now()

aiosession = ClientSession()

loop = asyncio.get_event_loop()

CLIENT_TYPE = pytgcalls.GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM
PLAYOUT_FILE = "/ubot/resources/vc.mp3"
OUTGOING_AUDIO_BITRATE_KBIT = 218


class Ubot(Client):
    _ubot = []
    _prefix = {}
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_id = API_ID
        self.api_hash = API_HASH
        self.device_model = "alcantara-ubot"
        self.vc = pytgcalls.GroupCallFactory(
            self, CLIENT_TYPE, OUTGOING_AUDIO_BITRATE_KBIT
        ).get_file_group_call(PLAYOUT_FILE)

    def on_message(self, filters=filters.Filter):
        def decorator(func):
            for ub in self._ubot:
                ub.add_handler(MessageHandler(func, filters))
            return func

        return decorator
        
    def set_prefix(self, user_id, prefix):
        self._prefix[self.me.id] = prefix

    async def start(self):
        await super().start()
        handler = await get_pref(self.me.id)
        if handler:
            self._prefix[self.me.id] = handler
        else:
            self._prefix[self.me.id] = ["."]
        self._ubot.append(self)

    async def stop(self):
        await super().stop()
        if self in self._ubot:
            self._ubot.remove(self)
            

ubot = Ubot(
    name="bot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    device_model="alcantara-Ubot",
)

async def get_prefix(user_id):
    return ubot._prefix.get(user_id, ".")

def anjay(cmd):
    command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")
 
    async def func(_, client, message):
        if message.text and message.from_user:
            text = message.text.strip()
            username = client.me.username or ""
            prefixes = await get_prefix(client.me.id)

            if not text:
                return False

            for prefix in prefixes:
                if not text.startswith(prefix):
                    continue

                without_prefix = text[len(prefix) :]

                for command in [cmd]:
                    if not re.match(
                        rf"^(?:{command}(?:@?{username})?)(?:\s|$)",
                        without_prefix,
                        flags=re.IGNORECASE if not False else 0,
                    ):
                        continue

                    without_command = re.sub(
                        rf"{command}(?:@?{username})?\s?",
                        "",
                        without_prefix,
                        count=1,
                        flags=re.IGNORECASE if not False else 0,
                    )
                    message.command = [command] + [
                        re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                        for m in command_re.finditer(without_command)
                    ]

                    return True

        return False

    return filters.create(func)


class Bot(Client):
    def __init__(self):
        super().__init__(
            name="ubot",
            api_hash=API_HASH,
            api_id=API_ID,
            bot_token=BOT_TOKEN,
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = self.me
        LOGGER(__name__).info(
            f"@{usr_bot_me.username} "
        )

    async def stop(self, *args):
        await super().stop()
        LOGGER(__name__).info("Bot stopped. Bye.")

bot = Bot()
