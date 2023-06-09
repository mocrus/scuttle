import disnake
from disnake.ext import commands
from cogs.db import collection



class Tops(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command(description="Топ найактивніших няшок в войсі")
    async def top_voice(self, ctx):
        #creat embed
        embed_top = disnake.Embed(
            title="Top Voice",
        )
        #get top
        rows = collection.find(limit=10).sort("vxp", -1) 
        my_data =  await rows.to_list(length=100)
        count = 0
        for row in my_data:
            #add field
            nam = disnake.utils.get(ctx.guild.members, id=int(row['id']))
            if nam == None: 
                continue
            balance = row["vxp"] 
            embed_top.add_field(
                name=f"# {count+1}. | {nam}",
                value= f"`{round(balance, 2)} хвилинок в войсі 🎙️`",
                inline = False
            )
            count += 1

        await ctx.send(embed=embed_top)

    @commands.slash_command(description="Топ найактивніших няшок в чаті")
    async def top_chat(self, ctx):
        #creat embed
        embed_top = disnake.Embed(
            title="Top Chat",
        )
        #get top
        rows = collection.find(limit=10).sort("cxp", -1) 
        my_data =  await rows.to_list(length=100)
        count = 0
        for row in my_data:
            #add field
            nam = disnake.utils.get(ctx.guild.members, id=int(row['id']))
            if nam == None: 
                continue
            balance = row["cxp"] 
            embed_top.add_field(
                name=f"# {count+1}. | {nam}",
                value= f"`{round(balance, 2)} повідомлень в чаті ✏️`",
                inline = False,
            )
            count += 1

        await ctx.send(embed=embed_top)

    @commands.slash_command(description="Топ найактивніших няшок взагалі")
    async def top_lvl(self, ctx):
        #creat embed
        embed_top = disnake.Embed(
        title="Top LVL",
        )
        #get top
        rows = collection.find(limit=10).sort("xp", -1) 
        my_data =  await rows.to_list(length=100)
        count = 0
        for row in my_data:
            #add field

            nam = disnake.utils.get(ctx.guild.members, id=int(row['id']))
            if nam == None: 
                continue
            balance = row["lvl"] 
            embed_top.add_field(
                name=f"# {count+1}. | {nam}",
                value= f"`{round(balance, 2)} рівень та {row['xp']} досвіду 📊`",
                inline = False
            )
            count += 1

        await ctx.send(embed=embed_top)


    @commands.slash_command(description="Топ найактивніших няшок взагалі", )
    async def top_balance(self, ctx):
        #get emoji
        emj = disnake.utils.get(ctx.guild.emojis, id=1085693327065747517)
        #creat embed
        embed_top = disnake.Embed(
        title="Top Balance",
        )
        #get top
        rows = collection.find(limit=10).sort("balance", -1) 
        my_data =  await rows.to_list(length=100)
        count = 0
        for row in my_data:
        #add field

            nam = disnake.utils.get(ctx.guild.members, id=int(row['id']))
            if nam == None: 
                continue
            balance = row["balance"] 
            embed_top.add_field(
                name=f"# {count+1}. | {nam}",
                value= f"`На його рахунку {round(balance, 2)}` {emj}",
                inline = False
            )
            count += 1

        await ctx.send(embed=embed_top)

    @commands.slash_command(description="Топ найактивніших няшок взагалі", )
    async def top_week(self, ctx):
        #creat embed
        embed_top = disnake.Embed(
        title="Top Week",
        )
        #get top
        rows = collection.find(limit=10).sort("week", -1) 
        my_data =  await rows.to_list(length=100)
        count = 0
        for row in my_data:
            #add field
            nam = disnake.utils.get(ctx.guild.members, id=int(row['id']))
            if nam == None: 
                continue
            balance = row["week"] 
            embed_top.add_field(
                name=f"# {count+1}. | {nam}",
                value= f"`{round(balance, 2)} повідомлень в чаті ✏️`",
                inline = False
            )
            count += 1

        await ctx.send(embed=embed_top)



def setup(bot):
    bot.add_cog(Tops(bot))