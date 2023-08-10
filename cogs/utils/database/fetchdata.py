"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

async def create_wallet(bot, _id):
    db = bot.database["limon"]
    collection = db["wallet"]

    if await collection.find_one({"_id": _id}) == None:
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

    if await collection.find_one({"_id": _id}) == None:
        new_data = {
            "_id": _id,
            "points": {
                "fisher_point": 0,
                "hunter_point": 0,
                "miner_point": 0,
                "forester_point": 0,
                "send_point": 0,
                "gamble_point": 0
            },
            "verified": False
        }
        await collection.insert_one(new_data)
    return await collection.find_one({"_id": _id}), collection


async def create_inventory_data(bot, _id):
    db = bot.database["limon"]
    collection = db["inventory"]

    if await collection.find_one({"_id": _id}) == None:
        new_data = {
            "_id": _id,
            "items": {}
        }
        await collection.insert_one(new_data)
    return await collection.find_one({"_id": _id}), collection
