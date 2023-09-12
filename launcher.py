"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

import asyncio
import logging
import logging.handlers
import discord
import os
from main import Limon
from dotenv import load_dotenv

load_dotenv()
DB_CONNECTION = os.getenv("MONGO_CONNECTION")
TOKEN = os.getenv("BOT_TOKEN")
PREFIXES = ('.', '<@994143430504620072>', 'limon', 'lim', '10')

async def main():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    async with Limon(
            command_prefix = PREFIXES,
            intents = discord.Intents.default(),
            activity = discord.Streaming(
                name="Eco & Fun {/} | New UPDATE!",
                url="https://www.twitch.tv/iamabduley"),
            database_connection = str(DB_CONNECTION)
    ) as bot:
        await bot.start(str(TOKEN))

asyncio.run(main())
