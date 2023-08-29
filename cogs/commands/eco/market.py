"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from discord import app_commands, Interaction, Embed, SelectOption, ButtonStyle, ui
from discord.ext import commands
from cogs.utils.constants import Emojis
from cogs.utils.functions import balance_check
from cogs.utils.transactions import DataGenerator
from cogs.utils.cooldown import set_cooldown
from cogs.utils.buttons import CloseButton
from cogs.utils.database.fetchdata import create_wallet, create_inventory_data
from yaml import Loader, load

yaml_file = open("cogs/assets/yaml_files/market_yamls/market.yml", "rb")
market = load(yaml_file, Loader=Loader)

fishfoods = market["fishfoods"]
ammonution = market["ammo"]

new_emoji = Emojis.new

class FishingFoodDropdown(ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            SelectOption(label=f"x{fishfoods[fishfood]['unit']} {fishfoods[fishfood]['name']} ", value = fishfood, description=f"{fishfoods[fishfood]['unit']} tanesi {fishfoods[fishfood]['price']:,} LC", emoji='🪱')
            for fishfood in fishfoods
        ]

        super().__init__(placeholder='Balık yemi seç...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):

        user = interaction.user
        value = self.values[0] # Selected option
        

        food_name = market["fishfoods"][value]["name"]
        food_unit = market["fishfoods"][value]["unit"]
        food_price = market["fishfoods"][value]["price"]

        user_wallet, w_collection = await create_wallet(self.bot, user.id)
        user_inv, i_collection = await create_inventory_data(self.bot, user.id)
        transaction_list = user_wallet["recent_transactions"]["transactions"]
        transactions = DataGenerator(transaction_list, food_price, False)

        
        if await balance_check(interaction, user_wallet["cash"], food_price) is False:
            return
        
        if "fishfoods" not in user_inv["items"]:
            fishfood_data = { "$set" : {"items.fishfoods" : {value: food_unit}}}
            await i_collection.update_one(user_inv ,fishfood_data)

        elif value not in user_inv["items"]["fishfoods"]:
            user_inv["items"]["fishfoods"].update({value: food_unit})
            await i_collection.replaceone({"_id": user.id}, user_inv)

        elif value in user_inv["items"]["fishfoods"]:
            user_inv["items"]["fishfoods"][value] += food_unit
            await i_collection.replace_one({"_id": user.id}, user_inv)

        user_wallet["cash"] -= food_price
        transaction_list = transactions.save_expense_data("market")
        await w_collection.replace_one({"_id": user.id}, user_wallet)

        await interaction.response.send_message(content = f"{new_emoji} :worm: **|** {interaction.user.mention} **{food_price:,} LC** ödeyerek {food_unit} adet **{food_name}** satın aldınız.")

class AmmoDropdown(ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            SelectOption(label=f"x{ammonution[ammo]['unit']} {ammonution[ammo]['name']} ", value = ammo, description=f"{ammonution[ammo]['unit']} tanesi {ammonution[ammo]['price']:,} LC")
            for ammo in ammonution
        ]

        super().__init__(placeholder='Mühimmat seç...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):

        user = interaction.user
        value = self.values[0] # Selected option

        ammo_name = market["ammo"][value]["name"]
        ammo_unit = market["ammo"][value]["unit"]
        ammo_price = market["ammo"][value]["price"]

        user_wallet, w_collection = await create_wallet(self.bot, user.id)
        user_inv, i_collection = await create_inventory_data(self.bot, user.id)
        transaction_list = user_wallet["recent_transactions"]["transactions"]
        transactions = DataGenerator(transaction_list, ammo_price, False)

        
        if await balance_check(interaction, user_wallet["cash"], ammo_price) is False:
            return
        
        if "ammo" not in user_inv["items"]:
            ammo_data = { "$set" : {"items.ammo" : {value: ammo_unit}}}
            await i_collection.update_one(user_inv, ammo_data)

        elif value not in user_inv["items"]["ammo"]:
            user_inv["items"]["ammo"].update({value: ammo_unit})
            await i_collection.replaceone({"_id": user.id}, user_inv)

        elif value in user_inv["items"]["ammo"]:
            user_inv["items"]["ammo"][value] += ammo_unit
            await i_collection.replace_one({"_id": user.id}, user_inv)

        user_wallet["cash"] -= ammo_price
        transaction_list = transactions.save_expense_data("market")
        await w_collection.replace_one({"_id": user.id}, user_wallet)

        await interaction.response.send_message(content = f"{new_emoji} **|** {interaction.user.mention} **{ammo_price:,} LC** ödeyerek {ammo_unit} adet **{ammo_name}** satın aldınız.")


class ButtonMenu(ui.View):

    @ui.button(label = "Balık Yemi", style = ButtonStyle.blurple)
    async def fishfood_button(self, interaction: Interaction, button):

        embed = Embed()
        embed.set_author(name="Menüden satın almak istediğiniz yem türünü seçiniz.")
        view = ui.View()
        view.add_item(FishingFoodDropdown())
        view.add_item(CloseButton(interaction.user.id))
        await interaction.response.send_message(embed = embed, view = view)
    
    @ui.button(label = "Mühimmat", style = ButtonStyle.blurple)
    async def ammo_button(self, interaction: Interaction, button):

        embed = Embed()
        embed.set_author(name="Menüden satın almak istediğiniz mühimmat türünü seçiniz.")
        view = ui.View()
        view.add_item(AmmoDropdown())
        view.add_item(CloseButton(interaction.user.id))
        await interaction.response.send_message(embed = embed, view = view)
    
class Market(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "market", description = "Open market and buy utilities")
    @app_commands.checks.dynamic_cooldown(set_cooldown(20))
    async def market(self, interaction: Interaction):

        embed = Embed(
            title = "Markete Hoş Geldiniz",
            description = """
            Bazı iş için gerekli araçları buradan LiCash karşılığında satın alabilirsiniz.
            Aşağıdaki butonlara tıklayarak açılan menüden istediğinizi satın alın. """,
            color = 0x2b2d31)
        view = ButtonMenu().add_item(CloseButton(interaction.user.id))
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Market(bot))