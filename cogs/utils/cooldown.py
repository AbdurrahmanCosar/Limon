"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from discord import app_commands, Interaction
from typing import Optional 
from cogs.utils.constants import Users

def set_cooldown(cooldown: float = 10.0) -> Optional[app_commands.Cooldown]:
    def cooldown_func(interaction = Interaction) -> Optional[app_commands.Cooldown]:
        if interaction.user.id in Users.admins:
            return None
        return app_commands.Cooldown(1, cooldown)
    return cooldown_func