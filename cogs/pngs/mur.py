# import disnake
# from disnake.ext import commands
# import aiohttp
# import random
# import io

# bot = commands.Bot(command_prefix='!', intents=disnake.Intents.all())

# @bot.event
# async def on_ready():
#     print('Бот успішно запущений')

# @bot.event    
# async def on_message(message):
#     if bot.user.mentioned_in(message):
#         await message.add_reaction('🌙')

#     await bot.process_commands(message)
# #--- test ---#
# #@bot.command()
# #async def mur(ctx, member: disnake.Member = None):
#     #if not member:
#         #member = ctx.author
#     #await ctx.send(f"{ctx.author.mention},Помуркав на вушко ❤️, {member.mention}!", delete_after=30)
#     #await ctx.message.delete()

# @bot.command()
# async def mur(ctx, member: disnake.Member = None):
#     if not member:
#         await ctx.send(f"{ctx.author.mention}, немає кому помуркотіти :c")


#     mur_gifs = [
#         "https://media.tenor.com/MpelG44DIYsAAAAM/cats-kitty.gif",
#         "https://media.tenor.com/n_zdha99hVMAAAAM/kitty.gif",
#         "https://media.tenor.com/J5dCW4RrePEAAAAM/kitten-lion-king.gif",
#         "https://media.tenor.com/tikIIf6NJvEAAAAM/cat-sleep.gif",
#         "https://i.gifer.com/9JG0.gif",
#         "https://i.gifer.com/8T2s.gif"
#     ]

#     random_mur_gifs = random.choice(mur_gifs)

#     #async with aiohttp.ClientSession() as session:
#         #async with session.get(random_mur_gifs) as resp:
#             #if resp.status != 200:
#                 #return await ctx.send('Не вдалося завантажити зображення...')
#             #data = io.BytesIO(await resp.read())
#             #await ctx.send(f"{ctx.author.mention} помуркав(ла) {member.mention} ❤️", file=disnake.File(data, 'pat.gif'))

#     async with aiohttp.ClientSession() as session:
#         async with session.get(random_mur_gifs) as resp:
#             if resp.status != 200:
#                 return await ctx.send('Не вдалося завантажити зображення...')
#             data = io.BytesIO(await resp.read())

#             # кастомізація embed
#             embed = disnake.Embed(description=f"{ctx.author.mention} помуркав(ла) {member.mention} ❤️")
#             embed.colour = disnake.Colour.from_rgb(255, 192, 203)  # код кольору рожевої полоски
#             embed.set_footer(text="Ціна реакції 10 рун")
#             embed.set_image(url=random_mur_gifs)

#             await ctx.send(embed=embed)
#     await ctx.message.delete()

# @bot.command()
# async def kiss(ctx, member: disnake.Member = None):
#     if not member:
#         await ctx.send(f"{ctx.author.mention}, немає кому поцілувати :c")
#         return

#     kiss_gifs = [
#         "https://media.tenor.com/217aKgnf16sAAAAM/kiss.gif",
#         "https://media.tenor.com/IM4-RWRjSNgAAAAM/kiss.gif",
#         "https://media.tenor.com/QjMZ6Dx33_QAAAAM/kuss-kussi.gif",
#         "https://media.tenor.com/wPzIJLI3IeQAAAAM/kiss-hot.gif",
#         "https://media.tenor.com/U7h-gyy--akAAAAM/kiss.gif",
#         "https://media.giphy.com/media/bm2O3nXTcKJeU/giphy.gif",
#         "https://media.giphy.com/media/G3va31oEEnIkM/giphy.gif"
#     ]

#     random_kiss_gifs = random.choice(kiss_gifs)

#     async with aiohttp.ClientSession() as session:
#         async with session.get(random_kiss_gifs) as resp:
#             if resp.status != 200:
#                 return await ctx.send('Не вдалося завантажити зображення...')
#             data = io.BytesIO(await resp.read())

#             # кастомізація embed
#             embed = disnake.Embed(description=f"{ctx.author.mention} поцілував(ла) {member.mention} ❤️")
#             embed.colour = disnake.Colour.from_rgb(255, 192, 203)  # код кольору рожевої полоски
#             embed.set_footer(text="Ціна реакції 10 рун")
#             embed.set_image(url=random_kiss_gifs)

#             await ctx.send(embed=embed)
#     await ctx.message.delete()

# @bot.command()
# async def pat(ctx, member: disnake.Member = None):
#     if not member:
#         await ctx.send(f"{ctx.author.mention}, немає кому гладити :c")
#         return

#     pat_gifs = [
#         "https://media.tenor.com/qjHkX9X0FOQAAAAS/milk-and-mocha-pat.gif",
#         "https://media.tenor.com/oGbO8vW_eqgAAAAM/spy-x-family-anya.gif",
#         "https://media.tenor.com/Dbg-7wAaiJwAAAAM/aharen-aharen-san.gif",
#         "https://media.tenor.com/aZFqg65KvssAAAAM/pat-anime.gif",
#         "https://media.tenor.com/JsjHFFy5O40AAAAM/kitten-pat.giff"
#     ]

#     random_pat_gifs = random.choice(pat_gifs)

#     async with aiohttp.ClientSession() as session:
#         async with session.get(random_pat_gifs) as resp:
#             if resp.status != 200:
#                 return await ctx.send('Не вдалося завантажити зображення...')
#             data = io.BytesIO(await resp.read())

#             # кастомізація embed
#             embed = disnake.Embed(description=f"{ctx.author.mention} погладив(ла) {member.mention} ❤️")
#             embed.colour = disnake.Colour.from_rgb(255, 192, 203)  # код кольору рожевої полоски
#             embed.set_footer(text="Ціна реакції 10 рун")
#             embed.set_image(url=random_pat_gifs)

#             await ctx.send(embed=embed)
#     await ctx.message.delete()

# @bot.command()
# async def hug(ctx, member: disnake.Member = None):
#     if not member:
#         await ctx.send(f"{ctx.author.mention}, немає кому обійняти :c")
#         return

#     hug_gifs = [
#         "https://media.tenor.com/NGFif4dxa-EAAAAj/hug-hugs.gif",
#         "https://media.tenor.com/S4he5WCX9lEAAAAM/hugs-cuddle.gif",
#         "https://media.tenor.com/-evl3vUtVhEAAAAM/hugs-cuddle.gif",
#         "https://media.tenor.com/J7eGDvGeP9IAAAAM/enage-kiss-anime-hug.gif",
#         "https://media.tenor.com/3mr1aHrTXSsAAAAM/hug-anime.gif"
#     ]

#     random_hug_gifs = random.choice(hug_gifs)

#     async with aiohttp.ClientSession() as session:
#         async with session.get(random_hug_gifs) as resp:
#             if resp.status != 200:
#                 return await ctx.send('Не вдалося завантажити зображення...')
#             data = io.BytesIO(await resp.read())

#             # кастомізація embed
#             embed = disnake.Embed(description=f"{ctx.author.mention} обійняв(ла) {member.mention} ❤️")
#             embed.colour = disnake.Colour.from_rgb(255, 192, 203)  # код кольору рожевої полоски
#             embed.set_footer(text="Ціна реакції 10 рун")
#             embed.set_image(url=random_hug_gifs)

#             await ctx.send(embed=embed)
#     await ctx.message.delete()

# @bot.command()
# async def punch(ctx, member: disnake.Member = None):
#     if not member:
#         await ctx.send(f"{ctx.author.mention}, немає кому вдарити :c")
#         return

#     punch_gifs = [
#         "https://media.tenor.com/qDDsivB4UEkAAAAM/anime-fight.gif",
#         "https://media.tenor.com/p_mMicg1pgUAAAAM/anya-forger-damian-spy-x-family.gif",
#         "https://media.tenor.com/gmvdv-e1EhcAAAAM/weliton-amogos.gif",
#         "https://media.tenor.com/nWTDZU5WQ4oAAAAM/anime-punching.gif",
#         "https://media.tenor.com/aEX1wE-WrEMAAAAM/anime-right-in-the-stomach.gif"
#     ]

#     random_punch_gifs = random.choice(punch_gifs)

#     async with aiohttp.ClientSession() as session:
#         async with session.get(random_punch_gifs) as resp:
#             if resp.status != 200:
#                 return await ctx.send('Не вдалося завантажити зображення...')
#             data = io.BytesIO(await resp.read())

#             # кастомізація embed
#             embed = disnake.Embed(description=f"{ctx.author.mention} уїбашив(ла) {member.mention} ❤️")
#             embed.colour = disnake.Colour.from_rgb(255, 192, 203)  # код кольору рожевої полоски
#             embed.set_footer(text="Ціна реакції 10 рун")
#             embed.set_image(url=random_punch_gifs)

#             await ctx.send(embed=embed)
#     await ctx.message.delete()

# @bot.command()
# async def feed(ctx, member: disnake.Member = None):
#     if not member:
#         await ctx.send(f"{ctx.author.mention}, немає кому вдарити :c")
#         return

#     feed_gifs = [
#         "https://i.gifer.com/7pDW.gif",
#         "https://i.gifer.com/P2ka.gif",
#         "https://media.tenor.com/Aflxvrwa0woAAAAM/kawaii-wholesome.gif",
#         "https://media.tenor.com/qi8MqDKmpl8AAAAM/lycoris-recoil-chisato.giff",
#         "https://media.tenor.com/Kpw8-sodxCcAAAAM/feed.gif"
#     ]

#     random_feed_gifs = random.choice(feed_gifs)

#     async with aiohttp.ClientSession() as session:
#         async with session.get(random_feed_gifs) as resp:
#             if resp.status != 200:
#                 return await ctx.send('Не вдалося завантажити зображення...')
#             data = io.BytesIO(await resp.read())

#             # кастомізація embed
#             embed = disnake.Embed(description=f"{ctx.author.mention} покормив(ла) {member.mention} ❤️")
#             embed.colour = disnake.Colour.from_rgb(255, 192, 203)  # код кольору рожевої полоски
#             embed.set_footer(text="Ціна реакції 10 рун")
#             embed.set_image(url=random_feed_gifs)

#             await ctx.send(embed=embed)
#     await ctx.message.delete()

# bot.run("MTA5MTQ4NTM3MDY5ODQzNjcyOQ.GsLAN8.P4VBnCRuY6yPbPbHAIWL9HbX-mMNZD0VGrT3Gw")