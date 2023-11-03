from discord.ext import commands

AUTO_ROLE_ID = 1170028803045736458
GUILD_ID = 884506342843379743


class AutoRole(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):

        if member.guild.id != GUILD_ID:
            return

        role = member.guild.get_role(AUTO_ROLE_ID)

        if (not role) or (member.bot):
            return

        try:
            await member.add_roles(role)
        except Exception as e:
            print(e)

async def setup(bot: commands.Bot):
    await bot.add_cog(AutoRole(bot))
