import disnake
from disnake.ext import commands
from cogs.db import collection_marrys

class ChildrenRemove(disnake.ui.View):
    def __init__(self, child: disnake.Member, parents: list):
        super().__init__()
        self.child = child
        self.parents = parents
    #create button
    @disnake.ui.button(label="Погодитись", style=disnake.ButtonStyle.success)
    async def agree(self, button: disnake.ui.Button, ctx: disnake.Interaction):
        #check who use
        if ctx.author.id != self.child.id:
            return await ctx.send("Не лізь своїм носом в чужі стосунки", ephemeral=True)
        emed = disnake.Embed(
            title=f"{ctx.author.name} був зданий в дитбудинок",
            description="ПЛАЧЕМО ВСІЄЮ ПОЛТАВСЬКОЮ ОБЛАСТЮ, КРІМ КРЕМЕНЧУКГА"
        )
        marry = await collection_marrys.find_one({"$or": [{"id1": self.parents[0].id}, {"id2": self.parents[0].id}]})

        childrens = marry['child'].remove(self.child.id)
        await collection_marrys.update_one({"$or": [{"id1": self.parents[0].id}, {"id2": self.parents[0].id}]}, {"$set": {"child": childrens}})
        await ctx.send(f"{self.parents[0].mention} та {self.parents[1].mention} дитина була здана в дитбудинок")
        await ctx.send(embed=emed, delete_after=60)

    #create button
    @disnake.ui.button(label="Відмовити", style=disnake.ButtonStyle.red)
    async def reject(self, button: disnake.ui.Button, ctx: disnake.Interaction):
        #check who use
        if ctx.author.id != self.child.id:
            return await ctx.send("Не лізь своїм носом в чужі стосунки", ephemeral=True)
        emed = disnake.Embed(
            title=f"{ctx.author.name} відмовився йти в дитбудинок",
            description="Визиваємо органи опіки дітей"
        )
        await ctx.send(f"{self.parents[0].mention} та {self.parents[1].mention} дитина відмовилась йти в дитбудинок", delete_after=60)
        await ctx.send(embed=emed, delete_after=60)

class ChildrenRemoveCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.slash_command()
    async def children_remove(self, ctx, child: disnake.Member=None):
        #get marry info
        marry = await collection_marrys.find_one({"$or": [{"id1": ctx.author.id}, {"id2": ctx.author.id}]})
        #check member needs
        if child is None:
            return await ctx.send("Ви не вказали дитини")
        elif child.id == marry['id1'] or child.id == marry["id2"]:
            return await ctx.send("Ви не можете взяти цього користувача в діти")
        elif child.id not in marry['child']:
            return await ctx.send("Цей не ваша дитина")
        elif child.get_role(1094326464394055700) is None:
            return await ctx.send("Цей користувач не під опікою")
        parent1 = disnake.utils.get(ctx.guild.members, id=marry['id1'])
        parent2 = disnake.utils.get(ctx.guild.members, id=marry['id2'])
        embed = disnake.Embed(
            title=f"{ctx.author.name} хоче взяти під опіку {child.name}",
            description="У вас є `1 хвилина` щоб відповісти на запит",
            color=disnake.Color.from_rgb(255, 192, 203)
        )

        await ctx.send(f"{ctx.author.mention} Вас хочуть взяти в діти")
        await ctx.send(embed=embed, delete_after=60, view=ChildrenRemove(child=child, parents=[parent1, parent2]))

def setup(bot):
    bot.add_cog(ChildrenRemoveCog(bot))
