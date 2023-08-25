"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from asyncio import sleep
from discord import app_commands, Interaction
from discord.ext import commands
from cogs.utils.database.fetchdata import create_inventory_data
from cogs.utils.cooldown import cooldown_for_jobs
from cogs.utils.functions import add_xp
from cogs.utils.constants import Emojis
from yaml import Loader, load
from random import choice, randint

basic_items_yaml = open("cogs/assets/yaml_files/market_yamls/basic_items.yml", "rb")
basic_item = load(basic_items_yaml, Loader=Loader)

wood_yaml = open("cogs/assets/yaml_files/job_yamls/wood.yml", "rb")
wood = load(wood_yaml, Loader=Loader)


class Forestry(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def cut_down_tree(self):
        tree = choice(list(wood.keys()))
        name = wood[tree]["name"]
        size = randint(3, 20)
        return name, size, tree

    @app_commands.command(name="forestry", description="Go lumberjack!")
    @app_commands.checks.dynamic_cooldown(cooldown_for_jobs())
    async def forestry(self, interaction: Interaction):
        
        user = interaction.user
        inventory, collection = await create_inventory_data(self.bot, user.id)

        equipment = inventory["items"]["forestry"]
        equipment["durability"] -= 4


        if basic_item["forestry"][equipment["custom_id"]]["type"] != "vehicle":
            average_tree = basic_item["forestry"][equipment["custom_id"]]["average_tree"]
            tree_count = randint(average_tree - 1, average_tree + 1)

            equipment["fuel"] -= (basic_item["forestry"][equipment["custom_id"]]["liter_per_tree"] * tree_count)

            felled_tree = []

            for _ in range(tree_count):
                name, size, tree = self.cut_down_tree()
                felled_tree.append([name, size])
                inventory["jobs_results"]["wood"].append(f"{tree}_{size}")
            felled_tree_ = [f":wood: {tree[0]} - {tree[1]}m\n" for tree_list in felled_tree for tree in tree_list]
            message = f":articulated_lorry: Aracımız geri döndü. İşte kestiği ağaçlar:\n{felled_tree_}"
        
        else:
            name, size, tree = self.cut_down_tree()

            message = f":wood: Harika! {size} metre uzunluğunda bir {name} kestiniz."
            inventory["jobs_results"]["wood"].append(f"{tree}_{size}")            
        
        await add_xp(self.bot, user.id, "forester_xp")
        await collection.replace_one({"_id": user.id}, inventory)
        await interaction.response.send_message(content = ":evergreen_tree: Kesmek için bir ağaç arıyoruz..")
        await sleep(4)
        await interaction.edit_original_response(content = message)

async def setup(bot: commands.Bot):
    await bot.add_cog(Forestry(bot))


    
