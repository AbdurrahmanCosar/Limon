from discord import app_commands, Interaction, File
from discord.ext import commands
from cogs.utils.database.fetchdata import create_wallet
from io import BytesIO
from PIL import Image, ImageChops, ImageDraw, ImageFont

BOT_ID = 994143430504620072 # Limon's ID

class _Assets:
    # Images
    default_avatar = Image.open("cogs/assets/images/DiscordLogo.png").convert("RGBA")
    limon_avatar = Image.open("cogs/assets/images/SenderLimon.png").convert("RGBA")
    template = Image.open(r"cogs/assets/images/BankAccountTemplate.png").convert("RGBA")
    rectangle = Image.open(r"cogs/assets/images/Rectangle.png").convert("RGBA")
    
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

Assets = _Assets()

class Functions:
    def user_not_found_err():
        avatar = Assets.default_avatar
        name = "User"
        return avatar, name

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

class Balance(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "balance", description="View your balance")
    async def balance(self, interaction: Interaction):
        await interaction.response.defer()

        user = interaction.user

        wallet, _ = await create_wallet(self.bot, user.id)

        first_transaction = wallet["recent_transactions"]["first_transaction"]
        second_transaction = wallet["recent_transactions"]["second_transaction"]

        #* --------------FIRST TRANSACTION--------------
        if len(first_transaction) > 0:
            # Meaning of f in the variables is First

            f_uid = first_transaction["user"] # User ID
            f_user = interaction.client.get_user(f_uid) # Get user in client
            
            # User Check
            if f_user is None:
                f_avatar, f_name = Functions.user_not_found_err()
            else:
                f_name = f_user.name
                f_avatar = f_user.avatar

                if f_avatar is None:
                    f_avatar = Assets.default_avatar
                
                f_avatar = f_avatar.replace(size=256)
                data = BytesIO(await f_avatar.read())
                f_avatar = Image.open(data).convert("RGBA")
            
            if first_transaction["transfer"] is True: # So Incomming Money Transer
                f_transfer_amount = f"+{first_transaction['amount']:,}".replace(',', '.')
                f_transfer_text = "Gelen Transfer" # is "Incomming Transfer"
                f_transfer_color = "#7eb44b" # Green

                if f_uid == BOT_ID:
                    f_transfer_text = "Hediye"
                    f_avatar = Assets.limon_avatar
            else:
                f_transfer_amount = f"-{first_transaction['amount']:,}".replace(',', '.')
                f_transfer_text = "Giden Transfer" # is "Outgoing Transfer"
                f_transfer_color = "#e04339" # Red
        
        #* --------------SECOND TRANSACTION--------------
        if len(second_transaction) > 0:
            # Meaning of s in the variables is Second

            s_uid = second_transaction["user"] # User ID
            s_user = interaction.client.get_user(s_uid) # Get user in client
            
            # User Check
            if s_user is None:
                s_avatar, s_name = Functions.user_not_found_err()
            else:
                s_name = s_user.name
                s_avatar = s_user.avatar

                if s_avatar is None:
                    s_avatar = Assets.default_avatar
                
                s_avatar = s_avatar.replace(size=256)
                data = BytesIO(await s_avatar.read())
                s_avatar = Image.open(data).convert("RGBA")
            
            if second_transaction["transfer"] is True: # So Incomming Money Transer
                s_transfer_amount = f"+{second_transaction['amount']:,}".replace(',', '.')
                s_transfer_text = "Gelen Transfer" # is "Incomming Transfer"
                s_transfer_color = "#7eb44b" # Green

                if s_uid == BOT_ID:
                    s_transfer_text = "Hediye"
                    s_avatar = Assets.limon_avatar
            else:
                s_transfer_amount = f"-{second_transaction['amount']:,}".replace(',', '.')
                s_transfer_text = "Giden Transfer" # is "Outgoing Transfer"
                s_transfer_color = "#e04339" # Red

        #* --------------BASE IMAGE AND RECTANGLE--------------
        img = Assets.template
        rectangle = Assets.rectangle
        w, h = img.size

        #* --------------COMMAND USER AVATAR--------------
        user_avatar = user.avatar # Command user

        if user_avatar is None:
            user_avatar = Assets.default_avatar

        user_avatar = user_avatar.replace(size=256)
        data = BytesIO(await user_avatar.read())
        user_avatar = Image.open(data).convert("RGBA")

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
            if len(second_transaction) > 0:
                
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

        #* --------------SAVE & SEND IMAGE--------------
        with BytesIO() as a:
            img.save(a, "PNG")
            a.seek(0)
            await interaction.followup.send(content = None, file = File(a, "LimonWallet.png"))

async def setup(bot: commands.Bot):
    await bot.add_cog(Balance(bot))        
        