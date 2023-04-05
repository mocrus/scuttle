import disnake
import easy_pil
from io import BytesIO
from disnake.ext import commands
from cogs.db import collection, collection_shop
from disnake import File

from easy_pil import Editor, load_image_async, Font



class ProfileAndBanner(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command(description="Ще одна чітерна штука яка зробить адміна ще гарнішим")
    async def buy_banner(self, ctx, url: str):
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
                    value= f"Діє до {row['off']}",
                    inline = False
                )
            await ctx.send(embed=embed_invent)
        else:
            await ctx.send("Ваш інвентар пустий. Купіть щось в магазині")



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
        edit.text((390, 420), text=voice, color="white", font=font)
        edit.text((565, 420), text=chat, color="white", font=font)
        edit.text((740, 420), text=balance, color="white", font=font)

        file = File(fp=edit.image_bytes, filename="profile.png")
        
        await ctx.send(file=file)
        
    @commands.slash_command()
    @commands.has_any_role(1071255622424731738, 1081231864389447732)
    async def week(self, ctx):
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


def setup(bot):
    bot.add_cog(ProfileAndBanner(bot))