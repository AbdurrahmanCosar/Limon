"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

def convert_rarity(rarity: str) -> str:

    if (rarity == "Ordinary"):
        return "Sıradan"
    elif (rarity == "Sparse"):
        return "Seyrek"
    elif (rarity == "Rare"):
        return "Nadir"
    elif (rarity == "Legendary"):
        return "Efsanevi"
    elif (rarity == "Ancient"):
        return "Kadim"