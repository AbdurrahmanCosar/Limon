from PIL import Image, ImageChops, ImageDraw, ImageFont
from ..database.fetchdata import create_wallet
from .functions import Functions
from ..constants import Assets

async def draw_balance_main(client, interaction):
    user = interaction.user

    wallet, _ = await create_wallet(client, user.id)
    transactions = wallet["recent_transactions"]["transactions"]

    #* --------------FIRST TRANSACTION--------------
    # Meaning of f in the variables is First
    first_transaction = transactions[0]

    f_uid = first_transaction["user"] # User ID

    if isinstance(f_uid, int):
        
        f_user = interaction.client.get_user(f_uid) # Get user in client
        
        # User Check
        if f_user is None:
            f_avatar, f_name = Functions.user_not_found_err()
        else:
            f_name = f_user.name
            f_avatar = f_user.avatar

            if f_avatar is None:
                f_avatar = Assets.default_avatar
            
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
            s_user = interaction.client.get_user(s_uid) # Get user in client
            
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
    img = Assets.template
    rectangle = Assets.rectangle
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

    money = f"{wallet['cash']:,}".replace(',', '.') # User's money -> 1.000.000

    # Balance 
    draw.text(((w/2),461), text = money, font = Assets.main_money_font, fill = "#ffffff", anchor = "ma")

    # Account No
    draw.text((333, 655), text = "Hesap No:", font = Assets.account_number_font, fill = "#bcbcbc")
    draw.text((530, 655), text = str(user.id), font = Assets.account_number_font, fill = "#ffffff")

    #* --------------RECTANGLE TRANSFER BOX--------------
    if len(first_transaction) == 0:
        text = "Geçmiş İşlem Bulunamadı"
        draw.text(((w/2), h/2), text = text, font = Assets.fail_font, fill = "#bcbcbc", anchor = "ma")
    else:
        img.paste(rectangle, (offset_x, offset_y), rectangle)

        # Transfer Text -> "Gelen Transfer" or "Giden Transfer"
        draw.text((332, offset_y + 70), text = f_transfer_text, font = Assets.transfer_text_font, fill = "#ffffff")

        # Avatar 
        f_avatar = Functions.circle(f_avatar, size = (180, 180))
        f_avatar = f_avatar.resize((180, 180), Image.LANCZOS)

        img.paste(f_avatar, (112, offset_y + 40), f_avatar)

        # Transfer User
        draw.text((332, offset_y + 131), text = f_name, font = Assets.transfer_user_font, fill = "#bcbcbc")

        # Transfer Amount
        draw.text((1170, transfer_money_offset_y), text = f_transfer_amount, font = Assets.transfer_money_font, fill = f_transfer_color, anchor = "ra")

        # Second Transaction Rectange Box
        if len(transactions) > 1:
            
            offset_y += 350
            img.paste(rectangle, (offset_x, offset_y), rectangle)

            # Transfer Text -> "Gelen Transfer" or "Giden Transfer"
            draw.text((332, offset_y + 70), text = s_transfer_text, font = Assets.transfer_text_font, fill = "#ffffff")

            # Avatar 
            s_avatar = Functions.circle(s_avatar, size = (180, 180))
            s_avatar = s_avatar.resize((180, 180), Image.LANCZOS)

            img.paste(s_avatar, (112, offset_y + 40), s_avatar)

            # Transfer User
            draw.text((332, offset_y + 131), text = s_name, font = Assets.transfer_user_font, fill = "#bcbcbc")

            # Transfer Amount
            transfer_money_offset_y += 350
            draw.text((1170, transfer_money_offset_y), text = s_transfer_amount, font = Assets.transfer_money_font, fill = s_transfer_color, anchor = "ra")

    #* --------------BOTTOM OPPORTUNITY BOX--------------
    draw.text((335,1901), text = "Fırsat Yok", font = Assets.fail_font, fill = "#bcbcbc", anchor = "ma")
    draw.text((915,1901), text = "Fırsat Yok", font = Assets.fail_font, fill = "#bcbcbc", anchor = "ma")

    return img


async def draw_balance_transactions(client, interaction):
    user = interaction.user

    wallet, _ = await create_wallet(client, user.id)

    transactions = wallet["recent_transactions"]["transactions"]
    
    img = Assets.transaction_template
    rectangle = Assets.transaction_rectangle
    draw = ImageDraw.Draw(img)
    
    offset_x = 63
    offset_y = 512

    user_avatar = user.avatar
    if user_avatar is None:
        user_avatar = Assets.default_avatar

    user_avatar = await Functions.open_avatar(user_avatar)

    # Masking on circle
    user_avatar = Functions.circle(user_avatar,size = (233, 233))
    user_avatar = user_avatar.resize((233, 233), Image.LANCZOS)
    img.paste(user_avatar, (941, 76), user_avatar)

    for transaction in transactions[:7]:

        img.alpha_composite(rectangle, (offset_x, offset_y))

        if transaction["transaction"]["type"] == "expense":
            avatar = Assets.expense_avatar
            transfer_name = transaction["user"]
            transfer_amount = f"-{transaction['amount']:,}".replace(',', '.')
            transfer_text = "Harcama"
            transfer_color = "#e04339" # Red
        elif transaction["transaction"]["type"] in ("transfer", "admin"):
            transfer_user = interaction.client.get_user(user.id)
            transfer_name = transfer_user.name

            if transfer_user.avatar is None:
                avatar = Assets.default_avatar
            else:
                avatar = await Functions.open_avatar(transfer_user.avatar)

            if transaction["transaction"]["is_incomming"] is True:
                transfer_amount = f"+{transaction['amount']:,}".replace(',', '.')
                transfer_text = "Gelen Transfer"
                transfer_color = "#7eb44b" # Green
            else:
                transfer_amount = f"-{transaction['amount']:,}".replace(',', '.')
                transfer_text = "Giden Transfer"
                transfer_color = "#e04339" # Red
        
        draw.text((278, offset_y + 45), text = transfer_text, font = Assets.transaction_transfer_text_font, fill="#ffffff")
        draw.text((278, offset_y + 96), text = transfer_name, font = Assets.transaction_transfer_user_font, fill="#bcbcbc")
        draw.text((1135, offset_y + 72), text = transfer_amount, font = Assets.transaction_transfer_money_font, fill = transfer_color, anchor = "ra")

        avatar = Functions.circle(avatar,size = (144, 144))
        avatar = avatar.resize((144, 144), Image.LANCZOS)
        img.paste(avatar, (110, offset_y + 26), avatar)

        offset_y += 216

    return img