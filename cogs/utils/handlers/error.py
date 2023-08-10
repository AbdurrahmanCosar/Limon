"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

import asyncio
from discord import app_commands, Interaction
from discord.ext import commands
import traceback
import sys
import time
from yaml import Loader, load

yaml_file = open("assets/yaml_files/emojis.yml", "rb")
emojis = load(yaml_file, Loader=Loader)

clock = emojis['clock']
cross = emojis["cross"]

class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def cog_load(self):
        tree = self.bot.tree
        self._old_tree_error = tree.on_error
        tree.on_error = self.on_app_command_error

    def cog_unload(self):
        tree = self.bot.tree
        tree.on_error = self._old_tree_error

    async def on_app_command_error(self, interaction: Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(content = f"{clock} **|** Lütfen <t:{int(time.time() + error.retry_after)}:R> tekrar deneyin!")
            await asyncio.sleep(error.retry_after - 1)

            try:
                await interaction.edit_original_response(content = f"{clock} {interaction.user.mention} **|** Bekleme süreniz sona erdi! **/{interaction.command.name}** komutunu kullanabilirsiniz.")
                await asyncio.sleep(15)
                await interaction.delete_original_response()
                return
            except:
                return

        if isinstance(error, app_commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = f'Bu komutun sorunsuz çalışabilmesi için **{fmt}** yetkisine ihtiyacım var.'
            await interaction.response.send_message(content = _message)
            return

        else:
            try:
                print(f"[{interaction.command.name}] {error}")
                await interaction.response.send_message(content = f"{cross} Beklenmedik bir hata oluştu. Lütfen bu hatayı geliştiriciye bildiriniz!", ephemeral=True)
            except:
                print(f"[{interaction.command.name}] {error}")

        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)