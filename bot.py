
from asyncio.windows_events import NULL
from turtle import title
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from pymongo import MongoClient
import datetime
import combat
import random
from PIL import Image, ImageDraw
import progressbar

load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=os.getenv('PREFIX'),
                   intents=intents, description="A testing bot")
bot.remove_command('help')
client = MongoClient(os.getenv('MONGO_URI'))
db = client.Primera
users = db.usuarios
character = db.personajes


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="llamando al fbi"))
    print('Logged in as')
    print(bot.user.name)
    print('------')


@bot.command()
async def findChara(ctx, *, name):
    user = character.find_one({'name': name})
    if user is None:
        await ctx.send("No existe el personaje")
    else:
        name = user['name']
        surname = user['surname']
        out = Image.new("RGB", (150, 100), (255, 255, 255))
        d = ImageDraw.Draw(out)

        # draw the progress bar to given location, width, progress and color
        d = progressbar.drawProgressBar(d, 10, 10, 100, 25, 1.0)
        out.save("output.jpg")
        file = discord.File("output.jpg", filename="output.jpg")
        embed = discord.Embed(
            title=f'{name} {surname}', description=user['description'], color=0x00ff00)
        embed.add_field(name="Genero", value=user['genre'])
        embed.add_field(name="Edad", value=user['age'])
        embed.add_field(name="Series", value=user['series'])
        embed.add_field(name="<:8_:987788929870745720> ATK",
                        value=user['atributtes']['attack'], inline=True)
        embed.add_field(name="<:def:987788969901182977>DEF",
                        value=user['atributtes']['defense'], inline=True)
        embed.add_field(name="<:acc:987788951202955264>ACC",
                        value=user['atributtes']['speed'], inline=True)
        embed.add_field(name="STA", value="100%", inline=True)
        embed.set_thumbnail(url=user['picture'])
        embed.set_image(url="attachment://output.jpg")
        await ctx.send(file=file, embed=embed)
        os.remove("./output.jpg")

@bot.command()
async def kombat(ctx,arg : str=None):
    if arg:
        chara = character.find_one({'name':arg})
        if chara is None:
            await ctx.send("No existe un personaje con ese nombre")
        elif chara['owner'] != ctx.author.id:
            await ctx.send("Ese personaje no te pertenece")
        else:
            query = character.aggregate([{ '$sample' : {'size' : 1}}])
            chara1 = list(query)
            var = combat.Combat(chara['name'],chara['atributtes']['attack'],chara['atributtes']['defense'],chara['atributtes']['speed'],chara['picture'],chara1[0]['name'],chara1[0]['atributtes']['attack'],chara1[0]['atributtes']['defense'],chara1[0]['atributtes']['speed'],chara1[0]['picture'])
            await ctx.send("EMPEZANDO COMBATE")
            await ctx.send(f"SE ENFRENTAN {chara['name']} {chara['surname']} VS {chara1[0]['name']} {chara1[0]['surname']}")
            await var.start_combat(ctx)
@bot.command()
@commands.cooldown(1, 604800, commands.BucketType.user)
async def weekly(ctx):
    user = users.find_one({"name": ctx.author.name})
    if len(user) > 0:
        randomN = random.randrange(800, 1000)
        users.update_one({"name": ctx.author.name}, {
                         "$inc": {"money": +randomN}})
        await ctx.send(f"Has ganado {randomN}")
    else:
        await ctx.send(f"{ctx.author.mention}, debes registrarte en la base de datos usando kstart")


@bot.command()
@commands.cooldown(1, 3600, commands.BucketType.user)
async def work(ctx):
    user = users.find_one({"name": ctx.author.name})
    if len(user) > 0:
        randomN = random.randrange(0, 150)
        users.update_one({"name": ctx.author.name}, {
                         "$inc": {"money": +randomN}})
        await ctx.send(f"Has trabajado y has ganado {randomN}")
    else:
        await ctx.send(f"{ctx.author.mention}, debes registrarte en la base de datos usando kstart")


@bot.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
    user = users.find_one({"name": ctx.author.name})
    if len(user) > 0:
        randomN = random.randrange(150, 300)
        users.update_one({"name": ctx.author.name}, {
                         "$inc": {"money": +randomN}})
        await ctx.send(f"Has ganado {randomN}")
    else:
        await ctx.send(f"{ctx.author.mention}, debes registrarte en la base de datos usando kstart")


@bot.command()
async def buy(ctx, arg: str = None):
    role = discord.utils.get(ctx.guild.roles, name="『🔥』┋MODERADORES")
    if arg:
        user = users.find_one({"name": ctx.author.name})
        if arg == "kill" & user['money'] >= 7000:
            users.update_one({"name": ctx.author.name},
                             {"$inc": {"money": -7000}})
            await ctx.send(f'{role.mention} ,{ctx.author.mention} ha comprado la custom {arg}')
        elif arg == "wish" & user['money'] >= 6000:
            users.update_one({"name": ctx.author.name},
                             {"$inc": {"money": -6000}})
            await ctx.send(f'{role.mention} ,{ctx.author.mention} ha comprado la custom {arg}')
        elif arg == "shield" & user['money'] >= 5000:
            users.update_one({"name": ctx.author.name},
                             {"$inc": {"money": -5500}})
            await ctx.send(f'{role.mention} ,{ctx.author.mention} ha comprado la custom {arg}')
        elif arg == "steal" & user['money'] >= 8000:
            users.update_one({"name": ctx.author.name},
                             {"$inc": {"money": -8000}})
            await ctx.send(f'{role.mention} ,{ctx.author.mention} ha comprado la custom {arg}')
        elif arg == "chara" & user['money'] >=10000:
            users.update_one({"name": ctx.author.name},
                             {"$inc": {"money": -10000}})
            query = character.aggregate([{ '$sample' : {'size' : 1}},{ '$match' : { 'owner' : 0 }}])
            chara = list(query)
            if query is None:
                await ctx.send("No hay mas personajes disponibles por el momento")
            else:
                character.update_one({"name" : chara['name']},
                {'owner' : ctx.author.id})
            await ctx.send(f"Has conseguido a {chara['name']} {chara['surname']}")
        else:
            await ctx.send("ese elemento no existe o no tienes el dinero suficiente")

    else:
        await ctx.send(f"{ctx.author.mention}, tienes que especificar la custom que quieres comprar")


@bot.command()
async def money(ctx, arg: discord.Member = None):
    if arg == None:
        user = users.find_one({"name": ctx.author.name})
        if len(user) > 0:
            embed = discord.Embed(
                description='money : '+str(user['money']), timestamp=datetime.datetime.utcnow())
            embed.set_author(name=ctx.author.name,
                             icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{ctx.author.mention}, debes registrarte en la base de datos usando kstart")
    else:
        user = users.find_one({"name": arg.name})
        if len(user) > 0:
            embed = discord.Embed(
                description='money : '+str(user['money']), timestamp=datetime.datetime.utcnow())
            embed.set_author(name=arg.name, icon_url=arg.avatar_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{ctx.author.mention}, debes registrarte en la base de datos usando kstart")


@bot.command()
async def avatar(ctx, arg: discord.Member = None):
    if arg == None:
        await ctx.send(ctx.author.avatar_url)
    else:
        await ctx.send(arg.avatar_url)


@bot.command()
async def start(ctx):
    if not users.find_one({"name": ctx.author.name}):
        users.insert_one({"id": ctx.author.id, "name": ctx.author.name,
                         "money": 0, "daily": 0, "weekly": 0, "work": 0, "tickets": 0})
        await ctx.send("Usuario agregado a la base de datos correctamente")
    else:
        await ctx.send("El usuario ya existe en la base de datos")


@bot.command()
async def give(ctx, arg: discord.Member = None, arg1: int = None):
    if arg:
        if arg1:
            user = users.find_one({"name": ctx.author.name})
            if len(user) > 0:
                if user['money'] > 0:
                    users.update_one({"name": arg.name}, {
                                     "$inc": {"money": +arg1}})
                    users.update_one({"name": ctx.author.name}, {
                                     "$inc": {"money": -arg1}})
                    await ctx.send("dinero enviado")
                else:
                    await ctx.send(f"{ctx.author.mention}, no tienes dinero suficiente para enviar")
            else:
                await ctx.send(f"{ctx.author.mention}, debes registrarte en la base de datos usando kstart")
        else:
            await ctx.send(f"{ctx.author.mention}, no has definido la cantidad que quieres dar")
    else:
        await ctx.send(f"{ctx.author.mention}, debes definir el usuario al que quieres dar el dinero")

    # info commands
@bot.command()
async def inventory(ctx):
    user = users.find_one({"name": ctx.author.name})
    if len(user) > 0:
        arr = character.find({'owner' : ctx.author.id})
        embed = discord.Embed(title=f"Inventario de {ctx.author.name}")
        for character in arr:
            embed.add_field(name=character['series'],value=f"{character['name']} {character['surname']}")
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"{ctx.author.mention}, debes registrarte en la base de datos usando kstart")
@bot.command()
async def help(ctx):
    embed = discord.Embed(title=f'Bienvenido a OTAKULIFE, {ctx.author.name}',
                          description="comandos en el servidor", timestamp=datetime.datetime.utcnow())
    embed.add_field(
        name="ver todos los comandos de el servidor", value="khelp")
    embed.add_field(name="visualiza tu dinero", value="kmoney")
    embed.add_field(name="menu de la tienda", value="kshop")
    embed.add_field(name="da dinero a otro usuario", value="kgive @usuario")
    embed.add_field(name="gana dinero cada 24 horas", value="kdaily")
    embed.add_field(name="gana dinero cada 7 dias", value="kweekly")
    embed.add_field(name="trabaja y gana dinero cada hora", value="kwork")
    embed.add_field(name="visualizar tu avatar", value="kavatar")
    await ctx.send(embed=embed)


@bot.command()
async def shop(ctx):
    command = "kbuy"
    embed = discord.Embed(title='tienda de OTAKULIFE', description=command +
                          " para comprar cualquier custom", timestamp=datetime.datetime.utcnow())
    embed.add_field(name="kill !kill para mas información",
                    value="7000 monedas")
    embed.add_field(name="wish !wish para mas información",
                    value="6000 monedas")
    embed.add_field(name="shield !shield para mas información",
                    value="5500 monedas")
    embed.add_field(name="steal !steal para mas información",
                    value="8000 monedas")
    await ctx.send(embed=embed)

    # admin commands


@bot.command()
@commands.has_any_role("『🔥』┋MODERADORES")
async def add(ctx, arg: discord.Member = None, arg1: int = None):
    if arg:
        if arg1:
            users.update_one({"name": arg.name}, {"$inc": {"money": +arg1}})
            user = users.find_one({"name": ctx.author.name})
            embed = discord.Embed(description=str(
                arg1)+" añadido, dinero actual: "+str(user['money']), timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{ctx.author.mention}, no has definido la cantidad que quieres añadir")
    else:
        await ctx.send(f"{ctx.author.mention}, tienes que tagear a un usuario para añadir dinero")


@bot.command()
@commands.has_any_role("『🔥』┋MODERADORES")
async def remove(ctx, arg: discord.Member = None, arg1: int = None):
    if arg:
        if arg1:
            users.update_one({"name": arg.name}, {"$inc": {"money": -arg1}})
            user = users.find_one({"name": ctx.author.name})
            embed = discord.Embed(description=str(
                arg1)+" removido, dinero actual: "+str(user['money']), timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{ctx.author.mention}, no has definido la cantidad que quieres restar")
    else:
        await ctx.send(f"{ctx.author.mention}, tienes que tagear a un usuario para restar dinero")

@bot.command()
@commands.has_any_role("『🔥』┋MODERADORES")
async def createChar(ctx, arg : str,arg1 : str,arg2 : str,arg3 : str,arg4 : str,arg5 : str,arg6 : str,arg7 : int,arg8 : int,arg9 : int,arg10 : int):
    if arg:
        if arg1:
            if arg2:
                if arg3:
                    if arg4:
                        if arg5:
                            if arg6:
                                if arg7:
                                    if arg8:
                                        if arg9:
                                            if arg10:
                                                character.insert_one({"name": arg, "surname": arg1, "description": arg2, "age": arg3, "genre": arg4, "series": arg5, "picture": arg6, "atributtes" : {"attack": arg7,"defense" : arg8,"speed" : arg9,"salud" : arg10}})
                                                await ctx.send("personaje creado satsfactoriamente")
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Ya has usado el comando.")
        return
    else:
        raise error


bot.run(os.getenv('TOKEN'))
