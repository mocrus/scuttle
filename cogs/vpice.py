import disnake
from disnake.ext import commands


class VoiCEACT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="voice")
    async def voice_text(self, ctx, channel: disnake.VoiceChannel):
        await ctx.author.move_to(channel)
        await ctx.send("123")
def setup(bot):
    bot.add_cog(VoiCEACT(bot))