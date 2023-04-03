import disnake
import datetime
from disnake.ext import commands

class ModerationCommand(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    

    @commands.slash_command(description="Вийди звідчи, РОЗБІЙНИК")
    @commands.has_any_role(1079801089962016849)
    async def kick_user(self, ctx, member: disnake.Member, *, reason=None):
        if reason is not None:
            embed = disnake.Embed(
            title="КІК",
            description=f"{ctx.author.mention} кікнув {member.mention}",
            color=disnake.Colour.yellow(),
        )
            embed.set_thumbnail(url=member.avatar)
            embed.add_field(name=f"Причина: {reason}", value=f":point_right: :point_left:")

        else:
            embed = disnake.Embed(
            title="КІК",
            description=f"{ctx.author.mention} кікнув {member.mention}",
            color=disnake.Colour.yellow(),
        )
            embed.set_thumbnail(url=member.avatar)
            embed.add_field(name=f"Причини не вказано", value=f":point_right: :point_left: ")    

        await ctx.send(embed=embed, delete_after=10)    
        await member.kick(reason=reason)
    

    @commands.slash_command(description="Вийди і не вертайся")
    @commands.has_any_role(1079801089962016849)
    async def ban_user(self, ctx, member: disnake.Member, *, reason=None):
        if reason is not None:
            embed = disnake.Embed(
            title="БАН",
            description=f"{ctx.author.mention} забанив {member.mention}",
            color=disnake.Colour.yellow(),
        )
            embed.set_thumbnail(url=member.avatar)
            embed.add_field(name=f"Причина: {reason}", value=f":point_right: :point_left:")
        
        else:
            embed = disnake.Embed(
            title="БАН",
            description=f"{ctx.author.mention} забанив {member.mention}",
            color=disnake.Colour.yellow(),
        )
            embed.set_thumbnail(url=member.avatar)
            embed.add_field(name=f"Причини не вказано", value=f":point_right: :point_left: ")
        
        await ctx.send(embed=embed, delete_after=10)
        await member.ban(reason=reason)


    @commands.slash_command(description="Подумай над сутністю життя")
    @commands.has_any_role(1079801089962016849)
    async def mute_user(self, ctx, member: disnake.Member, days=0, hours=0, minutes=0, reason=None):

        channel = disnake.utils.get(ctx.guild.channels, id=1076737017448255519)
        time = (int(days)*3600)+(int(minutes))+(int(hours)*60)

        if reason is not None:

            embed = disnake.Embed(
            title="МУТ",
            description=f"{ctx.author.mention} замутив {member.mention}",
            color=disnake.Colour.yellow(),
        )
            embed.set_thumbnail(url=member.avatar)
            embed.add_field(name=f"Причина: {reason}", value=f"{time} хвилин")

        else:

            embed = disnake.Embed(
            title="МУТ",
            description=f"{ctx.author.mention} замутив {member.mention}",
            color=disnake.Colour.yellow(),
        )
            embed.set_thumbnail(url=member.avatar)
            embed.add_field(name=f"Причини не вказано", value=f"{time} хвилин")



        time = datetime.datetime.now() + datetime.timedelta(minutes=int(time))
        await ctx.send(embed=embed, delete_after=10)
        await channel.send(embed=embed)
        await member.timeout(reason=reason, until=time)


    @commands.slash_command(description="Одумався?")
    @commands.has_any_role(1079801089962016849)
    async def unmute_user(self, ctx, member: disnake.Member, reason=None):
        channel = disnake.utils.get(ctx.guild.channels, id=1076737017448255519)
        if reason is not None:
            embed = disnake.Embed(
                title="РОЗМУТ",
                description=f"{ctx.author.mention} розмутив {member.mention}",
                color=disnake.Colour.yellow(),
        )
            embed.set_thumbnail(url=member.avatar)
            embed.add_field(name=f"Причина: {reason}", value=f":point_right: :point_left:")

        else:
            embed = disnake.Embed(
                title="РОЗМУТ",
                description=f"{ctx.author.mention} розмутив {member.mention}",
                color=disnake.Colour.yellow(),
            )
            embed.set_thumbnail(url=member.avatar)
            embed.add_field(name=f"Причини не вказано", value=f":point_right: :point_left: ")
        await channel.send(embed=embed)
        await member.timeout(reason=reason, until=None)
        await ctx.send(embed=embed, delete_after=10)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user: disnake.User):
        channel = disnake.utils.get(guild.channels, id=1076737017448255519)
        embd = disnake.Embed(
            title=(str(user.name)+"#"+str(user.discriminator)),
            description=f"{user.mention} був забанений!!!",
            color=disnake.Colour.yellow()
        )
        await channel.send(embed=embd)

    @commands.Cog.listener()
    async def on_member_remove(self, user):
        guild = self.bot.get_guild(750380875706794116)
        channel = guild.get_channel(1076737017448255519)
        embd = disnake.Embed(
            title=(str(user.name)+"#"+str(user.discriminator)),
            description=f"{user.mention} покинув сервер",
            color=disnake.Colour.yellow()
        )
        await channel.send(embed=embd)

    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message):
        if message.author.get_role(1060370273695699056) is None:
            channel = disnake.utils.get(message.guild.channels, id=1076737017448255519)
            embd = disnake.Embed(
                title=(str(message.author.name)+"#"+str(message.author.discriminator)),
                description=f"Було видалено повідомлення від {message.author.mention} в каналі {message.channel.name    }",
                color=disnake.Colour.yellow(),
                timestamp=datetime.datetime.now()
            )
            embd.add_field(name="Текст", value=f"{message.content}")
            embd.set_footer(text=f"Message ID: {message.id}\nID: {message.author.id}")
            await channel.send(embed=embd)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        channel = disnake.utils.get(guild.channels, id=1076737017448255519)
        embd = disnake.Embed(
            title=(str(user.name)+"#"+str(user.discriminator)),
            description=f"{user.mention} був розбанений!!!",
            color=disnake.Colour.yellow()
        )
        await channel.send(embed=embd)

    @commands.slash_command(description="Скоро мусорка")
    @commands.has_any_role(1079801089962016849)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount+1)
        await ctx.response.send_message(f"Chat cleared")

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, disnake.ext.commands.errors.MissingRole):
            await ctx.send("Ви не модератор")

    @kick_user.error
    async def kick_user_error(self, ctx, error):
        if isinstance(error, disnake.ext.commands.errors.MissingRole):
            await ctx.send("Ви не модератор")


    @ban_user.error
    async def ban_user_error(self, ctx, error):
        if isinstance(error, disnake.ext.commands.errors.MissingRole):
            await ctx.send("Ви не модератор")


    @mute_user.error
    async def mute_user_error(self, ctx, error):
        if isinstance(error, disnake.ext.commands.errors.MissingRole):
            await ctx.send("Ви не модератор")


    @unmute_user.error
    async def unmute_user_error(self, ctx, error):
        if isinstance(error, disnake.ext.commands.errors.MissingRole):
            await ctx.send("Ви не модератор")


def setup(bot):
    bot.add_cog(ModerationCommand(bot))