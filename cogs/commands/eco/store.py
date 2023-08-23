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
from cogs.utils.database.fetchdata import create_wallet, create_inventory_data
from yaml import load, Loader

item_yaml = open("cogs/assets/yaml_files/market_yamls/basic_items.yml", "rb")
items = load(item_yaml, Loader=Loader)
fishes = items["fishing"]
hunts = items["hunting"]
wood = items["forestry"]
mines = items["mining"]

sell = Emojis.sell
sold = Emojis.sold
new = Emojis.new
cross = Emojis.cross


class FishingEquipmentDropdown(ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            SelectOption(label=str(fishes[item]["name"]), value=item, description=f"{fishes[item]['price']:,} LC", emoji='🎣')
            for item in fishes]
        
        options.append(SelectOption(label="Ekipmanını Sat!", value="sellitem", description="Mevcut ekipmanını sat.", emoji=sell))

        super().__init__(placeholder='Balıkçılık Ekipmanı Seç...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        
        user = interaction.user
        value = self.values[0]
        fishing_item = fishes[value]

        user_wallet, w_collection = await create_wallet(self.bot, user.id)
        user_inventory, i_collection = await create_inventory_data(self.bot, user.id)

        if value == "sellitem":
            if "fishing" not in user_inventory["items"]:
                return await interaction.response.send_message(content = f"{cross} Mevcut bir balıkçılık ekipmanınız bulunmuyor.", ephemeral = True)
            else:
                name = fishing_item["name"]
                price = fishing_item["price"] * 60 // 100

                user_wallet["cash"] += int(price)
                user_inventory["items"].pop("fishing")

                await w_collection.replace_one({"_id": user.id}, user_wallet)
                await i_collection.replace_one({"_id": user.id}, user_inventory)

                await interaction.response.send_message(content = f"{sold} **{user.name} |** {name} ekipmanınızı {price:,} LC'e sattınız.")
        
        elif ("fishing" in user_inventory["items"]):
            return await interaction.response.send_message(content = f"{cross} Zaten bir balıkçılık ekipmanına sahipsiniz.", ephemeral = True)

        name = fishing_item["name"]
        price = fishing_item["price"]
        durability = 100

        if await balance_check(interaction, user_wallet["cash"], price) is False:
            return

        data = {"fishing": {"durability": durability}}

        user_inventory["items"].update(data)
        user_wallet["cash"] -= price

        await i_collection.replace_one({"_id": user.id}, user_inventory)
        await w_collection.replace_one({"_id": user.id}, user_wallet)

        await interaction.response.send_message(content = f"{new}🎣 **{user.name} |** {name} ekipmanını **{price:,} LC** ödeyerek satın aldınız.")

class HuntingEquipmentDropdown(ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            SelectOption(label=str(hunts[item]["name"]), value=item, description=f"{hunts[item]['price']:,} LC", emoji='🏹')
            for item in hunts
        ]
        options.append(SelectOption(label="Ekipmanını Sat!", value="sellitem", description="Mevcut ekipmanını sat.", emoji=sell))

        super().__init__(placeholder='Avcılık Ekipmanı Seç...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        user = interaction.user
        value = self.values[0]
        hunting_item = hunts[value]

        user_wallet, w_collection = await create_wallet(self.bot, user.id)
        user_inventory, i_collection = await create_inventory_data(self.bot, user.id)

        if value == "sellitem":
            if "hunting" not in user_inventory["items"]:
                return await interaction.response.send_message(content = f"{cross} Mevcut bir avcılık ekipmanınız bulunmuyor.", ephemeral = True)
            else:
                name = hunting_item["name"]
                price = hunting_item["price"] * 60 // 100

                user_wallet["cash"] += int(price)
                user_inventory["items"].pop("hunting")

                await w_collection.replace_one({"_id": user.id}, user_wallet)
                await i_collection.replace_one({"_id": user.id}, user_inventory)

                await interaction.response.send_message(content = f"{sold} **{user.name} |** {name} ekipmanınızı {price:,} LC'e sattınız.")
        
        elif ("hunting" in user_inventory["items"]):
            return await interaction.response.send_message(content = f"{cross} Zaten bir avcılık ekipmanına sahipsiniz.", ephemeral = True)

        name = hunting_item["name"]
        price = hunting_item["price"]
        durability = 100

        if await balance_check(interaction, user_wallet["cash"], price) is False:
            return

        data = {"hunting": {"durability": durability}}

        user_inventory["items"].update(data)
        user_wallet["cash"] -= price

        await i_collection.replace_one({"_id": user.id}, user_inventory)
        await w_collection.replace_one({"_id": user.id}, user_wallet)

        await interaction.response.send_message(content = f"{new}🏹 **{user.name} |** {name} ekipmanını **{price:,} LC** ödeyerek satın aldınız.")

class ForestryEquipmentDropdown(ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            SelectOption(label=str(wood[item]["name"]), value=item, description=f"Ortalama {wood[item]['average_tree']} Ağaç - {wood[item]['price']:,} LC", emoji='🌲')
            for item in wood
        ]
        options.append(SelectOption(label="Ekipmanını Sat!", value="sellitem", description="Mevcut ekipmanını sat.", emoji=sell))

        super().__init__(placeholder='Ormancılık Ekipmanı Seç...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        user = interaction.user
        value = self.values[0]
        forestry_item = wood[value]

        user_wallet, w_collection = await create_wallet(self.bot, user.id)
        user_inventory, i_collection = await create_inventory_data(self.bot, user.id)

        if value == "sellitem":
            if "forestry" not in user_inventory["items"]:
                return await interaction.response.send_message(content = f"{cross} Mevcut bir ormancılık ekipmanınız bulunmuyor.", ephemeral = True)
            else:
                name = forestry_item["name"]
                price = forestry_item["price"] * 60 // 100

                user_wallet["cash"] += int(price)
                user_inventory["items"].pop("forestry")

                await w_collection.replace_one({"_id": user.id}, user_wallet)
                await i_collection.replace_one({"_id": user.id}, user_inventory)

                await interaction.response.send_message(content = f"{sold} **{user.name} |** {name} ekipmanınızı {price:,} LC'e sattınız.")
        
        elif ("forestry" in user_inventory["items"]):
            return await interaction.response.send_message(content = f"{cross} Zaten bir ormancılık ekipmanına sahipsiniz.", ephemeral = True)
        
        name = forestry_item["name"]
        price = forestry_item["price"]

        if await balance_check(interaction, user_wallet["cash"], price) is False:
            return

        if forestry_item["type"] == "vehicle":
            data = {"forestry": {"durability": 100, "fuel": forestry_item["gas_tank_liter"]}}
            message = f"""{new}🌲 **{user.name} |** {name} ekipmanını **{price:,} LC** ödeyerek satın aldınız.\n
            `🪵Ortalama Ağaç: {forestry_item['average_tree']}`\n🪫`Yakıt Tüketimi/Ağaç: {forestry_item['liter_per_tree']}`\n⛽`Yakıt Deposu: {forestry_item['gas_tank_liter']}L`"""
        else:
            data = {"forestry": {"durability": 100}}
            message = f"{new}🌲 **{user.name} |** {name} ekipmanını **{price:,} LC** ödeyerek satın aldınız."

        user_wallet -= price
        user_inventory["items"].update(data)
        
        await w_collection.replace_one({"_id": user.id}, user_wallet)
        await i_collection.replace_one({"_id": user.id}, user_inventory)

        await interaction.response.send_message(content = message)

class MiningEquipmentDropdown(ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            SelectOption(label=str(mines[item]["name"]), value=item, description=f"Ortalama {mines[item]['average_mine']} Maden - {mines[item]['price']:,} LC", emoji='⛏️')
            for item in mines
        ]
        options.append(SelectOption(label="Ekipmanını Sat!", value="sellitem", description="Mevcut ekipmanını sat.", emoji=sell))

        super().__init__(placeholder='Madencilik Ekipmanı Seç...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        user = interaction.user
        value = self.values[0]
        mining_item = mines[value]

        user_wallet, w_collection = await create_wallet(self.bot, user.id)
        user_inventory, i_collection = await create_inventory_data(self.bot, user.id)

        if value == "sellitem":
            if "mining" not in user_inventory["items"]:
                return await interaction.response.send_message(content = f"{cross} Mevcut bir madencilik ekipmanınız bulunmuyor.", ephemeral = True)
            else:
                name = mining_item["name"]
                price = mining_item["price"] * 60 // 100

                user_wallet["cash"] += int(price)
                user_inventory["items"].pop("mining")

                await w_collection.replace_one({"_id": user.id}, user_wallet)
                await i_collection.replace_one({"_id": user.id}, user_inventory)

                await interaction.response.send_message(content = f"{sold} **{user.name} |** {name} ekipmanınızı {price:,} LC'e sattınız.")
        
        elif ("mining" in user_inventory["items"]):
            return await interaction.response.send_message(content = f"{cross} Zaten bir madencilik ekipmanına sahipsiniz.", ephemeral = True)
        
        name = mining_item["name"]
        price = mining_item["price"]

        if await balance_check(interaction, user_wallet["cash"], price) is False:
            return

        if mining_item["type"] == "vehicle":
            data = {"mining": {"durability": 100, "fuel": mining_item["gas_tank_liter"]}}
            message = f"""{new}⛏️ **{user.name} |** {name} ekipmanını **{price:,} LC** ödeyerek satın aldınız.\n
            `💎Ortalama Maden: {mining_item['average_mine']}`\n🪫`Yakıt Tüketimi/Maden: {mining_item['liter_per_mine']}`\n⛽`Yakıt Deposu: {mining_item['gas_tank_liter']}L`"""
        else:
            data = {"mining": {"durability": 100}}
            message = f"{new}⛏️ **{user.name} |** {name} ekipmanını **{price:,} LC** ödeyerek satın aldınız."

        user_wallet -= price
        user_inventory["items"].update(data)
        
        await w_collection.replace_one({"_id": user.id}, user_wallet)
        await i_collection.replace_one({"_id": user.id}, user_inventory)

        await interaction.response.send_message(content = message)

class CloseButton(ui.Button):
    def __init__(self, user_id):
        self.id = user_id
        super().__init__(label="Kapat", style=ButtonStyle.danger)

    async def callback(self, interaction: Interaction):
        if interaction.user.id != self.id:
            return await interaction.response.send_message(content = f"{cross} Bu menüyü kapatma izniniz bulunmuyor!", ephemeral = True)
        await interaction.message.delete()


class SecondaryButtonMenu(ui.View):
    
    @ui.button(label = "Balıkçılık", style=ButtonStyle.blurple, emoji='🎣')
    async def fishing_button(self, interaction: Interaction, button):
        view = ui.View()
        view.add_item(FishingEquipmentDropdown())
        view.add_item(CloseButton(interaction.user.id))
        embed = Embed(color=0x2b2d31).set_author(name="🎣 | Satın almak istediğiniz balıkçılık ekipmanını menüden seçiniz..")
        await interaction.response.send_message(embed = embed, view = view)

    @ui.button(label = "Avcılık", style=ButtonStyle.blurple, emoji='🏹')
    async def hunting_button(self, interaction: Interaction, button):
        view = ui.View()
        view.add_item(HuntingEquipmentDropdown())
        view.add_item(CloseButton(interaction.user.id))
        embed = Embed(color=0x2b2d31).set_author(name="🏹 | Satın almak istediğiniz avcılık ekipmanını menüden seçiniz..")
        await interaction.response.send_message(embed = embed, view = view)

    @ui.button(label = "Ormancılık", style=ButtonStyle.blurple, emoji='🌲')
    async def forestry_button(self, interaction: Interaction, button):
        view = ui.View()
        view.add_item(ForestryEquipmentDropdown())
        view.add_item(CloseButton(interaction.user.id))
        embed = Embed(color=0x2b2d31).set_author(name="🌲 | Satın almak istediğiniz ormancılık ekipmanını menüden seçiniz..")
        await interaction.response.send_message(embed = embed, view = view)

    @ui.button(label = "Madencilik", style=ButtonStyle.blurple, emoji='⛏️')
    async def mining_button(self, interaction: Interaction, button):
        view = ui.View()
        view.add_item(MiningEquipmentDropdown())
        view.add_item(CloseButton(interaction.user.id))
        embed = Embed(color=0x2b2d31).set_author(name="⛏️ | Satın almak istediğiniz madencilik ekipmanını menüden seçiniz..")
        await interaction.response.send_message(embed = embed, view = view)

class PrimaryButtonMenu(ui.View):
    
    @ui.button(label = "Ekipmanlar", style= ButtonStyle.blurple)
    async def equipments_button(self, interaction: Interaction, button):

        view = SecondaryButtonMenu()
        await interaction.response.edit_message(view = view)


class Store(commands.Cog):
    def __ini__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "store", description="Open store and buy equipment")
    async def store(self, interaction: Interaction):

        embed = Embed(
            title = "Mağazaya Hoş Geldiniz",
            description = """
            Mağazada iş yapmak için gerekli ekipmanları LiCash karşılığında satın alabilirsiniz.
            Aynı zamanda aldığınız eşyaları buradan satabilirsiniz. Ürünleri, fiyatlarının **`%60`** LiCash'e satabilirsiniz.
            """,
            color = 0x2b2d31)
        
        view = PrimaryButtonMenu()
        await interaction.response.send_message(embed = embed, view = view)
            
async def setup(bot: commands.Bot):
    await bot.add_cog(Store(bot))