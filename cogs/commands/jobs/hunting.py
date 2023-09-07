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
from cogs.utils.cooldown import set_cooldown
from cogs.utils.functions import add_xp
from cogs.utils.constants import Emojis
from yaml import Loader, load
from random import choice, randint

hunts_files = open("cogs/assets/yaml_files/job_yamls/hunts.yml", "rb")
hunts = load(hunts_files, Loader=Loader)

market_file = open("cogs/assets/yaml_files/market_yamls/market.yml", "rb")
market_items = load(market_file, Loader = Loader) 

class Hunting(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def hunt_prey(self):
        hunt = choice(list(hunts.keys()))
        name = hunts[hunt]["name"]

        return name, hunt

    @app_commands.command(name = "hunting", description = "Go hunting!")
    @app_commands.checks.dynamic_cooldown(set_cooldown(60))
    async def hunting(self, interaction: Interaction):

        user = interaction.user
        inventory, collection = await create_inventory_data(self.bot, user.id)

        if "hunting" not in inventory["items"]:
            return await interaction.response.send_message(content=f"{Emojis.cross} Ava çıkabilmek için bir avcılık ekipmanına sahip olmalısınız!", ephemeral=True)

        weapon = inventory["items"]["hunting"]
        
        # TODO: Ammonution for the type of weapon will be removed
        if weapon['custom_id'] == "bow":
            required_ammo = "arrow"
        else:
            required_ammo = "ammo"
        
        if ("ammo" in inventory and inventory["ammo"][required_ammo] == 0) or (required_ammo not in inventory["ammo"]):
                return await interaction.response.send_message(content=f"{Emojis.whiteCross} Hiç cephanen yok! Cephane olmadan ava çıkamazsın.", ephemeral=True)

        if weapon["durability"] < 4:
            return await interaction.response.send_message(content = f"{Emojis.whiteCross} Ekipmanınız eskimiş olmalı. Lütfen Jack ustaya gidin ve yenileyin.", ephemeral=True)

        weapon["durability"] -= 4

        if weapon["custom_id"] == "trap":
            trap_count = randint(2,4)
            preyed_hunts = []

            for _ in range(trap_count):
                name, hunt = self.hunt_prey()
                preyed_hunts.append(name)
                inventory["jobs_results"]["hunts"].append(hunt)

            preyed_hunts = [f":deer: {name}\n" for name in preyed_hunts]
            first_mesage = f":mouse_trap: Av için **{trap_count}** tane kapan kuruldu!"
            message = f":mouse_trap: Kapanları kontrol ettik ve işte yakaladıklarımız:\n{preyed_hunts}"

        else:
            name, hunt = self.hunt_prey()
            first_mesage = ":bow_and_arrow: Av aranıyor.."
            message = f":bow_and_arrow: Harika! Bir **{name}** avladık."
            inventory["ammo"][required_ammo] -= 1
            inventory["jobs_results"]["hunts"].append(hunt)

        await add_xp(self.bot, user.id, "hunter_xp")
        await collection.replace_one({"_id": user.id}, inventory)

        await interaction.response.send_message(content = first_mesage)
        await sleep(4)
        await interaction.edit_original_response(content = message)

async def setup(bot: commands.Bot):
    await bot.add_cog(Hunting(bot))
