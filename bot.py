import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
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
async def money(ctx,arg:discord.Member=None):
    if arg ==None:
        user = users.find_one({ "name": ctx.author.name })
        embed = discord.Embed(description='money : '+str(user['money']),timestamp=datetime.datetime.utcnow())
        embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        user = users.find_one({ "name": arg.name })
        embed = discord.Embed(description='money : '+str(user['money']),timestamp=datetime.datetime.utcnow())
        embed.set_author(name=arg.name,icon_url=arg.avatar_url)
        await ctx.send(embed=embed)
    

@bot.command()
async def avatar(ctx,arg :discord.Member=None):
    if arg ==None:
       await ctx.send(ctx.author.avatar_url)
    else:
       await ctx.send(arg.avatar_url)


@bot.command()
async def khelp(ctx):
    embed = discord.Embed(title='Bienvenido a OTAKULIFE',description="comandos en el servidor",timestamp=datetime.datetime.utcnow())
    embed.add_field(name="ver todos los comandos de el servidor",value="!help")
    embed.add_field(name="visualiza tu dinero",value="!money")
    embed.add_field(name="menu de la tienda",value="!shop")
    embed.add_field(name="da dinero a otro usuario",value="!give @usuario")
    embed.add_field(name="visualizar tu avatar",value="!avatar")
    await ctx.send(embed=embed)
    

bot.run(os.getenv("TOKEN"))
    


