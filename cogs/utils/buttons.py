from discord import Interaction, ButtonStyle, ui
from cogs.utils.constants import Emojis
from typing import Optional

class CloseButton(ui.Button):
    def __init__(self, uid: int, row: Optional[int] = None):
        self.id = uid
        self.row = row
        super().__init__(label="Kapat", style=ButtonStyle.danger, row = row)

    async def callback(self, interaction: Interaction):
        if interaction.user.id != self.id:
            return await interaction.response.send_message(content = f"{Emojis.cross} Bu menüyü kapatma izniniz bulunmuyor!", ephemeral = True)
        await interaction.message.delete()
