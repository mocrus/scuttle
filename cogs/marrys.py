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

    #create button
    @disnake.ui.button(label="Погодитись", style=disnake.ButtonStyle.success)
    async def agree(self, button: disnake.ui.Button, ctx: disnake.Interaction):
        #check who use
        if ctx.author.id != self.member.id:
            return await ctx.send("Не лізь своїм носом в чужі стосунки", ephemeral=True)
        role = disnake.utils.get(ctx.guild.roles, id=1077027040181633076)
        merry_gifs = [
                        "https://media.tenor.com/K6xMm3nxBg4AAAAM/marriage-marry.gif",
                        "https://media.tenor.com/WCeJaacSAecAAAAS/anime-wedding.gif",
                        "https://media.tenor.com/3OYmSePDSVUAAAAM/black-clover-licht.gif"
                        "https://media.tenor.com/CVLOKUa6PHAAAAAM/anime-wedding.gif"

                    ]

        random_marry_gifs = random.choice(merry_gifs)

        await collection_marrys.insert_one({
            "id1": ctx.author.id,
            "id2": self.author.id,
            "date": datetime.datetime.now(),
            "child": []
        })

        embed = disnake.Embed(
            title=f"Вітаємо заручених молодят!",
            description=f"{ctx.author.mention} обручились {self.member.mention} 💘",
            color=disnake.Color.from_rgb(255, 192, 203))
        

        async with aiohttp.ClientSession() as session:
            async with session.get(random_marry_gifs) as resp:
                if resp.status != 200:
                    return await ctx.send('Не вдалося завантажити зображення...')
                embed.set_image(url=random_marry_gifs)
        await ctx.delete_original_response()
        await collection.update_one({"id": self.author.id}, {"$inc": {"balance": -2000}})
        await ctx.author.add_roles(role)
        await self.author.add_roles(role)
        await ctx.send(embed=embed, delete_after=60)

    #create button
    @disnake.ui.button(label="Відмовити", style=disnake.ButtonStyle.red)
    async def reject(self, button: disnake.ui.Button, ctx: disnake.Interaction):
        #check who use
        if ctx.author.id != self.member.id:
            return await ctx.send("Не лізь своїм носом в чужі стосунки", ephemeral=True)
        emed = disnake.Embed(
            title=f"{ctx.author.name} відмовив(ла) {self.author.name}",
            description="ПЛАЧЕМО ВСІЄЮ ПОЛТАВСЬКОЮ ОБЛАСТЮ, КРІМ КРЕМЕНЧУКГА"
        )
        await ctx.delete_original_response()
        await ctx.send(embed=emed, delete_after=60)




class MarryCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    

    @commands.slash_command()
    async def marry(self, ctx, member: disnake.Member = None):
        #get user balance
        get_balnce = await collection.find_one({"id": ctx.author.id})
        #check member needs
        if member is None:
            return await ctx.send("Ви не вказали кому хочете зробити пропозицію")
        elif member.id == ctx.author.id:
            return await ctx.send("Ви не можете зробити пропозицію собі")
        elif ctx.author.get_role(1077027040181633076) is not None:
            return await ctx.send("Ти шо їбанувся, ти вже одружений(а)")
        elif member.get_role(1077027040181633076) is not None:
            return await ctx.send("Цей користувач уже одружений")
        elif get_balnce['balance'] < 2000:
            return await ctx.send("У вас недостатньо коштів щоб подати РАГС")
        embed = disnake.Embed(
            title=f"У вас є `1 хвилина` щоб прийняти чи відхилити пропозицію!",
            description=f"{ctx.author.mention} зробив пропозицію {member.mention} 💙",
            colour = disnake.Colour.from_rgb(255, 192, 203))  # код кольору рожевої полоски
            

        marry_gifs = [
                        "https://media.tenor.com/kK8gAeHtSPMAAAAC/marry-me.gif",
                        "https://media.tenor.com/uC3f95FIgogAAAAS/proposal-ring-for-real-the-story-of-reality-tv.gif",
                        "https://media.tenor.com/u7B_BCacat8AAAAM/wedding-ring-engaged.gif",
                        "https://media.tenor.com/R4EeoV4R-kUAAAAM/spy-x-family-loid-forger.gif",
                        "https://media.tenor.com/JdIwiQaoch8AAAAM/i-love-you-baby.gif"
                    ]

        random_marry_gifs = random.choice(marry_gifs)

        async with aiohttp.ClientSession() as session:
            async with session.get(random_marry_gifs) as resp:
                if resp.status != 200:
                    return await ctx.send('Не вдалося завантажити зображення...')
                embed.set_image(url=random_marry_gifs)
        
        await ctx.send(f"{member.mention} вам зробил пропозицію", delete_after=60)
        await ctx.send(embed=embed, delete_after=60,  view=MarryAssept(author=ctx.author, member=member))



def setup(bot):
    bot.add_cog(MarryCog(bot))