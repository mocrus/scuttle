import datetime
import random
import aiohttp
import disnake
from disnake.ext import commands
from cogs.db import collection_marrys, collection


class MarryAssept(disnake.ui.View):
    def __init__(self, author: disnake.Member = None, member: disnake.Member = None):
        super().__init__()
        self.author = author
        self.member = member

    @disnake.ui.button(label="Погодитись", style=disnake.ButtonStyle.success)
    async def agree(self, button: disnake.ui.Button, ctx: disnake.Interaction):
        if ctx.author.id != self.member.id:
            return await ctx.send("Не лізь своїм носом в чужі стосунки", ephemeral=True)
        role = disnake.utils.get(ctx.guild.roles, id=1077027040181633076)
        embed = disnake.Embed(
            title=f"{self.author.name} та {self.member} одружились",
            description=f"ВІТАЄМО МОЛОДЯТ"
        )
        merry_gifs = [
                        "https://media.tenor.com/K6xMm3nxBg4AAAAM/marriage-marry.gif",
                        "https://media.tenor.com/WCeJaacSAecAAAAS/anime-wedding.gif",
                        "https://media.tenor.com/3OYmSePDSVUAAAAM/black-clover-licht.gif",
                        "https://media.tenor.com/CVLOKUa6PHAAAAAM/anime-wedding.gif"
                    ]

        random_merry_gifs = random.choice(merry_gifs)

        async with aiohttp.ClientSession() as session:
            async with session.get(random_merry_gifs) as resp:
                if resp.status != 200:
                    return await ctx.send('Не вдалося завантажити зображення...')
                embed.set_image(url=random_merry_gifs)

        await collection_marrys.inser_one({
            "id1": ctx.author.id,
            "id2": self.member.id,
            "date": datetime.datetime.now()
        })
        await ctx.author.add_roles(role)
        await self.author.add_roles(role)
        await ctx.send(embed=embed, delete_after=60)

    @disnake.ui.button(label="Відмовити", style=disnake.ButtonStyle.red)
    async def reject(self, button: disnake.ui.Button, ctx: disnake.Interaction):
        if ctx.author.id != self.member.id:
            return await ctx.send("Не лізь своїм носом в чужі стосунки", ephemeral=True)
        emed = disnake.Embed(
            title=f"{ctx.author.name} відмовив(ла) {self.author.name}",
            description="ПЛАЧЕМО ВСІЄЮ ПОЛТАВСЬКОЮ ОБЛАСТЮ, КРІМ КРЕМЕНЧУКГА"
        )

        await ctx.send(embed=emed, delete_after=60)




class MarryCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    

    @commands.slash_command()
    async def marry(self, ctx, member: disnake.Member = None):
        get_balnce = await collection.find_one({"id": ctx.author.id})['balnce']
        if member is None:
            return await ctx.send("Ви не вказали кому хочете зробити пропозицію")
        elif member.id == ctx.author.id:
            return await ctx.send("Ви не можете зробити пропозицію собі")
        elif ctx.author.get_role(1077027040181633076) is not None:
            return await ctx.send("Ти шо їбанувся, ти вже одружений(а)")
        elif member.get_role(1077027040181633076) is not None:
            return await ctx.send("Цей користувач уже одружений")
        elif get_balnce< 2000:
            await ctx.send("У вас недостатньо коштів шоб подати РАГС")
        embd = disnake.Embed(
            title=f"{ctx.author.name} зробив пропозицію {member.name}",
            description="У вас є `1 хвилина` щоб прийняти чи відхилити пропозицію",   
        )
        merry_gifs = [
                        "https://media.tenor.com/kK8gAeHtSPMAAAAC/marry-me.gif",
                        "https://media.tenor.com/uC3f95FIgogAAAAS/proposal-ring-for-real-the-story-of-reality-tv.gif",
                        "https://media.tenor.com/u7B_BCacat8AAAAM/wedding-ring-engaged.gif",
                        "https://media.tenor.com/R4EeoV4R-kUAAAAM/spy-x-family-loid-forger.gif",
                        "https://media.tenor.com/JdIwiQaoch8AAAAM/i-love-you-baby.gif"
                    ]

        random_mur_gifs = random.choice(merry_gifs)

        async with aiohttp.ClientSession() as session:
            async with session.get(random_mur_gifs) as resp:
                if resp.status != 200:
                    return await ctx.send('Не вдалося завантажити зображення...')
                embd.set_image(url=random_mur_gifs)

        await ctx.send(f"{member.mention} вам зробил пропозицію", delete_after=60)
        await ctx.send(embed=embd, delete_after=60,  view=MarryAssept(author=ctx.author, member=member))



def setup(bot):
    bot.add_cog(MarryCog(bot))