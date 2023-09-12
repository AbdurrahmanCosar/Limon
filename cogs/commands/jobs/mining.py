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

basic_items_yaml = open("cogs/assets/yaml_files/market_yamls/basic_items.yml", "rb")
basic_item = load(basic_items_yaml, Loader=Loader)

mine_yaml = open("cogs/assets/yaml_files/job_yamls/mines.yml", "rb")
mines = load(mine_yaml, Loader=Loader)

class Mining(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def mine_goose(self):
        mine = choice(list(mines.keys()))
        name = mines[mine]["name"]
        weight = randint(10, 20)
        return name, weight, mine

    @app_commands.command(
            name="mining", 
            description="Go mining!",
            extras={
                'category': 'job',
                'help': "Kazmanızı alın ve maden kazın."
            })
    @app_commands.checks.dynamic_cooldown(set_cooldown(60))
    async def mining(self, interaction: Interaction):
        user = interaction.user
        inventory, collection = await create_inventory_data(self.bot, user.id)

        if "mining" not in inventory["items"]:
            mine = choice(list(mines.keys())[:4])
            name = mines[mine]["name"]
            weight = randint(5, 13)
            
            warning_message = f" {Emojis.warning_message} Bu kazma ile ağır ve farklı madenler çıkaramazsınız. Yeni bir kazma satın alın **`/store`**"
            message = f":gem: Harika! Basit bir kazma kullanarak madenden {weight}kg ağırlığında {name} çıkardınız.\n" + warning_message
            inventory["jobs_results"]["mines"].append(f"{mine}_{weight}")

        else:
            equipment = inventory["items"]["mining"]
            if equipment["durability"] < 4:
                return await interaction.response.send_message(content = f"{Emojis.whiteCross} Ekipmanınız eskimiş olmalı. Lütfen Jack ustaya gidin ve yenileyin.", ephemeral=True)
            equipment["durability"] -= 4

            

            if basic_item["mining"][equipment["custom_id"]]["type"] == "vehicle":
                if equipment["fuel"] < basic_item["mining"][equipment["custom_id"]]["liter_per_item"]:
                    return await interaction.response.send_message(content = f"{Emojis.whiteCross} :fuelpump: Aracınızın yakıtı bitmek üzere. Yakıt doldurmanız gerekiyor `/inventory > Garaj > Depoyu Doldur`", ephemeral=True)


                average_item = basic_item["mining"][equipment["custom_id"]]["average_item"]
                mine_count = randint(average_item - 1, average_item + 1)

                equipment["fuel"] -= (basic_item["mining"][equipment["custom_id"]]["liter_per_item"] * mine_count)
                excavated_mine = []

                for _ in range(mine_count):
                    name, weight, mine = self.mine_goose()
                    excavated_mine.append([name, weight])
                    inventory["jobs_results"]["mines"].append(f"{mine}_{weight}")
                    excavated_mine_ = "\n".join([f":gem: {mine[0]} - {mine[1]}m"  for mine in excavated_mine])
                    message = f":pick: Aracımız geri döndü. İşte çıkardığı madenler:\n{excavated_mine_}"

            else:
                name, weight, mine = self.mine_goose()

                message = f":gem: Harika! Madenden {weight}kg ağırlığında {name} çıkardınız."
                inventory["jobs_results"]["mines"].append(f"{mine}_{weight}")

        await add_xp(self.bot, user.id, "miner_xp")
        await collection.replace_one({"_id": user.id}, inventory)

        await interaction.response.send_message(content = ":pick: Madene iniyoruz..")
        await sleep(6)
        await interaction.edit_original_response(content = message)

async def setup(bot: commands.Bot):
    await bot.add_cog(Mining(bot))
