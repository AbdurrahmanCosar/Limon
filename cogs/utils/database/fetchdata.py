"""
 * limlim Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

async def create_wallet(bot, _id):

    """
    * Transfer Types: 
    *   transfer -> with other user 
    *   expense -> with shopping  
    
    * Transfer Data for User:

    *    "user": id: int,
    *    "amount": int,
    *    "transaction": {
    *        "type": transfer,
    *        "is_incomming": bool

    * Transfer Data for Shopping:

    *    "user": name: str, -> Store, Market
    *    "amount": int,
    *    "transaction": {
    *        "type": expense,
    *        "is_incomming": bool

    * Transfer Data by Admin:

    *    "user": bot_id: int,
    *    "amount": int,
    *    "transaction": {
    *        "type": admin,
    *        "is_incomming": bool
    """

    db = bot.database["limlim"]
    collection = db["wallet"]

    existing_data = await collection.find_one({"_id": _id})
    if existing_data is None:
        new_data = {
            "_id": _id,
            "cash": 20000,
            "accumulated_money": 0,
            "recent_transactions": {
                "transactions": [
                    {
                        "user": 994143430504620072,
                        "amount": 20000,
                        "transaction": {
                            "type": "admin",
                            "is_incomming": True
                        }
                    }
                ]
            }
        }
        await collection.insert_one(new_data)

    return await collection.find_one({"_id": _id}), collection

async def create_career_data(bot, _id):
    db = bot.database["limlim"]
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
                "gambler_xp": 0
            },
            "verified": False,
            "old_user": False
        }
        await collection.insert_one(new_data)

    return await collection.find_one({"_id": _id}), collection

async def create_inventory_data(bot, _id):
    db = bot.database["limlim"]
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