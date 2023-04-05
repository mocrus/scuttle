import disnake
import datetime
from disnake.ext import commands
from cogs.db import collection, collection_shop



class Paginator(disnake.ui.View):
    def __init__(self, embeds: list, author_id: int = None, member: disnake.Member = None):
        super().__init__()
        self.embeds = embeds
        self.author = author_id
        self.member = member
        self.costs = [0, 2500, 2500, 2500, 3500, 3500, 3500, 4500, 4500, 5500, 5500, 6500, 6500]
        self.roles = [0, 1085671197229994014, 1085673412061573240, 1085707689608351814, 1085679795481878710, 
                    1085709602043203594, 1085712151970328697, 1085713357253910599,
                    1077218489523240993, 1085714937546014740, 1085718665741209650,
                    1085719022391263313, 1085668121462984754]
        self.fon = [0, "https://imgur.com/lxoACBR.png", "https://imgur.com/bbobocT.png", "https://imgur.com/Q9Vi03N.png", "https://imgur.com/ML0dDtu.png",
                    "https://imgur.com/UDubCJM.png", "https://imgur.com/ebjeBPa.png", "https://imgur.com/TnLpUF3.png", "https://imgur.com/dMVW5gb.png",
                    "https://imgur.com/zgu2f6c.png","https://imgur.com/RoySOmW.png", "https://imgur.com/QM8ONan.png", "https://imgur.com/hZUyD5R.png"]
        self.curent_costs = 0
        self.current_embed = 0
    

    @disnake.ui.button(label="⬅️", style=disnake.ButtonStyle.primary)
    async def under(self, button: disnake.ui.Button, ctx: disnake.Interaction):
        if ctx.author.id != self.author:
            return await ctx.send("Не лізь сожрьот 🐻", ephemeral=True)
        if self.current_embed:
            self.current_embed, self.curent_costs = self.current_embed - 1, self.curent_costs - 1
            await ctx.response.edit_message(embed=self.embeds[self.current_embed])
        else:
            return await ctx.send("Це перша сотрінка", ephemeral=True)
        
    @disnake.ui.button(label="Придбати", style=disnake.ButtonStyle.success)
    async def buy(self, button: disnake.ui.Button, ctx: disnake.Interaction):
        a = await collection.find_one({"id": ctx.author.id})
        role = disnake.utils.get(ctx.guild.roles, id=self.roles[self.curent_costs])
        if a["balance"] < self.costs[self.curent_costs]:
            return await ctx.send("У вас недостатньо коштів", ephemeral=True)
        elif ctx.author.id != self.author:
            return await ctx.send("Не лізь сожрьот 🐻", ephemeral=True)
        elif self.costs[self.curent_costs] == 0:
            return await ctx.send("Цей банер не можна купити", ephemeral=True)
        else:
            b = await collection_shop.find_one({"id": ctx.author.id, "fon": self.curent_costs})
            if b is not None:
                return await ctx.send("Ви вже купили цей банер, загляніть в інвентар", ephemeral=True)
            await collection_shop.insert_one({"id": ctx.author.id, "fon": self.curent_costs, "off": (datetime.datetime.now()+datetime.timedelta(days=7))})
            await collection.update_one({"id": ctx.author.id}, {"$inc": {"balance": -self.costs[self.curent_costs]}})
            await collection.update_one({"id": ctx.author.id}, {"$set": {"fon": self.fon[self.curent_costs]}})
            await ctx.author.add_roles(role)                   
            return await ctx.send(f"Ви успішно купили банер", ephemeral=True)

           

    @disnake.ui.button(label="➡️", style=disnake.ButtonStyle.primary)
    async def upper(self, button: disnake.ui.Button, ctx: disnake.Interaction):
        if ctx.author.id != self.author:
            return await ctx.send("Не лізь сожрьот 🐻", ephemeral=True)
        elif self.current_embed < len(self.embeds)-1:
            self.current_embed, self.curent_costs = self.current_embed + 1, self.curent_costs + 1
            await ctx.response.edit_message(embed=self.embeds[self.current_embed])
        else:
            return await ctx.send("Це остання сторінка", ephemeral=True)





class ShopsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.members_to_be_charged = set()
        self.roles = [0, 1085671197229994014, 1085673412061573240, 1085707689608351814, 1085679795481878710, 
            1085709602043203594, 1085712151970328697, 1085713357253910599,
            1077218489523240993, 1085714937546014740, 1085718665741209650,
            1085719022391263313, 1085668121462984754]
        self.cost = [0, 2500, 2500, 2500, 3500, 3500, 3500, 4500, 4500, 5500, 5500, 6500, 6500]
        self.fon = [0, "https://imgur.com/lxoACBR.png", "https://imgur.com/bbobocT.png", "https://imgur.com/Q9Vi03N.png", "https://imgur.com/ML0dDtu.png",
                    "https://imgur.com/UDubCJM.png", "https://imgur.com/ebjeBPa.png", "https://imgur.com/TnLpUF3.png", "https://imgur.com/dMVW5gb.png",
                    "https://imgur.com/zgu2f6c.png","https://imgur.com/RoySOmW.png", "https://imgur.com/QM8ONan.png", "https://imgur.com/hZUyD5R.png"]

    @commands.slash_command(description="Завітайте в наш пречудовий магазин та купіть собі щось гарне")
    async def shop(self, ctx):
        emj1 = disnake.utils.get(ctx.guild.emojis, id=1085693327065747517)
        emj2 = disnake.utils.get(ctx.guild.emojis, id=1076689168098414682)
        embed_start = disnake.Embed(
            title="Вітаю в магазині!",
            description=f"Тут ви зможете купувати банери для свого профілю.\nБанер діє 7 днів",
            color=disnake.Colour.yellow())
        embed_start.set_image(url="https://imgur.com/lxoACBR.png")
        embed_start.add_field(name="Валюту можна получати такими методами:", value="> Спілкуватись в чаті\n > Спілкуватись у войсі")
        embed_start.add_field(name=f"Щоб дізнатись свій баланас, пропишіть команду /profile\nТакож можна отримати щоденну валюту, прописавши /daily", value=f"\n", inline=False)
        member = await collection.find_one({"id": ctx.author.id})

        embed_1 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 1. Полуничка та роль до нього\n{emj2} Ціна: 2,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/lxoACBR.png").set_footer(text=f"Ваш баланс {member['balance']}")
        embed_2 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 2. Нічне небо та роль до нього\n{emj2} Ціна: 2,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/bbobocT.png").set_footer(text=f"Ваш баланс {member['balance']}") 
        embed_3 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 3. Рожеві медузки та роль до нього\n{emj2} Ціна: 2,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/Q9Vi03N.png").set_footer(text=f"Ваш баланс {member['balance']}")
        embed_4 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 4. 80's та роль до нього\n{emj2} Ціна: 3,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/ML0dDtu.png").set_footer(text=f"Ваш баланс {member['balance']}")
        embed_5 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 5. Ретро вайб та роль до нього\n{emj2} Ціна: 3,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/UDubCJM.png").set_footer(text=f"Ваш баланс {member['balance']}")
        embed_6 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 6. Спокій та роль до нього\n{emj2} Ціна: 3,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/ebjeBPa.png").set_footer(text=f"Ваш баланс {member['balance']}")
        embed_7 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 7. Кролики та роль до нього\n{emj2} Ціна: 4,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/TnLpUF3.png").set_footer(text=f"Ваш баланс {member['balance']}")
        embed_8 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 8. Дед інсульт та роль до нього\n{emj2} Ціна: 4,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/dMVW5gb.png").set_footer(text=f"Ваш баланс {member['balance']}")
        embed_9 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 9. Квіткове поле та роль до нього\n{emj2} Ціна: 5,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/zgu2f6c.png").set_footer(text=f"Ваш баланс {member['balance']}")
        embed_10 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 10. Малий мандрівник та роль до нього\n{emj2} Ціна: 5,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/RoySOmW.png").set_footer(text=f"Ваш баланс {member['balance']}")
        embed_11 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 11. Вишукане мистецтво та роль до нього\n{emj2} Ціна: 6,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/QM8ONan.png").set_footer(text=f"Ваш баланс {member['balance']}")
        embed_12 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 12. Кицюк та роль до нього\n{emj2} Ціна: 6,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/hZUyD5R.png").set_footer(text=f"Ваш баланс {member['balance']}")
        embed_13 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 13. Кастомний банер\n{emj2} Ціна: 8,000 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://s3.amazonaws.com/criterion-production/editorial_content_posts/hero/7272-/Brxs411JK46J7qbllI1W8kHqMU5TyZ_original.jpg").set_footer(text=f"Ваш баланс {member['balance']}")

        embeds = [
            embed_start,
            embed_1,
            embed_2,
            embed_3,
            embed_4,
            embed_5,
            embed_6,
            embed_7,
            embed_8,
            embed_9,
            embed_10,
            embed_11,
            embed_12,
            embed_13
        ]
        await ctx.send(embed=embeds[0], view=Paginator(embeds=embeds, author_id=ctx.author.id), delete_after=300)

    @commands.slash_command()
    async def present(self, ctx, getter: disnake.Member=None, banner_num: int = None):
        role = disnake.utils.get(ctx.guild.roles, id=self.roles[banner_num])
        get_balance = await collection.find_one({"id": ctx.author.id})['balance']
        if getter is None:
            return await ctx.send("Вкажіть кому ви хочете подарувати")
        elif get_balance < self.cost[banner_num]:
            return await ctx.send("У вас недостатньо коштів")
        elif getter.id == ctx.author.id:
            return await ctx.send("Ви не можете подарувати подарунок собі")
        await collection_shop.insert_one({"id": getter.id, "fon": self.curent_costs, "off": (datetime.datetime.now()+datetime.timedelta(days=7))})
        await ctx.send("Ви подарували банер")
        await ctx.author.add_roles(role)




def setup(bot):
    bot.add_cog(ShopsCog(bot))