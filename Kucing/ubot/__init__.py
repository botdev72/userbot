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


class Ubot(Client):
    _ubot = []
    _prefix = {}
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.device_model = "reza-userbot"

    def on_message(self, filters=None):
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
        print(f"Starting Userbot ({self.me.id}|{self.me.first_name})")

    async def stop(self):
        await super().stop()
        if self in self._ubot:
            self._ubot.remove(self)
            

ubot = Ubot(
    name="ubot"
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
            name="bot",
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
