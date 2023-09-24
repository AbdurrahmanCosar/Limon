"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""
from discord import Interaction, Embed, Member, app_commands, ui, SelectOption
from discord.app_commands import Choice, command
from discord.ext import commands
from discord.webhook.async_ import interaction_message_response_params
from cogs.utils.cooldown import set_cooldown
from cogs.utils.buttons import CloseButton

topics = [
    {'name': "Ekonomi", 'value': "eco"},
    {'name': "Kumar ve Oyun", 'value': "gamble"},
    {'name': "İşler (balıçılık vs.)", 'value': "job"},
    {'name': "Genel Komutlar", 'value': "general"}
]


def _get_title_from_value(value: str) -> str:
    for i in topics:
        if i["value"] == value:
            return i["name"]

def _create_embed(user: Member, commands: str, count: int, title: str) -> Embed:
    embed = Embed(
        color = 0x2b2d31,
        description = commands)
    embed.set_author(name = f"{user.name} | Kategori: {title}", icon_url = user.avatar.url)
    embed.set_footer(text=f"Bu konu ile ilgili {count} komut listelendi.")
    
    return embed

def get_commands(bot: commands.Bot, topic: str) -> str and int:
    try:
        commandlist = [
            f"**`/ {command.name}`**\n{command.extras['help']}\n"
            for command in bot.tree.walk_commands()
            if command.extras['category'] == topic]
    except:
        pass

    commandcount = len(commandlist)
    commandlist = '\n'.join(commandlist)

    return commandlist, commandcount


class HelpTopicDropdown(ui.Select):
    def __init__(self, bot: commands.Bot, user: Member):
        self.bot = bot
        self.user = user

        options = [
            SelectOption(label = topic["name"], value = topic["value"])
            for topic in topics
        ]
        super().__init__(placeholder='Konu başlığı seçiniz...', min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: Interaction):
        user = interaction.user
        topic = self.values[0]
        try:
            command_list, command_count = get_commands(self.bot, topic)
            embed = _create_embed(user, command_list, command_count, _get_title_from_value(topic))

            view = ui.View()
            view.add_item(self)
            view.add_item(CloseButton(self.user.id))
        
            await interaction.response.edit_message(embed = embed, view = view)
        except Exception as e:
            print(e)

class HelpCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    
    @app_commands.command(
            name = "bot-help",
            description = "Get info about the bot",
            extras = {
                'category': 'general',
                'help': "Bot hakkında bilgi edinin."
            })
    @app_commands.checks.dynamic_cooldown(set_cooldown())
    @app_commands.choices(topic=[
        Choice(name = topic.get('name'), value = topic.get('value'))
        for topic in topics
    ])
    async def help(self, interaction: Interaction, topic: str):
        user = interaction.user

        command_list, command_count = get_commands(self.bot, topic)
        embed = _create_embed(user, command_list, command_count, _get_title_from_value(topic))

        view = ui.View()
        view.add_item(HelpTopicDropdown(self.bot, user))
        view.add_item(CloseButton(user.id))
                
        await interaction.response.send_message(embed = embed, view = view)

async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCommand(bot))
