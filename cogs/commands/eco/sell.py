"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from discord import app_commands, Interaction, Embed, ButtonStyle, ui
from discord.ext import commands
from cogs.utils.constants import Emojis, Game
from cogs.utils.buttons import CloseButton
from cogs.utils.database.fetchdata import create_inventory_data, create_wallet
from yaml import Loader, load

fishes_file = open("cogs/assets/yaml_files/job_yamls/fishes.yml", "rb")
fishes_list = load(fishes_file, Loader = Loader) 

mines_file = open("cogs/assets/yaml_files/job_yamls/mines.yml", "rb")
mines_list = load(mines_file, Loader = Loader) 

wood_file = open("cogs/assets/yaml_files/job_yamls/wood.yml", "rb")
wood_list = load(wood_file, Loader = Loader) 

hunt_file = open("cogs/assets/yaml_files/job_yamls/hunts.yml", "rb")
hunts_list = load(hunt_file, Loader = Loader) 


class ButtonMenu(ui.View):
    def __init__(self, uid, client, fish_price, hunt_price, mine_price, wood_price):
        super().__init__()
        self.id = uid
        self.client = client
        self.f_price = fish_price
        self.h_price = hunt_price
        self.m_price = mine_price
        self.w_price = wood_price

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user.id != self.id:
            await interaction.response.send_message(content = f"{Emojis.cross} Bu sizin envanteriniz değil. Buradaki butonları kullanamazsınız!", ephemeral = True)
            return False
        return True

    @ui.button(label = "Balıkları Sat", style = ButtonStyle.primary, emoji = ':fish:')
    async def sell_fishes_button(self, interacion: Interaction, button):
        user = interacion.user

        if self.f_price == 0:
            button.label = "Balık Yok!!"  # New Button Label
            button.style = ButtonStyle.secondary  # New Button Stlye
            button.disabled = True  # New Button Disabled
            return await interacion.response.edit_message(view=self)

        button.label = "Balıklar Satıldı!"  # New Button Label
        button.style = ButtonStyle.secondary  # New Button Stlye
        button.disabled = True  # New Button Disabled

        inventory, i_collection = await create_inventory_data(self.client, user.id)
        wallet, w_collection = await create_wallet(self.client, user.id)

        inventory["jobs_results"]["fishes"].clear()
        wallet['cash'] += self.f_price

        await i_collection.replace_one({"_id": user.id}, inventory)
        await w_collection.replace_one({"_id": user.id}, wallet)
        await interacion.response.edit_message(view = self)
  
    @ui.button(label = "Avları Sat", style = ButtonStyle.primary, emoji = ':deer:')
    async def sell_hunts_button(self, interacion: Interaction, button):
        user = interacion.user

        if self.h_price == 0:
            button.label = "Av Yok!!"  # New Button Label
            button.style = ButtonStyle.secondary  # New Button Stlye
            button.disabled = True  # New Button Disabled
            return await interacion.response.edit_message(view=self)

        button.label = "Avlar Satıldı!"  # New Button Label
        button.style = ButtonStyle.secondary  # New Button Stlye
        button.disabled = True  # New Button Disabled

        inventory, i_collection = await create_inventory_data(self.client, user.id)
        wallet, w_collection = await create_wallet(self.client, user.id)

        inventory["jobs_results"]["hunts"].clear()
        wallet['cash'] += self.h_price

        await i_collection.replace_one({"_id": user.id}, inventory)
        await w_collection.replace_one({"_id": user.id}, wallet)
        await interacion.response.edit_message(view = self)

    @ui.button(label = "Madenleri Sat", style = ButtonStyle.primary, emoji = ':gem:')
    async def sell_mines_button(self, interacion: Interaction, button):
        user = interacion.user

        if self.m_price == 0:
            button.label = "Maden Yok!!"  # New Button Label
            button.style = ButtonStyle.secondary  # New Button Stlye
            button.disabled = True  # New Button Disabled
            return await interacion.response.edit_message(view=self)

        button.label = "Madenler Satıldı!"  # New Button Label
        button.style = ButtonStyle.secondary  # New Button Stlye
        button.disabled = True  # New Button Disabled

        inventory, i_collection = await create_inventory_data(self.client, user.id)
        wallet, w_collection = await create_wallet(self.client, user.id)

        inventory["jobs_results"]["mines"].clear()
        wallet['cash'] += self.m_price

        await i_collection.replace_one({"_id": user.id}, inventory)
        await w_collection.replace_one({"_id": user.id}, wallet)
        await interacion.response.edit_message(view = self)

    @ui.button(label = "Oduları Sat", style = ButtonStyle.primary, emoji = ':wood:')
    async def sell_wood_button(self, interacion: Interaction, button):
        user = interacion.user

        if self.w_price == 0:
            button.label = "Odun Yok!!"  # New Button Label
            button.style = ButtonStyle.secondary  # New Button Stlye
            button.disabled = True  # New Button Disabled
            return await interacion.response.edit_message(view=self)

        button.label = "Odunlar Satıldı!"  # New Button Label
        button.style = ButtonStyle.secondary  # New Button Stlye
        button.disabled = True  # New Button Disabled

        inventory, i_collection = await create_inventory_data(self.client, user.id)
        wallet, w_collection = await create_wallet(self.client, user.id)

        inventory["jobs_results"]["wood"].clear()
        wallet['cash'] += self.w_price

        await i_collection.replace_one({"_id": user.id}, inventory)
        await w_collection.replace_one({"_id": user.id}, wallet)
        await interacion.response.edit_message(view = self)


class Sell(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="sell", description="Sell your (fishes, hunts etc.)")
    async def sell(self, interaction: Interaction):

        user = interaction.user

        wallet, w_collection = await create_wallet(self.bot, user.id)
        inventory, i_collection = await create_inventory_data(self.bot, user.id)

        inv = inventory["jobs_results"]
        
        # Fishes
        fish_price = 0
        fishes = [i.split('_') for i in inv["fishes"]]
        fish_count = len(fishes)
        for i in fishes:
            fish_price += (int(i[1]) * Game.FishPricePerSize) + fishes_list[i[0]]['price']

        # Hunts
        hunt_price = 0
        hunts = [i for i in inv['hunts']]
        hunt_count = len(hunts)
        for i in hunts:
            hunt_price += hunts_list[i]['price']

        # Mines
        mine_price = 0
        mines = [i.split('_') for i in inv["mines"]]
        mine_count = len(mines)
        for i in mines:
            mine_price += (int(i[1]) * Game.MinePricePerKG) + mines_list[i[0]]['price']

        # Wood
        wood_price = 0
        wood_ = [i.split('_') for i in inv["wood"]]
        wood_count = len(mines)
        for i in wood_:
            wood_price += (int(i[1]) * Game.WoodPricePerMeter) + wood_list[i[0]]['price']

        embed = Embed(
            color = 0x2b2d31,
            description="Merhaba, satıcıya hoş geldin! Burada balıklarını, madenlerini, odunlarını ve avlarını satabilirsin. İşte senin envanterin:"
        )
        embed.set_author(name=user.name, icon_url=user.avatar.url)
        embed.add_field(name = ":fish: Balıklar", value = f"{fish_count} adet balığınız var\nToplam **{fish_price}LC**", inline = True)
        embed.add_field(name = ":deer: Avlar", value = f"{hunt_count} adet avınız var\nToplam **{hunt_price}LC**", inline = True)
        embed.add_field(name = ":gem: Madenler", value = f"{mine_count} adet madeniniz var\nToplam **{mine_price}LC**", inline = False)
        embed.add_field(name = ":wood: Odunlar", value = f"{wood_count} adet odununuz var\nToplam **{wood_price}LC**", inline = True)

        view = ButtonMenu(user.id, self.bot, fish_price=fish_price, hunt_price=hunt_price, mine_price=mine_price, wood_price=wood_price)
        view.add_item(CloseButton(user.id))
        await interaction.response.send_message(embed=embed, view = view)


async def setup(bot: commands.Bot):
    await bot.add_cog(Sell(bot))
