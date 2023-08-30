"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from PIL import Image, ImageFont

class _Assets:
    # Images
    default_avatar = Image.open("cogs/assets/images/DiscordLogo.png").convert("RGBA")
    limon_avatar = Image.open("cogs/assets/images/SenderLimon.png").convert("RGBA")
    verify = Image.open(r"cogs/assets/images/badges/verify.png").convert("RGBA")

    
    # Fonts
    acumin_black_158 = ImageFont.truetype("cogs/assets/fonts/AcuminProExtraCondBlack.otf", 158)
    acumin_black_90 = ImageFont.truetype("cogs/assets/fonts/AcuminProExtraCondBlack.otf", 90)
    acumin_black_50 = ImageFont.truetype("cogs/assets/fonts/AcuminProExtraCondBlack.otf", 50, encoding="unic")
    acumin_bold_50 = ImageFont.truetype("cogs/assets/fonts/AcuminProExtraCondBold.otf", 50, encoding="unic")
    
    acumin_semibold_66 = transfer_money_font = ImageFont.truetype("cogs/assets/fonts/AcuminProExtraCondSemibold.otf", 66)
    acumin_semibold_49 = ImageFont.truetype("cogs/assets/fonts/AcuminProExtraCondSemibold.otf", 49, encoding="unic")
    acumin_semibold_47 = ImageFont.truetype("cogs/assets/fonts/AcuminProExtraCondSemibold.otf", 47, encoding="unic")

    bevietnam_bold_98 = ImageFont.truetype("cogs/assets/fonts/BeVietnamPro-Bold.ttf", 98)
    bevietnam_bold_61 = ImageFont.truetype("cogs/assets/fonts/BeVietnamPro-Bold.ttf", 61)
    bevietnam_bold_49 = ImageFont.truetype("cogs/assets/fonts/BeVietnamPro-Bold.ttf", 49)
    bevietnam_bold_46 = ImageFont.truetype("cogs/assets/fonts/BeVietnamPro-Bold.ttf", 46)
    bevietnam_bold_32 = ImageFont.truetype("cogs/assets/fonts/BeVietnamPro-Bold.ttf", 32)
    bevietnam_semibold_46 = ImageFont.truetype("cogs/assets/fonts/BeVietnamPro-SemiBold.ttf", 46)

    coolvetica_50 = ImageFont.truetype("cogs/assets/fonts/coolveticaRG.otf", 50)
    coolvetica_condensed_70 = ImageFont.truetype("cogs/assets/fonts/coolveticaCondensedRG.otf", 70)
    

Assets = _Assets()

class _Icons:
    _path = "cogs/assets/images/expense_icons/"
    expense_icons = {
        "market": {"name": "Market", "image": Image.open(_path + "market_icon.png").convert("RGBA")},
        "fuel": {"name": "Yakıt", "image": Image.open(_path + "fuel_icon.png").convert("RGBA")},
        "repair": {"name": "Tamir", "image": Image.open(_path + "repair_icon.png").convert("RGBA")},
        "store": {"name": "Mağaza", "image": Image.open(_path + "store_icon.png").convert("RGBA")},
        "sell": {"name": "Iş Geliri", "image": Image.open(_path + "sell_icon.png").convert("RGBA")},
    }

Icons = _Icons()