import os   
import disnake
import datetime
from disnake.ext import commands


TOKEN = "OTk1NzE2NDA1MDQxMjk5NDY3.G6v9IG.YIY9zw-N9GOEe0HznE0gajOKEX3uJWz2ZrjHjU"
TOKEN1 = "MTA4MDUzMTY5NzIzMTIxNjc1MA.G0-alE.UUXBL7VvWDo4biX9lNnM6kQW9i5v5TllOsO1iQ"

bot = commands.Bot(command_prefix="!", intents=disnake.Intents.all())
  
@bot.command()
@commands.is_owner()
async def load(ctx, extention):
    bot.load_extension(f"cogs.{extention}")


@bot.slash_command()
@commands.has_any_role(1071255622424731738)
async def activity(ctx, playing=None, listening=None, watching=None):
    if playing is not None:
        await bot.change_presence(activity=disnake.Activity(name=str(playing), type=disnake.ActivityType.playing))
    elif watching is not None:
        await bot.change_presence(activity=disnake.Activity(name=str(watching), type=disnake.ActivityType.watching))
    elif listening is not None:
        await bot.change_presence(activity=disnake.Activity(name=str(listening), type=disnake.ActivityType.listening))
    await ctx.send("Активіті встановлено")


@bot.command()  
@commands.is_owner()
async def unload(ctx, extention):
    bot.unload_extension(f"cogs.{extention}")

@bot.command()
@commands.is_owner()
async def reload(ctx, extention):   
    bot.reload_extension(f"cogs.{extention}")


for file in os.listdir("cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

bot.run(TOKEN)