"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from PIL import Image, ImageDraw, ImageChops
from io import BytesIO
from .assets import Assets, Icons

class Functions:
    def user_not_found_err():
        avatar = Assets.default_avatar
        name = "User"
        return avatar, name
    
    async def open_avatar(u_avatar):
        avatar = u_avatar.replace(size=256)
        data = BytesIO(await avatar.read())
        avatar = Image.open(data).convert("RGBA")
        return avatar

    def circle(pfp, size = (215,215)):
        pfp = pfp.resize(size, Image.LANCZOS).convert("RGBA")

        bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
        mask = Image.new("L", bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill = 255)
        mask = mask.resize(pfp.size, Image.LANCZOS)
        mask = ImageChops.darker(mask, pfp.split()[-1])
        pfp.putalpha(mask)

        return pfp

    def expense_icon(expense_type: str): #, expense_icons: dict
        types = {k:v for k, v  in Icons.expense_icons.items()}
        expense_type = expense_type.lower()

        if expense_type in types:
            items = types[expense_type]
            print(5)
            return items["name"], items["image"]

