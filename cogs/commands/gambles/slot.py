"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""
from asyncio import sleep
from discord import app_commands, Interaction
from discord.ext import commands
from cogs.utils.constants import Game, Emojis
from cogs.utils.cooldown import set_cooldown
from cogs.utils.functions import balance_check, add_xp
from cogs.utils.database.fetchdata import create_wallet
import random as r

MAX_BET_VALUE = Game.max_bet_value
slot_left = Emojis.slotleft
slot_mid = Emojis.slotmid
slot_right = Emojis.slotright
slot_seven = Emojis.slotseven
slot_cherry = Emojis.slotcherry
slot_cupcake = Emojis.slotcupcake
slot_heart = Emojis.slotheart
licash = Emojis.licash

class Slot(commands.Cog):
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
            if i[0] == "amount":
                value = i[1]
                user_data, collection = await create_wallet(self.bot, user.id)
                check = await balance_check(interaction, user_data["cash"], value)

                if check:
                    await add_xp(self.bot, user.id, "gamble_xp")
                    return True
                return False
            return False

    @app_commands.command(name="slot", description="Play slot")
    @app_commands.describe(amount="Enter the bet amount")
    @app_commands.checks.dynamic_cooldown(set_cooldown())
    async def slot(self, interaction: Interaction, amount: app_commands.Range[int, 1, MAX_BET_VALUE]):
        user = interaction.user
        user_data, collection = await create_wallet(self.bot, user.id)

        await interaction.response.send_message(f"`LİM SLOT`\n{slot_left}{slot_right}{slot_left}\n`------->` {licash}{amount:,}\n`------->` ???")
        await sleep(3)

        cupcake_reward = 5
        heart_reward = 2
        seven_reward = 3

        slots = {
            0 : slot_cherry,
            1 : slot_heart,
            2 : slot_seven,
            3 : slot_cupcake
        }

        rand = (r.randint(1, 1000) / 10)

        result1 = None
        result2 = None
        result3 = None

        win = amount

        if rand <= 30:
            result1 = slots[0]
            result2 = slots[0]
            result3 = slots[0]

        elif rand <= 40:
            win *= heart_reward

            result1 = slots[1]
            result2 = slots[1]
            result3 = slots[1]

        elif rand <= 48:
            win *= seven_reward

            result1 = slots[2]
            result2 = slots[2]
            result3 = slots[2]

        elif float(rand) <= 50:
            win *= cupcake_reward

            result1 = slots[3]
            result2 = slots[3]
            result3 = slots[3]

        else:
            result1 = r.choice(slots)
            result2 = r.choice(slots)
            result3 = r.choice(slots)

            while (result1 == result2 and result1 == result3):

                result1 = r.choice(slots)
                result2 = r.choice(slots)
                result3 = r.choice(slots)
            else:
                user_data['cash'] -= amount
                await collection.replace_one({"_id" : user.id}, user_data)
                await interaction.edit_original_response(content = f"`LİM SLOT`\n{result1}{result2}{result3}\n`------->` {licash}{amount:,}\n`------->` Kaybettin ;c")
                return

        user_data['cash'] += win
        await collection.replace_one({"_id" : user.id}, user_data)
        await interaction.edit_original_response(content = f"`LİM SLOT`\n{result1}{result2}{result3}\n`------->` {licash}{amount:,}\n`------->` {licash}{win:,}")

async def setup(bot :commands.Bot):
    await bot.add_cog(Slot(bot))
