from typing import Counter
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from numpy import number
from pymongo import MongoClient
import datetime

load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=os.getenv('PREFIX'),intents=intents,description="A testing bot")
bot.remove_command('help')
client = MongoClient(os.getenv('MONGO_URI'))
db = client.Primera
users = db.usuarios

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="llamando al fbi"))
    print('Logged in as')
    print(bot.user.name)
    print('------')

@bot.command()
async def buy(ctx,arg : str=None):
    role = discord.utils.get(ctx.guild.roles, name = "『🔥』┋MODERADORES")
    if arg:
        user = users.find_one({ "name": ctx.author.name })
        if arg =="kill" & user['money'] >=20000:
           users.update_one({"name" : ctx.author.name},{"$inc" : {"money" : -20000}})
           await ctx.send(f'{role.mention} ,{ctx.author.mention} ha comprado la custom {arg}')
        elif arg =="wish" & user['money'] >=45000:
           users.update_one({"name" : ctx.author.name},{"$inc" : {"money" : -45000}})
           await ctx.send(f'{role.mention} ,{ctx.author.mention} ha comprado la custom {arg}')
        elif arg =="shield" & user['money'] >=20000:
           users.update_one({"name" : ctx.author.name},{"$inc" : {"money" : -20000}})
           await ctx.send(f'{role.mention} ,{ctx.author.mention} ha comprado la custom {arg}')
        elif arg =="steal" & user['money'] >=35000:
           users.update_one({"name" : ctx.author.name},{"$inc" : {"money" : -35000}})
           await ctx.send(f'{role.mention} ,{ctx.author.mention} ha comprado la custom {arg}')
        else: ctx.send("ese elemento no existe o no tienes el dinero suficiente")
        
    else: await ctx.send(f"{ctx.author.mention}, tienes que especificar la custom que quieres comprar")


@bot.command()
async def money(ctx,arg:discord.Member=None):
    if arg ==None:
        user = users.find_one({ "name": ctx.author.name })
        if len(user) >0: 
            embed = discord.Embed(description='money : '+str(user['money']),timestamp=datetime.datetime.utcnow())
            embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else: ctx.send(f"{ctx.author.mention}, debes registrarte en la base de datos usando kstart")
    else:
        user = users.find_one({ "name": arg.name })
        if len(user) >0: 
            embed = discord.Embed(description='money : '+str(user['money']),timestamp=datetime.datetime.utcnow())
            embed.set_author(name=arg.name,icon_url=arg.avatar_url)
            await ctx.send(embed=embed)
        else: ctx.send(f"{ctx.author.mention}, debes registrarte en la base de datos usando kstart")
    

@bot.command()
async def avatar(ctx,arg :discord.Member=None):
    if arg ==None:
       await ctx.send(ctx.author.avatar_url)
    else:
       await ctx.send(arg.avatar_url)

@bot.command()
async def start(ctx):
    if len(users.find_one({ "name": ctx.author.name })) >0:
        await ctx.send("El usuario ya existe en la base de datos")
    else: 
        users.insert_one({"id" : ctx.author.id, "name" : ctx.author.name,"money" : 0,"daily" : 0,"weekly" : 0,"work" : 0,"tickets" : 0})
        await ctx.send("Usuario agregado a la base de datos correctamente")



    # info commands

@bot.command()
async def khelp(ctx):
    embed = discord.Embed(title=f'Bienvenido a OTAKULIFE, {ctx.author.mention}',description="comandos en el servidor",timestamp=datetime.datetime.utcnow())
    embed.add_field(name="ver todos los comandos de el servidor",value="khelp")
    embed.add_field(name="visualiza tu dinero",value="kmoney")
    embed.add_field(name="menu de la tienda",value="kshop")
    embed.add_field(name="da dinero a otro usuario",value="kgive @usuario")
    embed.add_field(name="visualizar tu avatar",value="!avatar")
    await ctx.send(embed=embed)

@bot.command()
async def shop(ctx):
    command = "kbuy"
    embed = discord.Embed(title='tienda de OTAKULIFE',description=command+" para comprar cualquier custom",timestamp=datetime.datetime.utcnow())
    embed.add_field(name="kill !kill para mas información",value="20000 monedas")
    embed.add_field(name="wish !wish para mas información",value="45000 monedas")
    embed.add_field(name="shield !shield para mas información",value="20000 monedas")
    embed.add_field(name="steal !steal para mas información",value="35000 monedas")
    await ctx.send(embed=embed)

    # admin commands

@bot.command()
@commands.has_any_role("『🔥』┋MODERADORES")
async def add(ctx,arg:discord.Member=None,arg1: int=None):
    if arg:
        if arg1:
            users.update_one({"name" : arg.name},{"$inc" : {"money" : +arg1}})
            user = users.find_one({ "name": ctx.author.name })
            embed = discord.Embed(description=str(arg1)+" añadido, dinero actual: "+str(user['money']),timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)
        else : await ctx.send(f"{ctx.author.mention}, no has definido la cantidad que quieres añadir")
    else : await ctx.send(f"{ctx.author.mention}, tienes que tagear a un usuario para añadir dinero")

@bot.command()
@commands.has_any_role("『🔥』┋MODERADORES")
async def remove(ctx,arg:discord.Member=None,arg1: int=None):
    if arg:
        if arg1:
            users.update_one({"name" : arg.name},{"$inc" : {"money" : -arg1}})
            user = users.find_one({ "name": ctx.author.name })
            embed = discord.Embed(description=str(arg1)+" removido, dinero actual: "+str(user['money']),timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)
        else : await ctx.send(f"{ctx.author.mention}, no has definido la cantidad que quieres restar")
    else : await ctx.send(f"{ctx.author.mention}, tienes que tagear a un usuario para restar dinero")

bot.run(os.getenv("TOKEN"))
    


