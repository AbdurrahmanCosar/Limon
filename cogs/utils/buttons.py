from discord import Interaction, ButtonStyle, ui
from cogs.utils.constants import Emojis

cross = Emojis.cross

class CloseButton(ui.Button):
    def __init__(self, uid):
        self.id = uid
        super().__init__(label="Kapat", style=ButtonStyle.danger)

    async def callback(self, interaction: Interaction):
        if interaction.user.id != self.id:
            return await interaction.response.send_message(content = f"{cross} Bu menüyü kapatma izniniz bulunmuyor!", ephemeral = True)
        await interaction.message.delete()