"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""
from cogs.utils.constants import Emojis
from cogs.utils.database.fetchdata import create_career_data

enought_balance = Emojis.enought_balance

async def balance_check(interaction, user_cash, required_amount):

    if user_cash < required_amount:
        return await interaction.response.send_message(
            content = f"{enought_balance} Yeterli bakiyeniz bulunmuyor! {user_cash-required_amount:,} LiCash eksik!",
            ephemeral = True)
    
async def add_xp(client, _id, xp_category):
    xp_types = [
        "fisher_xp",   # 0
        "hunter_xp",   # 1
        "miner_xp",    # 2
        "forester_xp", # 3
        "send_xp",     # 4
        "gamble_xp"    # 5
        ]
    
    if (xp_category not in xp_types) or (5 < xp_category < 0):
        raise KeyError("Please enter a valid category! (0-5)")
    
    if isinstance(int, xp_category):
        xp_category = xp_types[xp_category]

    user_data, collection = await create_career_data(client, _id)
    user_data["xp"][xp_category] += 2
    
    await collection.replace_one({"_id": _id}, user_data)
    print(f"Added XP to ({_id})")
