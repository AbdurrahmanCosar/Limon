"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from PIL import Image

class _Assets:

    # Images
    default_avatar =  Image.open("cogs/assets/images/DiscordLogo.png").convert("RGBA")
    limon_avatar =  Image.open("cogs/assets/images/SenderLimon.png").convert("RGBA")

    # Fonts
    _font_path = "cogs/assets/fonts/"

    acumin_black = _font_path + "AcuminProExtraCondBlack.otf"
    acumin_bold = _font_path + "AcuminProExtraCondBold.otf"
    acumin_semibold = _font_path + "AcuminProExtraCondSemibold.otf"

    bevietnam_bold = _font_path + "BeVietnamPro-Bold.ttf"
    bevietnam_semibold = _font_path + "BeVietnamPro-SemiBold.ttf"

    coolvetica = _font_path + "coolveticaRG.otf"
    coolvetica_condensed = _font_path + "coolveticaCondensedRG.otf"

class _Icons:
    _path = "cogs/assets/images/expense_icons/"
    expense_icons = {
        "market": {"name": "Market", "image": Image.open(_path + "icon_market.png").convert("RGBA")},
        "fuel": {"name": "Yakıt", "image": Image.open(_path + "icon_fuel.png").convert("RGBA")},
        "repair": {"name": "Tamir", "image": Image.open(_path + "icon_repair.png").convert("RGBA")},
        "store": {"name": "Mağaza", "image": Image.open(_path + "icon_store.png").convert("RGBA")},
        "sell": {"name": "Iş Geliri", "image": Image.open(_path + "icon_sell.png").convert("RGBA")},
    }

Assets = _Assets()
Icons = _Icons()
