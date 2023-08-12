"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from discord import Embed, utils
from discord.ext import commands

class Stats(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
        
    
    @commands.command(hidden = True)
    @commands.is_owner()
    async def stats(self, ctx):
        
        delta = utils.utcnow() - self.bot.uptime
        delta = str(delta).split(".")[0]
        
        embed = Embed(
            description= f"**Guild Count**\n{len(self.bot.guilds)} servers!\n\n**Uptime**\n{delta}s!\n\n**Ping**\n🏓 Pong! {round(self.bot.latency * 1000)}ms",
            color = 0x36393F)
        await ctx.send(embed = embed)
        


async def setup(bot: commands.Bot):
    await bot.add_cog(Stats(bot))