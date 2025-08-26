"""
This program runs a simulation of a pokemon game with 30 different pokemon!
Completed on Wednesday 16 December 2020
By Nikhil


Notes about the game:

I did not have enough time to make the 6v6 one at a time trainer battle unfortunately due to me investing my time on other areas
Since it takes a long time to get to a high level to test out the evolution and move changes, I have given a lot of money which you can use to buy pokemon candy for xp
If you want to test out the changing team feature, you can buy pokemon in the store
I added typings in the database for what is effective against what that are not actually used
In the beggining, if you do not put a valid pokemon three times, you will get pikachu!
There were a lot of lines so I did not put the amount of comments I would have liked
It is case sensitive!


Features added to the game which weren't originally intended:

*Added evolutions
*Added the ability to change moves
*Added status effects
*Added flinch moves
*Added priority moves
*Added recoil moves
*Added stat changing moves
*Added the ability to change your team once you have enough pokemon
*Added switching pokemon in the game
*Added a few more pokemon(Dratini&Gastly&Weedle&Caterpie&Machop evolution chain)
*Added the ability to get more than one of the same type of pokemon)
*Added IVs
*Added random moves for the AI
*Added increased crit ratio moves(Only had time to add two)
"""

#Imports
import random
import time

#Data Bases
your_pokemon = {} #Stores the pokemon you have
pokemon_team = [] #Stores the pokemon in your team

#List of all the pokemons base stats
#Format: Name: [[type1,type2("" if no second type)],hp, attack, special attack, defence, special defence, {0:starting_move, 1:other starting move, x: other move can be learned at x lvl, etc...}, {lvl:evolution at lvl}, what lvl can you find it in the wild]
pokemon_list = {
    "Charmander": [["Fire",""], 39, 52, 60, 43, 50, 65, {0:"Ember", 1:"Tackle", 2:"Growl", 12: "Dragon Breath"}, [16, "Charmeleon"],5],
    "Charmeleon": [["Fire",""], 58, 64, 80, 58, 65, 80, {0:"Dragon Breath", 1: "Ember", 19:"Fire Fang", 30: "Flamethrower"}, [36, "Charizard"],16],
    "Charizard": [["Fire","Flying"], 78, 84, 109, 78, 85, 100,{0:"Flamethrower", 1:"Dragon Breath", 37: "Air Slash", 54: "Inferno", 62:"Flare Blitz"},[1000],36],
    "Bulbasaur": [["Grass","Poison"], 45, 49, 65, 49, 65, 45, {0:"Vine Whip", 1:"Tackle", 2:"Growl",15:"Poison Powder"}, [16, "Ivysaur"],5],
    "Ivysaur": [["Grass","Poison"], 60, 62, 80, 63, 80, 60, {0:"Vine Whip", 1:"Poison Powder", 20:"Seed Bomb",25:"Take Down"},[32,"Venasaur"],16],
    "Venasaur": [["Grass","Poison"], 80, 82, 100, 83, 100, 80, {0:"Seed Bomb", 1:"Take Down", 37:"Petal Blizzard", 51:"Double Edge"},[1000],32],
    "Squirtle": [["Water",""], 44, 48, 50, 65, 64, 43, {0:"Water Gun",1:"Tackle", 2:"Tail Whip",15: "Water Pulse"},[16, "Wartortle"],5],
    "Wartortle": [["Water",""], 59, 63, 65, 80, 80, 58, {0:"Water Pulse", 1:"Tackle", 18:"Bite", 30:"Aqua Tail"},[36, "Blastoise"],16],
    "Blastoise": [["Water", ""], 79, 83, 85, 100, 105, 78, {0:"Aqua Tail", 1:"Bite", 37:"Flash Cannon", 42:"Iron Defence",49:"Hydro Pump" },[1000],36],
    "Pikachu": [["Electric",""], 35, 55, 50, 40, 50, 90, {0:"Thunder Shock", 1:"Thunder Wave", 12: "Quick Attack", 20: "Spark"},[1000],3],
    "Onix": [["Rock","Ground"], 35, 45, 30, 160, 45, 70, {0:"Rock Throw", 1:"Tackle", 8: "Rock Polish", 25: "Iron Tail"},[36, "Steelix"],10],
    "Steelix": [["Steel","Ground"], 75, 85, 55, 200, 65, 30, {0:"Iron Tail", 1:"Rock Throw",39:"Crunch", 52:"Stone Edge"},[1000],36],
    "Geodude": [["Rock", "Ground"], 40, 80, 30, 100, 30, 20, {0: "Tackle", 1: "Rock Throw", 15: "Take Down"},[25,"Graveler"],2],
    "Graveler": [["Rock","Ground"], 55, 95, 45, 115, 45, 35, {0:"Rock Throw", 1: "Take Down", 31: "Earthquake"},[50,"Golem"],25],
    "Golem": [["Rock","Ground"], 80, 120, 55, 130, 65, 45, {0:"Take Down", 1:"Earthquake",51:"Mega Punch", 60: "Double Edge"},[1000],50],
    "Gastly": [["Ghost",""], 30, 35, 100, 30, 35, 80, {0:"Lick", 1:"Payback"},[25,"Haunter"],7],
    "Haunter": [["Ghost","Poison"], 45, 50, 115, 45, 55, 95, {0: "Lick", 1:"Payback", 26: "Shadow Punch"},[40, "Gengar"],25],
    "Gengar": [["Ghost", "Poison"], 60, 65, 130, 60, 75, 110, {0:"Shadow Punch", 1: "Payback", 42: "Dark Pulse", 48: "Shadow Ball"},[1000],40],
    "Dratini": [["Dragon",""], 41, 64, 50, 45, 50, 50, {0:"Twister",1:"Thunder Wave",20:"Agility"},[30,"Dragonair"],10],
    "Dragonair": [["Dragon",""], 61, 84, 70, 65, 70, 70, {0:"Twister", 1:"Thunder Wave", 33: "Aqua Tail", 39: "Dragon Rush"},[55,"Dragonite"],30],
    "Dragonite": [["Dragon","Flying"], 91, 134, 100, 95, 100, 80, {0:"Aqua Tail", 1:"Dragon Rush", 56: "Extreme Speed"},[1000],55],
    "Caterpie": [["Bug",""], 45, 30, 20, 35, 20, 45, {0:"String Shot", 1:"Tackle", 6:"Bug Bite"},[7,"Metapod"],1],
    "Metapod": [["Bug", ""], 50, 20, 25, 55, 25, 30, {0:"String Shot", 1:"Bug Bite", 8: "Harden"},[10,"Butterfree"],7],
    "Butterfree": [["Bug", "Flying"], 60, 45, 90, 50, 80, 70, {0: "Bug Bite", 1:"String Shot", 12: "Poison Powder", 24: "Air Slash", 32:"Bug Buzz"},[1000],10],
    "Weedle": [["Bug", "Poison"], 40, 35, 20, 30, 20, 50, {0: "Poison Sting",1:"String Shot"},[7,"Kakuna"],1],
    "Kakuna": [["Bug", "Poison"], 45, 25, 25, 50, 25, 35, {0:"Poison Sting", 1:"String Shot", 8:"Harden"},[10, "Beedrill"],7],
    "Beedrill": [["Bug","Poison"], 65, 90, 45, 40, 80, 75, {0: "Poison Sting", 1:"String Shot", 22: "Poison Jab", 25:"Agility"},[1000],10],
    "Machop": [["Fighting",""], 70, 80, 35, 50, 35, 35, {0:"Leer",1:"Low Sweep"},[28,"Machoke"],3],
    "Machoke":[["Fighting",""], 80, 100, 50, 70, 60, 45, {0:"Leer",1:"Low Sweep", 31: "Strength"}, [48, "Machamp"],28],
    "Machamp": [["Fighting",""], 90, 130, 65, 80, 85, 55, {0:"Low Sweep", 1:"Strength", 60:"Cross Chop", 66: "Double Edge"},[1000],48]

}
#List of all the moves and their stats
#Format: Move Name: [damage, accuracy, special/physical, type, recoil percent, priority, [status effect, percent to inflict],[which stat change, who it inflicts on, id of stat change, magnitude of stat change, percent to inflict]]
move_list = {"Ember": [40, 100, "Special", "Fire",0,1,["Burned",10],[""],625],
             "Tackle": [40, 100, "Physical", "Normal",0,1,[""],[""],625],
             "Flamethrower": [90, 100, "Special", "Fire",0,1,["Burned",10],[""],625],
             "Vine Whip": [45, 100, "Physical", "Grass",0,1,[""],[""],625],
             "Seed Bomb": [80, 100, "Physical", "Grass",0,1,[""],[""],625],
             "Take Down": [90, 85, "Physical", "Normal",0.25,1,[""],[""],625],
             "Dragon Breath": [60, 100, "Special", "Dragon",0,1,["Paralyzed",30],[""],625],
             "Fire Fang": [65, 95, "Physical", "Fire", 0,1,["Burned",10],[""],625],
             "Water Pulse": [60, 100, "Special", "Water",0,1,[""],[""],625],
             "Water Gun": [40, 100, "Special", "Water",0,1,[""],[""],625],
             "Bite": [60, 100, "Physical", "Dark",0,1,[""],[""],625],
             "Thunder Shock": [40, 100, "Special", "Electric",0,1,["Paralyzed",10],[""],625],
             "Thunder Wave": [-1,90, "None", "Electric", 0,1, ["Paralyzed",100],[""],625],
             "Stone Edge": [100, 80, "Physical", "Rock", 0,1,[""],[""],1250],
             "Petal Blizzard": [90,100, "Physical", "Grass",0,1,[""],[""],625],
             "Poison Powder": [-1,75, "None", "Poison",0,1,["Poisoned",100],[""],625],
             "Hydro Pump": [110,80,"Special", "Water",0,1,[""],[""],625],
             "Flare Blitz": [120,100, "Physical", "Fire", 1/3,1, ["Burned", 10],[""],625],
             "Double Edge": [120,100, "Physical", "Normal", 1/3,1,[""],[""],625],
             "Aqua Tail": [90,90, "Physical", "Water",0,1,[""],[""],625],
             "Flash Cannon": [80,100, "Special", "Steel",0,1,[""],[""],625],
             "Spark": [65, 100, "Physical", "Electric",0,1, ["Paralyzed", 30],[""],625],
             "Iron Tail": [100, 75, "Physical", "Steel",0,1,[""],[""],625],
             "Crunch": [80, 100, "Physical", "Dark",0,1,[""],[""],625],
             "Rock Throw": [50, 90, "Physical", "Rock",0,1,[""],[""],625],
             "Earthquake": [100,100,"Physical", "Ground", 0,1,[""],[""],625],
             "Mega Punch": [80, 85, "Physical", "Normal", 0,1,[""],[""],625],
             "Air Slash": [75, 95, "Special", "Flying",0,1,["Flinched",30],[""],625],
             "Lick": [30, 100, "Physical", "Ghost",0,1,["Paralyzed", 30],[""],625],
             "Payback": [50, 100, "Physical", "Dark",0,1,[""],[""],625],
             "Quick Attack": [40, 100, "Physical", "Normal",0,2,[""],[""],625],
             "Shadow Punch": [60, 105, "Physical", "Ghost",0,1,[""],[""],625],
             "Dark Pulse": [80, 100, "Special", "Dark",0,1,["Flinched",20],[""],625],
             "Shadow Ball": [80,100, "Special", "Ghost",0,1,[""],["special defence", "enemy", 3, 1, 20],625],
             "Growl": [-1, 100, "None", "Normal",0,1,[""],["attack", "enemy", 0, 1, 100],625],
             "Inferno": [100, 50, "Special", "Fire",0,1,["Burned",100],[""],625],
             "Tail Whip": [-1, 100, "None", "Normal",0,1,[""],["defence", "enemy",2,1,100],625],
             "Iron Defence": [-1,100,"None", "Steel",0,1,[""],["defence","self",2,2,100],625],
             "Rock Polish": [-1,100,"None","Rock",0,1,[""],["speed","self",4,2,100],625],
             "Twister": [40, 100, "Special","Dragon",0,1,["Flinched",30],[""],625],
             "Agility": [-1,100, "None", "Psychic",0,1,[""],["speed", "self", 4, 2, 100],625],
             "Dragon Rush": [100,75, "Physical", "Dragon",0,1,["Flinched",20],[""],625],
             "Extreme Speed": [80,100, "Physical", "Normal",0,3,[""],[""],625],
             "String Shot": [-1, 95, "None", "Bug",0,1,[""],["speed", "enemy", 4, 2, 100],625],
             "Bug Bite": [60, 100,"Physical", "Bug",0,1,[""],[""],625],
             "Harden": [-1,105,"None", "Normal", 0,1,[""],["defence","self",2,1,100],625],
             "Bug Buzz": [90,100,"Special", "Bug", 0,1,[""],["special defence", "enemy", 3, 1, 10],625],
             "Poison Sting": [15,100,"Physical","Poison",0,1,["Poisoned",30],[""],625],
             "Poison Jab": [80, 100,"Physical","Poison",0,1,["Poisoned",30],[""],625],
             "Leer": [-1, 100, "None", "Normal",0,1,[""],["defence", "enemy", 2,1,100],625],
             "Low Sweep": [65, 100, "Physical", "Fighting",0,1,[""],["speed", "enemy", 4,1,100],625],
             "Strength": [80, 100, "Physical", "Normal",0,1,[""],[""],625],
             "Cross Chop": [100, 80, "Physical", "Fighting",0,1,[""],[""], 1250]
             }

#Data bases for what type is good/bad against what
type_effective = {"Fire":["Grass","Ice","Bug","Steel"],"Water":["Fire","Ground","Rock"],"Grass":["Water","Ground","Rock"],"Electric":["Water","Flying"],"Ground":["Fire","Electric","Poison","Rock","Steel"],"Rock":["Fire","Ice","Flying","Bug"],"Fighting":["Normal","Ice","Rock","Dark","Steel"],"Ghost":["Psychic","Ghost"],"Dark":["Psychic","Ghost"],"Psychic":["Fighting","Poison"],"Flying":["Grass","Fighting","Bug"],"Bug":["Grass","Psychic","Dark"],"Fairy":["Fighting","Dragon","Dark"],"Steel":["Ice","Rock","Fairy"],"Poison":["Grass","Fairy"],"Ice":["Grass","Ground","Flying","Dragon"],"Dragon":["Dragon"]}
type_not_effective = {"Fire":["Fire","Water","Rock","Dragon"],"Water":["Water","Grass","Dragon"],"Grass":["Fire","Grass","Poison","Flying","Bug","Dragon","Steel"],"Electric":["Electric","Grass","Dragon"],"Ground":["Grass","Bug"],"Rock":["Fighting","Ground","Steel"],"Normal":["Rock","Steel"],"Fighting":["Poison","Flying","Psychic","Bug","Fairy"],"Ghost":["Dark"],"Dark":["Fighting","Dark","Fairy"],"Psychic":["Psychic","Steel"],"Flying":["Electric","Rock","Steel"],"Bug":["Fire","Fighting","Poison","Flying","Ghost","Steel","Fairy"],"Fairy":["Fire","Poison","Steel"],"Steel":["Fire","Water","Electric","Steel"],"Poison":["Poison","Ground","Rock","Ghost"],"Ice":["Fire","Water","Ice","Steel"],"Dragon":["Steel"],}
type_no_effect = {"Electric":["Ground"],"Ground":["Flying"],"Fighting":["Ghost"],"Ghost":["Normal"],"Psychic":["Dark"],"Poison":["Steel"],"Dragon":["Fairy"],"Normal":["Ghost"]}

#Money and inventory variables
money = 2500
inventory = [10,0,0,0] #[pokeballs, small candies, medium candies, large candies]

#Stat stage data base
stat_stages = (2/8,2/7,2/6,2/5,2/4,2/3,2/2,3/2,4/2,5/2,6/2,7/2,8/2)

#Class for pokemon on your team
class Pokemon:
    def __init__(self, lvl, name, xp = 0, ivs = 0, cur_hp = "", moves = 0):
        #Makes unique name
        self.id = 1
        self.name = name
        for i in your_pokemon.values():
            self.id += 1
        self.id = str(self.id)
        self.id = self.name + "(" + self.id + ")"
        your_pokemon[self.id] = self
        if len(pokemon_team) < 6:
            pokemon_team.append(self.id)
        #Gives random ivs if it isn't caught or evolved because ivs stay the same
        if ivs == 0:
            self.ivs = [random.randint(0,15),random.randint(0,15),random.randint(0,15),random.randint(0,15),random.randint(0,15),random.randint(0,15)]
        else:
            self.ivs = ivs
        #Gets the data from the above data base and does the calculations to get the actual values
        self.type = [pokemon_list[self.name][0][0],pokemon_list[self.name][0][1]]
        self.lvl = lvl
        self.xp = xp
        self.max_hp = round(10+((2*(pokemon_list[self.name][1] + 0.02*(self.lvl-1)*pokemon_list[self.name][1]) + self.ivs[0] + 100)*self.lvl)/100,2)
        if cur_hp == "":
            self.cur_hp = self.max_hp
        else:
            self.cur_hp = round(cur_hp*self.max_hp,2)
        self.status_effects = []
        self.stat_changes = [1,1,1,1,1]
        self.att = round(5+((2*(pokemon_list[self.name][2] + 0.02*(self.lvl-1)*pokemon_list[self.name][2]) + self.ivs[1] + 100)*self.lvl)/100,2)
        self.sp_att = round(5+((2*(pokemon_list[self.name][3] + 0.02*(self.lvl-1)*pokemon_list[self.name][3]) + self.ivs[2] + 100)*self.lvl)/100,2)
        self.defence = round(5+((2*(pokemon_list[self.name][4] + 0.02*(self.lvl-1)*pokemon_list[self.name][4]) + self.ivs[3] + 100)*self.lvl)/100,2)
        self.sp_defence = round(5+((2*(pokemon_list[self.name][5] + 0.02*(self.lvl-1)*pokemon_list[self.name][5]) + self.ivs[4] + 100)*self.lvl)/100,2)
        self.speed = round(5+((2*(pokemon_list[self.name][6] + 0.02*(self.lvl-1)*pokemon_list[self.name][6]) + self.ivs[5] + 100)*self.lvl)/100,2)
        if moves == 0:
            self.moves = [pokemon_list[self.name][7][0], pokemon_list[self.name][7][1]]
        else:
            self.moves = [moves[0],moves[1]]
        self.poison_turns = 0

    def print_stats(self): #prints the stats in a neat form
        print(f"\nName: {self.id}\nType: {self.type}\nLvl: {self.lvl}\nXP: {self.xp} - {10 * (self.lvl) - self.xp}xp needed to level up!\nIVs: {self.ivs}\nMax HP: {self.max_hp}\nCurrent HP: {self.cur_hp}\nAttack: {self.att} * {self.stat_changes[0]}\nSpecial Attack: {self.sp_att} * {self.stat_changes[1]}\nDefence: {self.defence} * {self.stat_changes[2]}\nSpecial Defence: {self.sp_defence} * {self.stat_changes[3]}\nSpeed: {self.speed} * {self.stat_changes[4]}\nMoves: {self.moves[0]}, {self.moves[1]}")
    def lvl_up(self, evolved): #levels up the pokemon
        print(f"{self.id} leveled up! ({self.lvl}-→{self.lvl + 1})\n")
        #changes stats
        hp = self.cur_hp/self.max_hp
        self.xp -= 10 * self.lvl
        self.lvl += 1
        self.max_hp = round(10+((2*(pokemon_list[self.name][1] + 0.02*(self.lvl-1)*pokemon_list[self.name][1]) + self.ivs[0] + 100)*self.lvl)/100,2)
        self.cur_hp = self.max_hp * hp
        self.att = round(5+((2*(pokemon_list[self.name][2] + 0.02*(self.lvl-1)*pokemon_list[self.name][2]) + self.ivs[1] + 100)*self.lvl)/100,2)
        self.sp_att = round(5+((2*(pokemon_list[self.name][3] + 0.02*(self.lvl-1)*pokemon_list[self.name][3]) + self.ivs[2] + 100)*self.lvl)/100,2)
        self.defence = round(5+(2*(pokemon_list[self.name][4] + 0.02*(self.lvl-1)*pokemon_list[self.name][4]) + self.ivs[3] + 100*self.lvl)/100,2)
        self.sp_defence = round(5+((2*(pokemon_list[self.name][5] + 0.02*(self.lvl-1)*pokemon_list[self.name][5]) + self.ivs[4] + 100)*self.lvl)/100,2)
        self.speed = round(5+((2*(pokemon_list[self.name][6] + 0.02*(self.lvl-1)*pokemon_list[self.name][6]) + self.ivs[5] + 100)*self.lvl)/100,2)
        #Checks if it evolves
        if self.lvl >= pokemon_list[self.name][8][0]:
            if self.name in pokemon_team:
                pokemon_team.remove(self.name)
            evolved = Pokemon(self.lvl, pokemon_list[self.name][8][1], self.xp, [self.ivs[0],self.ivs[1], self.ivs[2], self.ivs[3],self.ivs[4],self.ivs[5]], self.cur_hp/self.max_hp, [self.moves[0],self.moves[1]])
            your_pokemon.pop(self.name)
            print(f"You pokemon evolved from a {self.name} into a {pokemon_list[self.name][8][1]}!\n")
        #Checks if a move can be learned
        if self.lvl in pokemon_list[self.name][7].keys():
            valid_choice = True
            while valid_choice:
                learn = input(f"Do you want your {self.id} to learn {pokemon_list[self.name][7][self.lvl]}? y/n ")
                if learn == "y" or learn == "n":
                    valid_choice = False
                else:
                    print("Invalid Input")
            if learn == "y":
                select = True
                while select:
                    which = input(f"Which move would you like to replace({self.moves[0]}/{self.moves[1]})? ")
                    print()
                    if which == self.moves[0] or which == self.moves[1]:
                        select = False
                    else:
                        print("Invalid Input")
                self.moves.remove(which)
                self.moves.append(pokemon_list[self.name][7][self.lvl])
        return evolved
    def calc_dmg(self, move, enemy): #Calculates Damage
        if self.cur_hp > 0:
            print(f"You used {move}!")
            multiplier = 0
            can_attack = True
            #Checks if unable to move bevause of status effects
            if "Flinched" in self.status_effects:
                print("Your pokemon flinched and could not move! \n")
                can_attack = False
            elif "Paralyzed" in self.status_effects:
                if random.randint(1,100) <= 25: #Checks if the move misses due to paralyzed
                    print("Your pokemon was paralyzed and could not move! \n")
                    can_attack = False
            if can_attack: #Checks if can attack
                if random.randint(1, 100) <= move_list[move][1]-5: #Checks accuracy
                    #Dmg calc
                    if move_list[move][0] != -1:
                        multiplier = (2 * self.lvl / 5) * move_list[move][0]
                        if "Burned" in self.status_effects:
                            multiplier /= 2
                        if move_list[move][2] == "Physical":
                            multiplier *= self.att * self.stat_changes[0]
                            multiplier /= (enemy.e_defence * enemy.e_stat_changes[2])
                        else:
                            multiplier *= self.sp_att * self.stat_changes[1]
                            multiplier /= (enemy.e_sp_defence * enemy.e_stat_changes[3])
                        multiplier /= 50
                        multiplier += 2
                        if random.randint(1, 10000) <= move_list[move][8]:
                            print("It's a crit!")
                            multiplier *= 1.5
                        multiplier *= how_effective_your_move(move, enemy.e_type[0], enemy.e_type[1]) * (random.randint(85, 100) / 100)
                        if move_list[move][3] in self.type:
                            multiplier *= 1.5
                        if move == "Payback" and self.speed * self.stat_changes[4] < enemy.e_speed * enemy.e_stat_changes[4]:
                            print("You did double damage because you were attacked first! ")
                            multiplier *= 2
                        print(f"You did {round(multiplier,2)} dmg to the enemy! ")
                        #Checks Recoil dmg
                        if move_list[move][4] != 0:
                            recoil = round(multiplier * move_list[move][4],2)
                            print(f"You took {recoil} dmg as recoil! ")
                            self.cur_hp -= recoil
                            print(f"You are on {round(self.cur_hp,2)} health! ")
                        #Checks if any status effects are inflicted
                        if move_list[move][6][0] != "":
                            if move_list[move][6][0] not in enemy.e_status_effects:
                                if random.randint(1, 100) <= move_list[move][6][1]:
                                    enemy.e_status_effects.append(move_list[move][6][0])
                                    if move_list[move][6][0] != "Flinched":
                                        print(f"The Enemy was {move_list[move][6][0]}! ")
                                    if move_list[move][6][0] == "Paralyzed":
                                        stage = stat_stages.index(enemy.e_stat_changes[4])
                                        enemy.e_stat_changes[4] = stat_stages[stage - 2]
                        #Checks if any stat changes
                        if move_list[move][7][0] != "":
                            if random.randint(1,100) <= move_list[move][7][4]:
                                if move_list[move][7][1] == "enemy":
                                    index = stat_stages.index(enemy.e_stat_changes[move_list[move][7][2]])
                                    if index != 0:
                                        index -= move_list[move][7][3]
                                        if index < 0:
                                            index = 0
                                        enemy.e_stat_changes[move_list[move][7][2]] = stat_stages[index]
                                        print(f"The enemy's {move_list[move][7][0]} was lowered by {move_list[move][7][3]} stages! ")
                                    else:
                                        print(f"The enemy's {move_list[move][7][0]} is already the lowest it can be! ")
                                else:
                                    index = stat_stages.index(self.stat_changes[move_list[move][7][2]])
                                    if index != 13:
                                        index += move_list[move][7][3]
                                        if index > 13:
                                            index = 13
                                        self.stat_changes[move_list[move][7][2]] = stat_stages[index]
                                        print(f"Your {move_list[move][7][0]} was raised by {move_list[move][7][3]} stages! ")
                                    else:
                                        print(f"Your {move_list[move][7][0]} is already the highest it can be! ")
                        enemy.e_cur_hp -= multiplier
                        if enemy.e_cur_hp < 0:
                            enemy.e_cur_hp = 0
                        print(f"The enemy is on {round(enemy.e_cur_hp, 2)} health! \n")
                    else: #If the move does no damage it will run this so the text doesnt say you did 0 dmg
                        if move_list[move][6][0] != "":
                            if move_list[move][6][0] not in enemy.e_status_effects:
                                if random.randint(1, 100) <= move_list[move][6][1]:
                                    enemy.e_status_effects.append(move_list[move][6][0])
                                    if move_list[move][6][0] != "Flinched":
                                        print(f"The Enemy was {move_list[move][6][0]}! \n")
                                    if move_list[move][6][0] == "Paralyzed":
                                        stage = stat_stages.index(enemy.e_stat_changes[4])
                                        enemy.e_stat_changes[4] = stat_stages[stage-2]
                            else:
                                print(f"The enemy is already {move_list[move][6][0]}! \n")
                        if move_list[move][7][0] != "":
                            if random.randint(1,100) <= move_list[move][7][4]:
                                if move_list[move][7][1] == "enemy":
                                    index = stat_stages.index(enemy.e_stat_changes[move_list[move][7][2]])
                                    if index != 0:
                                        index -= move_list[move][7][3]
                                        if index < 0:
                                            index = 0
                                        enemy.e_stat_changes[move_list[move][7][2]] = stat_stages[index]
                                        print(f"The enemy's {move_list[move][7][0]} was lowered by {move_list[move][7][3]} stages! \n")
                                    else:
                                        print(f"The enemy's {move_list[move][7][0]} is already the lowest it can be! \n")
                                else:
                                    index = stat_stages.index(self.stat_changes[move_list[move][7][2]])
                                    if index != 13:
                                        index += move_list[move][7][3]
                                        if index > 13:
                                            index = 13
                                        self.stat_changes[move_list[move][7][2]] = stat_stages[index]
                                        print(f"Your {move_list[move][7][0]} was raised by {move_list[move][7][3]} stages! \n")
                                    else:
                                        print(f"Your {move_list[move][7][0]} is already the highest it can be! \n")
                else:
                    print("You missed!\n")
                    multiplier = 0
            multiplier = round(multiplier,2)
            return multiplier
    def heal(self): #Heals the pokemon to max
        self.cur_hp = self.max_hp


class EnemyPokemon:
    def __init__(self, lvl, name):
        #Gets the stats
        self.e_name = name
        self.e_type = [pokemon_list[self.e_name][0][0],pokemon_list[self.e_name][0][1]]
        self.e_ivs = [random.randint(0,15),random.randint(0,15),random.randint(0,15),random.randint(0,15),random.randint(0,15),random.randint(0,15)]
        self.e_lvl = lvl
        self.e_xp = 0
        self.e_max_hp = round(10+ ((2*(pokemon_list[self.e_name][1] + (self.e_lvl-1)*0.02*pokemon_list[self.e_name][1]) + self.e_ivs[0] + 100)*self.e_lvl)/100,2)
        self.e_cur_hp = self.e_max_hp
        self.e_status_effects = []
        self.e_stat_changes = [1,1,1,1,1]
        self.e_att = round(5 +((2*(pokemon_list[self.e_name][2] + (self.e_lvl-1)*0.02*pokemon_list[self.e_name][2]) + self.e_ivs[1] + 100)*self.e_lvl)/100,2)
        self.e_sp_att = round(5 + ((2*(pokemon_list[self.e_name][3] + (self.e_lvl-1)*0.02*pokemon_list[self.e_name][3]) + self.e_ivs[2] + 100)*self.e_lvl)/100,2)
        self.e_defence = round(5 + ((2*(pokemon_list[self.e_name][4] + (self.e_lvl-1)*0.02*pokemon_list[self.e_name][4]) + self.e_ivs[3] + 100)*self.e_lvl)/100,2)
        self.e_sp_defence = round(5 + ((2*(pokemon_list[self.e_name][5] + (self.e_lvl-1)*0.02*pokemon_list[self.e_name][5]) + self.e_ivs[4] + 100)*self.e_lvl)/100,2)
        self.e_speed = round(5 + ((2*(pokemon_list[self.e_name][6] + (self.e_lvl-1)*0.02*pokemon_list[self.e_name][6]) + self.e_ivs[5] + 100)*self.e_lvl)/100,2)
        #Gets random moves that it could have learned at its level
        available_moves = []
        for i in range(0,self.e_lvl + 1): #Looks at each level up to its current
            if i in pokemon_list[self.e_name][7].keys(): #Sees if there are any moves that can be learned
                available_moves.append(pokemon_list[self.e_name][7][i]) #If there is, then it gets put into the available move list
        random.shuffle(available_moves) #Shuffles the moves
        self.e_moves = [available_moves[0], available_moves[1]] #Takes the first 2
        self.e_poison_turns = 0

    def e_print_stats(self): #Prints stats
        print(f"\nName: {self.e_name}\nType: {self.e_type}\nLvl: {self.e_lvl}\nXP: {self.e_xp} - {10 * (self.e_lvl) - self.e_xp}xp needed to level up!\nIVS: {self.e_ivs}\nMax HP: {self.e_max_hp}\nCurrent HP: {self.e_cur_hp}\nStatus Effects: {self.e_status_effects}\nAttack: {self.e_att} * {self.e_stat_changes[0]}\nSpecial Attack: {self.e_sp_att} * {self.e_stat_changes[1]}\nDefence: {self.e_defence} * {self.e_stat_changes[2]}\nSpecial Defence: {self.e_sp_defence} * {self.e_stat_changes[3]}\nSpeed: {self.e_speed} * {self.e_stat_changes[4]}\nMoves: {self.e_moves}")
    def e_calc_dmg(self, move, player): #calculates dmg
        if self.e_cur_hp > 0:
            print(f"The enemy used {move}!")
            multiplier = 0
            can_attack = True
            # Checks if unable to move because of status effects
            if "Flinched" in self.e_status_effects:
                print("The enemy flinched and could not move! \n")
                can_attack = False
            elif "Paralyzed" in self.e_status_effects:
                if random.randint(1, 100) <= 25:  # Checks if the move misses due to paralyzed
                    print("The enemy was paralyzed and could not move! \n")
                    can_attack = False
            if can_attack:  # Checks if can attack
                if random.randint(1, 100) <= move_list[move][1] - 5:  # Checks accuracy
                    # Dmg calc
                    if move_list[move][0] != -1:
                        multiplier = (2 * self.e_lvl / 5) * move_list[move][0]
                        if "Burned" in self.e_status_effects:
                            multiplier /= 2
                        if move_list[move][2] == "Physical":
                            multiplier *= self.e_att * self.e_stat_changes[0]
                            multiplier /= (player.defence * player.stat_changes[2])
                        else:
                            multiplier *= self.e_sp_att * self.e_stat_changes[1]
                            multiplier /= (player.sp_defence * player.stat_changes[3])
                        multiplier /= 50
                        multiplier += 2
                        if random.randint(1, 10000) <= move_list[move][8]:
                            print("It's a crit!")
                            multiplier *= 1.5
                        multiplier *= how_effective_enemy_move(move, player.type[0], player.type[1],1) * (random.randint(85, 100) / 100)
                        if move_list[move][3] in self.e_type:
                            multiplier *= 1.5
                        if move == "Payback" and self.e_speed * self.e_stat_changes[4] < player.speed * player.stat_changes[4]:
                            print("The enemy did double damage because they were attacked first! ")
                            multiplier *= 2
                        print(f"The enemy did {round(multiplier, 2)} dmg to you! ")
                        # Checks Recoil dmg
                        if move_list[move][4] != 0:
                            recoil = round(multiplier * move_list[move][4], 2)
                            print(f"The enemy took {recoil} damage as recoil! ")
                            self.e_cur_hp -= recoil
                            print(f"The enemy is on {round(self.e_cur_hp, 2)} health! ")
                        # Checks if any status effects are inflicted
                        if move_list[move][6][0] != "":
                            if move_list[move][6][0] not in player.status_effects:
                                if random.randint(1, 100) <= move_list[move][6][1]:
                                    player.status_effects.append(move_list[move][6][0])
                                    if move_list[move][6][0] != "Flinched":
                                        print(f"You were {move_list[move][6][0]}! ")
                                    if move_list[move][6][0] == "Paralyzed":
                                        stage = stat_stages.index(player.stat_changes[4])
                                        player.stat_changes[4] = stat_stages[stage - 2]
                        # Checks if any stat changes
                        if move_list[move][7][0] != "":
                            if random.randint(1, 100) <= move_list[move][7][4]:
                                if move_list[move][7][1] == "enemy":
                                    index = stat_stages.index(player.stat_changes[move_list[move][7][2]])
                                    if index != 0:
                                        index -= move_list[move][7][3]
                                        if index < 0:
                                            index = 0
                                        player.stat_changes[move_list[move][7][2]] = stat_stages[index]
                                        print(f"Your {move_list[move][7][0]} was lowered by {move_list[move][7][3]} stages! ")
                                    else:
                                        print(f"Your {move_list[move][7][0]} is already the lowest it can be! ")
                                else:
                                    index = stat_stages.index(self.stat_changes[move_list[move][7][2]])
                                    if index != 13:
                                        index += move_list[move][7][3]
                                        if index > 13:
                                            index = 13
                                        self.stat_changes[move_list[move][7][2]] = stat_stages[index]
                                        print(f"The enemy's {move_list[move][7][0]} was raised by {move_list[move][7][3]} stages! ")
                                    else:
                                        print(f"The enemy's {move_list[move][7][0]} is already the highest it can be! ")
                        player.cur_hp -= multiplier
                        if player.cur_hp < 0:
                            player.cur_hp = 0
                        print(f"You are on {round(player.cur_hp, 2)} health! \n")
                    else:  # If the move does no damage it will run this so the text doesnt say you did 0 dmg
                        if move_list[move][6][0] != "":
                            if move_list[move][6][0] not in player.status_effects:
                                if random.randint(1, 100) <= move_list[move][6][1]:
                                    player.status_effects.append(move_list[move][6][0])
                                    if move_list[move][6][0] != "Flinched":
                                        print(f"You were {move_list[move][6][0]}! \n")
                                    if move_list[move][6][0] == "Paralyzed":
                                        stage = stat_stages.index(player.stat_changes[4])
                                        player.stat_changes[4] = stat_stages[stage - 2]

                            else:
                                print(f"You are already {move_list[move][6][0]}! \n")
                        if move_list[move][7][0] != "":
                            if random.randint(1, 100) <= move_list[move][7][4]:
                                if move_list[move][7][1] == "enemy":
                                    index = stat_stages.index(player.stat_changes[move_list[move][7][2]])
                                    if index != 0:
                                        index -= move_list[move][7][3]
                                        if index < 0:
                                            index = 0
                                        player.stat_changes[move_list[move][7][2]] = stat_stages[index]
                                        print(f"Your {move_list[move][7][0]} was lowered by {move_list[move][7][3]} stages! \n")
                                    else:
                                        print(f"Your {move_list[move][7][0]} is already the lowest it can be! \n")
                                else:
                                    index = stat_stages.index(self.e_stat_changes[move_list[move][7][2]])
                                    if index != 13:
                                        index += move_list[move][7][3]
                                        if index > 13:
                                            index = 13
                                        self.e_stat_changes[move_list[move][7][2]] = stat_stages[index]
                                        print(f"The enemy's {move_list[move][7][0]} was raised by {move_list[move][7][3]} stages! \n")
                                    else:
                                        print(f"The enemy {move_list[move][7][0]} is already the highest it can be! \n")
                else:
                    print("The enemy missed!\n")
                    multiplier = 0
            multiplier = round(multiplier, 2)
            return multiplier


def start(): #Runs at the beginning of the code
    name = input("Enter your name: ")
    input(f"Welcome, {name}, to the land of Pokemon! (Press Enter To Continue) ")
    input("There are 7 main things you can do in this game!")
    input("1. Look for pokemon. Note that you can only use the pokemon in your team during this! You can level up and even evolve! ")
    input("2. Battle another trainer. This is a singles battle 6v6! (Didn't have time to make)")
    input("3. Look at your pokemons stats! ")
    input("4. Heal your pokemon! This costs a bit of money unlike the original games! ")
    input("5. Change your pokemon team! Since 6 pokemon can be in a pokemon team, you need 7 to be able to change that team! ")
    input("6. Go to the shop and buy various things such as a random lvl 1 pokemon or just a pokeball!")
    input("7. Use pokemon candy bought in the store! ")
    input("Your pokemon journey begins now! Time to start!\n")
    print("There are three starting pokemon you can choose! Charmander, Squirtle, or Bulbasaur! ")
    print("Charmander is a fire type!\nSquirtle is a water type!\nBulbasaur is a grass type!\n")
    invalid_starting = True
    count = 0
    while invalid_starting: #Makes you choose a valid starting pokemon
        count += 1
        if count <= 3: #Runs if the user has done a invalid input less than three times
            starting = input("Choose a starting pokemon! ")
            if starting != "Charmander" and starting != "Squirtle" and starting != "Bulbasaur": #Makes sure you choose one of the three
                print("Invalid Input! \n")
            else:
                #Makes the new pokemon
                print(f"You have chosen {starting}!")
                new_pokemon = Pokemon(1,starting)
                print("Time to catch pokemon! \n")
                invalid_starting = False
        else: #If they dont choose a valid pokemon three times, they will get pikachu similar to pokemon go!
            print("After being so indecisive, other trainers have picked there pokemon and none are left! \nFortunately, there is one left...")
            time.sleep(1)
            print("Pikachu! ")
            starting = "Pikachu"
            print(f"You have chosen {starting}!")
            new_pokemon = Pokemon(1,starting)
            print("Time to catch pokemon! \n")
            invalid_starting = False
    print("Just a quick note! Every pokemon will get a number according to if they are the first, second, etc pokemon you have caught\nTo specify a pokemon, you will have to use this format: pokemon_name(number).\nPress three to see your starting pokemon's name if you are still confused!\n")

    return name



def search(): #Gets the random pokemon
    global chosen_pokemon
    chosen_pokemon = input("Choose the pokemon you want to start with! ")
    chosen_pokemon = str(chosen_pokemon)
    if chosen_pokemon in your_pokemon.keys():
        if chosen_pokemon in pokemon_team:
            if your_pokemon[chosen_pokemon].cur_hp > 0:
                print(f"You have chosen {chosen_pokemon}! ")
                invalid_enemy = True
            else:
                print("This pokemon has fainted! \n")
            while invalid_enemy:
                random_pokemon = random.choice(list(pokemon_list))
                if pokemon_list[random_pokemon][9] <= your_pokemon[chosen_pokemon].lvl:
                    invalid_enemy = False
            print(f"After searching around, you found a {random_pokemon}!\nPrepare for battle! ")
            pokemon_battle(random_pokemon, chosen_pokemon)
        else:
            print("This pokemon is not on your team! \nPress 5 to change your team!\n")
    else:
        print("This pokemon does not exist! \n")


def pokemon_battle(random_pokemon, chosen_pokemon): #Simulates the pokemon battle
    global money
    global inventory
    global pokemon_team
    #gets the average level of your team to be the enemies level but makes it up to two levels higher or lower
    total = 0
    for each in pokemon_team:
        total += your_pokemon[each].lvl
    total /= len(pokemon_team)
    enemy_level = random.randint(-2, 2) + total
    if enemy_level > 100:
        enemy_level = 100
    if enemy_level < pokemon_list[random_pokemon][9]: #If the pokemon is lower than it should be possible(eg. lvl 14 charmeleon, it becomes charmeleon  at lvl 16) it will make it a valid lvl
        enemy_level = pokemon_list[random_pokemon][9]
    enemy_level = int(enemy_level)
    enemy = EnemyPokemon(enemy_level, random_pokemon) #Creates the enemy pokemon
    print(f"The enemy is lvl {enemy.e_lvl}!\n")
    #Starts the battle
    battle = True
    while battle:
        valid_move = True
        while valid_move:
            #Gets your move
            move = input(f"What do you want to do:\n\n{your_pokemon[chosen_pokemon].moves[0]}/{your_pokemon[chosen_pokemon].moves[1]}: Use one of your attack moves\nAnalyze: Analyze the opponents stats\nRun: Attempt to flee the battle\nPokeball: Attempt to catch the enemy pokemon\nSwitch: Switch your pokemon for another in your team\nStats:See your pokemons stats(doesn't take a turn)\n")
            if move in your_pokemon[chosen_pokemon].moves or move == "Analyze" or move == "Run" or move == "Pokeball" or move == "Switch" or move == "Stats":
                #List of conditions that a move can't be done if___
                if move == "Stats": #Checks if the move is stats
                    your_pokemon[chosen_pokemon].print_stats()
                elif move == "Pokeball" and inventory[0] < 1: #If no pokeballs and you try to throw one
                    print("You have no pokeballs! \n")
                elif move == "Switch": #Checks if anyone to switch into
                    can_change = False
                    for health in pokemon_team:
                        if health != chosen_pokemon:
                            if your_pokemon[health].cur_hp > 0:
                                can_change = True
                    if can_change: #If there is, then makes you choose who to switch into
                        check = chosen_pokemon
                        valid_pokemon = True
                        while valid_pokemon:
                            chosen_pokemon = input(f"Choose a pokemon to switch into(Cancel to choose another move)! \nPokemon on your team: {pokemon_team}\n")
                            if chosen_pokemon == "Cancel":
                                chosen_pokemon = check
                                print("Okay! Choose another move! \n")
                                valid_pokemon = False
                            elif chosen_pokemon in pokemon_team:
                                if your_pokemon[chosen_pokemon].cur_hp == 0:
                                    print("This pokemon fainted! \n")
                                elif chosen_pokemon == check:
                                    print("This pokemon is already out! \n")
                                else:
                                    print(f"You've switched into {chosen_pokemon}! \n")
                                    valid_pokemon = False
                                    valid_move = False
                            else:
                                print("This pokemon is not in your team or does not exist! \n")
                    else:
                        print("You have no pokemon to switch into! \n")

                else:
                    valid_move = False
            else:
                print("Invalid Move")
                print("")
        if move == "Run": #Checks if you can succesfully run
            if enemy.e_lvl != 0:
                if random.randint(0, round(enemy.e_lvl / your_pokemon[chosen_pokemon].lvl)) == 0:
                    print("You managed to run away! \nYou earned 0 xp! \n")
                    battle = False
                else:
                    print("You did not manage to run away! \n")
            else:
                print("You managed to run away! \n")
        elif move == "Analyze": #Prints the enemy stats if you analyze
            enemy.e_print_stats()
            print("")
        elif move == "Pokeball": #Runs if you try to catch the pokemon
            inventory[0] -= 1
            if pokemon_catch(enemy.e_max_hp,enemy.e_cur_hp) == 1:
                battle = False
                #Creates the new pokemon
                new_pokemon = Pokemon(enemy.e_lvl, enemy.e_name,0,[enemy.e_ivs[0],enemy.e_ivs[1], enemy.e_ivs[2], enemy.e_ivs[3],enemy.e_ivs[4],enemy.e_ivs[5]], enemy.e_cur_hp/enemy.e_max_hp,[enemy.e_moves[0],enemy.e_moves[1]])
                print(f"Your pokemon team earned {enemy.e_lvl*20} xp!")
                for i in pokemon_team: #Gives xp to each pokemon
                    your_pokemon[i].xp += enemy.e_lvl*20
            print(f"You now have {inventory[0]} pokeballs! \n")
        if battle == True:
            #AI
            e_move = enemy.e_moves[0]
            e_move1 = enemy.e_moves[1]
            if move_list[e_move][0] != -1:
                value = move_list[e_move][0] * move_list[e_move][1]/100 * how_effective_enemy_move(e_move,your_pokemon[chosen_pokemon].type[0],your_pokemon[chosen_pokemon].type[1],0) #Gets the move damage times the (percent chance to hit/100) times the effectiveness
                if move_list[e_move][3] in enemy.e_type:
                    value *= 1.5
            else:
                value = 0
            if move_list[e_move][6][0] != "":
                if move_list[e_move][6][0] not in your_pokemon[chosen_pokemon].status_effects:
                    value += move_list[e_move][6][1] #Adds the percent chance of a status effect to be inflicted to the value
            if move_list[e_move][7][0] != "":
                #Checks if it will have no effect
                if move_list[e_move][7][1] == "enemy" and your_pokemon[chosen_pokemon].stat_changes[move_list[e_move][7][2]] != 2/8:
                    value += move_list[e_move][7][4] * move_list[e_move][7][3] * your_pokemon[chosen_pokemon].stat_changes[move_list[e_move][7][2]]/4 #Adds half the value of the percent for a stat change
                elif enemy.e_stat_changes[move_list[e_move][7][2]] != 8/2 and move_list[e_move][7][0] == "self":
                    value += move_list[e_move][7][4] * move_list[e_move][7][3]/(your_pokemon[chosen_pokemon].stat_changes[move_list[e_move][7][2]]*4) #Adds half the value of the percent for a stat change

            if move_list[e_move1][0] != -1:
                value1 = move_list[e_move1][0] * move_list[e_move1][1] / 100 * how_effective_enemy_move(e_move1,your_pokemon[chosen_pokemon].type[0],your_pokemon[chosen_pokemon].type[1],0) #Gets the move damage times the (percent chance to hit/100) times the effectiveness
                if move_list[e_move1][3] in enemy.e_type:
                    value1 *= 1.5
            else:
                value1 = 0
            if move_list[e_move1][6][0] != "":
                if move_list[e_move1][6][0] not in your_pokemon[chosen_pokemon].status_effects:
                    value1 += move_list[e_move1][6][1] #Adds the percent chance of a status effect to be inflicted to the value
            if move_list[e_move1][7][0] != "": #Adds to the value if there is a status
                if move_list[e_move1][7][1] == "enemy" and your_pokemon[chosen_pokemon].stat_changes[move_list[e_move1][7][2]] != 2/8:
                    value1 += move_list[e_move1][7][4] * move_list[e_move1][7][3] * your_pokemon[chosen_pokemon].stat_changes[move_list[e_move1][7][2]]/4
                elif enemy.e_stat_changes[move_list[e_move1][7][2]] != 8/2 and move_list[e_move1][7][0] and move_list[e_move1][7][0] == "self":
                    value1 += move_list[e_move1][7][4] * move_list[e_move1][7][3]/(your_pokemon[chosen_pokemon].stat_changes[move_list[e_move1][7][2]]*4)
            value += random.randint(1,10)
            value1 += random.randint(1,10)
            if value1 > value: #Checks which value is larger
                e_move = e_move1

            if move == your_pokemon[chosen_pokemon].moves[0] or move == your_pokemon[chosen_pokemon].moves[1]: #Checks if your move was a attack move, else it will just run the opponents attack
                #Checks who goes first
                if move_list[e_move][5] > move_list[move][5]:
                    first = "enemy"
                elif move_list[e_move][5] < move_list[move][5]:
                    first = "player"
                else:
                    if your_pokemon[chosen_pokemon].speed*your_pokemon[chosen_pokemon].stat_changes[4] >= enemy.e_speed*enemy.e_stat_changes[4]:
                        first = "player"
                    else:
                        first = "enemy"
                #Runs the scripts in order of who is first
                if first == "enemy":
                    enemy.e_calc_dmg(e_move,your_pokemon[chosen_pokemon])
                    if your_pokemon[chosen_pokemon].cur_hp >= 0:
                        your_pokemon[chosen_pokemon].calc_dmg(move,enemy)
                else:
                    your_pokemon[chosen_pokemon].calc_dmg(move, enemy)
                    if enemy.e_cur_hp >= 0:
                        enemy.e_calc_dmg(e_move, your_pokemon[chosen_pokemon])
            else:
                enemy.e_calc_dmg(e_move, your_pokemon[chosen_pokemon])
            #Gives xp if the enemy faints
            enemy.e_cur_hp = round(enemy.e_cur_hp,2)
            your_pokemon[chosen_pokemon].cur_hp = round(your_pokemon[chosen_pokemon].cur_hp,2)
            #Does damage to the respective pokemon if they are burned or poisoned
            if "Burned" in your_pokemon[chosen_pokemon].status_effects and your_pokemon[chosen_pokemon].cur_hp != 0 and enemy.e_cur_hp != 0:
                your_pokemon[chosen_pokemon].cur_hp -= round((1/16)*your_pokemon[chosen_pokemon].max_hp,2)
                if your_pokemon[chosen_pokemon].cur_hp < 0:
                    your_pokemon[chosen_pokemon].cur_hp = 0
                print(f"You were hurt by the burn! ")
                print(f"You took {round((1/16)*your_pokemon[chosen_pokemon].max_hp,2)} damage! ")
                print(f"You are on {your_pokemon[chosen_pokemon].cur_hp} health! \n")
            if "Burned" in enemy.e_status_effects and enemy.e_cur_hp != 0 and your_pokemon[chosen_pokemon].cur_hp != 0:
                enemy.e_cur_hp -= round((1/16)*enemy.e_max_hp,2)
                print("The enemy was hurt by the burn! ")
                print(f"The enemy took {round((1/16)*enemy.e_max_hp,2)} damage! ")
                if enemy.e_cur_hp < 0:
                    enemy.e_cur_hp = 0
                print(f"The enemy is on {enemy.e_cur_hp} health! \n")
            if "Poisoned" in your_pokemon[chosen_pokemon].status_effects and your_pokemon[chosen_pokemon].cur_hp != 0 and enemy.e_cur_hp != 0:
                your_pokemon[chosen_pokemon].poison_turns += 1
                print("You were hurt by the poison! ")
                print(f"You took {round(your_pokemon[chosen_pokemon].poison_turns * your_pokemon[chosen_pokemon].max_hp/16,2)} damage! ")
                your_pokemon[chosen_pokemon].cur_hp -= round(your_pokemon[chosen_pokemon].poison_turns * your_pokemon[chosen_pokemon].max_hp/16,2)
                if your_pokemon[chosen_pokemon].cur_hp < 0:
                    your_pokemon[chosen_pokemon].cur_hp = 0
                print(f"You are on {your_pokemon[chosen_pokemon].cur_hp} health! \n")
            if "Poisoned" in enemy.e_status_effects and enemy.e_cur_hp != 0 and your_pokemon[chosen_pokemon].cur_hp != 0:
                enemy.e_poison_turns += 1
                print("The enemy was hurt by the poison! ")
                print(f"The enemy took {round(enemy.e_poison_turns * enemy.e_max_hp/16,2)} damage!")
                enemy.e_cur_hp -= round(enemy.e_poison_turns * enemy.e_max_hp/16,2)
                if enemy.e_cur_hp < 0:
                    enemy.e_cur_hp = 0
                print(f"The enemy is on {enemy.e_cur_hp} health! \n")
            #Removes flinch at the end of the turn
            if "Flinched" in your_pokemon[chosen_pokemon].status_effects and your_pokemon[chosen_pokemon].cur_hp != 0 and enemy.e_cur_hp != 0:
                your_pokemon[chosen_pokemon].status_effects.remove("Flinched")
            if "Flinched" in enemy.e_status_effects and enemy.e_cur_hp != 0 and your_pokemon[chosen_pokemon].cur_hp != 0:
                enemy.e_status_effects.remove("Flinched")

            if enemy.e_cur_hp == 0:
                print(f"The enemy fainted!\nYour pokemon team earned {40 * enemy.e_lvl} xp!\n")
                for i in pokemon_team:
                    your_pokemon[i].xp += enemy.e_lvl * 40
                battle = False
            if your_pokemon[chosen_pokemon].cur_hp == 0: #Checks if any pokemon to switch into if the current pokemon is knocked out
                go_on = False
                print(f"{chosen_pokemon} fainted! \n")
                for pokemon in pokemon_team:
                    if your_pokemon[pokemon].cur_hp != 0:
                        go_on = True
                if go_on == False:
                    print("All your pokemon have fainted! \n")
                    battle = False
                else:
                    valid_pokemon = True
                    while valid_pokemon: #Forces you to switch pokemon if there are ones that havent fainted in your team
                        chosen_pokemon = input(f"Choose a pokemon to switch into!  \nPokemon on your team: {pokemon_team}\n")
                        if chosen_pokemon in pokemon_team:
                            if your_pokemon[chosen_pokemon].cur_hp == 0:
                                print("This pokemon fainted! ")
                            else:
                                print(f"You've switched into {chosen_pokemon}! \n")
                                valid_pokemon = False
                        else:
                            print("This pokemon is not in your team or does not exist! ")
    if battle == False and your_pokemon[chosen_pokemon].cur_hp != 0 and move != "Run": #Gives xp if you win
        money += enemy.e_lvl * 10
        print(f"You earned ₽{enemy.e_lvl * 10}! \nYou are now on ₽{money}! \n")
    for who in pokemon_team: #Levels up pokemon if they gain enough xp
        who = your_pokemon[who]
        while who.xp >= (who.lvl) * 10 and who.lvl < 100:
            who = who.lvl_up(who)
    if battle == False: #Nullifies the stat changes at the end of the battle
        for i in your_pokemon.values():
            i.stat_changes = [1,1,1,1,1]


def pokemon_catch(e_max_hp, e_cur_hp):
    #Does a calculation for pokemon catch rate that I searched online
    m = random.randint(0,255)
    f = (e_max_hp * 1020)/(e_cur_hp*12)
    caught = 0
    print("")
    if f >= m:
        for i in range(3):
            time.sleep(0.8)
            print("*Pokeball shakes*\n")
        print("You caught the pokemon! \nIt has been added to your pokemon list!")
        caught = 1
    else:
        shake = random.randint(0,3)
        for amount in range(shake):
            time.sleep(0.8)
            print("*Pokeball shakes*\n")
        print("It broke out! ")
    return caught



def how_effective_your_move(move, e_type1,e_type2): #Uses the database to see how effective the move is
    effective = 1
    if move_list[move][3] in type_effective.keys():
        if e_type1 in type_effective[move_list[move][3]]:
            effective *= 2
        if e_type2 in type_effective[move_list[move][3]]:
            effective *= 2
    if move_list[move][3] in type_not_effective.keys():
        if e_type1 in type_not_effective[move_list[move][3]]:
            effective *= 0.5
        if e_type2 in type_not_effective[move_list[move][3]]:
            effective *= 0.5
    if move_list[move][3] in type_no_effect.keys():
        if e_type1 in type_no_effect[move_list[move][3]]:
            effective *= 0
        if e_type2 in type_no_effect[move_list[move][3]]:
            effective *= 0
    if effective == 0:
        print("It has no effect! ")
    elif effective < 1:
        print("It's not very effective...")
    elif effective == 1:
        print("It's effective! ")
    else:
        print("It's super effective! ")
    return effective


def how_effective_enemy_move(e_move, type1,type2,print_or_not=1): #Uses the database to see how effective the move is
    effective = 1
    if move_list[e_move][3] in type_effective.keys():
        if type1 in type_effective[move_list[e_move][3]]:
            effective *= 2
        if type2 in type_effective[move_list[e_move][3]]:
            effective *= 2
    if move_list[e_move][3] in type_not_effective.keys():
        if type1 in type_not_effective[move_list[e_move][3]]:
            effective *= 0.5
        if type2 in type_not_effective[move_list[e_move][3]]:
            effective *= 0.5
    if move_list[e_move][3] in type_no_effect.keys():
        if type1 in type_no_effect[move_list[e_move][3]]:
            effective *= 0
        if type2 in type_no_effect[move_list[e_move][3]]:
            effective *= 0
    if print_or_not == 1:
        if effective == 0:
            print("It has no effect! ")
        elif effective < 1:
            print("It's not very effective...")
        elif effective == 1:
            print("It's effective! ")
        else:
            print("It's super effective! ")
    return effective

player_name = start() #Gets the player name and starts the game

while True:
    option = input("What do you want to do? \n1.)Search for Pokemon in the wild\n2.)Battle another trainer(NOT MADE YET)\n3.)Look at your pokemon and their stats\n4.)Heal your pokemon\n5.)Change/Make your pokemon team you will use\n6.)Go to the shop\n7.)Use your pokemon candy\n")
    if option == "1" or option == "2" or option == "3" or option == "4" or option == "5" or option == "6" or option == "7": #Converts the number into an int so that it doesnt crash if you put a str in
        option = int(option)
        if option == 1: #Runs the search pokemon in the wild
            total = 0
            for i in pokemon_team:
                total += your_pokemon[i].cur_hp
            if total != 0:
                search()
            else:
                print("All your pokemon have fainted!\n")
        elif option == 2:
            print("Did not have enough time to code this D:\n")
        elif option == 3: #Prints the stats
            print("Your pokemon:")
            for pokemons in your_pokemon.keys():
                print(your_pokemon[pokemons].id)
            print(f"\nYour Pokemon team: \n{pokemon_team}\n")
            which = input("Would you like to see a specific pokemons stats? (y/n) ") #Checks if a specific pokemons stats is wanted to be seen
            if which == "y":
                which = input("Which pokemon would you like to see? ")
                if which not in your_pokemon:
                    print("You do not have this pokemon or it does not exist! \n")
                else:
                    your_pokemon[which].print_stats()
                    print("")
            else:
                print("Okay! Come back anytime! \n")
        elif option == 4: #Heals your pokemon for some money
            total = 0
            for poke in your_pokemon.values():
                total += (poke.max_hp - poke.cur_hp) + (len(poke.status_effects)*10)
            if total == 0:
                print("Your pokemon are at max already! \n")
            else:
                total = round(total,2)
                confirm = input(f"It will cost ₽{total}.\nAre you sure you want to do this(y/n)? ")
                if confirm.lower() == "y":
                    if money >= total:
                        money -= total
                        for poke in your_pokemon.values():
                            poke.heal()
                            poke.poison_turns = 0
                            poke.status_effects = []
                        print(f"Your pokemon healed to max! \nYou have ₽{money} left! \n")
                    else:
                        print("You do not have enough money! \n")
                else:
                    print("Ok, come back any time! \n")
        elif option == 5: #Lets you change your pokemon team
            if len(your_pokemon) > 6:
                if input("Are you sure you want to change your team? y/n ").lower() == "y":
                    pokemon_team.clear()
                    for i in range(6):
                        invalidpokemon = True
                        while invalidpokemon:
                            enter = input("Enter the pokemons name(pokemon to see your pokemon): ")
                            if enter != "pokemon":
                                if enter in your_pokemon.keys():
                                    if not enter in pokemon_team:
                                        print(f"{enter} is now on your team!\n")
                                        pokemon_team.append(enter)
                                        invalidpokemon = False
                                        your_team = "Your team: "
                                        for i in pokemon_team:
                                            if len(your_team) > 11:
                                                your_team += ", "
                                            your_team += i
                                        print(your_team)
                                    else:
                                        print("This pokemon is already on your team!")
                                else:
                                    print("You do not have this pokemon or it does not exist!")
                            else:
                                print("Your pokemon: ")
                                for i in your_pokemon.keys():
                                    print(i)
                                print("")
                    print("")
                else:
                    print("Ok. You can change your team anytime! ")
            else:
                print(f"You only have {len(your_pokemon)} pokemon.\nCatch {7 - len(your_pokemon)} more in the wild to be able to change your pokemon team of 6! \n")
        elif option == 6: #Lets you shop
            buy = int(input("Welcome to the pokestore! \nHere, we sell many useful things\nWhat would you like to buy/do?\n1.) Pokeballs\n2.) Small Candy \n3.) Medium Candy\n4.) Large Candy\n5.) A Random Pokemon\n6.) Leave the store\n"))
            #Creates a mini database for each item
            if buy == 1:
                buy = [5,"Pokeballs",0]
            elif buy == 2:
                buy = [7.5,"Small Candy",1]
            elif buy == 3:
                buy = [15,"Medium Candy",2]
            elif buy == 4:
                buy = [30,"Large Candy",3]
            elif buy == 5:
                buy = [150,"Random Pokemon"]
            else:
                buy = [0]
            if buy[0] != 0:
                print(f"They will cost ₽{buy[0]} each! ")
                amount = int(input("How many would you like to buy(0 or less to buy none)? "))
                if amount > 0:
                    if amount*buy[0] <= money:
                        certain = input(f"That will cost ₽{amount*buy[0]}\nAre you sure you want to buy? (y/n)")
                        if certain.lower() == "y":
                            if buy[1] != "Random Pokemon":
                                inventory[buy[2]] += amount
                                money -= amount*buy[0]
                                print(f"You have bought {amount} {buy[1]} for ₽{amount*buy[0]}! \nYou now have {inventory[buy[2]]} {buy[1]}!")
                                print(f"You now have ₽{money}! \n")
                            else:
                                money -= amount * buy[0]
                                for i in range(amount):
                                    input("Press Enter to Open")
                                    rand_poke = True
                                    while rand_poke:
                                        random_pokemon = random.choice(list(pokemon_list))
                                        if pokemon_list[random_pokemon][9] == 1:
                                            break
                                    print(f"You got a {random_pokemon}! \n")
                                    new_pokemon = Pokemon(1, random_pokemon)
                                print(f"You now have ₽{money}! \n")
                        else:
                            print("Ok! Come back any time! \n")
                    else:
                        print(f"You do not have enough to buy this!\nIt would cost ₽{amount*buy[0]} but you only have ₽{money}\n")
                else:
                    print("Ok! Come back any time! \n")
            else:
                print("Ok! Come back any time! \n")
        elif option == 7: #Lets your pokemon eat the candy
            if inventory[1] > 0 or inventory[2] > 0 or inventory[3] > 0:
                print(f"You have {inventory[1]} small candies, {inventory[2]} medium candies and {inventory[3]} large candies! ")
                invalid_choice = True
                while invalid_choice:
                    candy = input("Which candy would you like to use? (1 for small, 2 for medium, 3 for large, cancel to use none) ")
                    if ((candy == "1" or candy == "2" or candy == "3" )and inventory[int(candy)] > 0) or candy == "cancel":
                        invalid_choice = False
                    else:
                        print("Invalid Input")
                if candy != "cancel":
                    invalid_choice = True
                    while invalid_choice:
                        who = input("Which pokemon do you want to use it on? ")
                        if who not in your_pokemon.keys():
                            print("Invalid Input")
                        else:
                            invalid_choice = False
                    invalid_choice = True
                    candy = int(candy)
                    while invalid_choice:
                        amount = int(input("How many would you like to use? (0 or less to cancel)"))
                        if amount <= inventory[candy]:
                            invalid_choice = False
                        else:
                            print("Invalid Input")
                    if amount >= 1:
                        print(f"Your pokemon ate the candy and earned {amount*((candy)**2)*25}xp! ")
                        who = your_pokemon[who]
                        inventory[candy] -= amount
                        who.xp += ((candy)**2)*25 * amount
                        while who.xp >= (who.lvl) * 10 and who.lvl < 100:
                            who = who.lvl_up(who)
                        print()
                    else:
                        print("Okay! You can use them here any time! \n")


                else:
                    print("Ok! You can use them any time here! \n")
            else:
                print("You do not have any candies!\nYou can buy them in the shop! \n")
        else:
            print("Invalid input! \n")
