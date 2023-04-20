import disnake
from disnake.ext import commands
from cogs.db import collection_marrys

class DivorceAssept(disnake.ui.View):
    def __init__(self, member: disnake.Member, author: disnake.Member):
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
        embed = disnake.Embed(
            title=f"{self.author.name} та {self.member} розвелись",
            description=f"ПЛАЧЕМО ВСІЄЮ ПОЛТАВСЬКОЮ ОБЛАСТЮ, КРІМ КРЕМЕНЧУГА"
        )
        await collection_marrys.delete_one({"$or": [{"id1": ctx.author.id}, {"id2": ctx.author.id}]})
        await self.author.remove_roles(role)
        await self.member.remove_roles(role)
        await ctx.send(embed=embed, delete_after=60)



    #create button
    @disnake.ui.button(label="Відмовити", style=disnake.ButtonStyle.red)
    async def reject(self, button: disnake.ui.Button, ctx: disnake.Interaction):
        #check who use
        if ctx.author.id != self.member.id:
            return await ctx.send("Не лізь своїм носом в чужі стосунки", ephemeral=True)
        emed = disnake.Embed(
            title=f"{ctx.author.name} відмовив(ла) {self.author.name} в розлученні",
            description="Ми раді що ви вирішили свої питання без розлучення"
        )
        await ctx.send(embed=emed, delete_after=60)
        
class DivorceCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command()
    async def devorce(self, ctx):
        #get marry info
        get_marriage = await collection_marrys.find_one({"$or": [{"id1": ctx.author.id}, {"id2": ctx.author.id}]})
        #check member needs
        if get_marriage is None:
            return await ctx.send("Ви не в відносинах")
        embed = disnake.Embed(
            title=f"У вас є `1 хвилина` щоб прийняти чи відхилити пропозицію!",
            description=f"{ctx.author.mention} зробив пропозицію {member.mention} 💙",
            colour = disnake.Colour.from_rgb(255, 192, 203))  # код кольору рожевої полоски
        
        if get_marriage['id1']==ctx.author.id:
            member = disnake.utils.get(ctx.guild.members, id=get_marriage['id2'])
        else:
            member = disnake.utils.get(ctx.guild.members, id=get_marriage['id1'])

        await collection_marrys.delete_one(get_marriage)
        await ctx.send(f"{member.mention} потрібен ваш підпис для розлучення")
        await ctx.send(embed=embed, delete_after=60)

def setup(bot):
    bot.add_cog(DivorceCog(bot))