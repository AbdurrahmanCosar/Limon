"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""
from typing import List
from .DrawImage.assets import Icons

class DataGenerator:
    """Prepares a transaction data for user's transactions list"""

    def __init__(self, transactions: List, amount: int, is_incomming: bool = False):
        self.transactions = self._limited(transactions)
        self.amount = amount
        self.is_incomming = is_incomming

    def _limited(self, transactions: List):
        """Deleted for not exceed the limit"""
        if len(transactions) == 10:
            transactions.pop(-1)
            return transactions

    def save_transfer_data(self, uid: int):
        """It is used for the user's money transfer"""
        data = {
            "user": uid,
            "amount": self.amount,
            "transaction": {
                "type": "transfer",
                "is_incomming": self.is_incomming
            }
        }
        self.transactions.insert(0, data)
        return self.transactions

    def save_expense_data(self, shop_name: str):
        """It is used because the user earns or spends in commands such as /store, /market, /sell"""
        types = {k:v for k, v  in Icons.expense_icons.items()}
        shop_name = shop_name.lower()

        if shop_name in types:
            data = {
                "user": shop_name,
                "amount": self.amount,
                "transaction": {
                    "type": "expense",
                    "is_incomming": self.is_incomming
                }
            }
            self.transactions.insert(0, data)
            return self.transactions
        else:
            raise KeyError