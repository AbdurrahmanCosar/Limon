"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

async def create_wallet(bot, _id):
    db = bot.database["limon"]
    collection = db["wallet"]

    existing_data = await collection.find_one({"_id": _id})
    if existing_data is None:
        new_data = {
            "_id": _id,
            "cash": 10000,
            "accumulated_money": 0,
            "recent_transactions": {
                "first_transaction": {
                    "user": 994143430504620072,
                    "amount": 10000,
                    "transfer": True
                },
                "second_transaction": {}
            }
        }
        await collection.insert_one(new_data)

    return await collection.find_one({"_id": _id}), collection


async def create_career_data(bot, _id):
    db = bot.database["limon"]
    collection = db["career"]

    existing_data = await collection.find_one({"_id": _id})
    if existing_data is None:
        new_data = {
            "_id": _id,
            "xp": {
                "fisher_xp": 0,
                "hunter_xp": 0,
                "miner_xp": 0,
                "forester_xp": 0,
                "send_xp": 0,
                "gamble_xp": 0
            },
            "verified": False,
            "old_user": False
        }
        await collection.insert_one(new_data)
    
    return await collection.find_one({"_id": _id}), collection


async def create_inventory_data(bot, _id):
    db = bot.database["limon"]
    collection = db["inventory"]

    existing_data = await collection.find_one({"_id": _id})
    if existing_data is None:
        new_data = {
            "_id": _id,
            "jobs_results": {
                "fishes": [],
                "mines": [],
                "hunts": [],
                "wood": []
            },
            "items": {}
        }
        await collection.insert_one(new_data)
    
    return await collection.find_one({"_id": _id}), collection