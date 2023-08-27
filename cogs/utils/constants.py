"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""
from PIL import Image, ImageFont

class _Link:
    support_server = "https://discord.gg/8YX57rBGTM"

Link = _Link

class _Gamble:
    max_bet_value = 100000

Gamble = _Gamble()

class _Game:
    FuelPerLiter: 4
    FishPricePerSize: 3
    MinePricePerKG: 2
    WoodPricePerMeter: 3
    AxeRefreshPrice: 10000
    PickaxeRefreshPrice: 15000

Game = _Game()

class _Emojis:
    enought_balance = "" # will be add
    licash = "<:LiCash:1065713526217392260>"
    morelicash = "<:morelicash:1065713539572052054>"
    coinback = "<:coinback:1063599851440451686>"
    coinfront = "<:cupcoin:1063599862379188285>"
    send = "<:sendmoney:1065713543611166720>"
    limonbank = "<:limonbank:1066359624950886483>"
    cross = "<:fail:1066371681221877830>"
    whiteCross = "<:whiteCross:1063607559547781180>"
    settings = "<:settings:996129999713206393>"
    checkMark = "<:checkmark:1063600965325959240>"
    clock = "<:sandclock:1066371693557338163>"
    threedot = "<:3dot:1066371663446425621>"
    siradan = "<:sradan:1063600327833694248>"
    seyrek = "<:seyrek:1063600324067205140>"
    ender = "<:ender:1063600317230501928>"
    efsanevi = "<:efsanevi:1063600313875054733>"
    kadim = "<:kadim:1063600320153919578>"
    slotleft = "<a:slotLeft:1073655781695692940>"
    slotmid = "<a:slotMid:1001813237651750963>"
    slotright = "<a:slotRight:1073655847114252418>"
    slotseven = "<:slot7:1001820977468022804>"
    slotcherry = "<:slotCherry:1001820989082046476>"
    slotcupcake = "<:slotCupcake:1001820992928223274>"
    slotheart = "<:slotHeart:1001820997151903785>"
    up = "<:cup:1063601092505632808>"
    topgg = "<:topgglogo:1063600091472085032>"
    gift = "<:cupgift:1063600088020160523>"
    new = "<:limonnew:1066373834191687770>"
    sell = "<:selling:1066371697613213696>"
    sold = "<:sold:1066371703120330772>"
    career = "<:career:1066371667657494709>"
    done = "<:done:1066371678633996359>"
    decline = "<:decline:1066371673189789696>"

Emojis = _Emojis()

class _Channels:
    suggestions = 1063608269404381255
    report = None

class _Users:
    admins = [529577110197764096, 1047996741397532763]
    bot = 994143430504620072

Users = _Users()

Channels = _Channels()

class _Assets:
    # Images
    default_avatar = Image.open("cogs/assets/images/DiscordLogo.png").convert("RGBA")
    expense_avatar = default_avatar
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