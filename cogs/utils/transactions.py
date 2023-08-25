"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""
from typing import List
from .constants import Users


class Transaction:
    """Methods for Transactions"""

    def __init__(self, transactions: List):
        self.transactions = self._limited(transactions)
        

    def _limited(self, transactions: List):
        """Deleted for not exceed the limit"""
        if len(transactions) == 11:
            transactions.pop(-1)
            return transactions
    
    def save_data_for_user(self, uid: int, amount: int, is_incomming: bool):
        data = {
            "user": uid,
            "amount": amount,
            "transaction": {
                "type": "transfer",
                "is_incomming": is_incomming
            }
        }
        self.transactions.insert(0, data)
        return self.transactions

    def save_data_for_shopping(self, shop_name: str, amount: int, is_incomming: bool):
        data = {
            "user": shop_name,
            "amount": amount,
            "transaction": {
                "type": "expense",
                "is_incomming": is_incomming
            }
        }
        self.transactions.insert(0, data)
        return self.transactions
    
    def save_data_by_admin(self, amount: int):
        data = {
            "user":  Users.bot, # Limon's ID
            "amount": amount,
            "transaction": {
                "type": "admin",
                "is_incomming": True
            }
        }
        self.transactions.insert(0, data)
        return self.transactions