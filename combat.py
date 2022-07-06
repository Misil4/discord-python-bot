import random
import discord
import progressbar
from PIL import Image, ImageDraw
import os
import bot


def playerEmbed(name, player):

    # draw the progress bar to given location, width, progress and color
    embed = discord.Embed(
        title=f'{name} ', color=0x00ff00)
    embed.add_field(name="<:8_:987788929870745720> ATK",
                    value=player.attack, inline=True)
    embed.add_field(name="<:def:987788969901182977>DEF",
                    value=player.defense, inline=True)
    embed.add_field(name="<:acc:987788951202955264>ACC",
                    value=player.accuracy, inline=True)
    embed.set_image(url=player.photo)
    embed.add_field(name="STA", value=f"{player.stamina/10}%", inline=True)
    return embed


class Player:

    # Init player stats
    def __init__(self, attack, defense, accuracy, name, photo):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.accuracy = accuracy
        self.stamina = 1000
        self.photo = photo

    # Determine by accuracy if player attacks or not
    def attacking(self, enemy):
        if (random.randint(0, 100) <= self.accuracy):
            return 0
        else:
            damage = (self.attack*3)-enemy.defense
            return damage


class Combat:

    # Init player arr
    def __init__(self, name, attack, defense, accuracy, photo, name1, attack1, defense1, accuracy1, photo1):
        self.turn = []
        self.turn.append(Player(attack, defense, accuracy, name, photo))
        self.turn.append(Player(attack1, defense1, accuracy1, name1, photo1))

    # Init turn and player dice to decide order, start combat
    async def start_combat(self, ctx):
        count = random.randint(0, 1)
        print(f"count is {count}")
        turns = 0
        turn = await ctx.send(f"Turno actual :  {turns}")
        update = await ctx.send(embed=playerEmbed(name=self.turn[0].name, player=self.turn[0]))
        battle = await ctx.send("Esperando turno")
        update1 = await ctx.send(embed=playerEmbed(name=self.turn[1].name, player=self.turn[1]))
        while self.turn[0].stamina > 0 or self.turn[1].stamina > 0:
            if (count == 0):
                damage = self.turn[0].attacking(self.turn[1])
                self.turn[1].stamina -= damage
                await battle.edit(content=f"{self.turn[0].name} ha inflingido {damage/10}% de daño a {self.turn[1].name}")
                await update.edit(embed=playerEmbed(name=self.turn[0].name, player=self.turn[0]))
                damage = self.turn[1].attacking(self.turn[0])
                await battle.edit(content=f"{self.turn[1].name} ha inflingido {damage/10}% de daño a {self.turn[0].name}")
                self.turn[0].stamina -= damage
                await update1.edit(embed=playerEmbed(name=self.turn[1].name, player=self.turn[1]))
                count = 1
                turns += 1
                await turn.edit(content=f"Turno actual :  {turns}")
                if self.turn[0].stamina > 0 and self.turn[1].stamina <= 0:
                    embed = discord.Embed(title=f"Ganador {self.turn[0].name}",description=f"STA restante {self.turn[0].stamina}")
                    randomMoney = random.randint(1,200)
                    randomExp = random.randint(1,200)
                    embed.add_field(name="RECOMPENSAS",value=f"Has ganado ´{randomMoney}, tu personaje ha conseguido {randomExp}")
                    levelUp = bot.updateExp(randomExp,self.turn[0].name)
                    if levelUp:
                        await ctx.send("ENHORABUENA TU PERSONAJE HA SUBIDO DE NIVEL, TODAS LAS ESTADISTICAS HAN MEJORADO")
                    bot.updateMoney(ctx.author.name,randomMoney)
                    embed.set_image(url=self.turn[0].photo)
                    return await ctx.send(embed=embed)
                if self.turn[1].stamina > 0 and self.turn[0].stamina <= 0:
                   embed = discord.Embed(title=f"Ganador {self.turn[1].name}",description=f"STA restante {self.turn[1].stamina}")
                   embed.set_image(url=self.turn[1].photo)
                   return await ctx.send(embed=embed)
                else:
                    continue
            elif (count == 1):
                damage = self.turn[1].attacking(self.turn[0])
                await battle.edit(content=f"{self.turn[1].name} ha inflingido {damage/10}% de daño a {self.turn[0].name}")
                self.turn[0].stamina -= damage
                await update1.edit(embed=playerEmbed(name=self.turn[1].name, player=self.turn[1]))
                damage = self.turn[0].attacking(self.turn[1])
                await battle.edit(content=f"{self.turn[0].name} ha inflingido {damage/10}% de daño a {self.turn[1].name}")
                self.turn[1].stamina -= damage
                await update.edit(embed=playerEmbed(name=self.turn[0].name, player=self.turn[0]))
                count = 0
                turns += 1
                await turn.edit(content=f"Turno actual :  {turns}")
                if self.turn[0].stamina > 0 and self.turn[1].stamina <= 0:
                   embed = discord.Embed(title=f"Ganador {self.turn[0].name}",description=f"STA restante {self.turn[0].stamina}")
                   embed.set_image(url=self.turn[0].photo)
                   randomMoney = random.randint(1,200)
                   randomExp = random.randint(1,200)
                   embed.add_field(name="RECOMPENSAS",value=f"Has ganado ´{randomMoney}, tu personaje ha conseguido {randomExp}")
                   levelUp = bot.updateExp(randomExp,self.turn[0].name)
                   if levelUp:
                        await ctx.send("ENHORABUENA TU PERSONAJE HA SUBIDO DE NIVEL, TODAS LAS ESTADISTICAS HAN MEJORADO")
                   bot.updateMoney(ctx.author.name,randomMoney)
                   return await ctx.send(embed=embed)
                if self.turn[1].stamina > 0 and self.turn[0].stamina <= 0:
                    embed = discord.Embed(title=f"Ganador {self.turn[1].name}",description=f"STA restante {self.turn[1].stamina}")
                    embed.set_image(url=self.turn[1].photo)
                    return await ctx.send(embed=embed)
                else:
                    continue

# Init Combat
# combat = Combat()

# Start Combat
# combat.start_combat()
