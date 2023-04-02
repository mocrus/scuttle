import aiohttp
import disnake
import easy_pil
import random
from aiogram import Bot
from io import BytesIO
from disnake.ext import commands, tasks
import aioschedule
from disnake import File
from motor.motor_tornado import MotorClient
from easy_pil import Editor, load_image_async, Font


bot = Bot(token="6293959670:AAG8hBUsf4zECPXHQD__vo-8LZ8SZBEP1Cw")




cluster = MotorClient("mongodb+srv://mircus:0x14lzl04t39igh@botcluster.omo2cfl.mongodb.net/?retryWrites=true&w=majority")
db = cluster['botdb']
collection = db['users']
collection_shop = db['shop']

class Paginator(disnake.ui.View):
    def __init__(self, embeds: list, author_id: int = None):
        super().__init__()
        self.embeds = embeds
        self.author = author_id
        self.costs = [0, 2500, 2500, 2500, 3500, 3500, 3500, 4500, 4500, 5500, 5500, 6500, 6500]
        self.roles = [0, 1085671197229994014, 1085673412061573240, 1085707689608351814, 1085679795481878710, 
                    1085709602043203594, 1085712151970328697, 1085713357253910599,
                    1077218489523240993, 1085714937546014740, 1085718665741209650,
                    1085719022391263313, 1085668121462984754]
        self.fon = [0, "https://imgur.com/lxoACBR.png", "https://imgur.com/bbobocT.png", "https://imgur.com/Q9Vi03N.png", "https://imgur.com/ML0dDtu.png",
                    "https://imgur.com/UDubCJM.png", "https://imgur.com/ebjeBPa.png", "https://imgur.com/TnLpUF3.png", "https://imgur.com/dMVW5gb.png",
                    "https://imgur.com/zgu2f6c.png","https://imgur.com/RoySOmW.png", "https://imgur.com/QM8ONan.png", "https://imgur.com/hZUyD5R.png"]
        self.curent_costs = 0
        self.CurrentEmbed = 0
    
    @tasks.loop(hours=1)
    async def off_banner(self, ctx, role, banner):
        a = await collection_shop.find_one({"id": ctx.id, "fon": banner})
        if a['off']==0:
            await ctx.remove_roles(role)
            await collection.update_one({"id": ctx.id}, {"$set": {"fon": None}})
            await collection_shop.delete_one({"id": ctx.id, "fon": banner})
            self.off_banner.cancel()
        else:
            await collection_shop.update_one({"id": ctx.id, "fon": banner}, {"$inc": {"off" : -1}})



    @disnake.ui.button(label="⬅️", style=disnake.ButtonStyle.primary)
    async def under(self, button: disnake.ui.Button, ctx: disnake.Interaction):
        try:
            if ctx.author.id != self.author and self.author != 123:
                return await ctx.send("Не лізь сожрьот 🐻", ephemeral=True)
            if self.CurrentEmbed:
                await ctx.response.edit_message(embed=self.embeds[self.CurrentEmbed-1])
                self.CurrentEmbed = self.CurrentEmbed - 1
                self.curent_costs = self.curent_costs - 1
        except:
            return await ctx.send("Це перша сотрінка", ephemeral=True)
        
    @disnake.ui.button(label="Придбати", style=disnake.ButtonStyle.success)
    async def buy(self, button: disnake.ui.Button, ctx: disnake.Interaction):
        a = await collection.find_one({"id": ctx.author.id})
        b = await collection_shop.find_one({"id": ctx.author.id, "fon": self.curent_costs})
        role = disnake.utils.get(ctx.guild.roles, id=self.roles[self.curent_costs])
        if ctx.author.id != self.author and self.author != 123:
            return await ctx.send("Не лізь сожрьот 🐻", ephemeral=True)
        else:
            if a["balance"] < self.costs[self.curent_costs]:
                return await ctx.send("У вас недостатньо коштів", ephemeral=True)
            elif a["fon"]== self.fon[self.curent_costs]:
                await ctx.send("Ви вже використовуєте цей банер", ephemeral=True)
            elif self.costs[self.curent_costs] == 0:
                return await ctx.send("Цей банер не можна купити", ephemeral=True)
            elif b is not None:
                return await ctx.send("Ви вже купили цей банер, загляніть в інвентар", ephemeral=True)
            else:
                await collection_shop.insert_one({"id": ctx.author.id, "fon": self.curent_costs, "off": 168})
                await collection.update_one({"id": ctx.author.id}, {"$inc": {"balance": -self.costs[self.curent_costs]}})
                await collection.update_one({"id": ctx.author.id}, {"$set": {"fon": self.fon[self.curent_costs]}})
                await ctx.author.add_roles(role)
                self.off_banner.start(ctx=ctx.author, role=role, banner=self.curent_costs)                    
                return await ctx.send(f"Ви успішно купили банер", ephemeral=True)

    @disnake.ui.button(label="➡️", style=disnake.ButtonStyle.primary)
    async def upper(self, button: disnake.ui.Button, ctx: disnake.Interaction):
        if ctx.author.id != self.author and self.author != 123:
            return await ctx.send("Не лізь сожрьот 🐻", ephemeral=True)
        if self.CurrentEmbed != len(self.embeds):
            await ctx.response.edit_message(embed=self.embeds[self.CurrentEmbed+1])
            self.CurrentEmbed = self.CurrentEmbed + 1
            self.curent_costs = self.curent_costs + 1


class Economyc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.act = []

    @tasks.loop(seconds=1)
    async def chek_voice(self):
        guild = self.bot.get_guild(750380875706794116)
        for channel in guild.voice_channels:
            for member in channel.members:
                if member.voice.self_mute is False and member.get_role(1060370273695699056) is None:
                    await collection.update_many({"id": member.id}, {"$inc": {"xp": +1}})
                    await collection.update_one({"id": member.id}, {"$inc": {"vxp": +1}})
                    await collection.update_one({"id": member.id}, {"$inc": {"balance": +1}})
                    a = await collection.find_one({"id": member.id})
                    if a['xp']-a['last']>= a['next']:
                        await collection.update_many({"id": member.id}, {"$inc": {"last": +a['next']}})
                        await collection.update_one({"id": member.id}, {"$inc": {"lvl": +1}})
                        await collection.update_one({"id": member.id}, {"$inc": {"next": +150}})

    




    @tasks.loop(hours=1)
    async def off_banner(self, ctx, role, banner):
        a = await collection_shop.find_one({"id": ctx.id, "fon": banner})
        if a['off']==0:
            await ctx.remove_roles(role)
            await collection.update_one({"id": ctx.id}, {"$set": {"fon": None}})
            await collection_shop.delete_one({"id": ctx.id, "fon": banner})
            a = await collection_shop.find_one({"id": ctx.id, "fon": banner})
            if a is None:
                self.off_banner.cancel()
        else:
            await collection_shop.update_one({"id": ctx.id, "fon": banner}, {"$inc": {"off" : -1}})


    async def week(self):
        a = collection.find(limit=1).sort("week", -1)
        guild = self.bot.get_guild(750380875706794116)
        memb = await a.to_list(length=100)
        for b in memb:
            mem = guild.get_member(b['id'])
        ava = await easy_pil.load_image_async(mem.display_avatar.url)
        ava_edit = Editor(image=ava).resize(size=(150, 150)).rounded_corners(radius=100)
        img = Editor("cogs/pngs/back.png")
        if len(mem.name) >= 17:
            name = str(mem.name[:17]) + "..."
        else:
            name = mem.name
        img.text(position=(377, 226), text=name, font=Font.montserrat(variant="regular", size=25), color='white')
        img.text(position=(377, 288), text=f"{mem.top_role.name}", font=Font.montserrat(variant="regular", size=25), color='white')
        img.paste(image=ava_edit, position=(180, 187))
        img.save(fp='cogs\\pngs\\week.png', format='png')

        with open('cogs\pngs\week.png', 'rb') as f:
            image_data = f.read()
        with BytesIO(image_data) as image_binary:
            await guild.edit(banner=image_binary.read())
        await collection.update_many({}, {"$set": {"week": 0}})


    @commands.Cog.listener()
    async def on_ready(self):
        
        for guild in self.bot.guilds:
            aioschedule.every().sunday.at("23:59").do(self.week, args=self)
            channel = disnake.utils.get(self.bot.get_all_channels(), id=1082933881033986078)
            for member in guild.members:
                member : disnake.Member
                a, b = await collection.find_one({"id": member.id}), member.get_role(1060370273695699056)
                if a is None and b is None:
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
                    await channel.send(f"{member.name} was added")
                c = collection_shop.find({"id": member.id})
                my_data =  await c.to_list(length=100)
                rol = [0, 1085644279063523399, 1085673412061573240, 1085707689608351814, 1085679795481878710, 
                    1085709602043203594, 1085712151970328697, 1085713357253910599,
                    1077218489523240993, 1085714937546014740, 1085718665741209650,
                    1085719022391263313, 1085668121462984754]
                for row in my_data:

                    role = disnake.utils.get(guild.roles, id=rol[row['fon']])

                    self.off_banner.start(ctx=member, role=role, banner=row['fon'])
                self.chek_voice.start()




    @commands.Cog.listener()
    async def on_member_join(self, member):
        a, b = await collection.find_one({"id": member.id}), member.get_role(1060370273695699056)
        if a is None and b is None:
            await collection.insert_one({
                    'id': member.id,
                    'balance': 0.0,
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
        if message.author.get_role(1060370273695699056) is None:
            if message.channel.id not in [1066174497398468628, 1076680055780016138, 1071955972983107654, 1087073424054177902, 1072333954067202088]:
                if len(message.content)>=5:
                    await collection.update_one({"id": message.author.id}, {"$inc": {"balance": +1}})
                    await collection.update_one({"id": message.author.id}, {"$inc": {"xp": +1}})
                    await collection.update_one({"id": message.author.id}, {"$inc": {"cxp": +1}})
                    await collection.update_one({"id": message.author.id}, {"$inc": {"week": +1}})
                    a = await collection.find_one({"id": message.author.id})
                    if a['xp']-a['last'] >= a['next']:
                        await collection.update_one({"id": message.author.id}, {"$inc": {"lvl": +1}})
                        await collection.update_one({"id": message.author.id}, {"$inc": {"last": int(a['next'])}})
                        await collection.update_one({"id": message.author.id}, {"$inc": {"next": +150}})

    @commands.slash_command(description="Покаже ваш інвентар профілів")
    async def invetar(self, ctx, member: disnake.Member=None):
        if member is None:
            rows = collection_shop.find({"id": ctx.author.id})
        else:
            rows = collection_shop.find({"id": member.id})
        embed_invent = disnake.Embed(
            title="Inventar",
        )
        my_data =  await rows.to_list(length=100)
        if my_data != []: 
            fons = [0, "1. Полуничка та роль до нього", "2. Нічне небо та роль до нього", "3. Рожеві медузки та роль до нього", 
                    "4. 80's та роль до нього", "5. Ретро вайб та роль до нього", "6. Спокій та роль до нього",
                    "7. Кролики та роль до нього", "8. Дед інсульт та роль до нього", "9. Квіткове поле та роль до нього",
                    "10. Малий мандрівник та роль до нього", "11. Вишукане мистецтво та роль до нього", "12. Кицюк та роль до нього"]
            for row in my_data:
                embed_invent.add_field(
                    name=f"{fons[row['fon']]}",
                    value= f"Діє {row['off']} годин",
                    inline = False
                )
            await ctx.send(embed=embed_invent)
        else:
            await ctx.send("Ваш інвентар пустий. Купіть щось в магазині")
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
        
        embed_1 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 1. Полуничка та роль до нього\n{emj2} Ціна: 2,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/lxoACBR.png")
        embed_2 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 2. Нічне небо та роль до нього\n{emj2} Ціна: 2,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/bbobocT.png") 
        embed_3 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 3. Рожеві медузки та роль до нього\n{emj2} Ціна: 2,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/Q9Vi03N.png")
        embed_4 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 4. 80's та роль до нього\n{emj2} Ціна: 3,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/ML0dDtu.png")
        embed_5 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 5. Ретро вайб та роль до нього\n{emj2} Ціна: 3,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/UDubCJM.png")
        embed_6 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 6. Спокій та роль до нього\n{emj2} Ціна: 3,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/ebjeBPa.png")
        embed_7 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 7. Кролики та роль до нього\n{emj2} Ціна: 4,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/TnLpUF3.png")
        embed_8 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 8. Дед інсульт та роль до нього\n{emj2} Ціна: 4,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/dMVW5gb.png")
        embed_9 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 9. Квіткове поле та роль до нього\n{emj2} Ціна: 5,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/zgu2f6c.png")
        embed_10 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 10. Малий мандрівник та роль до нього\n{emj2} Ціна: 5,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/RoySOmW.png")
        embed_11 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 11. Вишукане мистецтво та роль до нього\n{emj2} Ціна: 6,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/QM8ONan.png")
        embed_12 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 12. Кицюк та роль до нього\n{emj2} Ціна: 6,500 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://imgur.com/hZUyD5R.png")
        embed_13 = disnake.Embed(
                    title="Вітаю в магазині!",
                    description=f"{emj2} 13. Кастомний банер\n{emj2} Ціна: 8,000 рун {emj1}",
                    color=disnake.Colour.yellow()).set_image(url="https://s3.amazonaws.com/criterion-production/editorial_content_posts/hero/7272-/Brxs411JK46J7qbllI1W8kHqMU5TyZ_original.jpg")

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
    

    @commands.slash_command(description="Топ найактивніших няшок в войсі")
    async def top_voice(self, ctx):
        embed_top = disnake.Embed(
            title="Top Voice",
        )
        rows = collection.find(limit=10).sort("vxp", -1) 
        my_data =  await rows.to_list(length=100)
        count = 0
        for row in my_data:
            nam = disnake.utils.get(ctx.guild.members, id=int(row['id']))
            if nam == None: 
                continue
            balance = row["vxp"] 
            embed_top.add_field(
                name=f"# {count+1}. | {nam}",
                value= f"{round(balance, 2)}🎙️",
                inline = False
            )
            count += 1

        await ctx.send(embed=embed_top)
        
    @commands.slash_command(description="Топ найактивніших няшок в чаті")
    async def top_chat(self, ctx):
        embed_top = disnake.Embed(
            title="Top Chat",
        )
        rows = collection.find(limit=10).sort("cxp", -1) 
        my_data =  await rows.to_list(length=100)
        count = 0
        for row in my_data:
            nam = disnake.utils.get(ctx.guild.members, id=int(row['id']))
            if nam == None: 
                continue
            balance = row["cxp"] 
            embed_top.add_field(
                name=f"# {count+1}. | {nam}",
                value= f"{round(balance, 2)}✏️",
                inline = False
            )
            count += 1

        await ctx.send(embed=embed_top)

    @commands.slash_command(description="Топ найактивніших няшок взагалі")
    async def top_all(self, ctx):
        embed_top = disnake.Embed(
        title="Top All",
        )
        rows = collection.find(limit=10).sort("xp", -1) 
        my_data =  await rows.to_list(length=100)
        count = 0
        for row in my_data:
            nam = disnake.utils.get(ctx.guild.members, id=int(row['id']))
            if nam == None: 
                continue
            balance = row["xp"] 
            embed_top.add_field(
                name=f"# {count+1}. | {nam}",
                value= f"{round(balance, 2)}📊",
                inline = False
            )
            count += 1

        await ctx.send(embed=embed_top)


    @commands.slash_command(description="Топ найактивніших няшок взагалі", )
    async def top_balance(self, ctx):
        emj = disnake.utils.get(ctx.guild.emojis, id=1085693327065747517)
        embed_top = disnake.Embed(
        title="Top Balance",
        )
        rows = collection.find(limit=10).sort("balance", -1) 
        my_data =  await rows.to_list(length=100)
        count = 0
        for row in my_data:
            nam = disnake.utils.get(ctx.guild.members, id=int(row['id']))
            if nam == None: 
                continue
            balance = row["balance"] 
            embed_top.add_field(
                name=f"# {count+1}. | {nam}",
                value= f"{round(balance, 2)} {emj}",
                inline = False
            )
            count += 1

        await ctx.send(embed=embed_top)

    @commands.slash_command(description="Покаже ваш прекрасний профіль")
    async def profile(self, ctx, member: disnake.Member=None):
        await ctx.response.defer()
        
        if member is None:
            a = await collection.find_one({"id" : ctx.author.id})
            image = await load_image_async(ctx.author.display_avatar.url)
            name = str(ctx.author.name)
            if len(name)>13:
                name = name[:11]+"..." + "#" + str(ctx.author.discriminator)
            else:
                name = name + "#" + str(ctx.author.discriminator)
                name = " " * (18 - len(name)) + name
        else:
            a = await collection.find_one({"id" : member.id})
            image = await load_image_async(member.display_avatar.url)
            name = str(member.name)
            if len(name)>13:
                name = name[:11]+"..." + "#" + str(member.discriminator)
            else:
                name = name + "#" + str(member.discriminator)
                name = " " * (18 - len(name)) + name    

        edit = Editor('cogs/pngs/background.png')

        font = Font.poppins(size=25, variant='regular')

        
        edit_ava = Editor(image).circle_image().resize((152, 152))
        if a['fon'] is None:
            img = Editor("cogs/pngs/banner.png")
        else:
            img = await load_image_async(a['fon'])
        edit_bckg = Editor(img).resize(size=(900, 255)).rounded_corners(radius=20)

        edit.paste(image=edit_bckg, position=(0, 0))
        edit.paste(Editor('cogs/pngs/ProgressBar.png'), (381, 210))
        edit.paste(Editor('cogs/pngs/ava.png'), position=(81, 165))
        edit.paste(edit_ava, position=(100, 187))
        prosent = (a['xp']-a['last'])/a['next']*100
        prosent = round(prosent, 2)
        if prosent != 0:
            width = 250*prosent/100
            x = 427+width
        else:
            width = 1
            x = 427
        edit.rectangle(position=(427, 253), width=250, height=2, outline="white", fill="white")
        edit.rectangle(position=(427, 253), width=width, height=2, outline="#FF00FF", fill="#FF00FF")
        
        edit.ellipse(position=(x, 245), width=20, height=20, fill="#FF00FF")
        edit.text(position=(52, 390), font=font, color="white", text=name)

        voice = int(a['vxp'])
        voice = "0" * (6 - len(str(voice))) + str(voice)
        chat = int(a["cxp"])
        chat = "0" * (6 - len(str(chat))) + str(chat)
        balance = int(a["balance"])
        balance = "0" * (6 - len(str(balance))) + str(balance)
        lvl = a['lvl']
        edit.text(position=(705, 240), text=f"{prosent} % / $ {lvl}", font=font, color="white")
        edit.text((400, 420), text=voice, color="white", font=font)
        edit.text((570, 420), text=chat, color="white", font=font)
        edit.text((740, 420), text=balance, color="white", font=font)

        file = File(fp=edit.image_bytes, filename="profile.png")
        
        await ctx.send(file=file)
        
    @commands.slash_command()
    async def set_banner(self, ctx, number:int):
        a = await collection_shop.find_one({"id": ctx.author.id, "fon": number})
        if a is None:
            await ctx.send("У вас нема цього банеру в інвентарі", delete_after=10)
        else:
            fons = [0, "https://imgur.com/lxoACBR.png", "https://imgur.com/bbobocT.png", "https://imgur.com/Q9Vi03N.png", "https://imgur.com/ML0dDtu.png",
                    "https://imgur.com/UDubCJM.png", "https://imgur.com/ebjeBPa.png", "https://imgur.com/TnLpUF3.png", "https://imgur.com/dMVW5gb.png",
                    "https://imgur.com/zgu2f6c.png","https://imgur.com/RoySOmW.png", "https://imgur.com/QM8ONan.png", "https://imgur.com/hZUyD5R.png"]
            await collection.update_one({"id": ctx.author.id}, {"$set": {"fon": fons[a['fon']]}})
            await ctx.send("Ви успішно застосували банер", delete_after=10)



    @commands.slash_command(description="Помуркай любимому котику")
    async def reaction_mur(ctx, member: disnake.Member = None):
        await ctx.response.defer()
        a = await collection.find_one({"id": ctx.author.id})
        if a['balance']>=10:
            if member is None:
                await ctx.send(f"{ctx.author.mention}, немає кому помуркотіти :c")

            else:
                mur_gifs = [
                    "https://media.tenor.com/MpelG44DIYsAAAAM/cats-kitty.gif",
                    "https://media.tenor.com/n_zdha99hVMAAAAM/kitty.gif",
                    "https://media.tenor.com/J5dCW4RrePEAAAAM/kitten-lion-king.gif",
                    "https://media.tenor.com/tikIIf6NJvEAAAAM/cat-sleep.gif",
                    "https://i.gifer.com/9JG0.gif",
                    "https://i.gifer.com/8T2s.gif"
                ]

                random_mur_gifs = random.choice(mur_gifs)

                async with aiohttp.ClientSession() as session:
                    async with session.get(random_mur_gifs) as resp:
                        if resp.status != 200:
                            return await ctx.send('Не вдалося завантажити зображення...')

                        embed = disnake.Embed(description=f"{ctx.author.mention} помуркав(ла) {member.mention} ❤️")
                        embed.colour = disnake.Colour.from_rgb(255, 192, 203)
                        embed.set_footer(text="Ціна реакції 10 рун")
                        embed.set_image(url=random_mur_gifs)
                        await collection.update_one({"id": ctx.author.id}, {"$inc": {"balance": -10}})
                        await ctx.send(embed=embed)
        else:
            await ctx.send("У вас недостатньо коштів шоб когосмусь помуркати")


    @commands.slash_command(description="Поцілуй любимого котика")
    async def reaction_kiss(ctx, member: disnake.Member = None):
        await ctx.response.defer()
        a = await collection.find_one({"id": ctx.author.id})
        if a['balance']>=10:
            if not member:
                await ctx.send(f"{ctx.author.mention}, немає кому поцілувати :c")
            else:
                kiss_gifs = [
                    "https://media.tenor.com/217aKgnf16sAAAAM/kiss.gif",
                    "https://media.tenor.com/IM4-RWRjSNgAAAAM/kiss.gif",
                    "https://media.tenor.com/QjMZ6Dx33_QAAAAM/kuss-kussi.gif",
                    "https://media.tenor.com/wPzIJLI3IeQAAAAM/kiss-hot.gif",
                    "https://media.tenor.com/U7h-gyy--akAAAAM/kiss.gif",
                    "https://media.giphy.com/media/bm2O3nXTcKJeU/giphy.gif",
                    "https://media.giphy.com/media/G3va31oEEnIkM/giphy.gif"
                ]

                random_kiss_gifs = random.choice(kiss_gifs)

                async with aiohttp.ClientSession() as session:
                    async with session.get(random_kiss_gifs) as resp:
                        if resp.status != 200:
                            return await ctx.send('Не вдалося завантажити зображення...')

                        embed = disnake.Embed(description=f"{ctx.author.mention} поцілував(ла) {member.mention} ❤️")
                        embed.colour = disnake.Colour.from_rgb(255, 192, 203)
                        embed.set_footer(text="Ціна реакції 10 рун")
                        embed.set_image(url=random_kiss_gifs)
                        await collection.update_one({"id": ctx.author.id}, {"$inc": {"balance": -10}})
                        await ctx.send(embed=embed)

        else:
            await ctx.send("У вас недостатньо коштів шоб когось поцілувати")


    @commands.slash_command(description="Погладь свого котика")
    async def reaction_pat(ctx, member: disnake.Member = None):
        await ctx.response.defer()
        a = await collection.find_one({"id": ctx.author.id})
        if a['balance']>=10:
            if not member:
                await ctx.send(f"{ctx.author.mention}, немає кому гладити :c")
                
            else:
                pat_gifs = [
                    "https://media.tenor.com/qjHkX9X0FOQAAAAS/milk-and-mocha-pat.gif",
                    "https://media.tenor.com/oGbO8vW_eqgAAAAM/spy-x-family-anya.gif",
                    "https://media.tenor.com/Dbg-7wAaiJwAAAAM/aharen-aharen-san.gif",
                    "https://media.tenor.com/aZFqg65KvssAAAAM/pat-anime.gif",
                    "https://media.tenor.com/JsjHFFy5O40AAAAM/kitten-pat.giff"
                ]

                random_pat_gifs = random.choice(pat_gifs)

                async with aiohttp.ClientSession() as session:
                    async with session.get(random_pat_gifs) as resp:
                        if resp.status != 200:
                            return await ctx.send('Не вдалося завантажити зображення...')

                        # кастомізація embed
                        embed = disnake.Embed(description=f"{ctx.author.mention} погладив(ла) {member.mention} ❤️")
                        embed.colour = disnake.Colour.from_rgb(255, 192, 203)  # код кольору рожевої полоски
                        embed.set_footer(text="Ціна реакції 10 рун")
                        embed.set_image(url=random_pat_gifs)
                        await collection.update_one({"id": ctx.author.id}, {"$inc": {"balance": -10}})
                        await ctx.send(embed=embed)

        else:
            await ctx.send("У вас недостатньо коштів шоб когось погладити")

    @commands.slash_command(description="Обійми сумуючого котика")
    async def reaction_hug(ctx, member: disnake.Member = None):
        await ctx.response.defer()
        a = await collection.find_one({"id": ctx.author.id})
        if a['balance']>=10:
            if not member:
                await ctx.send(f"{ctx.author.mention}, немає кому обійняти :c")
                
            else:
                hug_gifs = [
                    "https://media.tenor.com/NGFif4dxa-EAAAAj/hug-hugs.gif",
                    "https://media.tenor.com/S4he5WCX9lEAAAAM/hugs-cuddle.gif",
                    "https://media.tenor.com/-evl3vUtVhEAAAAM/hugs-cuddle.gif",
                    "https://media.tenor.com/J7eGDvGeP9IAAAAM/enage-kiss-anime-hug.gif",
                    "https://media.tenor.com/3mr1aHrTXSsAAAAM/hug-anime.gif"
                ]

                random_hug_gifs = random.choice(hug_gifs)

                async with aiohttp.ClientSession() as session:
                    async with session.get(random_hug_gifs) as resp:
                        if resp.status != 200:
                            return await ctx.send('Не вдалося завантажити зображення...')


                        embed = disnake.Embed(description=f"{ctx.author.mention} обійняв(ла) {member.mention} ❤️")
                        embed.colour = disnake.Colour.from_rgb(255, 192, 203)
                        embed.set_footer(text="Ціна реакції 10 рун")
                        embed.set_image(url=random_hug_gifs)
                        await collection.update_one({"id": ctx.author.id}, {"$inc": {"balance": -10}})
                        await ctx.send(embed=embed)
        else:
            await ctx.send("У вас недостатньо коштів шоб когось обійняти")


    @commands.slash_command(description="Уїби котику по рофлянчику")
    async def reaction_punch(ctx, member: disnake.Member = None):
        await ctx.response.defer()
        a = await collection.find_one({"id": ctx.author.id})
        if a['balance']>=10:
            if not member:
                await ctx.send(f"{ctx.author.mention}, немає кому вдарити :c")
                return

            punch_gifs = [
                "https://media.tenor.com/qDDsivB4UEkAAAAM/anime-fight.gif",
                "https://media.tenor.com/p_mMicg1pgUAAAAM/anya-forger-damian-spy-x-family.gif",
                "https://media.tenor.com/gmvdv-e1EhcAAAAM/weliton-amogos.gif",
                "https://media.tenor.com/nWTDZU5WQ4oAAAAM/anime-punching.gif",
                "https://media.tenor.com/aEX1wE-WrEMAAAAM/anime-right-in-the-stomach.gif"
            ]

            random_punch_gifs = random.choice(punch_gifs)

            async with aiohttp.ClientSession() as session:
                async with session.get(random_punch_gifs) as resp:
                    if resp.status != 200:
                        return await ctx.send('Не вдалося завантажити зображення...')

                    # кастомізація embed
                    embed = disnake.Embed(description=f"{ctx.author.mention} уїбашив(ла) {member.mention} ❤️")
                    embed.colour = disnake.Colour.from_rgb(255, 192, 203)  # код кольору рожевої полоски
                    embed.set_footer(text="Ціна реакції 10 рун")
                    embed.set_image(url=random_punch_gifs)
                    await collection.update_one({"id": ctx.author.id}, {"$inc": {"balance": -10}})
                    await ctx.send(embed=embed)
        else:
            await ctx.send("У вас недостатньо коштів шоб когось вдарити")


    @commands.slash_command(description="Погудуй голодного котика")
    async def reaction_feed(ctx, member: disnake.Member = None):
        await ctx.response.defer()
        a = await collection.find_one({"id": ctx.author.id})
        if a['balance']>=10:
            if not member:
                await ctx.send(f"{ctx.author.mention}, немає кого погодувати :c")
            else:
                feed_gifs = [
                    "https://i.gifer.com/7pDW.gif",
                    "https://i.gifer.com/P2ka.gif",
                    "https://media.tenor.com/Aflxvrwa0woAAAAM/kawaii-wholesome.gif",
                    "https://media.tenor.com/qi8MqDKmpl8AAAAM/lycoris-recoil-chisato.giff",
                    "https://media.tenor.com/Kpw8-sodxCcAAAAM/feed.gif"
                ]

                random_feed_gifs = random.choice(feed_gifs)

                async with aiohttp.ClientSession() as session:
                    async with session.get(random_feed_gifs) as resp:
                        if resp.status != 200:
                            return await ctx.send('Не вдалося завантажити зображення...')

                        embed = disnake.Embed(description=f"{ctx.author.mention} покормив(ла) {member.mention} ❤️")
                        embed.colour = disnake.Colour.from_rgb(255, 192, 203)
                        embed.set_footer(text="Ціна реакції 10 рун")
                        embed.set_image(url=random_feed_gifs)
                        await collection.update_one({"id": ctx.author.id}, {"$inc": {"balance": -10}})
                        await ctx.send(embed=embed)
        else:
            await ctx.send("У вас недостатньо коштів шоб когось погодувати")

    @commands.slash_command(description="Ще одна чітерна штука яка зробить адміна ще гарнішим")
    async def buy_banner(self, ctx, url: str):
        await ctx.respose.defer()
        a = await collection.find_one({"id": ctx.author.id})
        if ctx.author.get_role(1071952131940171868) is None:
            if a['balance'] >= 8000:
                role = disnake.utils.get(ctx.guild.roles, id=1087090449484882050)
                if ctx.author.get_role(1087090449484882050) is None:
                    await ctx.author.add_roles(role)
                await collection.update_one({"id" : ctx.author.id}, {"$set": {"fon": url}})
                await ctx.send("Ви успішно придбали кастомний банер")
                await collection.update_one({"id" : ctx.author.id}, {"$inc": {"balance": -8000}})
            else:
                await ctx.send("У вас недостатньо коштів")
        else:
            if a['balance'] >= 1:
                role = disnake.utils.get(ctx.guild.roles, id=1087090449484882050)
                if ctx.author.get_role(1087090449484882050) is None:
                    await ctx.author.add_roles(role)
                
                await collection.update_one({"id" : ctx.author.id}, {"$set": {"fon": url}})
                await ctx.send("Ви успішно придбали кастомний банер")
                await collection.update_one({"id" : ctx.author.id}, {"$inc": {"balance": -1}})
            else:
                await ctx.send("У вас недостатньо коштів")

    @daily.error
    async def everyday_bonus_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            hour = int(error.retry_after)//3600
            await ctx.send(f"{ctx.author.name} ви вже отримали свій бонус приходьте через {hour} години та {(int(error.retry_after)-hour*60*60)//60} хвилини", ephemeral=True)

def setup(bot):
    bot.add_cog(Economyc(bot))