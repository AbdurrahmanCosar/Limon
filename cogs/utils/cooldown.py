from discord import app_commands, Interaction
from typing import Optional 
from cogs.utils.constants import Admin
from cogs.utils.database.fetchdata import create_inventory_data
from yaml import Loader, load

items_file = open("cogs/assets/yaml_files/market_yamls/basic_items.yml", "rb")
market_items = load(items_file, Loader = Loader) 

def set_cooldown(interaction: Interaction, cooldown: float = 10.0) -> Optional[app_commands.Cooldown]:
    def cooldown_func(interaction: Interaction) -> Optional[app_commands.Cooldown]:
        if interaction.user.id in Admin.admins:
            return None
        return app_commands.Cooldown(1, cooldown)
    return cooldown_func

async def cooldown_for_jobs(interaction: Interaction, bot, cooldown: float = 300.0) -> Optional[app_commands.Cooldown]:
    async def cooldown_func(interaction: Interaction) -> Optional[app_commands.Cooldown]:
        if interaction.user.id in Admin.admins:
            return None
        
        inventory, _ = await create_inventory_data(bot, interaction.user.id)

        if interaction.command.name == "fishing":
            if "fishing" not in inventory["items"]:
                return await interaction.response.send_message(
                    content=f"{Emojis.cross} Balık tutabilmek için bir balıkçılık ekipmanına sahip olmalısınız!",
                    ephemeral=True)
            
            if inventory["items"]["fishing"]["durability"] < 4:
                return await interaction.response.send_message(content = f"{Emojis.whiteCross} Oltanız eskimiş olmalı. Lütfen Jack ustaya gidin ve yenileyin.", ephemeral=True)

        elif interaction.command.name == "forestry":
            if "forestry" not in inventory["items"]:
                return await interaction.response.send_message(
                    content=f"{Emojis.cross} Ağaç kesebilmek için bir ormancılık ekipmanına sahip olmalısınız!",
                    ephemeral=True)
            equipment = inventory["items"]["forestry"]

            if equipment["durability"] < 4:
                return await interaction.response.send_message(content = f"{Emojis.whiteCross} Ekipmanınız eskimiş olmalı. Lütfen Jack ustaya gidin ve yenileyin.", ephemeral=True)
            elif equipment["fuel"] < market_items["forestry"][equipment["custom_id"]]["liter_per_tree"]:
                return await interaction.response.send_message(content = f"{Emojis.whiteCross} :fuelpump: Aracınızın yakıtı bitmek üzere. Yakıt doldurmanız gerekiyor `/inventory > Garaj > Depoyu Doldur`", ephemeral=True)

        elif interaction.command.name == "hunting":
            if ("hunting" not in inventory["items"]):
                return await interaction.response.send_message(
                    content=f"{Emojis.cross} Avcılık yapabilmek için bir av ekipmanına ihtiyacınız var.",
                    ephemeral=True) 
            
            weapon = inventory["items"]["hunting"]
            required_ammo = market_items["hunting"][weapon]["ammo"]

            if weapon["durability"] < 4:
                return await interaction.response.send_message(content = f"{Emojis.whiteCross} Ekipmanın eskimiş olmalı. Lütfen Jack ustaya gidin ve yenileyin.", ephemeral=True)

            if (
            required_ammo != None and
            ("ammo" not in inventory or inventory["ammo"][required_ammo] == 0) ):
                return await interaction.response.send_message(
                    content=f"{Emojis.whiteCross} Hiç cephanen yok! Cephane olmadan ava çıkamazsın.", 
                    ephemeral=True)

        elif interaction.command.name == "mining":
            if "mining" not in inventory["items"]:
                return await interaction.response.send_message(
                    content=f"{Emojis.cross} Maden kazabilmek için bir madencilik ekipmanına sahip olmalısınız!",
                    ephemeral=True)
            
            equipment = inventory["items"]["mining"]

            if equipment["durability"] < 4:
                return await interaction.response.send_message(content = f"{Emojis.whiteCross} Ekipmanınız eskimiş olmalı. Lütfen Jack ustaya gidin ve yenileyin.", ephemeral=True)
            elif equipment["fuel"] < market_items["mining"][equipment["custom_id"]]["liter_per_mine"]:
                return await interaction.response.send_message(content = f"{Emojis.whiteCross} :fuelpump: Aracınızın yakıtı bitmek üzere. Yakıt doldurmanız gerekiyor `/inventory > Garaj > Depoyu Doldur`", ephemeral=True)

        return app_commands.Cooldown(1, cooldown)
    return cooldown_func