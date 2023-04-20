import disnake
from disnake.ext import commands
from cogs.db import collection_marrys

class ChildrenAdd(disnake.ui.View):
    def __init__(self, child: disnake.Member, parents: list):
        super().__init__()
        self.child = child
        self.parents = parents
    #create button
    @disnake.ui.button(label="Погодитись", style=disnake.ButtonStyle.success)
    async def agree(self, button: disnake.ui.Button, ctx: disnake.Interaction):
        #check who use
        if ctx.author.id == self.child.id:
            return await ctx.send("Не лізь своїм носом в чужі стосунки", ephemeral=True)
        role = disnake.utils.get(ctx.guild.roles, id=1094326464394055700)
        embed = disnake.Embed(
            title="ВІМАЄМО В ВАС ПОПОВНЕННЯ В СІМ'Ї",
            description=f"У {self.parents[0].mention} та {self.parents[1].mention} народився(лась) {self.child.mention}"
        )
        await ctx.author.add_roles(role)
        await collection_marrys.update_one({"id1": self.parents['0'].id}, {"$set":{"child": [self.child.id]}})
        await ctx.send(f"{self.parents[0].mention} та {self.parents[1].mention} у вас поповнення в сім'ї")
        await ctx.send(embed=embed, delete_after=60)

    #create button
    @disnake.ui.button(label="Відмовити", style=disnake.ButtonStyle.red)
    async def reject(self, button: disnake.ui.Button, ctx: disnake.Interaction):
        #check who use
        if ctx.author.id != self.child.id:
            return await ctx.send("Не лізь своїм носом в чужі стосунки", ephemeral=True)
        emed = disnake.Embed(
            title=f"{ctx.author.name} не захтів в сім'ю",
            description="ПЛАЧЕМО ВСІЄЮ ПОЛТАВСЬКОЮ ОБЛАСТЮ, КРІМ КРЕМЕНЧУКГА"
        )
        await ctx.send(f"{self.parents[0].mention} та {self.parents[1].mention} дитина відмовилась бути в вашій сім'ї ", delete_after=60)
        await ctx.send(embed=emed, delete_after=60)


class ChildrenAddCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.slash_command()
    async def children_add(self, ctx, child: disnake.Member=None):
        #get marry info
        marry = await collection_marrys.find_one({"$or": [{"id1": ctx.author.id}, {"id2": ctx.author.id}]})
        #check member needs
        if child is None:
            return await ctx.send("Ви не вказали дитини")
        elif child.id == marry['id1'] or child.id == marry["id2"]:
            return await ctx.send("Ви не можете взяти цього користувача в діти")
        elif child.get_role(1094326464394055700) is not None:
            return await ctx.send("Цей користувач вже всиновлений")
        parent1 = disnake.utils.get(ctx.guild.members, id=marry['id1'])
        parent2 = disnake.utils.get(ctx.guild.members, id=marry['id2'])
        embed = disnake.Embed(
            title=f"{ctx.author.name} хоче взяти під опіку {child.name}",
            description="У вас є `1 хвилина` щоб відповісти на запит",
            color=disnake.Color.from_rgb(255, 192, 203)
        )
        await ctx.send(f"{ctx.author.mention} Вас хочуть взяти в діти")
        await ctx.send(embed=embed, delete_after=60, view=ChildrenAdd(child=child, parents=[parent1, parent2]))

def setup(bot):
    bot.add_cog(ChildrenAddCog(bot))
