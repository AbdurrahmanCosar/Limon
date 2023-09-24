"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from discord import Embed, utils, app_commands, Interaction
from discord.ext import commands
from cogs.utils.constants import Users

class Stats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name = "ping",
        description = "View the bot latency",
        extras={
                'category': 'general',
                'help': "Botun gecikme değerlerini görüntüleyin."
            })
    async def stats(self, interaction: Interaction):

        delta = utils.utcnow() - self.bot.uptime
        delta = str(delta).split(".")[0]

        if interaction.user.id in Users.admins:
            embed = Embed(
                description = f"**Guild Count**\n{len(self.bot.guilds)} servers!\n\n**Uptime**\n{delta}s!\n\n**Ping**\n🏓 Pong! {round(self.bot.latency * 1000)}ms"
,
                color = 0x2b2d31)
            return await interaction.response.send_message(embed = embed, ephemeral = True)

        await interaction.response.send_message(content = f"🏓 Pong! {round(self.bot.latency * 1000)}ms", ephemeral = True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Stats(bot))
