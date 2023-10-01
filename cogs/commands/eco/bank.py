"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from discord import app_commands, Interaction, File, ui, ButtonStyle
from discord.ext import commands
from discord.interactions import Interaction
from cogs.utils.constants import Emojis
from cogs.utils.cooldown import set_cooldown
from cogs.utils.DrawImage.Draw.bank_ui import DrawBankImages
from cogs.utils.database.fetchdata import create_wallet
from io import BytesIO


class Button(ui.View, DrawBankImages):
    def __init__(self, client, uid: int, draw_class):
        super().__init__()
        self.draw = draw_class
        self.uid = uid
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 10, commands.BucketType.member)

    def disable_buttons(self, button):
        for child in self.children:
            if child.custom_id != button:
                child.disabled = False
                child.style = ButtonStyle.blurple
            else:
                child.style = ButtonStyle.success
                child.disabled = True

    async def interaction_check(self, interaction: Interaction):
        if self.uid != interaction.user.id:
            await interaction.response.send_message(content = f"Bu banka hesabı size ait değil. İşlem yapamazsınız!", ephemeral=True)
            return False

        interaction.message.author = interaction.user
        bucket = self.cd_mapping.get_bucket(interaction.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            await interaction.response.send_message(content = f"{Emojis.clock} Buton bekleme süresinde lütfen **`{round(retry_after,1)}s`** bekleyini! ", ephemeral = True)
            return False
        return True

    @ui.button(label=None, style = ButtonStyle.success, disabled = True, emoji=Emojis.home, custom_id="balance_btn")
    async def balance_button(self, interaction: Interaction, button):
        await interaction.response.defer()
        self.disable_buttons("balance_btn")

        img = await self.draw.draw_bank_balance()

        with BytesIO() as x:
            img.save(x, "PNG")
            x.seek(0)
            await interaction.edit_original_response(attachments = [File(x, "LimonWallet.png")], view=self)

    @ui.button(label=None, style = ButtonStyle.blurple, emoji=Emojis.transaction, custom_id="transaction_btn")
    async def transaction_button(self, interaction: Interaction, button):
        await interaction.response.defer()
        self.disable_buttons("transaction_btn")

        img = await self.draw.draw_bank_transactions()

        with BytesIO() as x:
            img.save(x, "PNG")
            x.seek(0)
            await interaction.edit_original_response(attachments = [File(x, "LimonTransaction.png")], view=self)

class Balance(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
            name = "balance",
            description="View your bank account", 
            extras={
                'category': "eco", 
                'help': "Banka hesabını ve işlem geçmişini görüntüleyin."
            })
    @app_commands.checks.dynamic_cooldown(set_cooldown(15))
    async def balance(self, interaction: Interaction):
        await interaction.response.defer()

        wallet, _ = await create_wallet(self.bot, interaction.user.id)
        transaction_list = wallet["recent_transactions"]["transactions"]

        draw = DrawBankImages(self.bot, interaction, transaction_list, wallet["cash"])
        img = await draw.draw_bank_balance()

        with BytesIO() as a:
            img.save(a, "PNG")
            a.seek(0)
            await interaction.followup.send(content = None, file = File(a, "LimonWallet.png"), view=Button(self.bot, interaction.user.id, draw))

async def setup(bot: commands.Bot):
    await bot.add_cog(Balance(bot))
