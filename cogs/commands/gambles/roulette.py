from discord import Button, app_commands, Interaction, ui, ButtonStyle, Embed, Member
from discord.audit_logs import F
from discord.ext import commands
from cogs.utils.constants import Game, Emojis
from cogs.utils.database.fetchdata import create_wallet
from cogs.utils.functions import add_xp, balance_check
from cogs.utils.buttons import CloseButton
from random import shuffle, choice
from asyncio import sleep

MAX_BET_VALUE = Game.max_bet_value
morelicash = Emojis.morelicash
whitecross = Emojis.whiteCross

class UpdateData:
    def __init__(self, bot: commands.Bot, user: Member, amount: int):
        self.bot = bot
        self.user = user
        self.amount = amount

    @property
    async def data(self):
        wallet, collection = await create_wallet(self.bot, self.user.id)
        return wallet, collection

    @property
    async def get_balance(self):
        wallet, collection = await create_wallet(self.bot, self.user.id)
        return wallet['cash']

    async def increase_balance(self, multplie: int = 2):
        wallet, collection = await self.data
        wallet['cash'] += self.amount * multplie
        await collection.replace_one({"_id": self.id}, wallet)

    async def decrease_balance(self):
        wallet, collection = await self.data
        wallet['cash'] -= self.amount
        await collection.replace_one({"_id": self.id}, wallet)


class RouletteButtons(ui.View, UpdateData):
    def __init__(self, bot: commands.Bot, user: Member, amount: int):
        ui.View.__init__(self, timeout=None)
        UpdateData.__init__(self, bot, user, amount)

        self.numbers = list(range(0, 37))
        shuffle(self.numbers)

        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 5, commands.BucketType.member)

    async def interaction_check(self, interaction: Interaction) -> bool:        
        if self.user.id != interaction.user.id:
            await interaction.response.send_message(content = f"{Emojis.cross} Bu sizin oyununuz değil. Butonlarla etkileşimde bulunamazsınız. Yeni bir oyun başlatın -> **`/roulette`**", ephemeral = True)
            return False

        balance = await self.get_balance
        if await balance_check(interaction, balance, self.amount) is False:
            return False

        interaction.message.author = interaction.user
        bucket = self.cd_mapping.get_bucket(interaction.message)
        retry_after = bucket.update_rate_limit()

        if retry_after:
            await interaction.response.send_message(content = f"{Emojis.clock} Buton bekleme süresinde lütfen **`{round(retry_after,1)}s`** bekleyini! ", ephemeral = True)
            return False

        await add_xp(self.bot, self.user.id, "gamble_xp")
        return True
    
    @property
    def _waiting_messsage(self):
        embed = Embed(description = "Topun durması bekleniyor..")
        return embed 

    def _embed_(self, color):
        embed = Embed(color = color, description = "Aynı miktarda tekrar oynamak için butonları kullanabilirsiniz.")
        return embed 

    def _win_embed(self, message: str, multplie: int = 2):
        embed = self._embed_(0x56ce41).set_author(name = f"{morelicash} Tebriker, {self.user.name}! {message} ve {self.amount * multplie} LC kazandınız.", icon_url = self.user.avatar.url)
        return embed

    def _lose_embed(self, message: str):
        embed = self._embed_(0xda3939).set_author(name = f"{whitecross} Maalesef, {self.user.name}! {message} ve kaybettiniz. ({self.amount:,}LC)",  icon_url = self.user.avatar.url)
        return embed

    @ui.button(label="Black", style = ButtonStyle.secondary, row=0)
    async def black_button(self, interaction: Interaction, button):

        num = choice(self.numbers)

        await interaction.response.send_message(embed = self._waiting_messsage, ephemeral=True)
        await sleep(3)

        if num % 2 == 0:
            await self.increase_balance()
            await interaction.edit_original_response(embed = self._win_embed("Top siyahın üzerinde durdu"))
        else:
            await self.decrease_balance()
            await interaction.edit_original_response(embed = self._lose_embed("Kırmızı geldi"))



    @ui.button(label="Red", style = ButtonStyle.danger, row=0)
    async def red_button(self, interaction: Interaction, button):
        num = choice(self.numbers)

        await interaction.response.send_message(embed = self._waiting_messsage, ephemeral=True)
        await sleep(3)

        if num % 2 == 0:
            await self.decrease_balance()
            await interaction.edit_original_response(embed = self._lose_embed("Siyah geldi"),)
        else:
            await self.increase_balance()
            await interaction.edit_original_response(embed = self._win_embed("Top kırmzının üzerinde durdu"))

    @ui.button(label="Green", style=ButtonStyle.success, row=0)
    async def green_button(self, interaction: Interaction, button):
        num = choice(self.numbers)

        await interaction.response.send_message(embed = self._waiting_messsage, ephemeral=True)
        await sleep(3)

        if num == 0:
            await self.increase_balance(5)
            await interaction.edit_original_response(embed = self._win_embed("İnanılmaz!! Top yeşilin üzerinde durdu", 5))
        elif num % 2 == 0:
            await self.decrease_balance()
            await interaction.edit_original_response(embed = self._lose_embed("Siyah geldi"))
        else:
            await self.decrease_balance()
            await interaction.edit_original_response(embed = self._lose_embed("Kırmızı geldi"))

    @ui.button(label="1-18", style = ButtonStyle.blurple, row=0)
    async def column1_button(self, interaction: Interaction, button):
        num = choice(self.numbers)

        await interaction.response.send_message(embed = self._waiting_messsage, ephemeral=True)
        await sleep(3)

        if 1 <= num <= 18:
            await self.increase_balance()
            await interaction.edit_original_response(embed = self._win_embed(f" {button.label} | Top {num} üzerinde durdu"))
        else:
            await self.decrease_balance()
            await interaction.edit_original_response(embed = self._lose_embed(f" {button.label} | Top {num} üzerinde durdu"))

    @ui.button(label="19-36", style = ButtonStyle.blurple, row=0)
    async def column2_button(self, interaction: Interaction, button):
        num = choice(self.numbers)

        await interaction.response.send_message(embed = self._waiting_messsage, ephemeral=True)
        await sleep(3)

        if 19 <= num <= 36:
            await self.increase_balance()
            await interaction.edit_original_response(embed = self._win_embed(f" {button.label} | Top {num} üzerinde durdu"))
        else:
            await self.decrease_balance()
            await interaction.edit_original_response(embed = self._lose_embed(f" {button.label} | Top {num} üzerinde durdu"))

    @ui.button(label="İlk Oniki", style = ButtonStyle.blurple, row = 1)
    async def first_twelve(self, interaction: Interaction, button):
        num = choice(self.numbers)

        await interaction.response.send_message(embed = self._waiting_messsage, ephemeral=True)
        await sleep(3)

        if 1 <= num <= 12:
            await self.increase_balance()
            await interaction.edit_original_response(embed = self._win_embed(f" {button.label} | Top {num} üzerinde durdu"))
        else:
            await self.decrease_balance()
            await interaction.edit_original_response(embed = self._lose_embed(f" {button.label} |Top {num} üzerinde durdu"))

    @ui.button(label="İkinci Oniki", style = ButtonStyle.blurple, row = 1)
    async def second_twelve(self, interaction: Interaction, button):
        num = choice(self.numbers)

        await interaction.response.send_message(embed = self._waiting_messsage, ephemeral=True)
        await sleep(3)

        if 12 <= num <= 24:
            await self.increase_balance()
            await interaction.edit_original_response(embed = self._win_embed(f" {button.label} | Top {num} üzerinde durdu"))
        else:
            await self.decrease_balance()
            await interaction.edit_original_response(embed = self._lose_embed(f" {button.label} | Top {num} üzerinde durdu"))

    @ui.button(label="Üçüncü Oniki", style = ButtonStyle.blurple, row = 1)
    async def thirty_twelve(self, interaction: Interaction, button):
        num = choice(self.numbers)

        await interaction.response.send_message(embed = self._waiting_messsage, ephemeral=True)
        await sleep(3)

        if 24 <= num <= 36:
            await self.increase_balance()
            await interaction.edit_original_response(embed = self._win_embed(f" {button.label} | Top {num} üzerinde durdu"))
        else:
            await self.decrease_balance()
            await interaction.edit_original_response(embed = self._lose_embed(f" {button.label} | Top {num} üzerinde durdu"))

class Roulette(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "roulette", description="Play Roulette")
    @app_commands.describe(amount="Enter the bet amount")
    async def roulette(self, interaction: Interaction, amount: app_commands.Range[int, 1, MAX_BET_VALUE]):
        user = interaction.user
        
        embed = Embed(title = "Top Dönüyor..", color = 0x2b2d31)
        embed.set_author(name = f"Bahis miktarı {amount:,} LiCash", icon_url = user.avatar.url)
        embed.set_image(url = "https://media.tenor.com/92nSRpL7ukkAAAAC/casino-gamble.gif")
        
        button = RouletteButtons(self.bot, user, amount)
        
        button.add_item(ui.Button(label = " - ", style = ButtonStyle.secondary, disabled = True, row=2))
        button.add_item(CloseButton(user.id, row = 2))
        button.add_item(ui.Button(label = " - ", style = ButtonStyle.secondary, disabled = True, row=2))
        
        await interaction.response.send_message(embed = embed, view = button)
        
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Roulette(bot))
