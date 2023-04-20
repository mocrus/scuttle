import datetime
import disnake
import easy_pil
from io import BytesIO
from disnake.ext import commands
from cogs.db import collection, collection_shop, collection_marrys
from disnake import File

from easy_pil import Editor, load_image_async, Font



class ProfileAndBanner(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command(description="Ще одна чітерна штука яка зробить адміна ще гарнішим")
    async def buy_banner(self, ctx, url: str):
        #get user
        a = await collection.find_one({"id": ctx.author.id})
        #check user is admin
        if ctx.author.get_role(1071952131940171868) is None:
            #check balance
            if a['balance'] >= 8000:
                role = disnake.utils.get(ctx.guild.roles, id=1087090449484882050)
                if ctx.author.get_role(1087090449484882050) is None:
                    await ctx.author.add_roles(role)
                #update balance
                await collection.update_one({"id" : ctx.author.id}, {"$set": {"fon": url}})
                await ctx.send("Ви успішно придбали кастомний банер")
                await collection.update_one({"id" : ctx.author.id}, {"$inc": {"balance": -8000}})
            else:
                await ctx.send("У вас недостатньо коштів")
        else:
            #check balance
            if a['balance'] >= 1:
                role = disnake.utils.get(ctx.guild.roles, id=1087090449484882050)
                if ctx.author.get_role(1087090449484882050) is None:
                    await ctx.author.add_roles(role)
                #update balance
                await collection.update_one({"id" : ctx.author.id}, {"$set": {"fon": url}})
                await ctx.send("Ви успішно придбали кастомний банер")
                await collection.update_one({"id" : ctx.author.id}, {"$inc": {"balance": -1}})
            else:
                await ctx.send("У вас недостатньо коштів")
    @commands.slash_command()
    async def set_banner(self, ctx, number:int):
        # get user
        a = await collection_shop.find_one({"id": ctx.author.id, "fon": number})
        #check banner
        if a is None:
            await ctx.send("У вас нема цього банеру в інвентарі", delete_after=10)
        else:
            fons = [0, "https://imgur.com/lxoACBR.png", "https://imgur.com/bbobocT.png", "https://imgur.com/Q9Vi03N.png", "https://imgur.com/ML0dDtu.png",
                    "https://imgur.com/UDubCJM.png", "https://imgur.com/ebjeBPa.png", "https://imgur.com/TnLpUF3.png", "https://imgur.com/dMVW5gb.png",
                    "https://imgur.com/zgu2f6c.png","https://imgur.com/RoySOmW.png", "https://imgur.com/QM8ONan.png", "https://imgur.com/hZUyD5R.png"]
            await collection.update_one({"id": ctx.author.id}, {"$set": {"fon": fons[a['fon']]}})
            await ctx.send("Ви успішно застосували банер", delete_after=10)

    @commands.slash_command(description="Покаже ваш інвентар профілів")
    async def invetar(self, ctx, member: disnake.Member=None):
        #find user
        if member is None:
            rows = collection_shop.find({"id": ctx.author.id})
        else:
            rows = collection_shop.find({"id": member.id})
        #create embed
        embed_invent = disnake.Embed(
            title="Inventar",
        )
        my_data =  await rows.to_list(length=100)
        #check inventar
        if my_data != []: 
            fons = [0, "1. Полуничка та роль до нього", "2. Нічне небо та роль до нього", "3. Рожеві медузки та роль до нього", 
                    "4. 80's та роль до нього", "5. Ретро вайб та роль до нього", "6. Спокій та роль до нього",
                    "7. Кролики та роль до нього", "8. Дед інсульт та роль до нього", "9. Квіткове поле та роль до нього",
                    "10. Малий мандрівник та роль до нього", "11. Вишукане мистецтво та роль до нього", "12. Кицюк та роль до нього"]
            #add field to embed
            for row in my_data:
                embed_invent.add_field(
                    name=f"{fons[row['fon']]}",
                    value= f"Діє до {row['off']}",
                    inline = False
                )
            await ctx.send(embed=embed_invent)
        else:
            await ctx.send("Ваш інвентар пустий. Купіть щось в магазині")



    @commands.slash_command(description="Покаже ваш прекрасний профіль")
    async def profile(self, ctx, member: disnake.Member=None):
        await ctx.response.defer()
        #check member mentioned and search it
        if member is None:
            
            a = await collection.find_one({"id" : ctx.author.id})
            image = await load_image_async(ctx.author.display_avatar.url)
            name = str(ctx.author.name)
            if len(name)>25:
                name = name[:20]+"..." + "#" + str(ctx.author.discriminator)
            else:
                name = name + "#" + str(ctx.author.discriminator)
                name = " " * (30 - len(name)) + name
        else:
            a = await collection.find_one({"id" : member.id})
            image = await load_image_async(member.display_avatar.url)
            name = str(member.name)
            if len(name)>25:
                name = name[:20]+"..." + "#" + str(member.discriminator)
            else:
                name = name + "#" + str(member.discriminator)
                name = " " * (30 - len(name)) + name
        #create img
        edit = Editor('cogs/pngs/dark.png')
        font = Font.montserrat(size=20, variant='regular')
        edit_ava = Editor(image).circle_image().resize((135, 135))
        if a['fon'] is None:
            img = Editor("cogs/pngs/banner.png")
        else:
            img = await load_image_async(a['fon'])
        edit_bckg = Editor(img). rounded_corners(radius=20)

        edit.paste(image=edit_bckg, position=(271, 96))
        edit.paste(edit_ava, position=(87, 115))
        prosent = (a['xp']-a['last'])/a['next']*100
        prosent = round(prosent, 2)
        if prosent != 0:
            width = 190*prosent/100
            x = 60+width
        else:
            width = 1
            x = 60
        edit.rectangle(position=(60, 280), width=190, height=2, outline="white", fill="white")
        edit.rectangle(position=(60, 280), width=width, height=2, outline="#AA3BFF", fill="#AA3BFF")
        edit.ellipse(position=(x, 272), width=20, height=20, fill="#AA3BFF")
        edit.text(position=(300, 470), font=font, color="white", text=name)

        voice = int(a['vxp'])
        voice = "0" * (6 - len(str(voice))) + str(voice)
        chat = int(a["cxp"])
        chat = "0" * (6 - len(str(chat))) + str(chat)
        balance = int(a["balance"])
        balance = "0" * (6 - len(str(balance))) + str(balance)
        lvl = a['lvl']
        edit.text(position=(90, 300), text=f"{prosent} % / $ {lvl}", font=font, color="white")
        edit.text((285, 408), text=voice, color="white", font=font)
        edit.text((437, 408), text=chat, color="white", font=font)
        edit.text((590, 408), text=balance, color="white", font=font)
        file = File(fp=edit.image_bytes, filename="profile.png")
        #send img
        await ctx.send(file=file)


    @commands.slash_command()
    @commands.has_any_role(1071255622424731738, 1081231864389447732)
    async def week(self, ctx):
        #geting all active users for a week
        rows = collection.find(limit=10).sort("week", -1) 
        my_data =  await rows.to_list(length=100)
        #getting number 1
        for row in my_data:
            if row["id"] !=192188318555832321:
                a=row['id']
                break
        # creating img
        guild = self.bot.get_guild(750380875706794116)
        mem = guild.get_member(a)
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
            #set guild banner
            await guild.edit(banner=image_binary.read())
        #set week xp to 0
        await collection.update_many({}, {"$set": {"week": 0}})

    @commands.slash_command()
    async def love_profile(self, ctx):
        #check marryd
        if ctx.author.get_role(1077027040181633076) is None:
            return await ctx.send("Ви не одружені")
        #search marry info
        marrys = await collection_marrys.find_one({"$or": [{"id1": ctx.author.id}, {"id2": ctx.author.id}]})
        #create img
        edit = Editor("cogs/pngs/love.png")
        font = Font.montserrat(size=25)
        memb1 = disnake.utils.get(ctx.guild.members, id=marrys["id1"])
        memb2 =  disnake.utils.get(ctx.guild.members, id=marrys["id2"])
        ava1, ava2 = await easy_pil.load_image_async(memb1.display_avatar.url), await easy_pil.load_image_async(memb2.display_avatar.url)
        ava1, ava2 = Editor(ava1).circle_image().resize((150, 150)), Editor(ava2).circle_image().resize((150, 150))
        edit.paste(ava1, position=(150, 170))
        edit.paste(ava2, position=(600, 170))
        #getting date
        date = datetime.datetime.now()-marrys["date"]
        dat = str(date).split(" ")
        #getting time
        if "day" in str(date):
            time = dat[2].split(":")
        else:
            time = dat[0].split(":")
        edit.text(position=(380, 303), text=f"{date.days}д. {time[0]}г. {time[1]}хв.", font=font, color="white")
        if len(memb1.name) >= 17:
            name1 = str(memb1.name[:17]) + "..."
        else:
            name1 = " " * (17 - len(memb1.name)) + memb1.name
        if len(memb2.name) >= 17:
            name2 = str(memb2.name[:17]) + "..."
        else:
            name2 = " " * (17 - len(memb2.name)) + memb2.name

        edit.text(position=(95, 380), text=f"{name1}", font=font, color="white")
        edit.text(position=(545, 380), text=f"{name2}", font=font, color="white")
        file = File(fp=edit.image_bytes, filename="profile.png")
        #send marry img
        await ctx.send(file=file)

def setup(bot):
    bot.add_cog(ProfileAndBanner(bot))