from discord import app_commands, Interaction, Member, File
from discord.ext import commands
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from cogs.utils.DrawImage.Draw.user_info import UserInfo
from typing import Optional
# user veya interaction user objesi gönderilecek


class UserInfoCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "user-info", description = "Show info about the user")
    @app_commands.describe(user = "Select a user")
    async def user_info(self, interaction: Interaction, user: Optional[Member]):
        await interaction.response.defer()

        member = user if user is not None else interaction.user

        draw = UserInfo(self.bot, interaction, member)
        img = await draw.draw_user_info()

        with BytesIO() as a:
            img.save(a, "PNG")
            a.seek(0)
            
            await interaction.followup.send(content= None, file = File(a, "profilecard.png"))

async def setup(bot: commands.Bot):
    await bot.add_cog(UserInfoCommand(bot))