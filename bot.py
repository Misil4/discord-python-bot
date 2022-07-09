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
import exp

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
        embed = discord.Embed(
            title=f'{name} {surname}', description=user['description'], color=0x00ff00, timestamp=datetime.datetime.utcnow())
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
        embed.set_image(url=user['picture'])
        if user['owner'] == '0':
            embed.set_footer(text="Sin dueño")
        else:
            User = await bot.fetch_user(user['owner'])
            embed.set_footer(
                text=f"pertenece a {User.name}", icon_url=User.avatar_url)
        await ctx.send(embed=embed)


@bot.command()
async def kombat(ctx, arg: str = None):
    if arg:
        chara = character.find_one({'name': arg})
        if chara is None:
            await ctx.send("No existe un personaje con ese nombre")
        elif chara['owner'] != str(ctx.author.id):
           await ctx.send("Ese personaje no te pertenece")
        else:
                query = character.aggregate([{ '$sample' : {'size' : 1}}])
                chara1 = list(query)
                if (chara1[0]['name'] == "Maxter"):
                    query = character.aggregate([{ '$sample' : {'size' : 1}}])
                    chara1 = list(query)
                var = combat.Combat(chara['name'],chara['atributtes']['attack'],chara['atributtes']['defense'],chara['atributtes']['speed'],chara['picture'],chara1[0]['name'],chara1[0]['atributtes']['attack'],chara1[0]['atributtes']['defense'],chara1[0]['atributtes']['speed'],chara1[0]['picture'])
                await ctx.send("EMPEZANDO COMBATE")
                await ctx.send(f"SE ENFRENTAN {chara['name']} {chara['surname']} VS {chara1[0]['name']} {chara1[0]['surname']}")
                await var.start_combat(ctx,character=character,users=users)
    else : await ctx.send("No has seleccionado ningun personaje")
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
        elif arg == "chara" & user['money'] >= 10000:
            users.update_one({"name": ctx.author.name},
                             {"$inc": {"money": -10000}})
            query = character.aggregate(
                [{'$sample': {'size': 1}}, {'$match': {'owner': 0}}])
            chara = list(query)
            if query is None:
                await ctx.send("No hay mas personajes disponibles por el momento")
            else:
                character.update_one({"name": chara['name']},
                                     {'owner': ctx.author.id})
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
async def chara(ctx):
    user = users.find_one({"name": ctx.author.name})
    if len(user) > 0:
        arr = character.find({'owner' : str(ctx.author.id)})
        embed = discord.Embed(title=f"Inventario de {ctx.author.name}",timestamp=datetime.datetime.utcnow())
        for chara in arr:
            print(chara)
            embed.add_field(name=chara['series'],value=f"{chara['name']} {chara['surname']} 100% " ,inline=True)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"{ctx.author.mention}, debes registrarte en la base de datos usando kstart")


@bot.command()
async def tradeChara(ctx,arg: discord.Member = None):
    user = users.find_one({"name": ctx.author.name})
    if len(user) > 0:
        user1 = users.find_one({"name" : arg.name})
        if len(user1) > 0:
            arr = character.find({'owner' : str(ctx.author.id)})
        embed = discord.Embed(title=f"{ctx.author.name}, Que personaje quieres tradear?",timestamp=datetime.datetime.utcnow())
        for i,chara in enumerate(arr):
            print(chara)
            embed.add_field(name=f"{i+1}- {chara['series']}",value=f"{chara['name']} {chara['surname']} 100% " ,inline=True)
        message = await ctx.send(embed=embed)
        await message.add_reaction("1️⃣")
        def check(reaction, user):  # Our check for the reaction
            return user == ctx.message.author  # We check that only the authors reaction counts
        reaction = await bot.wait_for("reaction_add", check=check) 
        await ctx.send("personaje seleccionado")
        arr = character.find({'owner' : str(arg.id)})
        embed = discord.Embed(title=f"{arg.name}, Que personaje quieres tradear?",timestamp=datetime.datetime.utcnow())
        for i,chara in enumerate(arr):
            print(chara)
            embed.add_field(name=f"{i+1}- {chara['series']}",value=f"{chara['name']} {chara['surname']} 100% " ,inline=True)
        message = await ctx.send(embed=embed)
        await message.add_reaction("1️⃣")
        def check(reaction, user):  # Our check for the reaction
            return user == arg  # We check that only the authors reaction counts
        reaction = await bot.wait_for("reaction_add", check=check) 
        await ctx.send("personaje seleccionado")
        await ctx.send(f"{arg.mention} Quieres confirmar?, escriba confirm para hacerlo o no para cancelar")
        def check1(message): 
            return message.author == ctx.author  # We check that only the authors reaction counts
        msg = await bot.wait_for("message",check=check1)
        if (msg.content == "confirm"):
            await ctx.send("Trade Confirmado")
        elif (msg.content == "no"):
            await ctx.send("Trade Cancelado")

        

    else: await ctx.send(f"{ctx.author.mention}, debes registrarte en la base de datos usando kstart")

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
    embed.add_field(name="menu para el sistema de batallas", value="kbattles")
    await ctx.send(embed=embed)

@bot.command()
async def battles(ctx):
    embed = discord.Embed(title=f'Menu de combate',
                          description="colecciona y utiliza personajes para ganar recompensas", timestamp=datetime.datetime.utcnow())
    embed.add_field(
        name="ver tu lista de personajes", value="kchara")
    embed.add_field(name="intercambia personajes con otros usuarios", value="ktradeChara @usuario")
    embed.add_field(name="combate contra un personaje aleatorio y gana recompensas", value="kkombat")
    embed.add_field(name="busca un personaje por su nombre", value="kfindChara <nombre>")
    embed.add_field(name="gasta 10000 monedas para reclutar un nuevo personaje", value="kbuy chara")
    embed.add_field(name="PROXIMAMENTE MAS COMANDOS", value="-")
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
async def createChar(ctx, arg: str, arg1: str, arg2: str, arg3: str, arg4: str, arg5: str, arg6: str, arg7: int, arg8: int, arg9: int, arg10: int):
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
                                                character.insert_one({"name": arg, "surname": arg1, "description": arg2, "age": arg3, "genre": arg4, "series": arg5, "picture": arg6, "atributtes": {
                                                                     "attack": arg7, "defense": arg8, "speed": arg9, "salud": arg10}, "owner": "0", "level": 1, "exp": 0})
                                                await ctx.send("personaje creado satsfactoriamente")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Ya has usado el comando.")
        return
    else:
        raise error


bot.run(os.getenv('TOKEN'))
