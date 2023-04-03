import disnake
from disnake.ext import commands


class VoiCEACT(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.command(name="voice")
    async def voice_text(self, ctx):
        voice_channel = await self.bot.fetch_channel(1092158662929293343)
        voice_client = await voice_channel.connect(mute=False, deafen=False)

        source = await disnake.FFmpegOpusAudio.from_probe("cogs\hello.mp3")
        voice_client.play(source)

def setup(bot):
    bot.add_cog(VoiCEACT(bot))