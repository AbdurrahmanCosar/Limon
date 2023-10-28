"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""
from PIL import Image, ImageDraw, ImageFont
from ..functions import Functions
from ..assets import Assets


class DrawBankImages:
    def __init__(self, client, interaction, transaction_list: list, balance: int):
        self.client = client
        self.interaction = interaction
        self.transactions = transaction_list
        self.balance = balance

    def special_badge(self):
        special_badge = Image.open(r"cogs/assets/images/100thYear.png").convert("RGBA")
        special_badge = special_badge.resize((213, 150), Image.LANCZOS)
        return special_badge

    async def draw_bank_balance(self):
        user = self.interaction.user
        transactions = self.transactions
        
        #* --------------BASE IMAGE AND RECTANGLE--------------
        img = Image.open(r"cogs/assets/images/CumhuriyetBankAccountTemplate.png").convert("RGBA")
        rectangle = Image.open(r"cogs/assets/images/Rectangle.png").convert("RGBA")
        w, h = img.size

        #* --------------PASTE 100th YEAR BADGE-------------
        special_badge = self.special_badge()
        img.paste(special_badge, (100, 100), special_badge)

        #* --------------COMMAND USER AVATAR--------------
        user_avatar = user.avatar # Command user
        if user_avatar is None:
            user_avatar = Assets.default_avatar

        user_avatar = await Functions.open_avatar(user_avatar)

        # Masking on circle
        user_avatar = Functions.circle(user_avatar,size = (213, 213))
        user_avatar = user_avatar.resize((213, 213), Image.LANCZOS)
        img.paste(user_avatar, (949, 79), user_avatar)

        #* --------------DRAWING--------------
        # Draw
        draw = ImageDraw.Draw(img)

        # Offsets
        offset_x = 60
        offset_y = 890
        transfer_money_offset_y = 983

        money = f"{self.balance:,}".replace(',', '.') # User's money -> 1.000.000

        # Fonts
        acumin_black_158 = ImageFont.truetype(Assets.acumin_black, 158, encoding="unic")
        acumin_black_90 =  ImageFont.truetype(Assets.acumin_black, 90, encoding="unic")
        acumin_semibold_66 = ImageFont.truetype(Assets.acumin_semibold, 66, encoding="unic")
        coolvetica_50 = ImageFont.truetype(Assets.coolvetica, 50, encoding="unic")
        coolvetica_condensed_70 =  ImageFont.truetype(Assets.coolvetica_condensed, 70, encoding="unic")

        # Balance 
        draw.text(((w/2),461), text = money, font = acumin_black_158, fill = "#ffffff", anchor = "ma")

        # Account No
        draw.text((333, 655), text = "Hesap No:", font = acumin_semibold_66, fill = "#bcbcbc")
        draw.text((530, 655), text = str(user.id), font = acumin_semibold_66, fill = "#ffffff")


        #* --------------FIRST TRANSACTION--------------
        # Meaning of f in the variables is First
        if len(transactions) > 0:
            first_transaction = transactions[0]

            f_uid = first_transaction["user"] # User ID

            if isinstance(f_uid, int):
                f_user = self.interaction.client.get_user(f_uid) # Get user in client

                # User Check
                if f_user is None:
                    f_name, f_avatar = Functions.user_not_found_err()
                else:
                    f_name = f_user.name
                    f_avatar = f_user.avatar

                    if f_avatar is None:
                        f_avatar = Assets.default_avatar
                    else:
                        # Open Avatar
                        f_avatar = await Functions.open_avatar(f_avatar)

                if first_transaction["transaction"]["is_incomming"] is True: # So Incomming Money Transer
                    f_transfer_amount = f"+{first_transaction['amount']:,}".replace(',', '.')
                    f_transfer_text = "Gelen Transfer" # is "Incomming Transfer"
                    f_transfer_color = "#7eb44b" # Green

                    if first_transaction["transaction"]["type"] == "admin":
                        f_transfer_text = "Hediye"
                        f_avatar = Assets.limon_avatar
                else:
                    f_transfer_amount = f"-{first_transaction['amount']:,}".replace(',', '.')
                    f_transfer_text = "Giden Transfer" # is "Outgoing Transfer"
                    f_transfer_color = "#e04339" # Red

            else:
                if first_transaction["transaction"]["is_incomming"] is False:
                    f_transfer_amount = f"-{first_transaction['amount']:,}".replace(',', '.')
                    f_name = first_transaction["user"]
                    f_transfer_text = "Harcama" # Expense
                    f_transfer_color = "#e04339" # Red
                else:
                    f_transfer_amount = f"+{first_transaction['amount']:,}".replace(',', '.')
                    f_name = first_transaction["user"]
                    f_transfer_text = "Gelir"
                    f_transfer_color = "#7eb44b"

                f_name, f_avatar = Functions.expense_icon(f_name)

            img.paste(rectangle, (offset_x, offset_y), rectangle)

            # Transfer Text -> "Gelen Transfer" or "Giden Transfer"
            draw.text((332, offset_y + 70), text = f_transfer_text, font = acumin_black_90, fill = "#ffffff")

            # Avatar 
            f_avatar = Functions.circle(f_avatar, size = (180, 180))
            f_avatar = f_avatar.resize((180, 180), Image.LANCZOS)

            img.paste(f_avatar, (112, offset_y + 40), f_avatar)

            # Transfer User
            draw.text((332, offset_y + 131), text = f_name, font = coolvetica_condensed_70, fill = "#bcbcbc")

            # Transfer Amount
            draw.text((1170, transfer_money_offset_y), text = f_transfer_amount, font = acumin_black_90, fill = f_transfer_color, anchor = "ra")

        #* --------------SECOND TRANSACTION--------------
        if len(transactions) > 1:
            # Meaning of s in the variables is Second
            second_transaction = transactions[1]

            s_uid = second_transaction["user"] # User ID
            if isinstance(s_uid, int):
                s_user = self.interaction.client.get_user(s_uid) # Get user in client

                # User Check
                if s_user is None:
                    s_name, s_avatar = Functions.user_not_found_err()
                else:
                    s_name = s_user.name
                    s_avatar = s_user.avatar

                    if s_avatar is None:
                        s_avatar = Assets.default_avatar

                    # Open Avatar
                    s_avatar = await Functions.open_avatar(s_avatar)

                if second_transaction["transaction"]["is_incomming"] is True: # So Incomming Money Transer
                    s_transfer_amount = f"+{second_transaction['amount']:,}".replace(',', '.')
                    s_transfer_text = "Gelen Transfer" # is "Incomming Transfer"
                    s_transfer_color = "#7eb44b" # Green

                    if second_transaction["transaction"]["type"] == "admin":
                        s_transfer_text = "Hediye"
                        s_avatar = Assets.limon_avatar
                else:
                    s_transfer_amount = f"-{second_transaction['amount']:,}".replace(',', '.')
                    s_transfer_text = "Giden Transfer" # is "Outgoing Transfer"
                    s_transfer_color = "#e04339" # Red

            else:
                if second_transaction["transaction"]["is_incomming"] is False:
                    s_transfer_amount = f"-{second_transaction['amount']:,}".replace(',', '.')
                    s_name = second_transaction["user"]
                    s_transfer_text = "Harcama" # Expense
                    s_transfer_color = "#e04339" # Red
                else:
                    s_transfer_amount = f"+{second_transaction['amount']:,}".replace(',', '.')
                    s_name = second_transaction["user"]
                    s_transfer_text = "Gelir"
                    s_transfer_color = "#7eb44b"

                s_name, s_avatar = Functions.expense_icon(s_name)

            offset_y += 350
            img.paste(rectangle, (offset_x, offset_y), rectangle)

            # Transfer Text -> "Gelen Transfer" or "Giden Transfer"
            draw.text((332, offset_y + 70), text = s_transfer_text, font = acumin_black_90, fill = "#ffffff")

            # Avatar 
            s_avatar = Functions.circle(s_avatar, size = (180, 180))
            s_avatar = s_avatar.resize((180, 180), Image.LANCZOS)

            img.paste(s_avatar, (112, offset_y + 40), s_avatar)

            # Transfer User
            draw.text((332, offset_y + 131), text = s_name, font = coolvetica_condensed_70, fill = "#bcbcbc")

            # Transfer Amount
            transfer_money_offset_y += 350
            draw.text((1170, transfer_money_offset_y), text = s_transfer_amount, font = acumin_black_90, fill = s_transfer_color, anchor = "ra")


        #* --------------RECTANGLE TRANSFER BOX--------------
        if len(transactions) == 0:
            text = "Geçmiş İşlem Bulunamadı"
            draw.text(((w/2), h/2), text = text, font = coolvetica_50, fill = "#bcbcbc", anchor = "ma")

        #* --------------BOTTOM OPPORTUNITY BOX--------------
        #draw.text((335,1901), text = "Fırsat Yok", font = coolvetica_50, fill = "#bcbcbc", anchor = "ma")
        #draw.text((915,1901), text = "Fırsat Yok", font = coolvetica_50, fill = "#bcbcbc", anchor = "ma")

        return img

    async def draw_bank_transactions(self):
        user = self.interaction.user
        transactions = self.transactions

        img = Image.open(r"cogs/assets/images/CumhuriyetTransactionTemplate.png").convert("RGBA")
        rectangle = Image.open(r"cogs/assets/images/CumhuriyetTransactionRectangle.png").convert("RGBA")
        w, h = img.size

        draw = ImageDraw.Draw(img)
        offset_y = 539

        user_avatar = user.avatar
        if user_avatar is None:
            user_avatar = Assets.default_avatar
        else:
            user_avatar = await Functions.open_avatar(user_avatar)
                        #* --------------FONTS--------------
        big_bold = ImageFont.truetype(Assets.bevietnam_bold, 61, encoding="unic")
        small_bold = ImageFont.truetype(Assets.bevietnam_bold, 46, encoding="unic")
        small_semibold = ImageFont.truetype(Assets.bevietnam_semibold, 46, encoding="unic")  

        #* --------------COLOURS--------------
        white = "#efefef"
        black2 = "#2b2b2b"
        gray = "#d8d8d8"
        black = "#151515"
        green = "#7eb44b"
        red = "#e04339"

        #* --------------PROFILE--------------
        user_avatar = Functions.circle(user_avatar,size = (179, 180))
        user_avatar = user_avatar.resize((179, 180), Image.LANCZOS)


        img.paste(user_avatar, (76, 76), user_avatar)
        user_name = f"{user.name[:12]}.." if len(user.name)>12 else user.name

        draw.text((296, 106), text = "Hoş Geldin", font = small_semibold, fill = "#cacaca")
        draw.text((296, 158), text = user_name, font = big_bold, fill = white)
        
        if len(transactions) == 0:
            draw.text(((w // 2), (h // 2)), text = "Geçmiş işlem bulunamadı", font = small_semibold, fill = gray, anchor = "ma")
        else:
            for index, data in enumerate(transactions[:6]):
                if index % 2 == 0:
                    img.paste(rectangle, (0, offset_y), rectangle)

                uid = data["user"]

                if isinstance(uid, int):
                    transfer_user = self.interaction.client.get_user(uid)

                    if transfer_user is None:
                        name, avatar = Functions.user_not_found_err()
                    else:
                        name = transfer_user.name
                        avatar = transfer_user.avatar

                        if avatar is None:
                            avatar = Assets.default_avatar
                        else:
                            avatar = await Functions.open_avatar(avatar)

                    if data["transaction"]["is_incomming"] is True:
                        text = "Gelen Transfer"
                        amount = f"+{data['amount']:,}".replace(',', '.')
                        color = green
                        transaction_side = "Kimden: "

                        if data["transaction"]["type"] == "admin":
                            text = "Hediye"
                            avatar = Assets.limon_avatar
                    else:
                        text = "Giden Transfer"
                        amount = f"-{data['amount']:,}".replace(',', '.')
                        color = red
                        transaction_side = "Kime: "

                else:
                    name, avatar = Functions.expense_icon(uid)
                    transaction_side = ""

                    if data["transaction"]["is_incomming"] is False:
                        text = "Harcama"
                        amount = f"-{data['amount']:,}".replace(',', '.')
                        color = red
                    else:
                        text = "Gelir"
                        amount = f"+{data['amount']:,}".replace(',', '.')
                        color = green

                name = f"{name[:12]}.." if len(name)>12 else name
                avatar = Functions.circle(avatar, size = (170, 170))
                avatar = avatar.resize((170, 170), Image.LANCZOS)
                img.paste(avatar, (75, offset_y + 25), avatar)

                draw.text((271, offset_y + 50), text = text, font = big_bold, fill = black)
                draw.text((271, offset_y + 127), text = transaction_side + name, font = small_bold, fill = black2)
                draw.text((1168, offset_y + 83), text = amount, font = big_bold, fill = color, anchor = "ra")
                draw.text(((w/2), 2080), text ="LIBANK", font = big_bold, fill = "#000000", anchor = "ma")

                offset_y += 225

        return img

