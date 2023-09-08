from typing import ByteString
from discord import app_commands, Interaction, File, ui, ButtonStyle, Embed
from discord.ext import commands
from io import BytesIO
from cogs.utils.DrawImage.Draw.career_ui import CareerUI
from cogs.utils.database.fetchdata import create_career_data

class InfoButton(ui.View):
    def __init__(self):
       super().__init__()

    @ui.button(label = "Nasıl Alacağım?", style = ButtonStyle.blurple)
    async def button_callback(self, interaction: Interaction, button):

        embed = Embed(
            title = "Nasıl Rozet Alacağım?",
            color = 0x2b2d31,
            description="""
                ***Rozetler Nedir?***
                > Rozetler sizin bir işte ne kadar iyi olduğunuzu göteren bir çeşit madalyadır.

                ***Peki nasıl rozet alabilirim?***
                > Rozet almak için iş yapmanız(`/fishing, /hunting, /mining, /forestry`) gerekiyor. Ne kadar çok iş yaparsanız o kadar puan kazanırsınız. Sadece iş değil **kumar oynayarak** ve **arkadaşlarınıza LiCash göndererek**, `Kumarbaz` ve `İyi İnsan` rozeti kazanabilirsiniz.

                ***Kaç tane rozet var?***
                > Toplamda 3 kademe(`Acemi, Amatör, Usta`) bulunuyor. Puanınız arttıkça rozetleriniz de kademenize göre değişiyor
                """
            )
        embed.set_author(name = interaction.user.name, icon_url = interaction.user.avatar.url)
        
        await interaction.response.send_message(embed = embed, ephemeral = True)


class Career(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
            name = "career", 
            description = "View your jobs points",
            extras={
                'category': 'general',
                'help': "Puanlarınızı ve rozetlerinizi görüntüleyin."
            })
    async def career(self, interaction: Interaction):
        await interaction.response.defer()

        career, _ = await create_career_data(self.bot, interaction.user.id)
        draw = CareerUI(interaction, career["xp"])
        img = draw.draw_career_ui()
        
        view = InfoButton()

        with BytesIO() as a:
            img.save(a, "PNG")
            a.seek(0)
            await interaction.followup.send(content = None, file = File(a, "LimonCareer.png"), view = view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Career(bot))
