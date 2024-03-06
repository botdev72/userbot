import asyncio
import logging
import os
import sys
import time
from datetime import datetime
from pyrogram import *
from Amang.core.bot import AmangBot
from Amang.core.userbot import Ubot
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from aiohttp import ClientSession
from .config import *
from .logging import LOGGER
from pyromod import listen

StartTime = time.time()
START_TIME = datetime.now()

aiosession = ClientSession()

mongo = MongoClient(MONGO_URL)

DATABASE_URL = DB_URL

cmd = cmd

ubot = Ubot(
    name="bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING, in_memory=True
)


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