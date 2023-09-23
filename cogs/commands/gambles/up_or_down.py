"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from discord import app_commands, Interaction, Embed, ui, ButtonStyle
from discord.ext import commands
from cogs.utils.cooldown import set_cooldown
from cogs.utils.database.fetchdata import create_wallet
from cogs.utils.functions import balance_check, add_xp
from cogs.utils.constants import Game, Emojis
from random import randint

MAX_BET_VALUE = Game.max_bet_value
morelicash = Emojis.morelicash

class UpAndDownButtons(ui.View):
    def __init__(self, client: commands.Bot, uid: int, embed: Embed, nums: list, amount: int):
        super().__init__()
        self.client = client
        self.uid = uid
        self.embed = embed
        self.nums = nums
        self.amount = amount
        self.index = 0
        self.unopened_list = [str(self.nums[0]), "?", "?", "?", "?"]

    async def interaction_check(self, interaction: Interaction):
        if self.uid != interaction.user.id:
            await interaction.response.send_message(content=f"Bu başkasının oyunu. Bu oyunu kendiniz için oynamak istiyorsanız **`/up-or-down`** komutunu kullanın!", ephemeral=True)
            return False
        return True

    def disabled_all_buttons(self):
        for child in self.children:
            child.disabled = True

    @ui.button(style=ButtonStyle.blurple, emoji="⬆️", custom_id="upbutton")
    async def up_button(self, interaction: Interaction, button):
        user = interaction.user
        wallet, collection = await create_wallet(self.client, user.id)

        for child in self.children:
            child.disabled = False

        current_index = self.index
        next_index = current_index + 1
        num_list = self.nums

        # in order not to get this part IndexError'
        if current_index == 4:
            next_index = 4

        if num_list[next_index] >= num_list[current_index]:
            self.unopened_list[next_index] = str(num_list[next_index])
            unopened_list_ = " - ".join(self.unopened_list)

            name, icon_url = f"{user.name} {unopened_list_}", user.avatar.url

            if "?" not in self.unopened_list:

                name, icon_url = f"{user.name} | Tebrikler! Hepsini doğru tahmin ederek {self.amount:,} LC kazandınız.", user.avatar.url
                self.embed.set_author(name=name, icon_url=icon_url)
                self.disabled_all_buttons()

                wallet["cash"] += self.amount

                await collection.replace_one({"_id": user.id}, wallet)
                await interaction.response.edit_message(embed=self.embed, view=self)
                return

            self.embed.set_author(name=name, icon_url=icon_url)

            if num_list[next_index] in (1, 10):
                button.disabled = True

            await interaction.response.edit_message(embed=self.embed, view=self)
            self.index += 1

        else:
            self.embed.set_author(
                name=f"{user.name} | Maalesef kaybettiniz;c",
                icon_url=user.avatar.url)
            num_list = ' - '.join([str(num) for num in num_list])
            self.embed.set_footer(text=f"Doğru diziliş : ({num_list})")
            self.disabled_all_buttons()

            wallet["cash"] -= self.amount

            await collection.replace_one({"_id": user.id}, wallet)
            await interaction.response.edit_message(embed=self.embed, view=self)
            return

    @ui.button(style=ButtonStyle.danger, emoji="⬇️", custom_id="downbutton")
    async def down_button(self, interaction: Interaction, button):
        user = interaction.user
        wallet, collection = await create_wallet(self.client, user.id)

        for child in self.children:
            child.disabled = False

        current_index = self.index
        next_index = current_index + 1
        num_list = self.nums

        # in order not to get this part IndexError'
        if current_index == 4:
            next_index = 4

        if num_list[next_index] <= num_list[current_index]:
            self.unopened_list[next_index] = str(num_list[next_index])
            unopened_list_ = " - ".join(self.unopened_list)

            name, icon_url = f"{user.name} {unopened_list_}", user.avatar.url

            if "?" not in self.unopened_list:
                name, icon_url = f"{user.name} | Tebrikler! Hepsini doğru tahmin ederek 10 LC kazandınız.", user.avatar.url
                self.embed.set_author(name=name, icon_url=icon_url)
                self.disabled_all_buttons()

                wallet["cash"] += self.amount

                await collection.replace_one({"_id": user.id}, wallet)
                await interaction.response.edit_message(embed=self.embed, view=self)
                return

            self.embed.set_author(name=name, icon_url=icon_url)

            if num_list[next_index] in (1, 10):
                button.disabled = True

            await interaction.response.edit_message(embed=self.embed, view=self)
            self.index += 1

        else:
            self.embed.set_author(
                name=f"{user.name} | Maalesef kaybettiniz;c",
                icon_url=user.avatar.url)
            num_list = ' - '.join([str(num) for num in num_list])
            self.embed.set_footer(text=f"Doğru diziliş : ({num_list})")

            self.disabled_all_buttons()
            wallet["cash"] -= self.amount

            await collection.replace_one({"_id": user.id}, wallet)
            await interaction.response.edit_message(embed=self.embed, view=self)
            return

class UpOrDownGame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def random_numlist_generator(self):
        i = 0
        nums = []

        while i <= 4:
            num = randint(1, 10)
            if num >= 8:
                num = randint(1, 7)
            elif num <= 2:
                num = randint(3, 10)

            if num not in nums:
                nums.append(num)
                i += 1
        return nums

    @app_commands.command(
            name="up-or-down", 
            description="Guess next number and win",
            extras={
                'category': 'gamble',
                'help': "Sonraki sayının, öncekinden büyük mü, küçük mü olacağını tahmin ederek seriyi tamamlayın."
            })
    @app_commands.describe(amount="Enter the bet amount")
    @app_commands.checks.dynamic_cooldown(set_cooldown())
    async def up_or_down_game(self, interaction: Interaction, amount: app_commands.Range[int, 1, MAX_BET_VALUE]):
        user = interaction.user

        wallet, _ = await create_wallet(self.bot, user.id)
        check = await balance_check(interaction, wallet['cash'], amount)
        if check is False:
            return

        await add_xp(self.bot, user.id, "gambler_xp")

        nums = self.random_numlist_generator()
        unopened_list = " ".join([str(nums[0]), " - ?", "- ?", "- ?", "- ?"])

        embed = Embed(
            description="Bir sonraki sayının, önceki sayıdan düşük mü, yüksek mi olacağını tahmin edin.",
            color=0x2b2d31)
        embed.set_author(
            name=f"{user.name} {unopened_list}", icon_url=user.avatar.url)

        button = UpAndDownButtons(self.bot, user.id, embed, nums, amount)

        if nums[0] == 1:
            button.down_button.disabled = True
        elif nums[0] == 10:
            button.up_button.disabled = True

        await interaction.response.send_message(embed=embed, view=button)

async def setup(bot: commands.Bot):
    await bot.add_cog(UpOrDownGame(bot))
