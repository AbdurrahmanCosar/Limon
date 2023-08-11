"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""
from cogs.utils.constants import Emojis

enought_balance = Emojis.enought_balance

async def balance_check(interaction, user_cash, required_amount):

    if user_cash < required_amount:
        return await interaction.response.send_message(
            content = f"{enought_balance} Yeterli bakiyeniz bulunmuyor! {user_cash-required_amount:,} LiCash eksik!",
            ephemeral = True)
    
