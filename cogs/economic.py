import disnake
import random
import asyncio
import datetime
from contextlib import suppress
from disnake.ext import commands, tasks
from cogs.db import collection, collection_shop


class Economyc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lock = asyncio.Lock()
        self.members_to_be_charged = set()
        self.roles = [0, 1085671197229994014, 1085673412061573240, 1085707689608351814, 1085679795481878710, 
            1085709602043203594, 1085712151970328697, 1085713357253910599,
            1077218489523240993, 1085714937546014740, 1085718665741209650,
            1085719022391263313, 1085668121462984754]
    @tasks.loop(hours=1)
    async def banner_off(self):
        banners = collection_shop.find({})
        my_data = await banners.to_list(length=100)
        for member in my_data:
            if member['off'] >=datetime.datetime.now() and member is not None:
                guild = self.bot.get_guild(750380875706794116)
                memb = guild.get_member(member['id'])
                role = disnake.utils.get(guild.roles, id=self.roles[member['fon']])
                await collection_shop.delete_one({"id": memb.id, "fon": member["fon"]})
                await memb.remove_roles(role)
                await collection.update_one({"id": member}, {"$set": {"fon": None}})


    @tasks.loop(seconds=1)
    async def add_voice_act(self):
        guild = self.bot.get_guild(750380875706794116)
        async with self.lock:
            for member in self.members_to_be_charged:
                user = guild.get_member(member)
                await collection.update_one({"id": member}, {"$inc": { "xp": +1, "vxp": +1, "balance": +1 }})
                a = await collection.find_one({"id": member})
                if a['xp']-a['last']>= a['next']:
                    await collection.update_one({"id": member}, {"$inc": { "lvl": +1, "next": +150, "last": a['next'] }})
                    if a['lvl']+1 == 30:
                        role_add = disnake.utils.get(guild.roles, id=1090415612045574224)
                        await collection.update_one({"id": member}, {"$inc": {"balance": +500}})
                        await user.add_roles(role_add)
                        
                    elif a['lvl']+1 == 60:
                        role_add = disnake.utils.get(guild.roles, id=1090415980922019960) 
                        await collection.update_one({"id": member}, {"$inc": {"balance": +100}})
                        await user.add_roles(role_add)
                        
                    elif a['lvl']+1 == 90:
                        role_add = disnake.utils.get(guild.roles, id=1090416208836300941)
                        await collection.update_one({"id": member}, {"$inc": {"balance": +1500}})
                        await user.add_roles(role_add)

                    elif a['lvl']+1 == 120:
                        role_add = disnake.utils.get(guild.roles, id=1090417882388758669)
                        await collection.update_one({"id": member}, {"$inc": {"balance": +2000}})
                        await user.add_roles(role_add)
                        
    @commands.command()
    @commands.has_any_role(1081231864389447732)
    async def check_db(self, ctx):
        for member in ctx.guild.members:
            user = await collection.find_one({"id": member.id})
            if user is None and member.get_role(1060370273695699056):
                await collection.insert_one({
                        'id': member.id,
                        'balance': 0,
                        'lvl': 0,
                        'cxp': 0,
                        'vxp': 0,
                        'xp': 0,
                        "last": 0,
                        'next' : 100,
                        'week': 0,
                        'fon': None,
                        'daily': 0                  
                    })
                await ctx.author.send(f"{member.name} Додано")

        await ctx.author.send(f"Перевірку завершено успішно")

    @commands.Cog.listener()
    async def on_ready(self):
        print("go")
        self.add_voice_act.start()
        self.banner_off.start()



    @commands.Cog.listener()
    async def on_member_join(self, member):
        a, b = await collection.find_one({"id": member.id}), member.get_role(1060370273695699056)
        if a is None and b is None:
            await collection.insert_one({
                    'id': member.id,
                    'balance': 0,
                    'lvl': 0,
                    'cxp': 0,
                    'vxp': 0,
                    'xp': 0,
                    'next' : 100,
                    "week":0,
                    "last": 0,
                    'fon': None,
                    'daily': 0
            })
    
    
    @commands.slash_command(description="Чітерна штука адміна, яка зробить тебе богатим")
    @commands.has_any_role(1071255622424731738)
    async def give(self, ctx, member: disnake.Member, summary: int):
        if summary <= 0:
            await ctx.send("Дай більше не жаднічай")
        else:
            await collection.update_one({"id": member.id}, {"$inc": {"balance": +summary}})
            await ctx.send(f"{ctx.author.name} gave {summary} coins to {member.name}")

    @give.error
    async def give_eroor(self, ctx, error):
        if isinstance(error, disnake.ext.commands.errors.MissingRole):
            await ctx.send("Ви не адмін")


    @commands.slash_command()
    @commands.cooldown(1, 43200, commands.BucketType.user)
    async def daily(self, ctx):
        a = await collection.find_one({"id": ctx.author.id})
        if a['daily'] == 0:
            b = random.randint(1, 100)
            await collection.update_one({"id": ctx.author.id}, {"$inc": {"balance": +b}})
            await collection.update_one({"id": ctx.author.id}, {"$set": {"daily": 1}})
            await ctx.send(f"Ваш бонус {b}", delete_after=10)
        else:
            b = random.randint(50, 100)
            await collection.update_one({"id": ctx.author.id}, {"$inc": {"balance": +b}})
            await collection.update_one({"id": ctx.author.id}, {"$set": {"daily": 0}})
            await ctx.send(f"Ваш бонус {b}", delete_after=10)


    @commands.Cog.listener()
    async def on_message(self, message : disnake.Message):
        if self.bot.user.mentioned_in(message):
            await message.add_reaction('🌙')
        await self.bot.process_commands(message)
        with suppress(AttributeError):  
            role = disnake.utils.get(message.guild.roles, id=1060370273695699056)
            if message.author is not None:
                if role not in message.author.roles:
                    if message.channel.id not in [1066174497398468628, 1076680055780016138, 1071955972983107654, 1087073424054177902, 1072333954067202088]:
                        if len(message.content)>=5:
                            await collection.update_one({"id": message.author.id}, {"$inc": {"balance": +1, "xp": +1, "cxp": +1, "week": +1}})
                            a = await collection.find_one({"id": message.author.id})
                            if a['xp']-a['last'] >= a['next']:
                                await collection.update_many({"id": message.author.id}, {"$inc": { "lvl": +1, "next": +150, "last": a['next'] }})
                                if a['lvl']+1 == 30:
                                    role_add = disnake.utils.get(message.guild.roles, id=1090415612045574224), disnake.utils.get(message.guild.roles, id=1071967354214420601)
                                    await collection.update_one({"id": message.author.id}, {"$inc": {"balance": +500}})
                                    await message.author.add_roles(role_add)
                                    
                                elif a['lvl']+1 == 60:
                                    role_add = disnake.utils.get(message.guild.roles, id=1090415980922019960), disnake.utils.get(message.guild.roles, id=1090415612045574224)
                                    await collection.update_one({"id": message.author.id}, {"$inc": {"balance": +1000}})
                                    await message.author.add_roles(role_add)
                                    
                                elif a['lvl']+1 == 90:
                                    role_add = disnake.utils.get(message.guild.roles, id=1090416208836300941), disnake.utils.get(message.guild.roles, id=1090415980922019960)
                                    await collection.update_one({"id": message.author.id}, {"$inc": {"balance": +1500}})
                                    await message.author.add_roles(role_add)
                                    
                                elif a['lvl']+1 == 120:
                                    role_add = disnake.utils.get(message.guild.roles, id=1090417882388758669), disnake.utils.get(message.guild.roles, id=1090416208836300941)
                                    await collection.update_one({"id": message.author.id}, {"$inc": {"balance": +2000}})
                                    await message.author.add_roles(role_add)
                                    






    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        async with self.lock:
            if after.channel is None or member.voice.self_mute:
                with suppress(KeyError):
                    self.members_to_be_charged.remove(member.id)
                return
        
            self.members_to_be_charged.add(member.id)
        
            
    @daily.error
    async def everyday_bonus_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            hour = int(error.retry_after)//3600
            await ctx.send(f"{ctx.author.name} ви вже отримали свій бонус приходьте через {hour} години та {(int(error.retry_after)-hour*60*60)//60} хвилини", ephemeral=True)

def setup(bot):
    bot.add_cog(Economyc(bot))