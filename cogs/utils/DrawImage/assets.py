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
    acumin_black = "cogs/assets/fonts/AcuminProExtraCondBlack.otf"
    acumin_bold = "cogs/assets/fonts/AcuminProExtraCondBold.otf"
    acumin_semibold = "cogs/assets/fonts/AcuminProExtraCondSemibold.otf"

    bevietnam_bold = "cogs/assets/fonts/BeVietnamPro-Bold.ttf"
    bevietnam_semibold = "cogs/assets/fonts/BeVietnamPro-SemiBold.ttf"

    coolvetica = "cogs/assets/fonts/coolveticaRG.otf"
    coolvetica_condensed = "cogs/assets/fonts/coolveticaCondensedRG.otf"

class _Icons:
    _path = "cogs/assets/images/expense_icons/"
    expense_icons = {
        "market": {"name": "Market", "image": Image.open(_path + "market_icon.png").convert("RGBA")},
        "fuel": {"name": "Yakıt", "image": Image.open(_path + "fuel_icon.png").convert("RGBA")},
        "repair": {"name": "Tamir", "image": Image.open(_path + "repair_icon.png").convert("RGBA")},
        "store": {"name": "Mağaza", "image": Image.open(_path + "store_icon.png").convert("RGBA")},
        "sell": {"name": "Iş Geliri", "image": Image.open(_path + "sell_icon.png").convert("RGBA")},
    }

Assets = _Assets()
Icons = _Icons()
