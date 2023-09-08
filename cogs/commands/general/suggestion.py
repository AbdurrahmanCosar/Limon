"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from discord import ui, app_commands, Embed, TextStyle, Interaction
from discord.ext import commands
import datetime
from cogs.utils.constants import Link, Channels

class SuggestionModal(ui.Modal, title= "Öneri"):
    answer = ui.TextInput(
        label = "Öneriniz nedir?",
        style = TextStyle.paragraph,
        placeholder= "Öneriniz hakkında detaylı açıklama yapınız.",
        required = True,
        max_length= 4000
    )

    async def on_submit(self, interaction: Interaction):

        suggestionMessage = Embed(
            title = self.title,
            description = f"{self.answer}",
            timestamp= datetime.datetime.utcnow(),
            color = 0xfff48a 
        )

        suggestionMessage.set_author(
            name = interaction.user,
            icon_url = interaction.user.avatar.url
        )

        failMessage = Embed(
            description = f"❌ **|** Upss, öneriniz gönderilemedi! Lütfen [destek sunucumuza]({Link.support_server}) gelin ve geliştiriciye bu sorunu bildirin.", 
            color = 0xff3333
        )

        suggestionsChannel = interaction.client.get_channel(Channels.suggestions)

        try:
            await suggestionsChannel.send(embed = suggestionMessage)
            await interaction.response.send_message("✅ **|** Önerilerinizi aldık. Teşekkür ederiz :)", ephemeral = True)
        except:
            await interaction.response.send_message(embed = failMessage, ephemeral = True)

class Suggestion(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
            name = "suggestion", 
            description = "Make a suggestion for bot",
            extras={
                'category': 'general',
                'help': "Önerilerinizi ve isteklerinizi destek sunucusuna gelmeden bildirin."
            })
    async def suggestion(self, interaction: Interaction):
        modal = SuggestionModal()
        await interaction.response.send_modal(modal)

async def setup(bot: commands.Bot):
    await bot.add_cog(Suggestion(bot))
