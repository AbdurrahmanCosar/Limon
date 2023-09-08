"""
 * Limon Bot for Discord
 * Copyright (C) 2022 AbdurrahmanCosar
 * This software is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
 * For more information, see README.md and LICENSE
"""
from PIL import Image, ImageDraw, ImageFont
from discord import Interaction
from cogs.utils.DrawImage.assets import Assets

levels = {
    "fisher": {"gold": 200, "silver": 150, "bronze": 50},
    "hunter": {"gold": 200, "silver": 150, "bronze": 50},
    "miner": {"gold": 200, "silver": 150, "bronze": 50},
    "forester": {"gold": 200, "silver": 150, "bronze": 50},
    "gambler": {"gold": 200, "silver": 150, "bronze": 50}
}


class CareerUI:
    def __init__(self, interaction: Interaction, point_dict: dict):
        self.interaction = interaction
        self.points = point_dict
    
    def get_badges(self) -> list:
        badges = []

        for level in levels:
            for user_key, user_value in self.points.items():
                for level_key, level_value in levels[level].items():
                    if user_key[:-3] == level:
                        if user_value >= level_value:
                            data = {
                                    "point": user_value,
                                    "image": f"badge_{level_key}_{user_key[:-3]}.png"
                                    }
                            badges.append(data)
                            break
        return badges

    def get_badge_name(self, badge: str) -> str:
        splits = badge.split('_')
        
        level = ""
        job = ""
        print(splits[2][:-4])
        
        if splits[1] == "gold":
            level = "Usta "
        elif splits[1] == "silver":
            level = "Amatör "
        else:
            level =  "Acemi "
            
        if splits[2][:-4] == "fisher":
            job = "Balıkçı"
        elif splits[2][:-4] == "miner":
            job = "Madenci"
        elif splits[2][:-4] == "forester":
            job = "Ormancı"
        elif splits[2][:-4] == "hunter":
            job = "Avcı"
        else:
            job = "Kumarbaz"
        
        return level + job

    def draw_career_ui(self) -> Image:
        badges = self.get_badges()
        
        img = Image.open("cogs/assets/images/CareerTemplate.png").convert("RGBA")
        rectangle = Image.open("cogs/assets/images/CareerRectangle.png").convert("RGBA")
        draw = ImageDraw.Draw(img)
        w, h = rectangle.size

        row = 0
        first_row_offset_x = 49
        first_row_offset_y = 49

        second_row_offset_x = 49
        second_row_offset_y = 340

        font_size = 35

        # Load default font
        font = ImageFont.truetype(Assets.acumin_semibold, font_size, encoding="unic")

        # Check to see if there are any badges
        if len(badges) == 0:
            w, h = img.size
            draw.text(((w // 2), ((h // 2) - 15)), text = "Henüz bir rozetiniz yok!", font = font, fill = "#bababa", anchor = "ma")            
            draw.text(((w // 2), ((h // 2) + 15)), text = "Nasıl alacağını öğrenmek için butona tıkla.", font = font, fill = "#bcbcbc", anchor = "ma")

        # Paste rectangle as a table (2x2)
        for badge in badges[:4]:
            _path_of_badge = "cogs/assets/images/badges/" + badge["image"]
            badge_name = self.get_badge_name(str(badge["image"]))
            point = f"{badge['point']} puan"

            # Check font size and reload font
            while font.getlength(badge_name) > (w - 22):
                font_size -= 14
                font = ImageFont.truetype(Assets.coolvetica, font_size, encoding="unic")

            # Load icon (badge image)
            icon = Image.open(_path_of_badge).convert("RGBA")
            icon = icon.resize((100,100), Image.LANCZOS)
            i_w, i_h = icon.size

            if row <= 1:
                
                # Paste rectangle
                img.paste(rectangle, (first_row_offset_x, first_row_offset_y), rectangle)
                
                # Set icon position and paste icon in rectangle
                icon_offset_x = first_row_offset_x + (w // 2 - i_w // 2)
                icon_offset_y = first_row_offset_y + (h // 3 - i_h // 2)
                img.paste(icon, (icon_offset_x, icon_offset_y), icon)

                # Write badge name and points
                draw.text(((first_row_offset_x + (w // 2)), ((h // 2) + 70)), text = badge_name, font = font, fill = "#ffffff", anchor = "ma")
                draw.text(((first_row_offset_x + (w // 2)), ((h // 2) + 100)), text = point, font = font, fill = "#ffffff", anchor = "ma")

                # Set new position
                first_row_offset_x += (w + 40)
                row += 1

            else:

                # Paste rectangle
                img.paste(rectangle, (second_row_offset_x, second_row_offset_y),rectangle)
                icon_offset_x = second_row_offset_x + (w // 2 - i_w // 2)
                icon_offset_y = second_row_offset_y + (h // 3 - i_h // 2)
                img.paste(icon, (icon_offset_x, icon_offset_y), icon)

                # Write badge name and points
                draw.text(((second_row_offset_x + (w // 2)), (second_row_offset_y + (h // 2) + 20)), text = badge_name, font = font, fill = "#ffffff", anchor = "ma")
                draw.text(((second_row_offset_x + (w // 2)), (second_row_offset_y + (h // 2) + 50)), text = point, font = font, fill = "#ffffff", anchor = "ma")
                second_row_offset_x += (w + 40)
        return img
