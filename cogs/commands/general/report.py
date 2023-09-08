"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from discord import ui, app_commands, Embed, ButtonStyle, Interaction, TextStyle
from discord.ext import commands
from cogs.utils.constants import Link, Channels
import datetime
import asyncio

class ReplyReportModal(ui.Modal, title= "Rapor Yanıtlama"):

    answer = ui.TextInput(
        label = "Raporu Yanıtlayın",
        style = TextStyle.paragraph,
        placeholder= "Hata hakkında detaylı bilgiler giriniz.",
        required = True,
        max_length= 4000
    )

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    async def on_submit(self, interaction: Interaction):
        user = interaction.client.get_user(int(self.user_id))

        reply_embed = Embed(
            description = str(self.answer),
            color = 0x2b2d31
        )
        reply_embed.set_author(name = f"Merhaba, {user.name}", icon_url = "https://cdn.discordapp.com/attachments/1056621448615170130/1094915068543639632/help.png")
        reply_embed.set_footer(text = f"Daha fazla yardım için destek sunucumuza gelebilirsin! |-> {Link.support_server}")

        try:
            await user.send(embed = reply_embed)
            await interaction.response.send_message(embed = reply_embed)
        except:
            await interaction.response.send_message(content = "Üzgünüm mesajı gönderemedim! Kullanıcı DM'leri kapatmış veya Limon ile bağlantsıını kesmiş olabilir!", ephemeral = True)

class ReplyReportButton(ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    @ui.button(label = "Reply", style = ButtonStyle.success)
    async def reply_button_callback(self, interaction: Interaction, button):

        button.disabled = True
        button.style = ButtonStyle.secondary
        button.label = "Replied!"

        modal = ReplyReportModal(self.user_id)
        await interaction.response.send_modal(modal)

class ReportModal(ui.Modal, title= "Bildir"):
    answer = ui.TextInput(
        label = "Hata Nedir?",
        style = TextStyle.paragraph,
        placeholder= "Hata hakkında detaylı bilgiler giriniz.",
        required = True,
        max_length= 4000
    )

    async def on_submit(self, interaction: Interaction):
        reportMessage = Embed(
            title = "Hata Raporu",
            description = f"{self.answer}",
            timestamp= datetime.datetime.utcnow(),
            color = 0xfff48a 
        )

        reportMessage.set_author(
            name = f"{interaction.user} ({interaction.user.id})",
            icon_url = interaction.user.avatar.url
        )

        failMessage = Embed(
            description = f"❌ **|** Upss, rapor gönderilemedi! Lütfen [destek sunucumuza]({Link.support_server}) gelin ve geliştiriciye bu sorunu bildirin.", 
            color = 0xff3333
        )

        reportsChannel = interaction.client.get_channel(Channels.report)

        try:
            view = ReplyReportButton(interaction.user.id)
            await reportsChannel.send(embed = reportMessage, view = view)
            await interaction.response.send_message("✅ **|** Rapor başarıyla gönderildi. Teşekkür ederiz :) Bizden cevap alabilmek için DM'lerini açık tut!", ephemeral = True)
        except:
            await interaction.response.send_message(embed = failMessage, ephemeral = True)

class Report(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
            name = "report", 
            description = "Report errors and bugs",
            extras={
                'category': 'general',
                'help': "Karşılaştığınız hataları, destek sunucusuna gelmeden bildirin."
            })
    @app_commands.checks.cooldown(1, 50, key=lambda i: (i.user.id))
    async def report(self, interaction: Interaction):
        modal = ReportModal()
        await interaction.response.send_modal(modal)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reply(self, ctx, user_id):
        try:
            user_id = int(user_id)
            user = self.bot.get_user(user_id)
            if user is None:
                msg = await ctx.send("Kullanıcı Bulunamadı")
                await asyncio.sleep(3)
                await msg.delete()
                return

            view = ReplyReportButton(user_id)
            await ctx.send(content = f"{user} adlı kullanıcıya hata yanıtı gönderin!", view = view)

        except TypeError:
            await ctx.send("Hatalı ID")
        except:
            msg = await ctx.send("Bir hata oluştu!")
            await asyncio.sleep(3)
            await msg.delete()

async def setup(bot: commands.Bot):
    await bot.add_cog(Report(bot))
