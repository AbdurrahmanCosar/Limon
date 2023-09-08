"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from discord import app_commands, Interaction, Member, File, ui, ButtonStyle
from discord.ext import commands
from io import BytesIO
from cogs.utils.DrawImage.Draw.send_ui import DrawSendImages
from cogs.utils.database.fetchdata import create_wallet
from cogs.utils.cooldown import set_cooldown
from cogs.utils.functions import add_xp
from cogs.utils.constants import Emojis
from cogs.utils.transactions import DataGenerator

SPACES = " ".join(["\u200b" for _ in range(18)])

class ConfirmButton(ui.View):
    def __init__(self, client: commands.Bot, uid: int, target: Member, amount: int, draw):
        super().__init__()
        self.client = client
        self.uid = uid
        self.target = target
        self.amount = amount
        self.draw = draw
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 10, commands.BucketType.member)

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user.id != self.uid:
            await interaction.response.send_message(content = f"{Emojis.cross} Bu sizin banka hesabınız değil. İşlemi onaylama yetkiniz bulunmuyor!", ephemeral = True)
            return False

        interaction.message.author = interaction.user
        bucket = self.cd_mapping.get_bucket(interaction.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            await interaction.response.send_message(content = f"{Emojis.clock} Buton bekleme süresinde lütfen **`{round(retry_after,1)}s`** bekleyini! ", ephemeral = True)
            return False
        return True

    @ui.button(label = f"{SPACES} Gönder {SPACES}", style = ButtonStyle.success)
    async def confirm_button(self, interaction: Interaction, button):
        await interaction.response.defer()

        uid = interaction.user.id
        user_wallet, user_collection = await create_wallet(self.client, uid)
        target_wallet, target_collection = await create_wallet(self.client, self.target.id)

        # Update sender user data (interaction.user)
        transaction_list = user_wallet["recent_transactions"]["transactions"]
        transactions = DataGenerator(transaction_list, self.amount, False)

        user_wallet["cash"] -= self.amount
        transaction_list = transactions.save_transfer_data(self.target.id)
        await add_xp(self.client, uid, "send_xp")
        await user_collection.replace_one({"_id": uid}, user_wallet)

        # Update receiver user data (target)
        transaction_list = target_wallet["recent_transactions"]["transactions"]
        transactions = DataGenerator(transaction_list, self.amount, True)

        target_wallet["cash"] += self.amount
        transaction_list = transactions.save_transfer_data(uid)
        await target_collection.replace_one({"_id": self.target.id}, target_wallet)

        img = await self.draw.draw_send_second()

        with BytesIO() as a:
            img.save(a, "PNG")
            a.seek(0)
            await interaction.edit_original_response(content = None, attachments = [File(a, "LimonSendCompleted.png")], view = None)

class Send(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
            name = "send", 
            description = "Send LiCash to Your Friends",
            extras = {
                'category': 'eco',
                'help': "Arkadaşlarınıza LiCash gönderin."
            })
    @app_commands.describe(target = "Tag your friend", amount = "Enter the amount")
    @app_commands.checks.dynamic_cooldown(set_cooldown(15))
    async def send(self, interaction: Interaction, target: Member, amount: app_commands.Range[int, 1000, 1000000]):
        await interaction.response.defer()

        user = interaction.user

        wallet, collection = await create_wallet(self.bot, user.id)
        balance = wallet["cash"]
        
        if target == user:
            return await interaction.followup.send(content = f"{Emojis.cross} Kendi kendinize LiCash gönderemezsiniz!", ephemeral = True) 
        elif balance < amount:
            return await interaction.followup.send(content = f"{Emojis.cross} LiCash göndermek istediğiniz miktar kadar LiCash'iniz bulunmuyor!", ephemeral = True) 
        elif await collection.find_one({"_id": target.id}) is None:
            return await interaction.followup.send(content = f"{Emojis.cross} LiCash göndermek istediğiniz kişinin banka hesabı bulunmuyor!", ephemeral = True) 


        draw = DrawSendImages(interaction, target, amount, balance)
        img = await draw.draw_send_first()

        button = ConfirmButton(self.bot, user.id, target, amount, draw) 

        with BytesIO() as a:
            img.save(a, "PNG")
            a.seek(0)
            await interaction.followup.send(content = None, file = File(a, "LimonSend.png"), view = button)

async def setup(bot: commands.Bot):
    await bot.add_cog(Send(bot))
