import os
import disnake
from disnake.ext import commands

TOKEN = ""

bot = commands.Bot(command_prefix="!", intents=disnake.Intents.all())


@bot.command()
@commands.is_owner()
async def load(ctx, extention):
    bot.load_extension(f"cogs.{extention}")


@bot.slash_command()
@commands.has_any_role(1071255622424731738)
async def activity(ctx, playing=None, listening=None, watching=None):
    if playing is not None:
        await bot.change_presence(activity=disnake.Activity(
            name=str(playing), type=disnake.ActivityType.playing
            ))
    elif watching is not None:
        await bot.change_presence(activity=disnake.Activity(
            name=str(watching),
            type=disnake.ActivityType.watching
            ))
    elif listening is not None:
        await bot.change_presence(activity=disnake.Activity(
            name=str(listening),
            type=disnake.ActivityType.listening
            ))
    await ctx.send("Активіті встановлено")


@bot.slash_command(description="Муркнути комусь на вушко")
async def mur(ctx, member: disnake.Member = None):
    if not member:
        member = ctx.author
    await ctx.send(
        f"{ctx.author.mention} помуркав на вушко ❤️, {member.mention}!",
        delete_after=30.0)


@bot.command()
@commands.is_owner()
async def unload(ctx, extention):
    bot.unload_extension(f"cogs.{extention}")


@bot.command()
@commands.is_owner()
async def reload(ctx, extention):
    bot.reload_extension(f"cogs.{extention}")


@bot.event
async def on_slash_command_error(inter, error):
    member = await bot.fetch_user(625243872905396228)
    await member.send(f"{error}")
    await member.send(f"{inter}")


for file in os.listdir("cogs"):
    if file != "db.py":
        if file.endswith(".py"):
            bot.load_extension(f"cogs.{file[:-3]}")

bot.run(TOKEN)
