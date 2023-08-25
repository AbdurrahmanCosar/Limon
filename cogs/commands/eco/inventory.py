"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from discord import app_commands, Interaction, Embed, ButtonStyle, ui
from discord.ext import commands
from cogs.utils.constants import Emojis
from cogs.utils.buttons import CloseButton
from cogs.utils.database.fetchdata import create_inventory_data
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

# WILL BE ADD GAS STATION

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

        if ("forestry" in user_items) and (items["forestry"][user_items["forestry"]] == "manual"):
            u_item = user_items["forestry"]
            i_item = items["forestry"][u_item]
            message += f":axe: {i_item['name']} - Hasar Durumu: **%{u_item['durability']}**\n"

        if ("mining" in user_items) and (items["mining"][user_items["mining"]] == "manual"):
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
        
        await interaction.response.edit_message(view= self)

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
        fishes_ = [f":fish: **{fish_dict[fish]['count']}**x {fishes_list[fish]['name']} - **{fish_dict['value']}**cm" for fish in fish_dict]
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
        mines_ = [f":gem: **{mine_dict[mine]['count']}**x {mines_list[mine]['name']} - **{mine_dict['value']}**kg" for mine in mine_dict]
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
        wood_ = [f":wood: **{wood_dict[w]['count']}**x {wood_list[w]['name']} - **{wood_dict['value']}**m" for w in wood_dict]
        wood_ = "\n".join(wood_) if len(wood_)>0 else "*Çantanızda hiç odun yok*"
        
        """-------------------Hunts-------------------"""
        hunts_dict = {}
        [hunts_.update({hunt: hunts_.get(hunt, 0) + 1}) for hunt in hunts]
        hunts_ = [f":deer: **{hunts_dict[hunt]['count']}**x {hunts_list[hunt]['name']}" for hunt in hunts_dict]
        wood_ = "\n".join(wood_) if len(wood_)>0 else "*Çantanızda hiç av yok*"
        
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

        forestry_vehice_message = "*Bir orman aracınız yok!*"
        mining_vehice_message = "*Bir maden aracınız yok!*"

        if ("forestry" in user_items) and (items["forestry"][user_items["forestry"]] =="vehicle"):
            
            u_vehicle = user_items["forestry"] # in user iventory
            i_vehicle = items["forestry"][u_vehicle["custom_id"]] # in basic_items.yml file
            forestry_vehice_message = f"""
            ***{i_vehicle['name']}***\n
            🪵`Ortalama Ağaç: {i_vehicle['average_tree']}`
            🛠️`Hasar Durumu: %{u_vehicle['durability']}`
            ⛽`Yakıt Deposu: {u_vehicle['fuel']}/**{i_vehicle['gas_tank_liter']}L**`
            """


        if ("mining" in user_items) and (items["mining"][user_items["mining"]] == "vehicle"):
            u_vehicle = user_items["mining"] # in user iventory
            i_vehicle = items["minig"][u_vehicle["custom_id"]] # in basic_items.yml file
            mining_vehice_message = f"""
            ***{i_vehicle['name']}***\n
            💎`Ortalama Maden: {i_vehicle['average_tree']}`
            🛠️`Hasar Durumu: %{u_vehicle['durability']}`
            ⛽`Yakıt Deposu: {u_vehicle['fuel']}/**{i_vehicle['gas_tank_liter']}L**`
            """
        embed = Embed(
            color=0x2b2d31, 
            description= f"""
            Bu sizin garajınız. Burada araçlarını ve durumarı görünür.
            \n════════════════════════════════\n
            {forestry_vehice_message}\n════════════════════════════════
            {mining_vehice_message}\n════════════════════════════════""")
        embed.set_author(name=f"{user.name} adlı kullanıcının garajı", icon_url = user.avatar.url)
        
        
        await interaction.response.edit_message(embed = embed, view = self)
        
        
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

