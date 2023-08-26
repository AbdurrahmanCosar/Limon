"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from discord import app_commands, Interaction, ui, SelectOption, Embed
from discord.ext import commands
from cogs.utils.constants import Emojis
from cogs.utils.functions import balance_check
from cogs.utils.cooldown import set_cooldown
from cogs.utils.buttons import CloseButton
from cogs.utils.database.fetchdata import create_wallet, create_inventory_data
from yaml import Loader, load

item_yaml = open("cogs/assets/yaml_files/market_yamls/basic_items.yml", "rb")
basic_items = load(item_yaml, Loader=Loader)


class Dropdown(ui.Select):
    def __init__(self, client, items, uid):
        self.client = client
        self.items = items
        self.uid = uid
        
        options = list({
            SelectOption(label=f"%{v['durability']} -- {12 * (100 - v['durability'])} LC", value=k, description=basic_items[k][v["custom_id"]]["name"], emoji="🛠️")
            for k, v in self.items.items()
        })

        super().__init__(placeholder='Onarılacak Ekipmanını Seç...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        user = interaction.user

        if self.uid != user.id:
            return await interaction.response.send_message(content = "**👨‍🔧 Jack:** Hey, dur bakalım! <@{self.uid}> için buradayım. Bu menü ile etkileşimde bulunamazsın.", ephemeral = True)

        inventory, i_collection = await create_inventory_data(self.client, user.id)
        wallet, w_collection = await create_wallet(self.client, user.id)

        value = self.values[0]
        price = 12 * (100 - self.items[value]["durability"])
        name = basic_items[inventory["items"][value]]["name"]


        if await balance_check(interaction, wallet['cash'], price) is False:
            return
        
        inventory["items"][value]["durability"] = 100
        wallet['cash'] -= price
        
        await i_collection.replace_one({"_id": user.id}, inventory)
        await w_collection.replace_one({"_id": user.id}, wallet)

        try:
            value = self.values[0]
            option = [e for e in self.options if e.value == value][0]
            self.options.remove(option)
            await interaction.response.edit_message(view = self.view)
        except:
            await interaction.response.edit_message(view = None)

        await interaction.followup.send(content = f"🛠️ {user.mention}**| 👨‍🔧 Jack:** İşte oldu! Senin için **{name}** ekipmanını tamir ettim *(%100)*. Bunun için **{price:,} LC** ödedin.")

        
        
        
        


class Repairman(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "repair", description = "Go to Jack and repair your items")
    @app_commands.checks.dynamic_cooldown(set_cooldown())
    async def repairman(self, interaction: Interaction):

        user = interaction.user
        inventory, _ = await create_inventory_data(self.bot, user.id)


        items = {k:v for k, v in inventory["items"].items() if v["durability"] < 100}

        item_count = len(items)

        if item_count == 0:
            return await interaction.response.send_message(content = "**👨‍🔧 Jack:** Onarılması gereken bir ekipmanın yok. Önce onları kullanmalısın", ephemeral=True)

        view = ui.View()
        view.add_item(Dropdown(self.bot, items, user.id))
        view.add_item(CloseButton(user.id))

        embed = Embed(
            title="👨‍🔧 Tamirci Jack'e Hoş Geldiniz!",
            description = f"""
            Merhaba, ben Jack. Senin için eskimiş, hasarlı ekipmanlarını onarabilirim.
            - *Bakalım nelerin onarılması gerekiyormuş?*
                - *Onarılması gereken `{item_count}` ekipmanınız var.*
                - *Menüden bir tanesini seç, bende senin için o ekipmanı onarayım.*

            (Ücretler menüde yazıyor) 
            """,
            color = 0x2b2d31)

        await interaction.response.send_message(embed = embed, view = view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Repairman(bot))