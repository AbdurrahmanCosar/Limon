from discord import Member, Interaction, Embed
from datetime import datetime
from zoneinfo import ZoneInfo
from .constants import Channels

class AdminLogger:
    def __init__(self, admin: Member, target: Member, interaction: Interaction):
        self.admin = admin
        self.target = target
        self.interaction = interaction

    async def verify_message(self, is_verified: bool = False):

        admin = self.admin
        target = self.target
        location = ZoneInfo("Europe/Istanbul")
        time = datetime.now(tz=location).strftime("%H:%M:%S - %a %m %Y")

        title = "Onay Kaldırıldı!"
        message = f"{target.name} adlı kullanıcının onayı, {admin.name} tarafından kaldırıldı!"
        color = 0xdf624f # Red
        
        if is_verified is True:
            title = ":tada: Tebrikler, Onaylandınız! :tada:'"
            message = f"**{target.name}** adlı kullanıcı, {admin.name} tarafından onaylandı."
            color = 0x87e157 # Green

        embed = Embed(title=title, description=message, color=color)
        embed.set_footer(text = f"{time} | {target.id}", icon_url = target.avatar.url)

        channel = self.interaction.client.get_channel(Channels.verify)
        await channel.send(embed = embed)
