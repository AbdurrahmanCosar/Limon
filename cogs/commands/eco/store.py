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
    def __init__(self, bot):
        self.bot = bot

        options = [
            SelectOption(label=str(fishes[item]["name"]), value=item, description=f"{fishes[item]['price']:,} LC", emoji='🎣')
            for item in fishes]
        options.append(SelectOption(label="Ekipmanını Sat!", value="sellitem", description="Mevcut ekipmanını sat.", emoji=sell))

        super().__init__(placeholder='Balıkçılık Ekipmanı Seç...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        try:
            user = interaction.user
            value = self.values[0]

            user_wallet, w_collection = await create_wallet(self.bot, user.id)
            user_inventory, i_collection = await create_inventory_data(self.bot, user.id)

            if value == "sellitem":
                if "fishing" not in user_inventory["items"]:
                    return await interaction.response.send_message(content = f"{cross} Mevcut bir balıkçılık ekipmanınız bulunmuyor.", ephemeral = True)
                else:
                    name = fishes[value]["name"]
                    price = fishes[value]["price"] * 60 // 100

                    user_wallet["cash"] += int(price)
                    user_inventory["items"].pop("fishing")

                    await w_collection.replace_one({"_id": user.id}, user_wallet)
                    await i_collection.replace_one({"_id": user.id}, user_inventory)

                    await interaction.response.send_message(content = f"{sold} **{user.name} |** {name} ekipmanınızı {price:,} LC'e sattınız.")

            elif ("fishing" in user_inventory["items"]):
                return await interaction.response.send_message(content = f"{cross} Zaten bir balıkçılık ekipmanına sahipsiniz.", ephemeral = True)

            name = fishes[value]["name"]
            price = fishes[value]["price"]
            durability = 100

            transaction_list = user_wallet["recent_transactions"]["transactions"]
            print(transaction_list)
            transactions = DataGenerator(transaction_list, price, False)
            print(transactions.print_transaction)


            if await balance_check(interaction, user_wallet["cash"], price) is False:
                return

            data = {"fishing": {"custom_id": value,"durability": durability}}

            user_inventory["items"].update(data)
            user_wallet["cash"] -= price
            transaction_list = transactions.save_expense_data("store")

            await i_collection.replace_one({"_id": user.id}, user_inventory)
            await w_collection.replace_one({"_id": user.id}, user_wallet)

            await interaction.response.send_message(content = f"{new}🎣 **{user.name} |** {name} ekipmanını **{price:,} LC** ödeyerek satın aldınız.")
        except Exception as e:
            print(e)

class HuntingEquipmentDropdown(ui.Select):
    def __init__(self, bot):
        self.bot = bot

        options = [
            SelectOption(label=str(hunts[item]["name"]), value=item, description=f"{hunts[item]['price']:,} LC", emoji='🏹')
            for item in hunts
        ]
        options.append(SelectOption(label="Ekipmanını Sat!", value="sellitem", description="Mevcut ekipmanını sat.", emoji=sell))

        super().__init__(placeholder='Avcılık Ekipmanı Seç...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        user = interaction.user
        value = self.values[0]

        user_wallet, w_collection = await create_wallet(self.bot, user.id)
        user_inventory, i_collection = await create_inventory_data(self.bot, user.id)

        if value == "sellitem":
            if "hunting" not in user_inventory["items"]:
                return await interaction.response.send_message(content = f"{cross} Mevcut bir avcılık ekipmanınız bulunmuyor.", ephemeral = True)
            else:
                name = hunts[value]["name"]
                price = hunts[value]["price"] * 60 // 100

                user_wallet["cash"] += int(price)
                user_inventory["items"].pop("hunting")

                await w_collection.replace_one({"_id": user.id}, user_wallet)
                await i_collection.replace_one({"_id": user.id}, user_inventory)

                await interaction.response.send_message(content = f"{sold} **{user.name} |** {name} ekipmanınızı {price:,} LC'e sattınız.")

        elif ("hunting" in user_inventory["items"]):
            return await interaction.response.send_message(content = f"{cross} Zaten bir avcılık ekipmanına sahipsiniz.", ephemeral = True)

        name = hunts[value]["name"]
        price = hunts[value]["price"]
        durability = 100

        if await balance_check(interaction, user_wallet["cash"], price) is False:
            return

        transaction_list = user_wallet["recent_transactions"]["transactions"]
        transactions = DataGenerator(transaction_list, price, False)

        print(transactions.print_transaction)

        data = {"hunting": {"custom_id": value, "durability": durability}}

        user_inventory["items"].update(data)
        user_wallet["cash"] -= price
        transaction_list = transactions.save_expense_data("store")

        await i_collection.replace_one({"_id": user.id}, user_inventory)
        await w_collection.replace_one({"_id": user.id}, user_wallet)

        await interaction.response.send_message(content = f"{new}🏹 **{user.name} |** {name} ekipmanını **{price:,} LC** ödeyerek satın aldınız.")

class ForestryEquipmentDropdown(ui.Select):
    def __init__(self, bot):
        self.bot = bot

        options = [
            SelectOption(label=str(wood[item]["name"]), value=item, description=f"Ortalama {wood[item]['average_item']} Ağaç - {wood[item]['price']:,} LC", emoji='🌲')
            for item in wood
        ]
        options.append(SelectOption(label="Ekipmanını Sat!", value="sellitem", description="Mevcut ekipmanını sat.", emoji=sell))

        super().__init__(placeholder='Ormancılık Ekipmanı Seç...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        user = interaction.user
        value = self.values[0]

        user_wallet, w_collection = await create_wallet(self.bot, user.id)
        user_inventory, i_collection = await create_inventory_data(self.bot, user.id)

        if value == "sellitem":
            if "forestry" not in user_inventory["items"]:
                return await interaction.response.send_message(content = f"{cross} Mevcut bir ormancılık ekipmanınız bulunmuyor.", ephemeral = True)
            else:
                name = wood[value]["name"]
                price = wood[value]["price"] * 60 // 100

                user_wallet["cash"] += int(price)
                user_inventory["items"].pop("forestry")

                await w_collection.replace_one({"_id": user.id}, user_wallet)
                await i_collection.replace_one({"_id": user.id}, user_inventory)

                return await interaction.response.send_message(content = f"{sold} **{user.name} |** {name} ekipmanınızı {price:,} LC'e sattınız.")

        elif ("forestry" in user_inventory["items"]):
            return await interaction.response.send_message(content = f"{cross} Zaten bir ormancılık ekipmanına sahipsiniz.", ephemeral = True)

        name = wood[value]["name"]
        price = wood[value]["price"]

        if await balance_check(interaction, user_wallet["cash"], price) is False:
            return

        transaction_list = user_wallet["recent_transactions"]["transactions"]
        transactions = DataGenerator(transaction_list, price, False)

        if wood[value]["type"] == "vehicle":
            data = {"forestry": {"custom_id": value, "durability": 100, "fuel": wood[value]["gas_tank_liter"]}}
            message = f"""{new}🌲 **{user.name} |** {name} ekipmanını **{price:,} LC** ödeyerek satın aldınız.\n
            `🪵Ortalama Ağaç: {wood[value]['average_item']}`\n🪫`Yakıt Tüketimi/Ağaç: {wood[value]['liter_per_item']}`\n⛽`Yakıt Deposu: {wood[value]['gas_tank_liter']}L`"""
        else:
            data = {"forestry": {"custom_id": value, "durability": 100}}
            message = f"{new}🌲 **{user.name} |** {name} ekipmanını **{price:,} LC** ödeyerek satın aldınız."

        user_wallet["cash"] -= price
        user_inventory["items"].update(data)
        transaction_list = transactions.save_expense_data("store")

        await w_collection.replace_one({"_id": user.id}, user_wallet)
        await i_collection.replace_one({"_id": user.id}, user_inventory)

        await interaction.response.send_message(content = message)

class MiningEquipmentDropdown(ui.Select):
    def __init__(self, bot):
        self.bot = bot

        options = [
            SelectOption(label=str(mines[item]["name"]), value=item, description=f"Ortalama {mines[item]['average_item']} Maden - {mines[item]['price']:,} LC", emoji='⛏️')
            for item in mines
        ]
        options.append(SelectOption(label="Ekipmanını Sat!", value="sellitem", description="Mevcut ekipmanını sat.", emoji=sell))

        super().__init__(placeholder='Madencilik Ekipmanı Seç...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        user = interaction.user
        value = self.values[0]

        user_wallet, w_collection = await create_wallet(self.bot, user.id)
        user_inventory, i_collection = await create_inventory_data(self.bot, user.id)

        if value == "sellitem":
            if "mining" not in user_inventory["items"]:
                return await interaction.response.send_message(content = f"{cross} Mevcut bir madencilik ekipmanınız bulunmuyor.", ephemeral = True)
            else:
                name = mines[value]["name"]
                price = mines[value]["price"] * 60 // 100

                user_wallet["cash"] += int(price)
                user_inventory["items"].pop("mining")

                await w_collection.replace_one({"_id": user.id}, user_wallet)
                await i_collection.replace_one({"_id": user.id}, user_inventory)

                await interaction.response.send_message(content = f"{sold} **{user.name} |** {name} ekipmanınızı {price:,} LC'e sattınız.")

        elif ("mining" in user_inventory["items"]):
            return await interaction.response.send_message(content = f"{cross} Zaten bir madencilik ekipmanına sahipsiniz.", ephemeral = True)

        name = mines[value]["name"]
        price = mines[value]["price"]

        if await balance_check(interaction, user_wallet["cash"], price) is False:
            return

        transaction_list = user_wallet["recent_transactions"]["transactions"]
        transactions = DataGenerator(transaction_list, price, False)

        if mines[value]["type"] == "vehicle":
            data = {"mining": {"custom_id": value, "durability": 100, "fuel": mines[value]["gas_tank_liter"]}}
            message = f"""{new}⛏️ **{user.name} |** {name} ekipmanını **{price:,} LC** ödeyerek satın aldınız.\n
            `💎Ortalama Maden: {mines[value]['average_item']}`\n🪫`Yakıt Tüketimi/Maden: {mines[value]['liter_per_item']}`\n⛽`Yakıt Deposu: {mines[value]['gas_tank_liter']}L`"""
        else:
            data = {"mining": {"custom_id": value, "durability": 100}}
            message = f"{new}⛏️ **{user.name} |** {name} ekipmanını **{price:,} LC** ödeyerek satın aldınız."

        user_wallet["cash"] -= price
        user_inventory["items"].update(data)
        transaction_list = transactions.save_expense_data("store")

        await w_collection.replace_one({"_id": user.id}, user_wallet)
        await i_collection.replace_one({"_id": user.id}, user_inventory)

        await interaction.response.send_message(content = message)

class SecondaryButtonMenu(ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @ui.button(label = "Balıkçılık", style=ButtonStyle.blurple, emoji='🎣')
    async def fishing_button(self, interaction: Interaction, button):
        view = ui.View()
        view.add_item(FishingEquipmentDropdown(self.bot))
        view.add_item(CloseButton(interaction.user.id))
        embed = Embed(color=0x2b2d31).set_author(name="🎣 | Satın almak istediğiniz balıkçılık ekipmanını menüden seçiniz..")
        await interaction.response.send_message(embed = embed, view = view)


    @ui.button(label = "Avcılık", style=ButtonStyle.blurple, emoji='🏹')
    async def hunting_button(self, interaction: Interaction, button):
        view = ui.View()
        view.add_item(HuntingEquipmentDropdown(self.bot))
        view.add_item(CloseButton(interaction.user.id))
        embed = Embed(color=0x2b2d31).set_author(name="🏹 | Satın almak istediğiniz avcılık ekipmanını menüden seçiniz..")
        await interaction.response.send_message(embed = embed, view = view)

    @ui.button(label = "Ormancılık", style=ButtonStyle.blurple, emoji='🌲')
    async def forestry_button(self, interaction: Interaction, button):
        view = ui.View()
        view.add_item(ForestryEquipmentDropdown(self.bot))
        view.add_item(CloseButton(interaction.user.id))
        embed = Embed(color=0x2b2d31).set_author(name="🌲 | Satın almak istediğiniz ormancılık ekipmanını menüden seçiniz..")
        await interaction.response.send_message(embed = embed, view = view)

    @ui.button(label = "Madencilik", style=ButtonStyle.blurple, emoji='⛏️')
    async def mining_button(self, interaction: Interaction, button):
        view = ui.View()
        view.add_item(MiningEquipmentDropdown(self.bot))
        view.add_item(CloseButton(interaction.user.id))
        embed = Embed(color=0x2b2d31).set_author(name="⛏️ | Satın almak istediğiniz madencilik ekipmanını menüden seçiniz..")
        await interaction.response.send_message(embed = embed, view = view)

class PrimaryButtonMenu(ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @ui.button(label = "Ekipmanlar", style= ButtonStyle.blurple)
    async def equipments_button(self, interaction: Interaction, button):
        view = SecondaryButtonMenu(self.bot)
        await interaction.response.edit_message(view = view)

class Store(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
            name = "store", 
            description = "Open store and buy equipment",
            extras = {
                'category': 'job',
                'help': "İş yapmak için gerekli ekipmanları satın alın."
            })
    @app_commands.checks.dynamic_cooldown(set_cooldown(20))
    async def store(self, interaction: Interaction):
        embed = Embed(
            title = "Mağazaya Hoş Geldiniz",
            description = """
            Mağazada iş yapmak için gerekli ekipmanları LiCash karşılığında satın alabilirsiniz.
            Aynı zamanda aldığınız eşyaları buradan satabilirsiniz. Ürünleri, fiyatlarının **`%60`** LiCash'e satabilirsiniz.
            """,
            color = 0x2b2d31)

        view = PrimaryButtonMenu(self.bot)
        view.add_item(CloseButton(interaction.user.id))
        await interaction.response.send_message(embed = embed, view = view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Store(bot))
