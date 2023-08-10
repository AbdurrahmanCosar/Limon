"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

import os
from typing import Optional
import discord
from discord.ext import commands
import motor.motor_asyncio

class Limon(commands.Bot):
    def __init__(
            self,
            *args,
            testing_guild_id: Optional[int] = None,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.testing_guild_id = testing_guild_id
        self.database = motor.motor_asyncio.AsyncIOMotorClient("DB_CONNECTION")
        self.initial_extensions = self.extension_loader()

    async def on_ready(self):
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

        for extension in self.initial_extensions:
            await self.load_extension(extension)

        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            self.tree.copy_global_to(guild=guild)
        await self.tree.sync()