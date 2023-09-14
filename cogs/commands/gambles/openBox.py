"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from asyncio import sleep
from discord import app_commands, Interaction
from discord.app_commands import Choice
from discord.ext import commands
from cogs.utils.functions import add_xp
from cogs.utils.constants import Emojis
from cogs.utils.cooldown import set_cooldown
from cogs.utils.database.fetchdata import create_wallet
from cogs.utils.functions import balance_check
from random import randint

morelicash = Emojis.morelicash

boxes = {
    # 'boxName': [name, boxPrice, mixValue, maxValue]
    "woodenBox": ["Tahta", 10000, 7000, 20000],
    "silverBox": ["Gümüş", 20000, 17000, 30000],
    "goldenBox": ["Altın", 50000, 35000, 60000],
    "platinBox": ["Platin", 70000, 59000, 80000],
    "diamondBox": ["Elmas", 100000, 50000, 210000]
}

class OpenBox(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def interaction_check(self, interaction: Interaction) -> bool:
        user = interaction.user
        data = interaction.namespace

        """
        * Interaction.data gives us only the first option
        * Interaction.namespace gives all options for the command
        """

        for i in data:
            if i[0] == "box":
                value = i[1]
                user_data, _ = await create_wallet(self.bot, user.id)
                check = await balance_check(interaction, user_data["cash"], boxes[value][1])

                if check:
                    await add_xp(self.bot, user.id, "gambler_xp")
                    return True
                return False
            return False

    @app_commands.command(
            name="open-box", 
            description="Open a box and get rich",
            extras={
                'category': 'gamble',
                'help': "Kutu açın ve zengin olun."
            })
    @app_commands.describe(box="Select a box")
    @app_commands.checks.dynamic_cooldown(set_cooldown(7200))
    @app_commands.choices(box=[
        Choice(name=f"Tahta Kasa - {boxes['woodenBox'][1]:,}LC", value="woodenBox"),
        Choice(name=f"Gümüş Kasa - {boxes['silverBox'][1]:,}LC" , value="silverBox"),
        Choice(name=f"Altın Kasa - {boxes['goldenBox'][1]:,}LC", value="goldenBox"),
        Choice(name=f"Platin Kasa - {boxes['platinBox'][1]:,}LC", value="platinBox"),
        Choice(name=f"Elmas Kasa - {boxes['diamondBox'][1]:,}LC", value="diamondBox"),
    ])
    async def openbox(self, interaction: Interaction, box: str):
        user = interaction.user
        user_data, collection = await create_wallet(self.bot, user.id)

        selected_box = boxes.get(box)
        reward = randint(selected_box[2], selected_box[3])
        percentage = ((reward - selected_box[1]) / selected_box[1]) * 100
        message = f"{selected_box[0]} kasa açıldı! Içinden tam **{reward:,}LC** çıktı. Kâr: **`%{(reward - selected_box[1]) /}`**"

        user_data["cash"] -= selected_box[1]
        user_data["cash"] += reward
        await collection.replace_one({"_id": user.id}, user_data)

        await interaction.response.send_message(content = ":gift: Kutu açılıyor..")
        await sleep(4)
        await interaction.edit_original_response(content = message)

async def setup(bot: commands.Bot):
    await bot.add_cog(OpenBox(bot))
