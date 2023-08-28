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
    expense_avatar = Image.open("cogs/assets/images/expense_icons/market_icon.png").convert("RGBA")
    limon_avatar = Image.open("cogs/assets/images/SenderLimon.png").convert("RGBA")
    template = Image.open(r"cogs/assets/images/BankAccountTemplate.png").convert("RGBA")
    rectangle = Image.open(r"cogs/assets/images/Rectangle.png").convert("RGBA")
    transaction_template = Image.open(r"cogs/assets/images/TransactionTemplate.png").convert("RGBA")
    transaction_rectangle = Image.open(r"cogs/assets/images/TransactionRectangle.png").convert("RGBA")

    
    # Fonts
    main_money_font = ImageFont.truetype("cogs/assets/fonts/AcuminProExtraCondBlack.otf", 158)
    account_number_font = transfer_money_font = ImageFont.truetype("cogs/assets/fonts/AcuminProExtraCondSemibold.otf", 66)
    fail_font = ImageFont.truetype("cogs/assets/fonts/coolveticaRG.otf", 50)

    box_big_font = ImageFont.truetype("cogs/assets/fonts/AcuminProExtraCondBlack.otf", 190)
    box_medium_font = ImageFont.truetype("cogs/assets/fonts/AcuminProExtraCondBlack.otf", 120)
    box_small_font = ImageFont.truetype("cogs/assets/fonts/AcuminProExtraCondBlack.otf", 66)

    transfer_text_font = ImageFont.truetype("cogs/assets/fonts/AcuminProExtraCondBlack.otf", 90)
    transfer_money_font = ImageFont.truetype("cogs/assets/fonts/AcuminProExtraCondBlack.otf", 90)
    transfer_user_font = ImageFont.truetype("cogs/assets/fonts/coolveticaCondensedRG.otf", 70)

    transaction_transfer_text_font_b = ImageFont.truetype("cogs/assets/fonts/BeVietnamPro-Bold.ttf", 61)
    transaction_transfer_font_s = ImageFont.truetype("cogs/assets/fonts/BeVietnamPro-SemiBold.ttf", 46)
    transaction_transfer_user_font = ImageFont.truetype("cogs/assets/fonts/BeVietnamPro-Bold.ttf", 46)

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