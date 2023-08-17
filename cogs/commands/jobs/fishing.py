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
from cogs.utils.database.fetchdata import create_inventory_data
from cogs.utils.functions import add_point
from cogs.utils.constants import Emojis
from yaml import Loader, load
from random import choice, randint
from typing import List, Optional


fishes_file = open("cogs/assets/yaml_files/job_yamls/fishes.yml", "rb")
fishes = load(fishes_file, Loader = Loader) 

market_file = open("cogs/assets/yaml_files/market_yamls/market.yml", "rb")
market = load(market_file, Loader = Loader) 

class Fishing(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.fish_list = list(fishes.keys())

    def catch_fish(self):
        fish = choice(self.fish_list)
        name = fishes[fish]['name']
        size = randint(15,22)
        return name, size, fish

    async def food_autocompletion(
        self,
        interaction: Interaction, 
        current: str
        ) -> List[Choice[str]]:
        user = interaction.user
        inventory, collection = await create_inventory_data(self.bot, user.id)

        data = []
        # Remove food
        if "fishfoods" in inventory:
            fishoods = inventory["fishfoods"]
            fishfoods_in_market = market["fishfoods"]
            for food in fishoods:
                if fishoods[food] == 0:
                    fishoods.pop(food)
                data.append(
                    Choice(
                    name=f"{fishfoods_in_market[food]['name']} x{fishoods[food]}",
                    value=food)
                )

        return data[:24]

    
    @app_commands.command(name = "fishing", description="Go fishing!")
    @app_commands.describe(food = "Oltanıza hangi yemi takacaksınız?")
    @app_commands.autocomplete(food=food_autocompletion)
    async def fishing(self, interaction: Interaction, food: Optional[str]):

        user = interaction.user
        inventory, collection = await create_inventory_data(self.bot, user.id)

        # Rod Check

        if "fishing" not in inventory["items"]:
            return await interaction.response.send_message(
                content=f"{Emojis.cross} Balık tutabilmek için bir balıkçılık ekipmanına sahip olmalısınız!",
                ephemeral=True)

        # User's rod
        rod = inventory["items"]["fishing"]
        """*
        rod: {custom_id: "harpoon", durability: 96}
        """
        
        if rod["durability"] < 4:
            return await interaction.response.send_message(content = f"{Emojis.whiteCross} Oltanız eskimiş olmalı. Lütfen Jack ustaya gidin ve yenileyin.", ephemeral=True)
        rod["durability"] -= 4

        # Fish List
        

        if (food is None) and (rod["custom_id"] == "fishingrod"):
            return await interaction.response.send_message(content = f"{Emojis.whiteCross} Hey, yem takmayı unuttun! Yem olmadan balık tutamayız.", ephemeral= True)
        elif (food is not None):
            inventory["fishfoods"][food] - 1


        if rod["name"] == "fishnet":
            caught_fishes = []
            fish_count = randint(3,5)

            for _ in range(fish_count):
                name, size, fish = self.catch_fish()
                caught_fishes.append([name, size])
                inventory["jobs_results"]["fishes"].append(f"{fish}_{size}")

            caught_fishes_ = [f":fish: **{fish[0]}** - **{fish[1]}cm**\n" for fish_list in caught_fishes for fish in fish_list]
            first_message = ":fishing_pole_and_fish: Ağ atıldı.."
            message = f":fishing_pole_and_fish: **Ağ çekildi!** işte yakaladıklarımız:\n{caught_fishes_}"

        else:
            name, size, fish = self.catch_fish()
            
            first_message = ":fishing_pole_and_fish: Olta atıldı.."
            message = f":fishing_pole_and_fish: **Harika!** {size}cm uzunluğunda bir {name} yakaladınız."
            inventory["jobs_results"]["fishes"].append(f"{fish}_{size}")
        
        await add_point(self.bot, user.id, "fisher_xp")
        await collection.replace_one({"_id": user.id}, inventory)
        await interaction.response.send_message(content = first_message)
        await sleep(4)
        await interaction.edit_original_response(content = message)

async def setup(bot: commands.Bot):
    await bot.add_cog(Fishing(bot))