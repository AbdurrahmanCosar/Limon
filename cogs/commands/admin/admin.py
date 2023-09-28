"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""
from re import A
from discord import app_commands, ui, ButtonStyle, Interaction, TextStyle, Member, Embed
from discord.ext import commands
from cogs.utils.database.fetchdata import create_career_data, create_wallet
from cogs.utils.transactions import DataGenerator
from cogs.utils.constants import Users
from cogs.utils.functions import is_admin
from cogs.utils.cooldown import set_cooldown
from cogs.utils.log import AdminLogger

class SendMoneyModal(ui.Modal, title= "Send Money"):
    amount = ui.TextInput(
        label = "Enter the amount",
        style = TextStyle.short,
        placeholder= "Enter the amount as integer. Max -> 99999999",
        required = True,
        max_length= 8
    )

    def __init__(self, bot: commands.Bot, user: Member):
        super().__init__()
        self.bot = bot
        self.user = user

    async def on_submit(self, interaction: Interaction):
        # Will be add self.amount check. If self.amount contains dot, comma etc. remove them
        data, collection = await create_wallet(self.bot, self.user.id)
        transaction_list = data["recent_transactions"]["transactions"]

        amount = int(str(self.amount))
        transactions = DataGenerator(transaction_list, amount, True)

        data['cash'] += amount
        transaction_list = transactions.save_admin_data()

        await collection.replace_one({"_id": self.user.id}, data)
        await interaction.response.send_message(
            content = f"**{self.user.name}** adlı kullanıcının hesabına **{self.bot.user.name}** tarafından **{amount:,}** eklendi.")


class UserMenuButtons(ui.View):
    def __init__(self, bot: commands.Bot, user: Member):
        super().__init__()
        self.bot = bot
        self.user = user

    async def interaction_check(self, interaction: Interaction) -> bool:
        if is_admin(interaction.user.id) is False:
            await interaction.response.send_message(content = "Broo, cidden bastın mı bu butona?", ephemeral = True)
            return False
        return True

    @ui.button(label = "Verify", style = ButtonStyle.success)
    async def verify_callback(self, interaction: Interaction, button):
        user = interaction.user
        data, collection = await create_career_data(self.bot, self.user.id)

        if data['verified'] is True:
            is_verified = False
            # Set new button
            button.label = "Verify"
            button.style = ButtonStyle.success

            data['verified'] = False
            message = f"**{self.user.name}** adlı kullanıcını onayı {user.name} tarafından kaldırıldı!"
        else:
            is_verified = True
            # Set new button
            button.label = "Unverify"
            button.style = ButtonStyle.danger

            data['verified'] = True
            message = f"**{self.user.name}**, {user.name} tarafından onaylandı!"

        await AdminLogger(user, self.user, interaction).verify_message(is_verified)

        await collection.replace_one({"_id": self.user.id}, data)
        await interaction.response.edit_message(view = self)
        await interaction.followup.send(content = message)

    @ui.button(label = "Give LiCash", style = ButtonStyle.blurple)
    async def give_money_callback(self, interaction: Interaction, button):

        modal = SendMoneyModal(self.bot, self.user)
        await interaction.response.send_modal(modal)

    @ui.button(label = "Reset Transaction", style = ButtonStyle.danger)
    async def reset_transaction_callback(self, interaction: Interaction, button):
        user = self.user

        data, collection = await create_wallet(self.bot, user.id)
        
        data["recent_transactions"]["transactions"] = []
        await collection.replace_one({"_id": user.id}, data)
        await interaction.response.send_message(
                content = f"**{user.name}** adlı kullanıcının işlem geçmişi, {interaction.user.name} tarafından sıfırlanı!")


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(
            name = "admin", 
            description = "open admin menu",
            extras={
                'category': 'general',
                'help': "Sadece adminler için :("
            })
    @app_commands.describe(target = "Enter the user")
    @app_commands.checks.dynamic_cooldown(set_cooldown(7200))
    async def admin(self, interaction: Interaction, target: Member):
        author = interaction.user
        if is_admin(author.id) is False:
            return await interaction.response.send_message(content = ":/", ephemeral = True)

        user = self.bot.get_user(target.id)
        if not user:
            return await interaction.response.send_message(content = "Kullanıcı bulunamadı!")

        data, _ = await create_career_data(self.bot, target.id)
        view = UserMenuButtons(self.bot, user)

        embed = Embed(
                title = "Admin Paneli",
                color = 0x2b2d31,
                description = f"**{user.name}** için ne yapmak istiyorsunuz?")
        embed.set_author(
                name = f"Menü {author.name} için açıldı. | {author.id}", 
                icon_url = author.avatar.url)

        # Set verify button
        if data['verified'] is True:
            view.verify_callback.label = "Unverify"
            view.verify_callback.style = ButtonStyle.danger

        await interaction.response.send_message(embed=embed, view=view)
            

async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
