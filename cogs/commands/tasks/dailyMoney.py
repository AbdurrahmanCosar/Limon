"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from discord.ext import commands, tasks
from random import randint

class DailyMoneyTask(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.daily_money_amount = 1000
        self.daily_money_task.start()

    @tasks.loop(hours=24)
    async def daily_money_task(self):
        print("Started Task: Daily Money")

        db = self.bot.database["limon"]
        collection = db["wallet"]

        money = randint(1000, 3400)
        self.daily_money_amount += money

        await collection.update_many(
            {},
            {
                "$inc" : {
                    "accumulated_money": self.daily_money_amount
                }
            }
        )
        print("Users were given money daily")

    @daily_money_task.before_loop
    async def before_daily_money_task(self):
        print('waiting...')
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):
    await bot.add_cog(DailyMoneyTask(bot))