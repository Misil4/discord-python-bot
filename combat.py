import random

attack = 5
defense = 14
accuracy = 10


class Player:

    # Init player stats
    def __init__(self,attack,defense,accuracy):
        self.attack = attack
        self.defense = defense
        self.accuracy = accuracy
        self.stamina = 1000

    # Determine by accuracy if player attacks or not
    def attacking(self, enemy):
        if (random.randint(0, 100) <= self.accuracy):
            return 0
        else:
            damage = (self.attack*3)-enemy.defense
            return damage


class Combat:

    # Init player arr
    def __init__(self,attack,defense,accuracy,attack1,defense1,accuracy1):
        self.turn = []
        self.turn.append(Player(attack,defense,accuracy))
        self.turn.append(Player(attack1,defense1,accuracy1))

    # Init turn and player dice to decide order, start combat
    async def start_combat(self,ctx):
        count = random.randint(0,1)
        print(f"count is {count}")
        turns = 0
        while(self.turn[0].stamina > 0 or self.turn[1].stamina >0 ):
           print(f"turn {turns}")
           if (count == 0):
             damage = self.turn[0].attacking(self.turn[1])
             self.turn[1].stamina-=damage
             await ctx.send(f"player make {damage} to player1")
             damage = self.turn[1].attacking(self.turn[0])
             self.turn[0].stamina-=damage
             await ctx.send(f"player1 make {damage} to player")
             count = 1
             turns+=1
           elif (count ==1):
             damage = self.turn[1].attacking(self.turn[0])
             self.turn[0].stamina-=damage
             ctx.send(f"player1 make {damage} to player")
             damage = self.turn[0].attacking(self.turn[1])
             self.turn[1].stamina-=damage
             await ctx.send(f"player make {damage} to player1")
             count = 0
             turns+=1
        if (self.turn[0].stamina <=0):
            await ctx.send("player 1 winner")
        elif (self.turn[1].stamina <=0):
            await ctx.send("player winner")

# Init Combat
# combat = Combat()

# Start Combat
# combat.start_combat()
             
