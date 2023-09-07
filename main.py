"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

import os
from re import A
from typing import Optional
import discord
from discord.ext import commands
import motor.motor_asyncio
from cogs.utils.downloader import ImageDownloader
from cogs.utils.database.admin_db import get_collection
import asyncio


class Limon(commands.Bot):
    def __init__(
            self,
            *args,
            testing_guild_id: Optional[int] = None,
            database_connection: str,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.testing_guild_id = testing_guild_id
        self.database = motor.motor_asyncio.AsyncIOMotorClient(database_connection)

    async def download(self):
        if os.path.isdir("cogs/assets/images") is True:
            return print("Images have already downloaded")

        data, _ = await get_collection(self)
        downloader = await ImageDownloader(data['images']).start_download()
        if downloader is True:
            return print("Download is completed!")
        print("An error has occurred!")


    async def on_ready(self):
        self.uptime = discord.utils.utcnow()
        print("{} is online!".format(self.user.name))

    def extension_loader(self):

        initial_extensions = ["cogs.utils.handlers.runner"]
        folders = os.listdir("./cogs/commands")  # path of commands

        for folder in folders:
            if folder != "__pycache__":
                files = os.listdir(f"./cogs/commands/{folder}")

                for file in files:
                    if file != "__pycache__":
                        initial_extensions.append(f"cogs.commands.{folder}.{file[:-3]}")

        return initial_extensions

    async def setup_hook(self) -> None:
        await self.download()
        print(os.getcwd())
        initial_extensions = self.extension_loader()
        for extension in initial_extensions:
            await self.load_extension(extension)

        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            self.tree.copy_global_to(guild=guild)
        await self.tree.sync()  
