"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from discord import app_commands, Interaction, Embed, ButtonStyle, ui, SelectOption
from discord.ext import commands
from cogs.utils.constants import Emojis, Game
from cogs.utils.buttons import CloseButton
from cogs.utils.functions import balance_check
from cogs.utils.transactions import DataGenerator
from cogs.utils.database.fetchdata import create_inventory_data, create_wallet
from cogs.utils.cooldown import set_cooldown
from yaml import Loader, load

cross = Emojis.cross

fishes_file = open("cogs/assets/yaml_files/job_yamls/fishes.yml", "rb")
fishes_list = load(fishes_file, Loader = Loader) 

mines_file = open("cogs/assets/yaml_files/job_yamls/mines.yml", "rb")
mines_list = load(mines_file, Loader = Loader) 

wood_file = open("cogs/assets/yaml_files/job_yamls/wood.yml", "rb")
wood_list = load(wood_file, Loader = Loader) 

hunt_file = open("cogs/assets/yaml_files/job_yamls/hunts.yml", "rb")
hunts_list = load(hunt_file, Loader = Loader) 

item_yaml = open("cogs/assets/yaml_files/market_yamls/basic_items.yml", "rb")
items = load(item_yaml, Loader = Loader) 

class Dropdown(ui.Select):
    def __init__(self, client: commands.Bot, vehicles: dict, uid: int):
        self.client = client
        self.vehicles = vehicles
        self.uid = uid

        options = list({
            SelectOption(label=f"%{v['fuel']} / {items[k][v['custom_id']]['gas_tank_liter']} -- {Game.FuelPerLiter * (items[k][v['custom_id']]['gas_tank_liter'] - v['fuel'])} LC", value=k, description=items[k][v['custom_id']]["name"], emoji="🛠️")
            for k, v in self.vehicles.items()
        })

        super().__init__(placeholder='Benzin Doldurulacak Aracını Seç...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        user = interaction.user

        if self.uid != user.id:
            return await interaction.response.send_message(content = "Hey, dur bakalım! <@{self.uid}> için buradayım. Bu menü ile etkileşimde bulunamazsın.", ephemeral = True)

        inventory, i_collection = await create_inventory_data(self.client, user.id)
        wallet, w_collection = await create_wallet(self.client, user.id)

        value = self.values[0]

        inventory_vehicle = inventory["items"][value]
        price = Game.FuelPerLiter * (items[value][inventory_vehicle["custom_id"]]["gas_tank_liter"] - self.vehicles[value]["fuel"])
        name = items[value][inventory_vehicle['custom_id']]["name"]

        transaction_list = wallet["recent_transactions"]["transactions"]
        transactions = DataGenerator(transaction_list, price, False)


        if await balance_check(interaction, wallet['cash'], price) is False:
            return

        gas_tank_liter = items[value][inventory_vehicle["custom_id"]]["gas_tank_liter"]

        inventory["items"][value]["fuel"] = gas_tank_liter
        wallet['cash'] -= price
        transaction_list = transactions.save_expense_data("fuel")

        await i_collection.replace_one({"_id": user.id}, inventory)
        await w_collection.replace_one({"_id": user.id}, wallet)

        try:
            value = self.values[0]
            option = [e for e in self.options if e.value == value][0]
            self.options.remove(option)
            await interaction.response.edit_message(view = self.view)
        except:
            await interaction.response.edit_message(view = None)

        await interaction.followup.send(content = f"⛽ **|** {user.mention} İşte oldu! Senin için **{name}** ekipmanının deposunu doldurdum *({gas_tank_liter}L)*. Bunun için **{price:,} LC** ödedin.")

class GasStationButton(ui.View):
    def __init__(self, client: commands.Bot, uid: int):
        super().__init__()
        self.client = client
        self.uid = uid

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user.id != self.uid:
            await interaction.response.send_message(content = f"{cross} Bu sizin garajınız değil. Buradaki butonları kullanamazsınız!", ephemeral = True)
            return False
        return True

    @ui.button(label="Benzin Doldur!", style=ButtonStyle.success, emoji="⛽")
    async def fuel_button(self, interaction: Interaction, button):
        user = interaction.user
        inventory, _ = await create_inventory_data(self.client, user.id)

        vehicles = {
            k:v 
            for k, v in inventory["items"].items()
            if k in ("forestry", "mining") and (items[k][v['custom_id']]["type"] == "vehicle") and (v["fuel"] < items[k][v['custom_id']]['gas_tank_liter'])}
    
        view = ui.View()
        view.add_item(Dropdown(self.client, vehicles, user.id))
        view.add_item(CloseButton(user.id))

        embed = Embed(
            title="⛽ Benzin İstasyonuna Hoş Geldiniz!",
            description = f"""
            Merhaba. Araçlarının depolarını fulleyelim!
            - *Bakalım hangilerini deposu boşmuş?*
                - *Doldurulması gereken `{len(vehicles)}` aracınız var.*
                - *Menüden bir tanesini seç ve deposunu doldur.*

            (Ücretler menüde yazıyor) 
            """,
            color = 0x2b2d31)

        await interaction.response.edit_message(embed = embed, view = view)


class ButtonMenu(ui.View):
    def __init__(self, uid, client):
        super().__init__()
        self.id = uid
        self.client = client

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user.id != self.id:
            await interaction.response.send_message(content = f"{cross} Bu sizin envanteriniz değil. Buradaki butonları kullanamazsınız!", ephemeral = True)
            return False
        return True

    def disable_buttons(self, button):
        for child in self.children:
            if child.custom_id != button:
                child.disabled = False
                child.style = ButtonStyle.blurple
            else:
                child.style = ButtonStyle.success
                child.disabled = True

    @ui.button(label = "Ekipmanlar", style = ButtonStyle.blurple, custom_id = "equipments_button")
    async def equipments_button(self, interaction: Interaction, button):
        self.disable_buttons("equipments_button")

        user = interaction.user
        inventory, collection = await create_inventory_data(self.client, user.id)

        user_items = inventory["items"]
        message = ""

        if ("forestry" in user_items) and (items["forestry"][user_items["forestry"]["custom_id"]]["type"] == "manual"):
            u_item = user_items["forestry"]
            i_item = items["forestry"][u_item["custom_id"]]
            message += f":axe: {i_item['name']} - Hasar Durumu: **%{u_item['durability']}**\n"

        if ("mining" in user_items) and (items["mining"][user_items["mining"]["custom_id"]]["type"] == "manual"):
            u_item = user_items["mining"]
            i_item = items["mining"][u_item["custom_id"]]
            message += f":pick: {i_item['name']} - Hasar Durumu: **%{u_item['durability']}**\n"

        if ("fishing" in user_items):
            u_item = user_items["fishing"]
            i_item = items["fishing"][u_item["custom_id"]]
            message += f":fishing_pole_and_fish: {i_item['name']} - Hasar Durumu: **%{u_item['durability']}**\n"

        if ("hunting" in user_items):
            u_item = user_items["hunting"]
            i_item = items["hunting"][u_item["custom_id"]]
            message += f":bow_and_arrow: {i_item['name']} - Hasar Durumu: **%{u_item['durability']}**\n"

        if len(message) == 0:
            message = "Hiç ekipmanınız yok"

        embed = Embed(
            color=0x2b2d31, 
            description= f"""
            Bunlar sizin ekipmanlarınız. Burada iş için gerekli ekipmanlarınız görünür. Eğer araç almışsanız bunu garajda görebilirsiniz.
            \n════════════════════════════════\n
            {message}""")
        embed.set_author(name=f"{user.name} adlı kullanıcının ekipmanları", icon_url = user.avatar.url)

        await interaction.response.edit_message(embed = embed, view=self)

    @ui.button(label  = "Çanta", style = ButtonStyle.blurple, custom_id = "backpack_button")
    async def backpack_button(self, interaction: Interaction, button):
        self.disable_buttons("backpack_button")

        user = interaction.user
        inventory, collection = await create_inventory_data(self.client, user.id)

        fishes = inventory["jobs_results"]["fishes"]
        mines = inventory["jobs_results"]["mines"]
        wood = inventory["jobs_results"]["wood"]
        hunts = inventory["jobs_results"]["hunts"]

        """-------------------Fishes-------------------"""
        key_value = [fish.split('_') for fish in fishes]
        fish_dict = {
            key: {
                'value': sum(int(value) for key_, value in key_value if key_ == key),
                'count': len([value for key_, value in key_value if key_ == key])
            }
            for key in set(key for key, _ in key_value)
        }
        fishes_ = [f":fish: **{fish_dict[fish]['count']}**x {fishes_list[fish]['name']} - **{fish_dict[fish]['value']}**cm" for fish in fish_dict]
        fishes_ = "\n".join(fishes_) if len(fishes_)>0 else "*Çantanızda hiç balık yok*"

        """-------------------Mines-------------------"""
        key_value = [mine.split('_') for mine in mines]
        mine_dict = {
            key: {
                'value': sum(int(value) for key_, value in key_value if key_ == key),
                'count': len([value for key_, value in key_value if key_ == key])
            }
            for key in set(key for key, _ in key_value)
        }
        mines_ = [f":gem: **{mine_dict[mine]['count']}**x {mines_list[mine]['name']} - **{mine_dict[mine]['value']}**kg" for mine in mine_dict]
        mines_ = "\n".join(mines_) if len(mines_)>0 else "*Çantanızda hiç maden yok*"

        """-------------------Wood-------------------"""
        key_value = [w.split('_') for w in wood]
        wood_dict = {
            key: {
                'value': sum(int(value) for key_, value in key_value if key_ == key),
                'count': len([value for key_, value in key_value if key_ == key])
            }
            for key in set(key for key, _ in key_value)
        }
        wood_ = [f":wood: **{wood_dict[w]['count']}**x {wood_list[w]['name']} - **{wood_dict[w]['value']}**m" for w in wood_dict]
        wood_ = "\n".join(wood_) if len(wood_)>0 else "*Çantanızda hiç odun yok*"
        
        """-------------------Hunts-------------------"""
        hunts_dict = {hunt: {"count": hunts.count(hunt)} for hunt in hunts}
        hunts_ = [f":deer: **{hunts_dict[hunt]['count']}**x {hunts_list[hunt]['name']}" for hunt in hunts_dict]
        hunts_ = "\n".join(hunts_) if len(hunts_)>0 else "*Çantanızda hiç av yok*"
        
        embed = Embed(
            color=0x2b2d31, 
            description= f"""
            Bu sizin çantanız. Burada rozetleriniz ve iş yaparak(balıkçılık, avcılık vs.) kazandıklarınız görünür.
            \n════════════════════════════════\n
            ***BALIKLAR:***\n{fishes_}\n════════════════════════════════
            ***AVLAR:***\n{hunts_}\n════════════════════════════════
            ***MADENLER:***\n{mines_}\n════════════════════════════════
            ***ODUNLAR:***\n{wood_}\n════════════════════════════════
            """)
        embed.set_author(name=f"{user.name} adlı kullanıcının çantası", icon_url = user.avatar.url)

        await interaction.response.edit_message(embed = embed, view= self)

    @ui.button(label = "Garaj", style = ButtonStyle.blurple, custom_id = "garage_button")
    async def garage_button(self, interaction: Interaction, button):
        self.disable_buttons("garage_button")

        user = interaction.user
        inventory, collection = await create_inventory_data(self.client, user.id)

        user_items = inventory["items"]

        forestry_vehicle_message = "*Bir orman aracınız yok!*"
        mining_vehicle_message = "*Bir maden aracınız yok!*"

        vehicle_count = 0

        if ("forestry" in user_items) and (items["forestry"][user_items["forestry"]["custom_id"]]["type"] =="vehicle"):

            u_vehicle = user_items["forestry"] # in user iventory
            i_vehicle = items["forestry"][u_vehicle["custom_id"]] # in basic_items.yml file
            forestry_vehicle_message = f"""
            ***{i_vehicle['name']}***\n
            🪵`Ortalama Ağaç: {i_vehicle['average_item']}`
            🛠️`Hasar Durumu: %{u_vehicle['durability']}`
            ⛽`Yakıt Deposu: {u_vehicle['fuel']}/**{i_vehicle['gas_tank_liter']}L**`
            """
            vehicle_count += 1

        if ("mining" in user_items) and (items["mining"][user_items["mining"]["custom_id"]]["type"] == "vehicle"):
            u_vehicle = user_items["mining"] # in user iventory
            i_vehicle = items["mining"][u_vehicle["custom_id"]] # in basic_items.yml file
            mining_vehicle_message = f"""
            ***{i_vehicle['name']}***\n
            💎`Ortalama Maden: {i_vehicle['average_item']}`
            🛠️`Hasar Durumu: %{u_vehicle['durability']}`
            ⛽`Yakıt Deposu: {u_vehicle['fuel']}/**{i_vehicle['gas_tank_liter']}L**`
            """
            vehicle_count += 1

        embed = Embed(
            color=0x2b2d31, 
            description= f"""
            Bu sizin garajınız. Burada araçlarını ve durumarı görünür.
            \n════════════════════════════════\n
            {forestry_vehicle_message}\n════════════════════════════════
            {mining_vehicle_message}\n════════════════════════════════""")
        embed.set_author(name=f"{user.name} adlı kullanıcının garajı", icon_url = user.avatar.url)

        view = GasStationButton(self.client, user.id)
        
        if vehicle_count == 0:
            view.fuel_button.disabled = True
            view.fuel_button.style = ButtonStyle.secondary

        await interaction.response.edit_message(embed = embed, view = view)

class Inventory(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "inventory", description="Open inventory and view your equipments/items")
    @app_commands.checks.dynamic_cooldown(set_cooldown(10))
    async def inventory(self, interaction: Interaction):
        embed = Embed(
            color=0x2b2d31, 
            description= f"Envanterinizdekileri görüntülemek için aşağıdaki butonları kullanabilirsiniz.")
        embed.set_author(name=f"{interaction.user.name} adlı kullanıcının garajı", icon_url = interaction.user.avatar.url)
        embed.add_field(name=":toolbox: Ekipmanar", value="Bu menüde ekipmanlarınızı görüntülersiniz. Ancak araçlarınızı burada göremezsiniz. Onun için **Garaj** butonuna tıklayın", inline=False)
        embed.add_field(name=":shopping_bags: Çanta", value="Bu menüde balıklarınızı, avlarınızı, odunlarınızı ve madenlerinizi görüntüleyebilirsiniz.", inline=False)
        embed.add_field(name=":truck: Garaj",value="Bu menüde iş için satın aldığınızı araçları ve durumlarını görüntüleyebilirsiniz", inline=False)

        view = ButtonMenu(interaction.user.id, self.bot).add_item(CloseButton(interaction.user.id))
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Inventory(bot))
