"""
 * limlim Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""
from discord.ext import commands

class DeleteData:
    def __init__(self, bot: commands.Bot, _id: int):
        self.bot = bot
        self.id = _id
        self.colls = ("career", "wallet", "inventory") # Available collections

    @property
    def get_db(self):
        return self.bot.database['limlim']

    async def _check(collection: str) -> bool:
        db = self.get_db
        collection = db[collection]

        if await collection.find_one({"_id": self.id}) is True:
            return True
        return False

    async def delete_one(self, collection: str):
        """
        It's used to delete user's data from just one collection
        Enter a collection name
        
        Example
        -------
        'wallet'
        'inventory'
        'career'

        """
        db = self.get_db

        if collection in self.colls:
            if self._check(collection) is True:
                coll = db[collection]
                await coll.delete_one({"_id": self.id})

    async def delete_many(self, collections: tuple | list):
        """
        It's used to delete user's data from many collections at one time
        Enter collections names as a list or tuple

        Example
        -------
        ("wallet", "career")
        ["wallet", "career", "inventory"]
        """
        db = self.get_db

        for coll in collections:
            if coll in self.colls:
                if self._check(coll) is True:
                    coll = db[coll]
                    await coll.delete_one({"_id": self.id})

    async def delete_all(self):
        """ It's used to delete user's data from all collections at one time"""
        db = self.get_db

        for coll in self.colls:
            if self._check(coll) is True:
                coll = db[coll]
                await coll.delete_one({"_id": self.id})

