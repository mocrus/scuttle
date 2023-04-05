import disnake
import aiohttp
import random
from disnake.ext import commands
from cogs.db import collection, collection_shop



class RPCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.slash_command(description="Помуркай любимому котику")
    async def reaction_mur(ctx, member: disnake.Member = None):
        await ctx.response.defer()
        a = await collection.find_one({"id": ctx.author.id})
        if ctx.author.premium_since is not None:
            if member is None:
                await ctx.send(f"{ctx.author.mention}, немає кому помуркотіти :c")

            else:
                mur_gifs = [
                    "https://media.tenor.com/MpelG44DIYsAAAAM/cats-kitty.gif",
                    "https://media.tenor.com/n_zdha99hVMAAAAM/kitty.gif",
                    "https://media.tenor.com/J5dCW4RrePEAAAAM/kitten-lion-king.gif",
                    "https://media.tenor.com/tikIIf6NJvEAAAAM/cat-sleep.gif",
                    "https://i.gifer.com/9JG0.gif",
                    "https://i.gifer.com/8T2s.gif"
                ]

                random_mur_gifs = random.choice(mur_gifs)

                async with aiohttp.ClientSession() as session:
                    async with session.get(random_mur_gifs) as resp:
                        if resp.status != 200:
                            return await ctx.send('Не вдалося завантажити зображення...')

                        embed = disnake.Embed(description=f"{ctx.author.mention} помуркав(ла) {member.mention} ❤️")
                        embed.colour = disnake.Colour.from_rgb(255, 192, 203)
                        embed.set_footer(text="Ціна реакції 10 рун")
                        embed.set_image(url=random_mur_gifs)
                        await ctx.send(embed=embed)
        else:
            if a['balance']>=10:
                if member is None:
                    await ctx.send(f"{ctx.author.mention}, немає кому помуркотіти :c")

                else:
                    mur_gifs = [
                        "https://media.tenor.com/MpelG44DIYsAAAAM/cats-kitty.gif",
                        "https://media.tenor.com/n_zdha99hVMAAAAM/kitty.gif",
                        "https://media.tenor.com/J5dCW4RrePEAAAAM/kitten-lion-king.gif",
                        "https://media.tenor.com/tikIIf6NJvEAAAAM/cat-sleep.gif",
                        "https://i.gifer.com/9JG0.gif",
                        "https://i.gifer.com/8T2s.gif"
                    ]

                    random_mur_gifs = random.choice(mur_gifs)

                    async with aiohttp.ClientSession() as session:
                        async with session.get(random_mur_gifs) as resp:
                            if resp.status != 200:
                                return await ctx.send('Не вдалося завантажити зображення...')

                            embed = disnake.Embed(description=f"{ctx.author.mention} помуркав(ла) {member.mention} ❤️")
                            embed.colour = disnake.Colour.from_rgb(255, 192, 203)
                            embed.set_footer(text="Ціна реакції 10 рун")
                            embed.set_image(url=random_mur_gifs)
                            await collection.update_one({"id": ctx.author.id}, {"$inc": {"balance": -10}})
                            await ctx.send(embed=embed)
            else:
                await ctx.send("У вас недостатньо коштів шоб когосмусь помуркати")


    @commands.slash_command(description="Поцілуй любимого котика")
    async def reaction_kiss(ctx, member: disnake.Member = None):
        await ctx.response.defer()
        a = await collection.find_one({"id": ctx.author.id})
        if a['balance']>=10 or ctx.author.premium_since is not None:
            if not member:
                await ctx.send(f"{ctx.author.mention}, немає кому поцілувати :c")
            else:
                kiss_gifs = [
                    "https://media.tenor.com/217aKgnf16sAAAAM/kiss.gif",
                    "https://media.tenor.com/IM4-RWRjSNgAAAAM/kiss.gif",
                    "https://media.tenor.com/QjMZ6Dx33_QAAAAM/kuss-kussi.gif",
                    "https://media.tenor.com/wPzIJLI3IeQAAAAM/kiss-hot.gif",
                    "https://media.tenor.com/U7h-gyy--akAAAAM/kiss.gif",
                    "https://media.giphy.com/media/bm2O3nXTcKJeU/giphy.gif",
                    "https://media.giphy.com/media/G3va31oEEnIkM/giphy.gif"
                ]

                random_kiss_gifs = random.choice(kiss_gifs)

                async with aiohttp.ClientSession() as session:
                    async with session.get(random_kiss_gifs) as resp:
                        if resp.status != 200:
                            return await ctx.send('Не вдалося завантажити зображення...')

                        embed = disnake.Embed(description=f"{ctx.author.mention} поцілував(ла) {member.mention} ❤️")
                        embed.colour = disnake.Colour.from_rgb(255, 192, 203)
                        embed.set_footer(text="Ціна реакції 10 рун")
                        embed.set_image(url=random_kiss_gifs)
                        if ctx.author.premium_since is None:
                            await collection.update_one({"id": ctx.author.id}, {"$inc": {"balance": -10}})
                        await ctx.send(embed=embed)

        else:
            await ctx.send("У вас недостатньо коштів шоб когось поцілувати")


    @commands.slash_command(description="Погладь свого котика")
    async def reaction_pat(ctx, member: disnake.Member = None):
        await ctx.response.defer()
        a = await collection.find_one({"id": ctx.author.id})
        if a['balance']>=10 or ctx.author.premium_since is not None:
            if not member:
                await ctx.send(f"{ctx.author.mention}, немає кому гладити :c")
                
            else:
                pat_gifs = [
                    "https://media.tenor.com/qjHkX9X0FOQAAAAS/milk-and-mocha-pat.gif",
                    "https://media.tenor.com/oGbO8vW_eqgAAAAM/spy-x-family-anya.gif",
                    "https://media.tenor.com/Dbg-7wAaiJwAAAAM/aharen-aharen-san.gif",
                    "https://media.tenor.com/aZFqg65KvssAAAAM/pat-anime.gif",
                    "https://media.tenor.com/JsjHFFy5O40AAAAM/kitten-pat.giff"
                ]

                random_pat_gifs = random.choice(pat_gifs)

                async with aiohttp.ClientSession() as session:
                    async with session.get(random_pat_gifs) as resp:
                        if resp.status != 200:
                            return await ctx.send('Не вдалося завантажити зображення...')

                        # кастомізація embed
                        embed = disnake.Embed(description=f"{ctx.author.mention} погладив(ла) {member.mention} ❤️")
                        embed.colour = disnake.Colour.from_rgb(255, 192, 203)  # код кольору рожевої полоски
                        embed.set_footer(text="Ціна реакції 10 рун")
                        embed.set_image(url=random_pat_gifs)
                        if ctx.author.premium_since is None:
                            await collection.update_one({"id": ctx.author.id}, {"$inc": {"balance": -10}})
                        await ctx.send(embed=embed)

        else:
            await ctx.send("У вас недостатньо коштів шоб когось погладити")

    @commands.slash_command(description="Обійми сумуючого котика")
    async def reaction_hug(ctx, member: disnake.Member = None):
        await ctx.response.defer()
        a = await collection.find_one({"id": ctx.author.id})
        if a['balance']>=10 or ctx.author.premium_since is not None:
            if not member:
                await ctx.send(f"{ctx.author.mention}, немає кому обійняти :c")
                
            else:
                hug_gifs = [
                    "https://media.tenor.com/NGFif4dxa-EAAAAj/hug-hugs.gif",
                    "https://media.tenor.com/S4he5WCX9lEAAAAM/hugs-cuddle.gif",
                    "https://media.tenor.com/-evl3vUtVhEAAAAM/hugs-cuddle.gif",
                    "https://media.tenor.com/J7eGDvGeP9IAAAAM/enage-kiss-anime-hug.gif",
                    "https://media.tenor.com/3mr1aHrTXSsAAAAM/hug-anime.gif"
                ]

                random_hug_gifs = random.choice(hug_gifs)

                async with aiohttp.ClientSession() as session:
                    async with session.get(random_hug_gifs) as resp:
                        if resp.status != 200:
                            return await ctx.send('Не вдалося завантажити зображення...')


                        embed = disnake.Embed(description=f"{ctx.author.mention} обійняв(ла) {member.mention} ❤️")
                        embed.colour = disnake.Colour.from_rgb(255, 192, 203)
                        embed.set_footer(text="Ціна реакції 10 рун")
                        embed.set_image(url=random_hug_gifs)
                        if ctx.author.premium_since is None:
                            await collection.update_one({"id": ctx.author.id}, {"$inc": {"balance": -10}})
                        await ctx.send(embed=embed)
        else:
            await ctx.send("У вас недостатньо коштів шоб когось обійняти")


    @commands.slash_command(description="Уїби котику по рофлянчику")
    async def reaction_punch(ctx, member: disnake.Member = None):
        await ctx.response.defer()
        a = await collection.find_one({"id": ctx.author.id})
        if a['balance']>=10 or ctx.author.premium_since is not None:
            if not member:
                await ctx.send(f"{ctx.author.mention}, немає кому вдарити :c")
                return

            punch_gifs = [
                "https://media.tenor.com/qDDsivB4UEkAAAAM/anime-fight.gif",
                "https://media.tenor.com/p_mMicg1pgUAAAAM/anya-forger-damian-spy-x-family.gif",
                "https://media.tenor.com/gmvdv-e1EhcAAAAM/weliton-amogos.gif",
                "https://media.tenor.com/nWTDZU5WQ4oAAAAM/anime-punching.gif",
                "https://media.tenor.com/aEX1wE-WrEMAAAAM/anime-right-in-the-stomach.gif"
            ]

            random_punch_gifs = random.choice(punch_gifs)

            async with aiohttp.ClientSession() as session:
                async with session.get(random_punch_gifs) as resp:
                    if resp.status != 200:
                        return await ctx.send('Не вдалося завантажити зображення...')

                    # кастомізація embed
                    embed = disnake.Embed(description=f"{ctx.author.mention} уїбашив(ла) {member.mention} ❤️")
                    embed.colour = disnake.Colour.from_rgb(255, 192, 203)  # код кольору рожевої полоски
                    embed.set_footer(text="Ціна реакції 10 рун")
                    embed.set_image(url=random_punch_gifs)
                    if ctx.author.premium_since is None:
                            await collection.update_one({"id": ctx.author.id}, {"$inc": {"balance": -10}})
                    await ctx.send(embed=embed)
        else:
            await ctx.send("У вас недостатньо коштів шоб когось вдарити")


    @commands.slash_command(description="Погудуй голодного котика")
    async def reaction_feed(ctx, member: disnake.Member = None):
        await ctx.response.defer()
        a = await collection.find_one({"id": ctx.author.id})
        if a['balance']>=10 or ctx.author.premium_since is not None:
            if not member:
                await ctx.send(f"{ctx.author.mention}, немає кого погодувати :c")
            else:
                feed_gifs = [
                    "https://i.gifer.com/7pDW.gif",
                    "https://i.gifer.com/P2ka.gif",
                    "https://media.tenor.com/Aflxvrwa0woAAAAM/kawaii-wholesome.gif",
                    "https://media.tenor.com/qi8MqDKmpl8AAAAM/lycoris-recoil-chisato.giff",
                    "https://media.tenor.com/Kpw8-sodxCcAAAAM/feed.gif"
                ]

                random_feed_gifs = random.choice(feed_gifs)

                async with aiohttp.ClientSession() as session:
                    async with session.get(random_feed_gifs) as resp:
                        if resp.status != 200:
                            return await ctx.send('Не вдалося завантажити зображення...')

                        embed = disnake.Embed(description=f"{ctx.author.mention} покормив(ла) {member.mention} ❤️")
                        embed.colour = disnake.Colour.from_rgb(255, 192, 203)
                        embed.set_footer(text="Ціна реакції 10 рун")
                        embed.set_image(url=random_feed_gifs)
                        if ctx.author.premium_since is None:
                            await collection.update_one({"id": ctx.author.id}, {"$inc": {"balance": -10}})
                        await ctx.send(embed=embed)
        else:
            await ctx.send("У вас недостатньо коштів шоб когось погодувати")

def setup(bot):
    bot.add_cog(RPCommands(bot))