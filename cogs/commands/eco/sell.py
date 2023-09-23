"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from discord import app_commands, Interaction, Embed, ButtonStyle, ui, Member
from discord.ext import commands
from cogs.utils.constants import Emojis, Game
from cogs.utils.cooldown import set_cooldown
from cogs.utils.transactions import DataGenerator
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
    def __init__(self, user: Member, client: commands.Bot, prices: list, embed: Embed):
        super().__init__()
        self.user = user
        self.client = client
        self.embed = embed
        self.prices = prices
        self.total_money = 0

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user.id != self.user.id:
            await interaction.response.send_message(content = f"{Emojis.cross} Bu sizin envanteriniz değil. Buradaki butonları kullanamazsınız!", ephemeral = True)
            return False
        return True

    def enable_button(self):
        for child in self.children:
            if child.custom_id == "withdraw":
                if child.disabled is True:
                    child.disabled = False

    @ui.button(label = "Balıkları Sat", style = ButtonStyle.primary, emoji = '🐟', custom_id = "sellfishes")
    async def sell_fishes_button(self, interaction: Interaction, button):
        user = interaction.user

        button.label = "Balıklar Satıldı!"  # New Button Label
        button.style = ButtonStyle.secondary  # New Button Stlye
        button.disabled = True  # New Button Disabled

        self.total_money += self.prices[0]
        self.enable_button()

        inventory, collection = await create_inventory_data(self.client, user.id)
        inventory["jobs_results"]["fishes"].clear()

        self.embed.set_footer(text = f"Satıcıdan alınacak toplam LiCash: {self.total_money:,}")

        await collection.replace_one({"_id": user.id}, inventory)
        await interaction.response.edit_message(embed = self.embed, view = self)
  
    @ui.button(label = "Avları Sat", style = ButtonStyle.primary, emoji = '🦌', custom_id = "sellhunts")
    async def sell_hunts_button(self, interaction: Interaction, button):
        user = interaction.user

        button.label = "Avlar Satıldı!"  # New Button Label
        button.style = ButtonStyle.secondary  # New Button Stlye
        button.disabled = True  # New Button Disabled

        self.total_money += self.prices[1]
        self.enable_button()

        inventory, collection = await create_inventory_data(self.client, user.id)
        inventory["jobs_results"]["hunts"].clear()
        self.embed.set_footer(text = f"Satıcıdan alınacak toplam LiCash: {self.total_money:,}")
        
        await collection.replace_one({"_id": user.id}, inventory)
        await interaction.response.edit_message(embed = self.embed, view = self)

    @ui.button(label = "Madenleri Sat", style = ButtonStyle.primary, emoji = '💎', custom_id = "sellmines")
    async def sell_mines_button(self, interaction: Interaction, button):
        user = interaction.user

        button.label = "Madenler Satıldı!"  # New Button Label
        button.style = ButtonStyle.secondary  # New Button Stlye
        button.disabled = True  # New Button Disabled

        self.total_money += self.prices[2]
        self.enable_button()

        inventory, collection = await create_inventory_data(self.client, user.id)
        inventory["jobs_results"]["mines"].clear()

        self.embed.set_footer(text = f"Satıcıdan alınacak toplam LiCash: {self.total_money:,}")

        await collection.replace_one({"_id": user.id}, inventory)
        await interaction.response.edit_message(embed = self.embed, view = self)

    @ui.button(label = "Odunları Sat", style = ButtonStyle.primary, emoji = '🪵', custom_id = "sellwood")
    async def sell_wood_button(self, interaction: Interaction, button):
        user = interaction.user

        button.label = "Odunlar Satıldı!"  # New Button Label
        button.style = ButtonStyle.secondary  # New Button Stlye
        button.disabled = True  # New Button Disabled

        self.total_money += self.prices[3]
        self.enable_button()

        inventory, collection = await create_inventory_data(self.client, user.id)
        inventory["jobs_results"]["wood"].clear()

        self.embed.set_footer(text = f"Satıcıdan alınacak toplam LiCash: {self.total_money:,}")

        await collection.replace_one({"_id": user.id}, inventory)
        await interaction.response.edit_message(embed = self.embed, view = self)

    @ui.button(label = "Paranı Al", style = ButtonStyle.success, disabled = True, custom_id = "withdraw")
    async def withdraw_money(self, interaction: Interaction, button):
        user = interaction.user

        wallet, collection = await create_wallet(self.client, user.id)
        transaction_list = wallet["recent_transactions"]["transactions"]
        transactions = DataGenerator(transaction_list, self.total_money, True)

        self.embed.set_footer(text = f"Hesabınıa aktarılan LiCash: {self.total_money}")

        wallet["cash"] += self.total_money
        transaction_list = transactions.save_expense_data("sell")
        

        button.label = "Paran Çekildi!"
        button.disabled = True

        await collection.replace_one({"_id": user.id}, wallet)
        await interaction.response.edit_message(embed = self.embed, view = self)
        await interaction.followup.send(
            content = f"{Emojis.morelicash} {user.mention} **|** İş yaparak elde ettiklerinizi başarıyla sattınız." +
            f"\nToplam geliriniz **{self.total_money:,}LC** -> **`/ balance`** komutu ile paranızı kontrol edebilirsiniz.")

        self.total_money = 0

class Sell(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="sell", 
            description="Sell your (fishes, hunts etc.)",
            extras={
                'category': 'job',
                'help': "İş yaparak kazandıklarınızı(balıklar, odunlar vs.) satın."
            })
    @app_commands.checks.dynamic_cooldown(set_cooldown(30))
    async def sell(self, interaction: Interaction):
        user = interaction.user

        inventory, _ = await create_inventory_data(self.bot, user.id)
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
            description="Merhaba, satıcıya hoş geldin! Burada balıklarını, madenlerini, odunlarını ve avlarını satabilirsin.\n" + 
            "Elindekileri sattıktan sonra paranı çekmeyi unutma! İşte senin envanterin:"
        )
        embed.set_author(name=user.name, icon_url=user.avatar.url)
        embed.add_field(name = ":fish: Balıklar", value = f"{fish_count} adet balığınız var\nToplam **{fish_price:,}LC**", inline = True)
        embed.add_field(name = ":deer: Avlar", value = f"{hunt_count} adet avınız var\nToplam **{hunt_price:,}LC**", inline = True)
        embed.add_field(name = ":gem: Madenler", value = f"{mine_count} adet madeniniz var\nToplam **{mine_price:,}LC**", inline = False)
        embed.add_field(name = ":wood: Odunlar", value = f"{wood_count} adet odununuz var\nToplam **{wood_price:,}LC**", inline = True)

        prices = [fish_price, hunt_price, mine_price, wood_price]

        view = ButtonMenu(user, self.bot, prices,  embed=embed)
        view.add_item(CloseButton(user.id))

        if fish_price == 0:
            view.sell_fishes_button.label = "Balık Yok!!"  # New Button Label
            view.sell_fishes_button.style = ButtonStyle.secondary  # New Button Stlye
            view.sell_fishes_button.disabled = True  # New Button Disabled
        if hunt_price == 0:
            view.sell_hunts_button.label = "Av Yok!!"  # New Button Label
            view.sell_hunts_button.style = ButtonStyle.secondary  # New Button Stlye
            view.sell_hunts_button.disabled = True  # New Button Disabled
        if mine_count == 0:
            view.sell_mines_button.label = "Maden Yok!!"  # New Button Label
            view.sell_mines_button.style = ButtonStyle.secondary  # New Button Stlye
            view.sell_mines_button.disabled = True  # New Button Disabled
        if wood_price == 0:
            view.sell_wood_button.label = "Balık Yok!!"  # New Button Label
            view.sell_wood_button.style = ButtonStyle.secondary  # New Button Stlye
            view.sell_wood_button.disabled = True  # New Button Disabled

        await interaction.response.send_message(embed=embed, view = view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Sell(bot))
