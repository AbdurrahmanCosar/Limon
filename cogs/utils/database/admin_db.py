"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""
async def get_collection(bot):
    db = bot.database['limlim']
    collection = db["admin"]
    data = await collection.find_one({"id": "admin"})
    
    return data, collection
