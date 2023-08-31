"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from PIL import Image, ImageDraw
from ..functions import Functions
from ..assets import Assets

class DrawBankImages:
    def __init__(self, client, interaction, transaction_list: list, balance: int):
        self.client = client
        self.interaction = interaction
        self.transactions = transaction_list
        self.balance = balance

    async def draw_bank_balance(self):
        user = self.interaction.user
        transactions = self.transactions

        #* --------------FIRST TRANSACTION--------------
        # Meaning of f in the variables is First
        first_transaction = transactions[0]

        f_uid = first_transaction["user"] # User ID

        if isinstance(f_uid, int):
            f_user = self.interaction.client.get_user(f_uid) # Get user in client

            # User Check
            if f_user is None:
                f_avatar, f_name = Functions.user_not_found_err()
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
            f_transfer_amount = f"-{first_transaction['amount']:,}".replace(',', '.')
            f_name = first_transaction["user"]
            f_transfer_text = "Harcama" # Expense
            f_transfer_color = "#e04339" # Red
            f_avatar = Assets.expense_avatar

            # Open Avatar
            #f_avatar = await Functions.open_avatar(f_avatar)

        #* --------------SECOND TRANSACTION--------------
        if len(transactions) > 1:
            # Meaning of s in the variables is Second
            second_transaction = transactions[1]

            s_uid = second_transaction["user"] # User ID
            if isinstance(s_uid, int):
                s_user = self.interaction.client.get_user(s_uid) # Get user in client

                # User Check
                if s_user is None:
                    s_avatar, s_name = Functions.user_not_found_err()
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
                s_transfer_amount = f"-{second_transaction['amount']:,}".replace(',', '.')
                s_name = second_transaction["user"]
                s_transfer_text = "Harcama" # Expense
                s_transfer_color = "#e04339" # Red
                s_avatar = Assets.expense_avatar

        #* --------------BASE IMAGE AND RECTANGLE--------------
        img = Image.open(r"cogs/assets/images/BankAccountTemplate.png").convert("RGBA")
        rectangle = Image.open(r"cogs/assets/images/Rectangle.png").convert("RGBA")
        w, h = img.size

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

        # Balance 
        draw.text(((w/2),461), text = money, font = Assets.acumin_black_158, fill = "#ffffff", anchor = "ma")

        # Account No
        draw.text((333, 655), text = "Hesap No:", font = Assets.acumin_semibold_66, fill = "#bcbcbc")
        draw.text((530, 655), text = str(user.id), font = Assets.acumin_semibold_66, fill = "#ffffff")

        #* --------------RECTANGLE TRANSFER BOX--------------
        if len(first_transaction) == 0:
            text = "Geçmiş İşlem Bulunamadı"
            draw.text(((w/2), h/2), text = text, font = Assets.coolvetica_50, fill = "#bcbcbc", anchor = "ma")
        else:
            img.paste(rectangle, (offset_x, offset_y), rectangle)

            # Transfer Text -> "Gelen Transfer" or "Giden Transfer"
            draw.text((332, offset_y + 70), text = f_transfer_text, font = Assets.acumin_black_90, fill = "#ffffff")

            # Avatar 
            f_avatar = Functions.circle(f_avatar, size = (180, 180))
            f_avatar = f_avatar.resize((180, 180), Image.LANCZOS)

            img.paste(f_avatar, (112, offset_y + 40), f_avatar)

            # Transfer User
            draw.text((332, offset_y + 131), text = f_name, font = Assets.coolvetica_condensed_70, fill = "#bcbcbc")

            # Transfer Amount
            draw.text((1170, transfer_money_offset_y), text = f_transfer_amount, font = Assets.acumin_black_90, fill = f_transfer_color, anchor = "ra")

            # Second Transaction Rectange Box
            if len(transactions) > 1:

                offset_y += 350
                img.paste(rectangle, (offset_x, offset_y), rectangle)

                # Transfer Text -> "Gelen Transfer" or "Giden Transfer"
                draw.text((332, offset_y + 70), text = s_transfer_text, font = Assets.acumin_black_90, fill = "#ffffff")

                # Avatar 
                s_avatar = Functions.circle(s_avatar, size = (180, 180))
                s_avatar = s_avatar.resize((180, 180), Image.LANCZOS)

                img.paste(s_avatar, (112, offset_y + 40), s_avatar)

                # Transfer User
                draw.text((332, offset_y + 131), text = s_name, font = Assets.coolvetica_condensed_70, fill = "#bcbcbc")

                # Transfer Amount
                transfer_money_offset_y += 350
                draw.text((1170, transfer_money_offset_y), text = s_transfer_amount, font = Assets.transfer_money_font, fill = s_transfer_color, anchor = "ra")

        #* --------------BOTTOM OPPORTUNITY BOX--------------
        draw.text((335,1901), text = "Fırsat Yok", font = Assets.coolvetica_50, fill = "#bcbcbc", anchor = "ma")
        draw.text((915,1901), text = "Fırsat Yok", font = Assets.coolvetica_50, fill = "#bcbcbc", anchor = "ma")

        return img

    async def draw_bank_transactions(self):
        user = self.interaction.user
        transactions = self.transactions

        img = Image.open(r"cogs/assets/images/TransactionTemplate.png").convert("RGBA")
        rectangle = Image.open(r"cogs/assets/images/TransactionRectangle.png").convert("RGBA")
        w, h = img.size

        draw = ImageDraw.Draw(img)

        offset_y = 539

        user_avatar = user.avatar
        if user_avatar is None:
            user_avatar = Assets.default_avatar

        #* --------------FONTS--------------
        big_bold = Assets.bevietnam_bold_61
        small_bold = Assets.bevietnam_bold_46
        small_semibold = Assets.bevietnam_semibold_46

        #* --------------COLOURS--------------
        white = "#efefef"
        gray = "#bcbcbc"
        black = "#151515"
        green = "#7eb44b"
        red = "#e04339"

        #* --------------PROFILE--------------
        user_avatar = await Functions.open_avatar(user_avatar)
        user_avatar = Functions.circle(user_avatar,size = (180, 180))
        user_avatar = user_avatar.resize((180, 180), Image.LANCZOS)

        img.paste(user_avatar, (76, 76), user_avatar)

        draw.text((296, 76 + 30), text = "Hoş Geldin", font = small_semibold, fill = "#cacaca")
        draw.text((296, 128 + 30), text = user.name, font = big_bold, fill = white)

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

            avatar = Functions.circle(avatar, size = (170, 170))
            avatar = avatar.resize((170, 170), Image.LANCZOS)
            img.paste(avatar, (75, offset_y + 25), avatar)

            draw.text((271, offset_y + 50), text = text, font = big_bold, fill = black)
            draw.text((271, offset_y + 127), text = transaction_side + name, font = small_bold, fill = gray)
            draw.text((1168, offset_y + 83), text = amount, font = big_bold, fill = color, anchor = "ra")
            draw.text(((w/2), 2080), text ="LIBANK", font = big_bold, fill = "#000000", anchor = "ma")

            offset_y += 225

        return img