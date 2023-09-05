"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""

from PIL import Image, ImageDraw, ImageFont
from ...database.fetchdata import create_career_data, create_wallet
from ..functions import Functions
from ..assets import Assets
from discord import Interaction, Member
from discord.ext.commands import Bot

levels = {
    "fisher": {"gold": 200, "silver": 150, "bronze": 50},
    "hunter": {"gold": 200, "silver": 150, "bronze": 50},
    "miner": {"gold": 200, "silver": 150, "bronze": 50},
    "forester": {"gold": 200, "silver": 150, "bronze": 50},
    "gambler": {"gold": 200, "silver": 150, "bronze": 50}
}

class UserInfo:
    def __init__(self, client: Bot, interaction: Interaction, user: Member):
        self.client = client
        self.interaction = interaction
        self.user = user

    async def user_badges(self):
        user_data, _ = await create_career_data(self.client, self.user.id)
        user_points = user_data["xp"]

        badges = []

        for level in levels:
            for user_key, user_value in user_points.items():
                for level_key, level_value in levels[level].items():
                    if user_key[:-3] == level:
                        if user_value >= level_value:
                            badges.append(f"{level_key}_{user_key[:-3]}.png")
                            break
        return badges

    async def draw_user_info(self):
        TINT_COLOR = (0, 0, 0) # Black
        TRANSPARENCY = .25 # Degree of transparency, 0-100%
        OPACITY = int(255 * TRANSPARENCY)

        img = Image.open(r"cogs/assets/images/user_info_template.png").convert("RGBA")
        guild_icon = Assets.default_avatar

        avatar = Assets.default_avatar

        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))

        draw = ImageDraw.Draw(img)
        layer_draw = ImageDraw.Draw(layer)

        member = self.user

        offset_y = 162 
        offset_x = 235
        len_badge = 0

        badges = []
        user_badges = await self.user_badges()

        name_offset_y = 119
        display_name_offset_y = 65

        if len(user_badges) > 0:
            for i in user_badges[:7]:
                badge = Image.open(f"cogs/assets/images/badges/{i}").convert("RGBA")
                badges.append(badge)
                len_badge += 45

            # Rounded Rectangle for Badges
            x_ = 232

            x_1 = x_ -5
            x_2 = x_ + len_badge + 5

            y_1 = offset_y - 5
            y_2 = offset_y + 45

            layer_draw.rounded_rectangle([(x_1, y_1), (x_2, y_2)], fill = (14, 14, 14, 25), radius = 5)

            for i in badges:
                i = i.resize((40, 40), Image.LANCZOS)
                layer.paste(i, (offset_x, offset_y), i)
                offset_x += 45

            name_offset_y = 104
            display_name_offset_y = 45
        img.paste(layer, (0,0), layer)

        user_data, _ = await create_wallet(self.client, member.id)
        money = f"{user_data['cash']:,}"

        if self.interaction.guild.icon is not None:
            guild_icon = await Functions.open_avatar(self.interaction.guild.icon)

        if member.avatar is not None:
            avatar = await Functions.open_avatar(member.avatar)

        avatar = Functions.add_corners(avatar, 30)
        guild_icon = Functions.circle(guild_icon, size = (54, 54))

        def rectangle(y_, text_size):
            x_ = 44
            x_1 = x_ - 1
            x_2 = x_ + text_size + 20
            y_1 = y_ - 5
            y_2 = y_ + 45

            shape = [(x_1, y_1), (x_2,y_2)]
            draw.rounded_rectangle(shape, fill ="#ffffff", radius = 13)

        name = f"{member.name[:12]}.." if len(member.name)>12 else member.name
        display_name = f"{member.display_name[:12]}.." if len(member.display_name)>12 else member.display_name
        status = str(self.interaction.guild.get_member(member.id).status).upper()
        top_role = member.top_role.name.upper()
        created_at = member.created_at.strftime("%b %d, %Y")
        joined_at = member.joined_at.strftime("%b %d, %Y")

        acumin_black_50 = ImageFont.truetype(Assets.acumin_black, 50, encoding="unic")
        acumin_bold_50 = ImageFont.truetype(Assets.acumin_bold, 50, encoding="unic")
        acumin_semibold_47 = ImageFont.truetype(Assets.acumin_semibold, 47, encoding="unic")
        acumin_semibold_49 = ImageFont.truetype(Assets.acumin_semibold, 49, encoding="unic")



        draw.text((227, display_name_offset_y), display_name ,font = acumin_black_50, fill = "#ffffff")
        draw.text((227, name_offset_y), name, font = acumin_bold_50, fill = "#bcbcbc")
        draw.text((44, 320), "USER ID", font =  acumin_black_50, fill = "#ffffff")
        draw.text((44, 447), "STATUS", font =  acumin_black_50, fill="#ffffff")
        draw.text((44, 583), "TOP ROLE", font =  acumin_black_50, fill="#ffffff")

        # DATE
        draw.text((67, 834), created_at, font = acumin_semibold_47, fill="#ffffff")
        draw.text((356, 834), joined_at, font = acumin_semibold_47, fill="#ffffff")

        # SIDE BAR
        draw.text((758, 302), money, font = acumin_semibold_49, fill= "#ffffff", anchor="ma")
        draw.text((758, 733), "Kaldırıldı!", font = acumin_semibold_49, fill= "#ffffff", anchor="ma")

        # BOTTOM
        # ID
        y = 378
        id_text_len = draw.textlength(text = str(member.id) , font = acumin_bold_50)

        rectangle(y, id_text_len)
        draw.text((54, y), str(member.id), font = acumin_bold_50, fill = "#303338")

        # Status
        y = 505
        status_text_len = draw.textlength(text = str(status) , font = acumin_bold_50)

        rectangle(y, status_text_len)
        draw.text((54, y), status, font = acumin_bold_50, fill = "#303338")

        # Top Role
        y = 641
        top_role_text_len = draw.textlength(text = str(top_role) , font = acumin_bold_50)
        rectangle(y, top_role_text_len)
        draw.text((54, y), top_role, font = acumin_bold_50, fill = "#303338")

        avatar = avatar.resize((180, 180), Image.LANCZOS)
        img.paste(avatar, (29,29), avatar)
        img.paste(guild_icon, (414, 775), guild_icon)

        return img
