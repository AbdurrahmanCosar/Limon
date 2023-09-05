"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from re import A
from discord import Interaction, Member
from PIL import Image, ImageDraw, ImageFont
from discord.enums import E
from ..assets import Assets
from ..functions import Functions
from datetime import datetime

class DrawSendImages:
    def __init__(self, interaction: Interaction, user: Member, amount: int, balance: int):
        self.interaction = interaction
        self.user = user
        self.amount = amount
        self.balance = balance

    async def draw_send_first(self):
        user = self.interaction.user

        # Command User Avatar
        avatar = user.avatar
        if avatar is None:
            avatar = Assets.default_avatar

        target_name = self.user.name
        target_id = self.user.id
        amount = f"{self.amount:,}".replace(',','.')

        img = Image.open(r"cogs/assets/images/send_template.png").convert("RGBA")
        draw = ImageDraw.Draw(img)

        big_font =  ImageFont.truetype(Assets.bevietnam_bold, 61, encoding="unic")
        medium_font = ImageFont.truetype(Assets.bevietnam_bold, 46, encoding="unic")

        small_font = ImageFont.truetype(Assets.bevietnam_bold, 32, encoding="unic")
        #* --------------COLOURS--------------
        gray = "#bcbcbc"
        black = "#151515"

        #* --------------RECTANGLE--------------
        avatar = await Functions.open_avatar(avatar)
        avatar = Functions.add_corners(avatar, 24)
        avatar = avatar.resize((191, 191), Image.LANCZOS)
        img.paste(avatar, (79, 500), avatar)

        draw.text((299, 552), text = user.name, font = medium_font, fill = gray)
        draw.text((299, 605), text = str(user.id), font = small_font, fill = gray)
        draw.text((1154, 578), text = str(self.balance), font = medium_font, fill = gray, anchor = "ra")

        #* --------------INFORMATION--------------
        draw.text((192, 944), text = target_name, font = big_font, fill = black)
        draw.text((192, 1188), text = str(target_id), font = big_font, fill = black)
        draw.text((192, 1455), text = amount, font = big_font, fill = black)

        return img

    async def draw_send_second(self):
        user = self.interaction.user

        # Command User Avatar
        avatar = user.avatar
        if avatar is None:
            avatar = Assets.default_avatar

        target_name = self.user.name
        amount = f"{self.amount:,}".replace(',','.')

        img = Image.open(r"cogs/assets/images/send_template_complete.png").convert("RGBA")
        draw = ImageDraw.Draw(img)

        main_font = ImageFont.truetype(Assets.bevietnam_bold, 98, encoding="unic")
        secondary_font = ImageFont.truetype(Assets.bevietnam_bold, 49, encoding="unic")

        #* --------------COLOURS--------------
        white = "#ffffff"
        black = "#151515"

        #* --------------INFORMATION--------------
        date = datetime.now().strftime("%H:%M:%S  %d/%-m/%Y")

        avatar = await Functions.open_avatar(avatar)
        avatar = Functions.circle(avatar, (140, 140))
        avatar = avatar.resize((140, 140), Image.LANCZOS)
        img.paste(avatar, (1045, 62), avatar)

        draw.text((619, 963), text = amount, font = main_font, fill = white, anchor = "ma")
        draw.text((191, 1405), text = target_name, font = secondary_font, fill = black)
        draw.text((191, 1695), text = "Para Transferi", font = secondary_font, fill = black)
        draw.text((191, 1979), text = date, font = secondary_font, fill = black)

        return img
