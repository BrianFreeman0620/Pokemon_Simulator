from random import *
from math import *
import pandas as pd
import copy

class Type:
    
    def __init__(self, typeName):
        self.typeName = typeName
        self.effectDict = {}
        
    def setEffectiveness(self, typeName, damageMult):
        self.effectDict[typeName] = damageMult
        
class Move:
    
    def __init__(self, moveName, typeName, power, accuracy, pp, phySpe, healing,
                 chance, stat, target, stages, hitTimes, priority, charge, crit, 
                 sound, feint):
        self.moveName = moveName
        self.moveType = Type(typeName)
        self.power = power
        self.accuracy = accuracy
        self.pp = pp
        self.currentPP = pp
        self.phySpe = phySpe
        self.healing = healing
        self.chance = chance
        self.stat = stat
        self.target = target
        self.stages = stages
        self.hitTimes = hitTimes.split("/")
        self.priority = priority
        self.charge = charge
        self.crit = crit
        self.sound = sound
        self.feint = feint
        
    def Secondary(self):
        success = randint(1, 10)
        if success <= self.chance:
            if self.stat in ["Flinch", "Confuse", "Trap"]:
                return ["Volatile", self.stat, self.target, self.stages]
            elif self.stat in ["Burn", "Sleep", "Freeze", "Paralyze", "Poison",
                               "Rest", "Badly Poison", "Tri Attack", "Healthy"]:
                return ["Status", self.stat, self.target, self.stages]
            else:
                return ["Stat", self.stat, self.target, self.stages]
        else:
            return ["Failure"]
        
class Item:
    def __init__(self, itemName, consumable, effect, secondEffect, multiplier,
                 fling):
        self.itemName = itemName
        self.consumable = consumable
        self.effect = effect
        self.secondEffect = secondEffect
        self.multiplier = multiplier
        self.consumed = False
        self.fling = fling
    
    def __str__(self):
        if self.consumed:
            return "None"
        else:
            return self.itemName
    
    def Consume(self):
        self.consumed = True

class Pokemon:
    
    def __init__(self, pokemonName, typeName1, typeName2 = "None"):
        self.pokemonName = pokemonName
        self.Type1 = Type(typeName1)
        self.Type2 = Type(typeName2)
        self.Moves = [None, None, None, None, None]
        self.BaseStats = {"HP" : 48, "Attack" : 48, "Defense" : 48,
                      "Special Attack": 48, "Special Defense": 48, 
                      "Speed" : 48}
        self.Level = 5
        self.Stats = {"HP" : 20, "Attack" : 10, "Defense" : 10,
                      "Special Attack": 10, "Special Defense": 10, 
                      "Speed" : 10}
        self.IV = [15, 15, 15, 15, 15, 15]
        self.EV = [0, 0, 0, 0, 0, 0]
        self.currentHp = 20
        self.statModifier = {"Attack" : 1, "Defense" : 1,
                      "Special Attack": 1, "Special Defense": 1, 
                      "Speed" : 1, "Accuracy": 1, "Evasion": 1}
        self.plusNature = "HP"
        self.minusNature = "HP"
        self.status = "Healthy"
        self.volatile = {"Flinch" : 0, "Confuse" : 0, "Badly Poison" : 0, "Trap" : 0, 
                         "Blocked Moves" : [5], "Intangible" : " ", "Substitute" : 0}
        self.sleepCounter = 0
        self.item = None
        self.turnOut = 0
        self.recharge = 0
        self.chargeMove = None
        self.intangibility = False
        self.transformed = False
        self.tempPokemon = None
    
    def setBaseStat(self, statName, baseStat):
        if statName in self.Stats:
            self.BaseStats[statName] = baseStat
            
    def megaEvolve(self, megaDict, megaList):
        for megaPokemon in megaList:
            if self.pokemonName == megaPokemon:
                try:
                    if self.item.effect == "Mega" and megaDict[self.pokemonName][1] == self.item.itemName:
                        self.setBaseStat("HP", megaDict[self.pokemonName][0].BaseStats["HP"])
                        self.setBaseStat("Attack", megaDict[self.pokemonName][0].BaseStats["Attack"])
                        self.setBaseStat("Defense", megaDict[self.pokemonName][0].BaseStats["Defense"])
                        self.setBaseStat("Special Attack", megaDict[self.pokemonName][0].BaseStats["Special Attack"])
                        self.setBaseStat("Special Defense", megaDict[self.pokemonName][0].BaseStats["Special Defense"])
                        self.setBaseStat("Speed", megaDict[self.pokemonName][0].BaseStats["Speed"])
                        
                        self.setStats(self.Level, self.plusNature, self.minusNature,
                                      self.IV, self.EV)
                        
                        self.pokemonName = megaDict[self.pokemonName][0].pokemonName
                        
                        return True
                except:
                    if self.item.effect == "Mega" and megaDict[self.pokemonName + " X"][1] == self.item.itemName:
                        self.setBaseStat("HP", megaDict[self.pokemonName + " X"][0].BaseStats["HP"])
                        self.setBaseStat("Attack", megaDict[self.pokemonName + " X"][0].BaseStats["Attack"])
                        self.setBaseStat("Defense", megaDict[self.pokemonName + " X"][0].BaseStats["Defense"])
                        self.setBaseStat("Special Attack", megaDict[self.pokemonName + " X"][0].BaseStats["Special Attack"])
                        self.setBaseStat("Special Defense", megaDict[self.pokemonName + " X"][0].BaseStats["Special Defense"])
                        self.setBaseStat("Speed", megaDict[self.pokemonName + " X"][0].BaseStats["Speed"])
                        
                        self.setStats(self.Level, self.plusNature, self.minusNature,
                                      self.IV, self.EV)
                        
                        self.pokemonName = megaDict[self.pokemonName + " X"][0].pokemonName
                        
                        return True
                    
                    elif self.item.effect == "Mega" and megaDict[self.pokemonName + " Y"][1] == self.item.itemName:
                        self.setBaseStat("HP", megaDict[self.pokemonName + " Y"][0].BaseStats["HP"])
                        self.setBaseStat("Attack", megaDict[self.pokemonName + " Y"][0].BaseStats["Attack"])
                        self.setBaseStat("Defense", megaDict[self.pokemonName + " Y"][0].BaseStats["Defense"])
                        self.setBaseStat("Special Attack", megaDict[self.pokemonName + " Y"][0].BaseStats["Special Attack"])
                        self.setBaseStat("Special Defense", megaDict[self.pokemonName + " Y"][0].BaseStats["Special Defense"])
                        self.setBaseStat("Speed", megaDict[self.pokemonName + " Y"][0].BaseStats["Speed"])
                        
                        self.setStats(self.Level, self.plusNature, self.minusNature,
                                      self.IV, self.EV)
                        
                        self.pokemonName = megaDict[self.pokemonName + " Y"][0].pokemonName
                        
                        return True
            
        return False
    
    def setStats(self, level, posNature = "HP", negNature = "HP", 
                 IV = [15,15,15,15,15,15], EV = [0,0,0,0,0,0]):
        self.Level = level
        counter = 0
        evTotal = 0
        for evValue in EV:
            evTotal += evValue
        if evTotal > 510:
            evFix = 510 / evTotal
        else:
            evFix = 1
        for stat in self.BaseStats:
            if stat == "HP":
                self.Stats["HP"] = int((2 * self.BaseStats[stat] + IV[counter] 
                + (floor(EV[counter] * evFix)/4)) * level / 100) + level + 10
                self.currentHp = self.Stats["HP"]
            elif posNature == stat and posNature != negNature:
                self.Stats[stat] = int((int((2 * self.BaseStats[stat] 
                + IV[counter] + (floor(EV[counter] * evFix)/4)) * level / 100) 
                    + 5) * 1.1)
                self.plusNature = posNature
            elif negNature == stat and posNature != negNature:
                self.Stats[stat] = int((int((2 * self.BaseStats[stat] 
                + IV[counter] + (floor(EV[counter] * evFix)/4)) * level / 100) 
                    + 5) * .9)
                self.minusNature = negNature
            else:
                self.Stats[stat] = int((int((2 * self.BaseStats[stat] 
                + IV[counter] + (floor(EV[counter] * evFix)/4)) * level / 100) 
                    + 5))
            counter += 1
        self.IV = IV
        self.EV = EV
    
    def newMove(self, newMove):
        for move in range(4):
            if self.Moves[move] == None:
                self.Moves[move] = newMove
                break
            
    def replaceMove(self, newMove, position):
        self.Moves[position - 1] = newMove
        
    def showMoves(self):
        for move in range(4):
            if not self.Moves[move] == None:
                print("Move " + str(move + 1) + ": " + self.Moves[move].moveName + " (" 
                      + str(self.Moves[move].currentPP) + "/" + str(self.Moves[move].pp) + ")")
                
    def newItem(self, item):
        self.item = item
                
    def modifyStat(self, stat, modifier):
        normalStats = [1/4, 2/7, 1/3, 2/5, 1/2, 2/3, 1, 3/2, 2, 5/2, 3, 7/2, 4]
        accuracyStats = [1/3, 3/8, 3/7, 1/2, 3/5, 3/4, 1, 4/3, 5/3, 2, 7/3, 8/3, 3]
        
        statSplit = stat.split("/")
        modifierSplit = modifier.split("/")
        
        for statNumber in range(len(statSplit)):
            if statSplit[statNumber] in ["Attack", "Defense", "Special Attack", "Special Defense", "Speed"]:
                for i in range(13):
                    if round(self.statModifier[statSplit[statNumber]], 2) == round(normalStats[i], 2):
                        newModifier = int(modifierSplit[statNumber]) + i
                if newModifier < 0:
                    newModifier = 0
                elif newModifier > 12:
                    newModifier = 12
                self.statModifier[statSplit[statNumber]] = normalStats[newModifier]
            elif statSplit[statNumber] in ["Accuracy", "Evasion"]:
                for i in range(13):
                    if round(self.statModifier[statSplit[statNumber]], 2) == round(accuracyStats[i], 2):
                        newModifier = int(modifierSplit[statNumber]) + i
                if newModifier < 0:
                    newModifier = 0
                elif newModifier > 12:
                    newModifier = 12
                self.statModifier[statSplit[statNumber]] = accuracyStats[newModifier]
            if int(modifierSplit[statNumber]) < 0:
                print(self.pokemonName + "'s " + statSplit[statNumber] + " was lowered!")
            elif int(modifierSplit[statNumber]) > 0:
                print(self.pokemonName + "'s " + statSplit[statNumber] + " was raised!")
    
    def changeStatus(self, status):
        success = False
        
        if status == "Tri Attack":
            triAttackStatus = randint(1, 3)
            if triAttackStatus == 1:
                status = "Burn"
            elif triAttackStatus == 2:
                status = "Freeze"
            else:
                status = "Paralyze"
        
        if status in ["Flinch", "Confuse"]:
            success = True
            self.volatile[status] = 1
        elif status == "Trap":
            success = True
            self.volatile[status] = 4
        elif status == "Poison" or status == "Badly Poison":
            if self.Type1.typeName == "Poison" or self.Type2.typeName == "Poison" or self.Type1.typeName == "Steel" or self.Type2.typeName == "Steel":
                pass
            else:
                self.status = "Poison"
                success = True
                if status == "Badly Poison":
                    self.volatile[status] = 1
        else:
            if self.Type1.typeName == "Fire" or self.Type2.typeName == "Fire":
                if status != "Burn":
                    self.status = status
                    success = True
            elif self.Type1.typeName == "Electric" or self.Type2.typeName == "Electric":
                if status != "Paralyze":
                    self.status = status
                    success = True
            elif self.Type1.typeName == "Ice" or self.Type2.typeName == "Ice":
                if status != "Freeze":
                    self.status = status
                    success = True
            elif self.status == "Healthy":
                self.sleepCounter = 0
                self.status = status
                success = True
            else:
                self.status = status
                success = True
            
        if success:
            if status == "Burn":
                print(self.pokemonName + " was burned!")
            elif status == "Poison":
                print(self.pokemonName + " was poisoned!")
            elif status == "Paralyze":
                print(self.pokemonName + " was paralyzed! It may be unable to move!")
            elif status == "Freeze":
                print(self.pokemonName + " was frozen solid!")
            elif status == "Sleep":
                print(self.pokemonName + " was put to sleep!")
            elif status == "Confuse":
                print(self.pokemonName + " was confused!")

class Team():
    
    def __init__(self):
        self.pokemonList = [None, None, None, None, None, None]
        self.alivePokemon = 0
        self.activePokemon = None
        self.reflect = 0
        self.lightScreen = 0
        self.mega = False
        
    def addPokemon(self, newPokemon):
        if self.alivePokemon < 6:
            for pokemonNumber in range(6):
                if self.pokemonList[pokemonNumber] == None:
                    self.pokemonList[pokemonNumber] = newPokemon
                    if pokemonNumber == 0:
                        self.activePokemon = self.pokemonList[pokemonNumber]
                    break
            self.alivePokemon += 1
    
    def showTeam(self):
        for pokemonNumber in range(6):
            if not self.pokemonList[pokemonNumber] == None:
                print("Pokemon " + str(pokemonNumber + 1) + ": " 
                      + self.pokemonList[pokemonNumber].pokemonName + " " 
                      + str(self.pokemonList[pokemonNumber].currentHp) + "/" 
                      + str(self.pokemonList[pokemonNumber].Stats["HP"]))
    
    def Switch(self, position):
        if not self.pokemonList[position - 1] == None:
            if self.pokemonList[position - 1].currentHp > 0:
                if self.activePokemon.transformed:
                    self.activePokemon.transformed = False
                    self.activePokemon.Stats = self.activePokemon.tempPokemon[0]
                    self.activePokemon.Type1 = self.activePokemon.tempPokemon[1]
                    self.activePokemon.Type2 = self.activePokemon.tempPokemon[2]
                    self.activePokemon.Moves = self.activePokemon.tempPokemon[3]
                if self.activePokemon.volatile["Badly Poison"] > 0:
                    self.activePokemon.volatile = {"Flinch" : 0, "Confuse" : 0, "Badly Poison" : 1, "Trap" : 0, 
                                                   "Blocked Moves" : [5], "Intangible" : " ", "Substitute" : 0}
                else:
                    self.activePokemon.volatile = {"Flinch" : 0, "Confuse" : 0, "Badly Poison" : 0, "Trap" : 0,
                                                   "Blocked Moves" : [5], "Intangible" : " ", "Substitute" : 0}
                self.activePokemon.statModifier = {"Attack" : 1, "Defense" : 1,
                      "Special Attack": 1, "Special Defense": 1, "Speed" : 1, 
                      "Accuracy": 1, "Evasion": 1}
                self.activePokemon.turnOut = 0
                self.activePokemon = self.pokemonList[position - 1]
                print("Switched to " + self.pokemonList[position - 1].pokemonName + "!")
   
    def megaEvolve(self, megaDict, megaList):
        tryMega = self.activePokemon.megaEvolve(megaDict, megaList)
        if tryMega:
            self.mega = True
            print("The Pokemon mega evolved into " + self.activePokemon.pokemonName + "!")
         
class Battle():
    
    def __init__(self, Team1, Team2):
        self.team1 = Team1
        self.team2 = Team2
        self.weather = ["Clear", 0]
    
    def typeMatchup(self):
        typeNameList = ["Bug", "Dark", "Dragon", "Electric", "Fairy", "Fighting",
                     "Fire", "Flying", "Ghost", "Grass", "Ground", "Ice", "Normal",
                     "Poison", "Psychic", "Rock", "Steel", "Water", "None"]
        typeMatchupDict = {0:[1,2,1,1,.5,.5,.5,.5,.5,2,1,1,1,.5,2,1,.5,1,1],
                           1:[1,.5,1,1,.5,.5,1,1,2,1,1,1,1,1,2,1,1,1,1],
                           2:[1,1,2,1,0,1,1,1,1,1,1,1,1,1,1,1,.5,1,1],
                           3:[1,1,.5,.5,1,1,1,2,1,.5,0,1,1,1,1,1,1,2,1],
                           4:[1,2,2,1,1,2,.5,1,1,1,1,1,1,.5,1,1,.5,1,1],
                           5:[.5,2,1,1,.5,1,1,.5,0,1,1,2,2,.5,.5,2,2,1,1],
                           6:[2,1,.5,1,1,1,.5,1,1,2,1,2,1,1,1,.5,2,.5,1],
                           7:[2,1,1,.5,1,2,1,1,1,2,1,1,1,1,1,.5,.5,1,1],
                           8:[1,.5,1,1,1,1,1,1,2,1,1,1,0,1,2,1,1,1,1],
                           9:[.5,1,.5,1,1,1,.5,.5,1,.5,2,1,1,.5,1,2,.5,2,1],
                           10:[.5,1,1,2,1,1,2,0,1,.5,1,1,1,2,1,2,2,1,1],
                           11:[1,1,2,1,1,1,.5,2,1,2,2,.5,1,1,1,1,.5,.5,1],
                           12:[1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,.5,.5,1,1],
                           13:[1,1,1,1,2,1,1,1,.5,2,.5,1,1,.5,1,.5,0,1,1],
                           14:[1,0,1,1,1,2,1,1,1,1,1,1,1,2,.5,1,.5,1,1],
                           15:[2,1,1,1,1,.5,2,2,1,1,.5,2,1,1,1,1,.5,1,1],
                           16:[1,1,1,.5,2,1,.5,1,1,1,1,2,1,1,1,2,.5,.5,1],
                           17:[1,1,.5,1,1,1,2,1,1,.5,2,1,1,1,1,2,1,.5,1],
                           18:[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]}
        self.typeList = []
        for attacking in range(19):
            self.typeList.append(Type(typeNameList[attacking]))
            for defending in range(19):
                self.typeList[attacking].setEffectiveness(typeNameList[defending],
                        typeMatchupDict[attacking][defending])
    
    def fixType(self):
        for pokemon in self.team1.pokemonList:
            if not pokemon == None:
                for Type in self.typeList:
                    if pokemon.Type1.typeName == Type.typeName:
                        pokemon.Type1 = Type
                    elif pokemon.Type2.typeName == Type.typeName:
                        pokemon.Type2 = Type
                    for move in pokemon.Moves:
                        if move == None:
                            pass
                        elif move.moveType.typeName == Type.typeName:
                            move.moveType = Type
        
        for pokemon in self.team2.pokemonList:
            if not pokemon == None:    
                for Type in self.typeList:
                    if pokemon.Type1.typeName == Type.typeName:
                        pokemon.Type1 = Type
                    elif pokemon.Type2.typeName == Type.typeName:
                        pokemon.Type2 = Type
                    for move in pokemon.Moves:
                        if move == None:
                            pass
                        elif move.moveType.typeName == Type.typeName:
                            move.moveType = Type
    
    def damageCalc(self, moveNumber, playerNum):
        moveNumber -= 1
        if playerNum == 1:
            pokemon1 = self.team1.activePokemon
            pokemon2 = self.team2.activePokemon
        else:
            pokemon1 = self.team2.activePokemon
            pokemon2 = self.team1.activePokemon
        
        if pokemon1.Moves[moveNumber].moveType.typeName == pokemon1.Type1.typeName:
            stab = 1.5
        elif pokemon1.Moves[moveNumber].moveType.typeName == pokemon1.Type2.typeName:
            stab = 1.5
        else:
            stab = 1
            
        typeEffect =  pokemon1.Moves[moveNumber].moveType.effectDict[pokemon2.Type1.typeName]
        if not pokemon2.Type2.typeName == "None":
            typeEffect *= pokemon1.Moves[moveNumber].moveType.effectDict[pokemon2.Type2.typeName]
        
        if pokemon1.Moves[moveNumber].stat == "Set Damage" and typeEffect > 0:
            damage = pokemon1.Moves[moveNumber].power
        elif pokemon1.Moves[moveNumber].stat == "Level Damage" and typeEffect > 0:
            damage = pokemon1.Level
        else:
            if self.weather[0] != "Clear":
                if self.weather[0] == "Rain Dance":
                    if pokemon1.Moves[moveNumber].moveName in ["Solar Beam", "Solar Blade"] or pokemon1.Moves[moveNumber].moveType.typeName == "Fire":
                        weatherBoost = .5
                    elif pokemon1.Moves[moveNumber].moveType.typeName == "Water":
                        weatherBoost = 2
                    else:
                        weatherBoost = 1
                elif self.weather[0] == "Sunny Day":
                    if pokemon1.Moves[moveNumber].moveType.typeName == "Fire":
                        weatherBoost = 2
                    elif pokemon1.Moves[moveNumber].moveType.typeName == "Water":
                        weatherBoost = .5
                    else:
                        weatherBoost = 1
                elif self.weather[0] == "Hail":
                    if pokemon1.Moves[moveNumber].moveName in ["Solar Beam", "Solar Blade"]:
                        weatherBoost = .5
                    else:
                        weatherBoost = 1
                elif self.weather[0] == "Sandstorm":
                    if pokemon1.Moves[moveNumber].moveName in ["Solar Beam", "Solar Blade"]:
                        weatherBoost = .5
                    else:
                        weatherBoost = 1
                    if (pokemon2.Type1.typeName == "Rock" or pokemon2.Type2.typeName == "Rock") and pokemon1.Moves[moveNumber].phySpe == "Special":
                        weatherBoost /= 1.5
            else:
                weatherBoost = 1
            if pokemon1.Moves[moveNumber].phySpe == "Physical":
                if pokemon1.Moves[moveNumber].moveName == "Facade":
                    if pokemon1.status in ["Burn", "Paralyze", "Poison"]:
                        statusMult = 2
                    else:
                        statusMult = 1
                elif pokemon1.status == "Burn":
                    statusMult = .5
                else:
                    statusMult = 1
                if pokemon1.item.effect == "Attack" and not pokemon1.item.consumed:
                    itemMult = pokemon1.item.multiplier
                elif pokemon1.item.effect == pokemon1.Moves[moveNumber].moveType.typeName and pokemon1.item.secondEffect == "Attack" and not pokemon1.item.consumed:
                    itemMult = pokemon1.item.multiplier
                elif pokemon1.item.consumed and pokemon1.Moves[moveNumber].moveName == "Acrobatics":
                    itemMult = 2
                else:
                    itemMult = 1
                if pokemon2.item.effect == pokemon1.Moves[moveNumber].moveType.typeName and pokemon2.item.secondEffect == "Defend" and typeEffect > 1 and not pokemon2.item.consumed:
                    pokemon2.item.Consume()
                    itemMult *= pokemon1.item.multiplier
                    print(pokemon2.pokemonName + " lessened the damage with its " + pokemon2.item.itemName + "!")
                if pokemon1.Moves[moveNumber].moveName == "Knock Off" and not pokemon2.item.consumed:
                    pokemon2.item.Consume()
                    itemMult *= 1.5
                    print(pokemon2.pokemonName + " had its " + pokemon2.item.itemName + " removed!")
                if pokemon2.status == "Sleep" or pokemon2.status == "Rest":
                    if pokemon1.Moves[moveNumber].moveName == "Wake-Up Slap":
                        statusMult *= 2
                if pokemon1.Moves[moveNumber].moveName == "Magnitude":
                    magnitudeNum = choice([str(4), str(10), str(5), str(5), 
                                           str(9), str(9), str(6), str(6), 
                                           str(6), str(6), str(8), str(8), 
                                           str(8), str(8), str(7), str(7), 
                                           str(7), str(7), str(7), str(7)])
                    if magnitudeNum == "4":
                        powerMult = 1
                    elif magnitudeNum == "5":
                        powerMult = 3
                    elif magnitudeNum == "6":
                        powerMult = 5
                    elif magnitudeNum == "7":
                        powerMult = 7
                    elif magnitudeNum == "8":
                        powerMult = 9
                    elif magnitudeNum == "9":
                        powerMult = 11
                    elif magnitudeNum == "10":
                        powerMult = 15
                elif pokemon1.Moves[moveNumber].moveName == "Gyro Ball":
                    if pokemon1.status == "Paralyze":
                        paraBoost = 2
                    else:
                        paraBoost = 1
                    if pokemon2.status == "Paralyze":
                        paraBoost *= .5
                    else:
                        paraBoost *= 1
                    powerMult = (25 * paraBoost * (pokemon1.Stats["Speed"] 
                    * pokemon1.statModifier["Speed"]) / (pokemon2.Stats["Speed"] 
                    * pokemon2.statModifier["Speed"])) + 1
                    if powerMult > 150:
                        powerMult = 150
                    elif powerMult < 1:
                        powerMult = 1
                elif pokemon1.Moves[moveNumber].moveName == "Reversal":
                    if pokemon1.currentHp >= pokemon1.Stats["HP"] * .6875:
                        powerMult = 1
                    elif pokemon1.currentHp >= pokemon1.Stats["HP"] * .3542:
                        powerMult = 2
                    elif pokemon1.currentHp >= pokemon1.Stats["HP"] * .2083:
                        powerMult = 4
                    elif pokemon1.currentHp >= pokemon1.Stats["HP"] * .1042:
                        powerMult = 5
                    elif pokemon1.currentHp >= pokemon1.Stats["HP"] * .0417:
                        powerMult = (15/2)
                    else:
                        powerMult = 10
                else:
                    powerMult = 1
                if pokemon1.Moves[moveNumber].moveName == "Fling":
                    if pokemon1.item.fling > 0 and not pokemon1.item.consumed:
                        damage = floor((floor(floor(floor(((2 * pokemon1.Level) / 5) + 2) * pokemon1.item.fling * powerMult
                              * (pokemon1.Stats["Attack"]/pokemon2.Stats["Defense"])) / 50) 
                                + 2) * (stab * typeEffect * pokemon1.statModifier["Attack"] /
                                   pokemon2.statModifier["Defense"] * (randint(85, 100) / 100)
                                   * statusMult * itemMult * weatherBoost))
                        print(pokemon1.pokemonName + " flung its " + pokemon1.item.itemName + "!")
                        pokemon1.item.Consume()
                    else:
                        damage = 0
                        print(pokemon1.pokemonName + " failed to fling a thing!")
                else:
                    damage = floor((floor(floor(floor(((2 * pokemon1.Level) / 5) + 2) * pokemon1.Moves[moveNumber].power * powerMult
                          * (pokemon1.Stats["Attack"]/pokemon2.Stats["Defense"])) / 50) 
                            + 2) * (stab * typeEffect * pokemon1.statModifier["Attack"] /
                               pokemon2.statModifier["Defense"] * (randint(85, 100) / 100)
                               * statusMult * itemMult * weatherBoost))
            else:
                if pokemon1.item.effect == "Special Attack" and not pokemon1.item.consumed:
                    itemMult = pokemon1.item.multiplier
                elif pokemon1.item.effect == pokemon1.Moves[moveNumber].moveType.typeName and pokemon1.item.secondEffect == "Attack" and not pokemon1.item.consumed:
                    itemMult = pokemon1.item.multiplier
                else:
                    itemMult = 1
                if pokemon2.item.effect == pokemon1.Moves[moveNumber].moveType.typeName and pokemon2.item.secondEffect == "Defend" and typeEffect > 1 and not pokemon2.item.consumed:
                    pokemon2.item.Consume()
                    itemMult *= pokemon1.item.multiplier
                    print(pokemon2.pokemonName + " lessened the damage with its " + pokemon2.item.itemName + "!")
                if pokemon1.Moves[moveNumber].moveName == "Electro Ball":
                    if pokemon1.status == "Paralyze":
                        paraBoost = .5
                    else:
                        paraBoost = 1
                    if pokemon2.status == "Paralyze":
                        paraBoost *= 2
                    else:
                        paraBoost *= 1
                    speedComp = (paraBoost * (pokemon2.Stats["Speed"] 
                    * pokemon2.statModifier["Speed"]) / (pokemon1.Stats["Speed"] 
                    * pokemon1.statModifier["Speed"]))
                    if speedComp > 1:
                        powerMult = 1
                    elif speedComp > .5:
                        powerMult = 1.5
                    elif speedComp > .3333:
                        powerMult = 2
                    elif speedComp > .25:
                        powerMult = 3
                    else:
                        powerMult = (15/4)
                elif pokemon1.Moves[moveNumber].moveName == "Trump Card":
                    if pokemon1.Moves[moveNumber].currentPP == 5:
                        powerMult = 4
                    elif pokemon1.Moves[moveNumber].currentPP == 4:
                        powerMult = 5
                    elif pokemon1.Moves[moveNumber].currentPP == 3:
                        powerMult = 6
                    elif pokemon1.Moves[moveNumber].currentPP == 2:
                        powerMult = 8
                    elif pokemon1.Moves[moveNumber].currentPP == 1:
                        powerMult = 20
                elif pokemon1.Moves[moveNumber].moveName in ["Eruption", "Water Spout", "Dragon Energy"]:
                    powerMult = pokemon1.currentHp / pokemon1.Stats["HP"]
                    if powerMult < (1/150):
                        powerMult = (1/150)
                else:
                    powerMult = 1
                if pokemon1.Moves[moveNumber].moveName not in ["Secret Sword", "Psyshock", "Psystrike"]:
                    damage = floor((floor(floor(floor(((2 * pokemon1.Level) / 5) + 2) 
                    * pokemon1.Moves[moveNumber].power * powerMult * (pokemon1.Stats["Special Attack"] 
                    / pokemon2.Stats["Special Defense"])) / 50) + 2) * (stab 
                        * typeEffect * pokemon1.statModifier["Special Attack"] / 
                        pokemon2.statModifier["Special Defense"] * (randint(85, 100) / 100) 
                        * itemMult * weatherBoost))
                else:
                    damage = floor((floor(floor(floor(((2 * pokemon1.Level) / 5) + 2) 
                    * pokemon1.Moves[moveNumber].power * powerMult * 
                    (pokemon1.Stats["Special Attack"] / pokemon2.Stats["Defense"])) / 50) + 2) * 
                        (stab * typeEffect * pokemon1.statModifier["Special Attack"] / 
                         pokemon2.statModifier["Defense"] * (randint(85, 100) / 100) 
                         * itemMult * weatherBoost))
                if pokemon1.Moves[moveNumber].moveName == "Dream Eater":
                    if pokemon2.status == "Sleep" or pokemon2.status == "Rest":
                        pass
                    else:
                        typeEffect = 0
                        damage = 0
        if (pokemon1.turnOut > 1 and pokemon1.Moves[moveNumber].moveName == "Fake Out") or (damage == 0 and pokemon1.Moves[moveNumber].moveName == "Fling"):
            damage = 0
        elif damage < 1 and typeEffect > 0:
            damage = 1
        return damage, typeEffect
        
    def Attack(self, moveNumber, priority1, priority2, playerNum, computer, computer2 = False):
        if playerNum == 1:
            pokemon1 = self.team1.activePokemon
            pokemon2 = self.team2.activePokemon
            attackingTeam = self.team1
            defendingTeam = self.team2
        else:
            pokemon1 = self.team2.activePokemon
            pokemon2 = self.team1.activePokemon
            defendingTeam = self.team1
            attackingTeam = self.team2
        damage, typeEffect = self.damageCalc(moveNumber, playerNum)
        
        if damage == 0 and pokemon1.Moves[moveNumber - 1].power > 0:
            hit = 0
        elif pokemon2.intangibility:
            hit = 0
        elif self.weather[0] == "Hail" and pokemon1.Moves[moveNumber - 1].moveName == "Blizzard":
            hit = 101
        elif self.weather[0] == "Rain Dance" and pokemon1.Moves[moveNumber - 1].moveName in ["Thunder", "Hurricane"]:
            hit = 101
        elif self.weather[0] == "Sunny Day" and pokemon1.Moves[moveNumber - 1].moveName in ["Thunder", "Hurricane"]:
            hit = randint(1, 140)
        else:
            hit = randint(1, 100)
        
        if hit <= pokemon1.Moves[moveNumber - 1].accuracy * pokemon1.statModifier["Accuracy"] / pokemon2.statModifier["Evasion"] or pokemon1.Moves[moveNumber - 1].accuracy == 101:
            beatStatus = True
            if pokemon1.recharge == 1:
                beatStatus = False
                pokemon1.recharge = 0
                print(pokemon1.pokemonName + " must recharge!")
            elif pokemon1.status == "Freeze":
                unthaw = randint(1, 5)
                if pokemon1.Moves[moveNumber - 1].moveName in ["Flame Wheel",
                                 "Sacred Fire", "Flare Blitz", "Scald",
                                 "Steam Eruption", "Burn Up", "Pyro Ball",
                                 "Scorching Sands"] or self.weather[0] == "Sunny Day":
                    pokemon1.changeStatus("Healthy")
                    print(pokemon1.pokemonName + " used " + pokemon1.Moves[moveNumber -1].moveName +
                          " and thawed itself out!")
                elif unthaw != 1:
                    beatStatus = False
                    print(pokemon1.pokemonName + " is frozen solid!")
                else:
                    pokemon1.changeStatus("Healthy")
                    print(pokemon1.pokemonName + " thawed out!")
            elif pokemon1.status == "Paralyze":
                fullyPara = randint(1, 4)
                if fullyPara == 1:
                    beatStatus = False
                    print(pokemon1.pokemonName + " is fully paralyzed!")
            elif pokemon1.status == "Sleep":
                if pokemon1.sleepCounter == 0:
                    beatStatus = False
                    pokemon1.sleepCounter = 1
                    print(pokemon1.pokemonName + " is fast asleep!")
                else:
                    wakeUp = randint(1, (7 - pokemon1.sleepCounter))
                    if wakeUp == 1:
                        pokemon1.changeStatus("Healthy")
                        print(pokemon1.pokemonName + " woke up!")
                    else:
                        beatStatus = False
                        pokemon1.sleepCounter += 1
                        print(pokemon1.pokemonName + " is fast asleep!")
            elif pokemon1.status == "Rest":
                if pokemon1.sleepCounter == 2:
                    pokemon1.changeStatus("Healthy")
                    print(pokemon1.pokemonName + " woke up!")
                else:
                    beatStatus = False
                    pokemon1.sleepCounter += 1
                    print(pokemon1.pokemonName + " is fast asleep!")
            
            if beatStatus:
                if pokemon1.volatile["Flinch"] == 1:
                    if pokemon1.Stats["Speed"] * pokemon1.statModifier["Speed"] < pokemon2.Stats["Speed"] * pokemon2.statModifier["Speed"] or priority1 < priority2:
                        beatStatus = False
                        print(pokemon1.pokemonName + " flinched!")
                        pokemon1.recharge = 0
                    pokemon1.volatile["Flinch"] = 0
                if pokemon1.volatile["Confuse"] > 0 and beatStatus:
                    if pokemon1.volatile["Confuse"] == 6:
                        pokemon1.volatile["Confuse"] = 0
                        print(pokemon1.pokemonName + " snapped out of confusion!")
                    elif pokemon1.volatile ["Confuse"] > 1:
                        snapOut = randint(1, 4)
                        if snapOut == 1:
                            pokemon1.volatile["Confuse"] = 0
                            print(pokemon1.pokemonName + " snapped out of confusion!")
                        else:
                            pokemon1.volatile["Confuse"] += 1
                            print(pokemon1.pokemonName + " is confused!")
                            hitSelf = randint(1, 3)
                            if hitSelf == 1:
                                beatStatus = False
                                print(pokemon1.pokemonName + " hit themself in confusion!")
                                damage = floor((floor(floor(floor(((2 * pokemon1.Level) / 5) + 2) 
                                * 40 * (pokemon1.Stats["Attack"]/pokemon1.Stats["Defense"])) / 50) + 2) 
                                * (pokemon1.statModifier["Attack"] / pokemon1.statModifier["Defense"] * (randint(85, 100) / 100)))
                                pokemon1.currentHp -= damage
                                pokemon1.recharge = 0
                    else:
                        pokemon1.volatile["Confuse"] += 1
                        print(pokemon1.pokemonName + " is confused!")
                        hitSelf = randint(1, 3)
                        if hitSelf == 1:
                            beatStatus = False
                            print(pokemon1.pokemonName + " hit themself in confusion!")
                            damage = floor((floor(floor(floor(((2 * pokemon1.Level) / 5) + 2) 
                            * 40 * (pokemon1.Stats["Attack"]/pokemon1.Stats["Defense"])) / 50) + 2) 
                            * (pokemon1.statModifier["Attack"] / pokemon1.statModifier["Defense"] * (randint(85, 100) / 100)))
                            pokemon1.currentHp -= damage
                            pokemon1.recharge = 0
                if pokemon1.Moves[moveNumber - 1].charge == "Charge" and pokemon1.recharge == 0 and beatStatus:
                    if not (pokemon1.Moves[moveNumber - 1].moveName in ["Solar Beam", "Solar Blade"] and self.weather[0] == "Sunny Day"):
                        pokemon1.recharge = -1
                        pokemon1.chargeMove = moveNumber - 1
                        print(pokemon1.pokemonName + " is preparing a " + pokemon1.Moves[moveNumber - 1].moveName + "!")
                        if pokemon1.Moves[moveNumber - 1].stat == "Intangible":
                            pokemon1.intangibility = True
                            pokemon1.volatile["Intangible"] = pokemon1.Moves[moveNumber - 1].moveName
                        if pokemon1.item.itemName == "Power Herb" and not pokemon1.item.consumed:
                            pokemon1.recharge = 0
                            pokemon1.intangibility = False
                            pokemon1.volatile["Intangible"] = " "
                            pokemon1.item.Consume()
                            print(pokemon1.pokemonName + "'s Power Herb instantly charged up the attack!")
                        else:
                            beatStatus = False
            else:
                pokemon1.recharge = 0
                    
            if pokemon2.intangibility:
                secondaryList = ["Failure"]
            elif pokemon1.turnOut > 1 and pokemon1.Moves[moveNumber - 1].moveName == "Fake Out":
                print("Fake Out only works on the first turn out!")
            else:
                secondaryList = pokemon1.Moves[moveNumber - 1].Secondary()
                if secondaryList[0] == "Failure" and pokemon1.Moves[moveNumber - 1].moveName in ["Fire Fang", "Ice Fang", "Thunder Fang"]:
                    fangFlinch = randint(1, 10)
                    if fangFlinch == 1:
                        secondaryList = ["Volatile", "Flinch", "Opponent", 1]
            
            if beatStatus:
                if pokemon1.item.secondEffect == "Block" and "Choice" in pokemon1.item.itemName and not pokemon1.item.consumed:
                    blockedMoves = [5]
                    for number in range(4):
                        if number + 1 != moveNumber:
                            blockedMoves.append(number + 1)
                    pokemon1.volatile["Blocked Moves"] = blockedMoves
                
                if not pokemon1.chargeMove is None:
                    pokemon1.Moves[pokemon1.chargeMove].currentPP -= 1
                    print(pokemon1.pokemonName + " used " + pokemon1.Moves[pokemon1.chargeMove].moveName + "!")
                    pokemon1.chargeMove = None
                    pokemon1.recharge = 0
                else:
                    pokemon1.Moves[moveNumber - 1].currentPP -= 1
                    print(pokemon1.pokemonName + " used " + pokemon1.Moves[moveNumber - 1].moveName + "!")
                    pokemon1.volatile["Intangible"] = " "
                if pokemon1.Moves[moveNumber - 1].stat == "Protect":
                    pokemon1.intangibility = True
                    pokemon1.volatile["Intangible"] = "Protect"
                else:
                    pokemon1.intangibility = False
                if secondaryList[0] == "Stat":
                    if secondaryList[2] == "Self":
                        if pokemon1.Moves[moveNumber - 1].moveName == "Teleport" and attackingTeam.alivePokemon > 1:
                            if not computer:
                                attackingTeam.showTeam()
                                position = int(input("\nWho would you like to switch to? "))
                            else:
                                position = randint(1, 6)
                                while attackingTeam.pokemonList[position - 1].currentHp == 0:
                                    position = randint(1, 6)
                            attackingTeam.Switch(position)
                        elif pokemon1.Moves[moveNumber - 1].moveName == "Growth" and self.weather[0] == "Sunny Day":
                            pokemon1.modifyStat("Attack/Special Attack", "2/2")
                        else:
                            pokemon1.modifyStat(secondaryList[1], secondaryList[3])
                    else:
                        if not pokemon2.intangibility and not (pokemon2.volatile["Substitute"] > 0  and not pokemon1.Moves[moveNumber - 1].sound):
                            if typeEffect > 0 or pokemon1.Moves[moveNumber - 1].power == 0:
                                if pokemon1.Moves[moveNumber - 1].moveName == "Transform" and not (pokemon1.transformed or pokemon2.transformed):
                                    pokemon1.tempPokemon = [pokemon1.Stats, pokemon1.Type1, pokemon1.Type2, pokemon1.Moves]
                                    pokemon1.Stats = pokemon2.Stats
                                    pokemon1.Type1 = pokemon2.Type1
                                    pokemon1.Type2 = pokemon2.Type2
                                    pokemon1.Moves = copy.deepcopy(pokemon2.Moves)
                                    for movePP in range(4):
                                        pokemon1.Moves[movePP].currentPP = 5
                                    pokemon1.transformed = True
                                    print(pokemon1.pokemonName + " transformed into " + pokemon2.pokemonName + "!")
                                else:
                                    pokemon2.modifyStat(secondaryList[1], secondaryList[3])
                                    if pokemon1.Moves[moveNumber - 1].moveName == "Parting Shot" and attackingTeam.alivePokemon > 1:
                                        if not computer:
                                            attackingTeam.showTeam()
                                            position = int(input("\nWho would you like to switch to? "))
                                        else:
                                            position = randint(1, 6)
                                            while attackingTeam.pokemonList[position - 1].currentHp == 0:
                                                position = randint(1, 6)
                                        attackingTeam.Switch(position)
                elif secondaryList[0] == "Status":
                    if secondaryList[2] == "Self":
                        if pokemon1.status == "Healthy" or pokemon1.Moves[moveNumber - 1].moveName in ["Refresh", "Rest"]:
                            pokemon1.changeStatus(secondaryList[1])
                    else:
                        if not pokemon2.intangibility and not (pokemon2.volatile["Substitute"] > 0  and not pokemon1.Moves[moveNumber - 1].sound):
                            if typeEffect > 0 or pokemon1.Moves[moveNumber - 1].power == 0:
                                if pokemon2.status == "Healthy":
                                    pokemon2.changeStatus(secondaryList[1])
                elif secondaryList[0] == "Volatile":
                    if secondaryList[2] == "Self":
                        if pokemon1.volatile[secondaryList[1]] == 0:
                            pokemon1.changeStatus(secondaryList[1])
                    else:
                        if not pokemon2.intangibility and not (pokemon2.volatile["Substitute"] > 0  and not pokemon1.Moves[moveNumber - 1].sound):
                            if typeEffect > 0 or pokemon1.Moves[moveNumber - 1].power == 0:
                                if pokemon2.volatile[secondaryList[1]] == 0:
                                    pokemon2.changeStatus(secondaryList[1])
                elif pokemon1.Moves[moveNumber - 1].moveName == "Substitute" and pokemon1.volatile["Substitute"] >= 0:
                    pokemon1.volatile["Substitute"] = floor(pokemon1.Stats["HP"] * 0.25)
                elif pokemon1.Moves[moveNumber - 1].moveName == "Reflect" and attackingTeam.reflect == 0:
                    attackingTeam.reflect = 5
                elif pokemon1.Moves[moveNumber - 1].moveName == "Light Screen" and attackingTeam.lightScreen == 0:
                    attackingTeam.lightScreen = 5
                elif pokemon1.Moves[moveNumber - 1].stat == "Weather":
                    if self.weather[0] != pokemon1.Moves[moveNumber - 1].moveName:
                        self.weather = [pokemon1.Moves[moveNumber - 1].moveName, 5]
                        if self.weather[0] == "Rain Dance":
                            print("It started to rain!")
                        elif self.weather[0] == "Sunny Day":
                            print("The sunlight turned harsh!")
                        elif self.weather[0] == "Hail":
                            print("It started to hail!")
                        elif self.weather[0] == "Sandstorm":
                            print("A sandstorm kicked up!")
                
                if pokemon1.Moves[moveNumber - 1].power == 0:
                    if pokemon1.Moves[moveNumber - 1].moveName in ["Moonlight", "Synthesis", "Morning Sun"]:
                        if self.weather[0] in ["Hail", "Rain Dance", "Sandstorm"]:
                            weatherShift = .5
                        elif self.weather[0] == "Sunny Day":
                            weatherShift = 4/3
                        else:
                            weatherShift = 1
                    elif pokemon1.Moves[moveNumber - 1].moveName == "Shore Up" and self.weather == "Sandstorm":
                        weatherShift = 4/3
                    else:
                        weatherShift = 1
                    healDamage = floor(pokemon1.Moves[moveNumber - 1].healing * pokemon1.Stats["HP"] * weatherShift)
                elif pokemon1.Moves[moveNumber - 1].moveName == "Struggle":
                    if pokemon2.intangibility:
                        print(pokemon2.pokemonName + " is in an intangible state!")
                        healDamage = 0
                    else:
                        healDamage = (-1) * floor(pokemon1.Stats["HP"] / 4)
                else:
                    if pokemon2.intangibility and not (pokemon1.Moves[moveNumber - 1].moveName in ["Earthquake", "Magnitude", "Surf", "Whirlpool", "Twister", "Gust", "Thunder", "Hurricane", "Sky Uppercut"] or pokemon1.Moves[moveNumber - 1].feint):
                        print(pokemon2.pokemonName + " is in an intangible state!")
                        healDamage = 0
                    elif typeEffect > 0:
                        if (pokemon1.Moves[moveNumber - 1].moveName in ["Earthquake", "Magnitude", "Surf", "Whirlpool", "Twister", "Gust", "Thunder", "Hurricane", "Sky Uppercut"] or pokemon1.Moves[moveNumber - 1].feint) and pokemon2.intangibility:
                            if pokemon1.Moves[moveNumber - 1].moveName in ["Earthquake", "Magnitude"] and pokemon2.volatile["Intangible"] == "Dig":
                                damage *= 2
                            elif pokemon1.Moves[moveNumber - 1].moveName in ["Surf", "Whirlpool"] and pokemon2.volatile["Intangible"] == "Dive":
                                damage *= 2
                            elif pokemon1.Moves[moveNumber - 1].moveName in ["Twister", "Gust"] and pokemon2.volatile["Intangible"] == "Fly":
                                damage *= 2
                            elif pokemon1.Moves[moveNumber - 1].moveName in ["Thunder", "Hurricane", "Sky Uppercut"] and pokemon2.volatile["Intangible"] == "Fly":
                                damage *= 1
                            elif pokemon1.Moves[moveNumber - 1].feint and pokemon2.volatile["Intangible"] == "Protect":
                                print(pokemon2.pokemonName + " couldn't protect itself!")
                            else:
                                print(pokemon2.pokemonName + " is in an intangible state!")
                                healDamage = 0
                                damage = 0
                        elif pokemon1.Moves[moveNumber - 1].stat == "OHKO":
                            damage = pokemon2.Stats["HP"]
                        if defendingTeam.reflect > 0 and pokemon1.Moves[moveNumber - 1].phySpe == "Physical" and pokemon1.Moves[moveNumber - 1].moveName != "Seismic Toss":
                            damage *= .5
                        elif defendingTeam.lightScreen > 0 and pokemon1.Moves[moveNumber - 1].phySpe == "Special" and pokemon1.Moves[moveNumber - 1].moveName not in ["Dragon Rage", "Night Shade", "Sonic Boom"]:
                            damage *= .5
                        hits = randint(int(pokemon1.Moves[moveNumber - 1].hitTimes[0]), int(pokemon1.Moves[moveNumber - 1].hitTimes[1]))
                        for attackHits in range(hits):
                            if pokemon1.Moves[moveNumber - 1].moveName in ["Brick Break", "Psychic Fangs"] and typeEffect > 0:
                                defendingTeam.lightScreen = 0
                                defendingTeam.reflect = 0
                            if pokemon2.volatile["Substitute"] <= 0 or pokemon1.Moves[moveNumber - 1].sound:
                                crit = randint(1, 24)
                                if crit <= 1 * pokemon1.Moves[moveNumber - 1].crit:
                                    if pokemon1.Moves[moveNumber - 1].phySpe == "Physical" or pokemon1.Moves[moveNumber].moveName in ["Secret Sword", "Psyshock", "Psystrike"]:
                                        if pokemon2.statModifier["Defense"] > 1:
                                            defMod = pokemon2.statModifier["Defense"]
                                        else:
                                            defMod = 1
                                    else:
                                        if pokemon2.statModifier["Special Defense"] > 1:
                                            defMod = pokemon2.statModifier["Special Defense"]
                                        else:
                                            defMod = 1
                                    if pokemon1.Moves[moveNumber - 1].phySpe == "Physical":
                                        if pokemon1.statModifier["Attack"] < 1:
                                            attMod = pokemon1.statModifier["Attack"]
                                        else:
                                            attMod = 1
                                    else:
                                        if pokemon1.statModifier["Special Attack"] < 1:
                                            attMod = pokemon1.statModifier["Special Attack"]
                                        else:
                                            attMod = 1
                                    pokemon2.currentHp -= int(damage * 1.5 * defMod / attMod)
                                    print("Critical hit!")
                                    healDamage = ceil(damage * 1.5 * pokemon1.Moves[moveNumber - 1].healing)
                                else:
                                    pokemon2.currentHp -= int(damage)
                                    healDamage = ceil(damage * pokemon1.Moves[moveNumber - 1].healing)
                            else:
                                crit = randint(1, 24)
                                if crit <= 1 * pokemon1.Moves[moveNumber - 1].crit:
                                    if pokemon1.Moves[moveNumber - 1].phySpe == "Physical" or pokemon1.Moves[moveNumber].moveName in ["Secret Sword", "Psyshock", "Psystrike"]:
                                        if pokemon2.statModifier["Defense"] > 1:
                                            defMod = pokemon2.statModifier["Defense"]
                                        else:
                                            defMod = 1
                                    else:
                                        if pokemon2.statModifier["Special Defense"] > 1:
                                            defMod = pokemon2.statModifier["Special Defense"]
                                        else:
                                            defMod = 1
                                    if pokemon1.Moves[moveNumber - 1].phySpe == "Physical":
                                        if pokemon1.statModifier["Attack"] < 1:
                                            attMod = pokemon1.statModifier["Attack"]
                                        else:
                                            attMod = 1
                                    else:
                                        if pokemon1.statModifier["Special Attack"] < 1:
                                            attMod = pokemon1.statModifier["Special Attack"]
                                        else:
                                            attMod = 1
                                    pokemon2.volatile["Substitute"] -= int(damage * 1.5 * defMod / attMod)
                                    print("Critical hit!")
                                    healDamage = ceil(damage * 1.5 * pokemon1.Moves[moveNumber - 1].healing)
                                else:
                                    pokemon2.volatile["Substitute"] -= int(damage)
                                    healDamage = ceil(damage * pokemon1.Moves[moveNumber - 1].healing)
                                if floor(pokemon2.volatile["Substitute"]) <= 0:
                                    pokemon2.volatile["Substitute"] = 0
                                    print(pokemon2.pokemonName + "'s substitute broke!")
                        if hits > 1:
                            print("Hit " + str(hits) + " times!")
                
                if pokemon1.Moves[moveNumber - 1].power > 0:
                    if typeEffect == 0:
                        print("It had no effect...")
                        healDamage = 0
                    else:
                        if pokemon1.Moves[moveNumber - 1].charge == "Recharge":
                            pokemon1.recharge = 1
                        if typeEffect < 1:
                            print("It was not very effective.")
                        elif typeEffect > 1:
                            print("It was super effective!")
                        if pokemon1.Moves[moveNumber - 1].moveName in ["Volt Switch", "U-turn", "Flip Turn"] and attackingTeam.alivePokemon > 1:
                            if not computer:
                                attackingTeam.showTeam()
                                position = int(input("\nWho would you like to switch to? "))
                            else:
                                position = randint(1, 6)
                                while attackingTeam.pokemonList[position - 1].currentHp == 0 or attackingTeam.pokemonList[position - 1] == pokemon1:
                                    position = randint(1, 6)
                            attackingTeam.Switch(position)
                
                if healDamage > 0:
                    print(pokemon1.pokemonName + " had its health restored!")
                elif healDamage < 0:
                    print(pokemon1.pokemonName + " was hit in recoil!")
                
                pokemon1.currentHp += healDamage
        else:
            if not pokemon1.chargeMove is None:
                pokemon1.Moves[pokemon1.chargeMove].currentPP -= 1
                print(pokemon1.pokemonName + " used " + pokemon1.Moves[pokemon1.chargeMove].moveName + "!")
                pokemon1.chargeMove = None
            else:
                pokemon1.Moves[moveNumber - 1].currentPP -= 1
                print(pokemon1.pokemonName + " used " + pokemon1.Moves[moveNumber - 1].moveName + "!")
            print("The attack missed!")
            
        if pokemon1.Moves[moveNumber - 1].currentPP <= 0 and str(pokemon1.item) == "Leppa Berry" and not pokemon1.item.consumed:
            pokemon1.item.Consume()
            print(pokemon1.pokemonName + " restored PP with its Leppa Berry!")
            if 10 <= pokemon1.Moves[moveNumber - 1].pp:
                pokemon1.Moves[moveNumber - 1].currentPP = 10
            else:
                pokemon1.Moves[moveNumber - 1].currentPP = pokemon1.Moves[moveNumber - 1].pp
            
        if pokemon1.currentHp > pokemon1.Stats["HP"]:
            pokemon1.currentHp = pokemon1.Stats["HP"]
        elif pokemon1.currentHp <= 0:
            pokemon1.currentHp = 0
            pokemon2.volatile["Trap"] = 0
            print(pokemon1.pokemonName + " fainted!")
            attackingTeam.alivePokemon -= 1
            if attackingTeam.alivePokemon > 0:
                 while attackingTeam.activePokemon.currentHp <= 0:
                     if computer:
                        attackingTeam.showTeam()
                        position = int(input("\nWho would you like to switch to? "))
                     else:
                        position = randint(1, 6)
                        while attackingTeam.pokemonList[position - 1].currentHp == 0:
                            position = randint(1, 6)
                     attackingTeam.Switch(position)
        
        if pokemon2.currentHp <= 0:
            pokemon2.currentHp = 0
            pokemon1.volatile["Trap"] = 0
            print(pokemon2.pokemonName + " fainted!") 
            defendingTeam.alivePokemon -= 1
            if defendingTeam.alivePokemon > 0:
                 while defendingTeam.activePokemon.currentHp <= 0:
                     if not computer2:
                            defendingTeam.showTeam()
                            position = int(input("\nWho would you like to switch to? "))
                     else:
                        position = randint(1, 6)
                        while defendingTeam.pokemonList[position - 1].currentHp == 0:
                            position = randint(1, 6)
                     defendingTeam.Switch(position)
                     
        if pokemon2.status in pokemon2.item.effect.split("/") and not pokemon2.item.consumed and "Berry" in pokemon2.item.itemName:
            print(pokemon2.pokemonName + " status was cured by a "+ pokemon2.item.itemName + "!")
            pokemon2.changeStatus("Healthy")
            pokemon2.item.Consume()
        elif pokemon2.volatile["Confuse"] == 1 and "Confuse" in pokemon2.item.effect.split("/") and not pokemon2.item.consumed:
            print(pokemon2.pokemonName + " status was cured by a berry!")
            pokemon2.volatile["Confuse"] = 0
            pokemon2.item.Consume()
        elif pokemon2.status == "Freeze":
            if pokemon1.Moves[moveNumber - 1].moveName in ["Flame Wheel",
                                 "Sacred Fire", "Flare Blitz", "Scald",
                                 "Steam Eruption", "Burn Up", "Pyro Ball",
                                 "Scorching Sands"]:
                    pokemon2.changeStatus("Healthy")
                    print(pokemon1.pokemonName + " used " + pokemon1.Moves[moveNumber -1].moveName +
                          " and thawed " + pokemon2.pokemonName + " out!")
        elif pokemon2.status in ["Rest", "Sleep"]:
            if pokemon1.Moves[moveNumber - 1].moveName == "Wake-Up Slap":
                pokemon2.changeStatus("Healthy")
                print(pokemon2.pokemonName + " was woken up with Wake-Up Slap!")
                     
    def Turn(self, megaDict, megaList, computer = False):
        alive1 = int(self.team1.alivePokemon)
        alive2 = int(self.team2.alivePokemon)
        player1Choice = "nothing"
        player2Choice = "nothing"
        self.team1.activePokemon.turnOut += 1
        self.team2.activePokemon.turnOut += 1
        
        if self.team1.activePokemon.turnOut == 1 and self.team1.activePokemon.item.itemName == "Choice Scarf":
            self.team1.activePokemon.modifyStat("Speed" , "1")
        if self.team2.activePokemon.turnOut == 1 and self.team2.activePokemon.item.itemName == "Choice Scarf":
            self.team2.activePokemon.modifyStat("Speed" , "1")
        
        print("\n" + self.team1.activePokemon.pokemonName + " " + 
              str(self.team1.activePokemon.currentHp) + "/" + 
              str(self.team1.activePokemon.Stats["HP"]) + "\nItem: " +
              str(self.team1.activePokemon.item))
        
        if computer:
            print(self.team2.activePokemon.pokemonName + " " + 
              str(self.team2.activePokemon.currentHp) + "/" + 
              str(self.team2.activePokemon.Stats["HP"]))
        else:    
            print(self.team2.activePokemon.pokemonName + " " + 
              str(self.team2.activePokemon.currentHp) + "/" + 
              str(self.team2.activePokemon.Stats["HP"]) + "\nItem: " +
              str(self.team2.activePokemon.item))
        
        if self.team1.activePokemon.recharge == 0:
            print("\n" + self.team1.activePokemon.pokemonName + "\n")
            self.team1.activePokemon.showMoves()
            if self.team1.activePokemon.volatile["Trap"] > 0:
                player1Choice == "attack"
                willStruggle = True
                for moveNum in range(5):
                    if self.team1.activePokemon.Moves[moveNum].currentPP > 0 and (moveNum + 1) not in self.team1.activePokemon.volatile["Blocked Moves"]:
                        willStruggle = False
                if willStruggle:
                    print(self.team1.activePokemon.pokemonName + " has run out of moves!")
                    team1Move = 5
                    priority1 = 0
                else:
                    team1Move = int(input("Choose a move "))
                    while self.team1.activePokemon.Moves[team1Move - 1].currentPP <= 0 or team1Move in self.team1.activePokemon.volatile["Blocked Moves"]:
                        team1Move = int(input("The move has no PP!\nChoose a Move "))
                    priority1 = self.team1.activePokemon.Moves[team1Move - 1].priority
            else:
                while not player1Choice in ["attack", "switch"]:
                    player1Choice = str(input("Would you like to attack or switch? "))
                    if player1Choice == "switch":
                        priority1 = 6
                        self.team1.showTeam()
                        player1Switch = int(input("Who would you like to switch to? "))
                    elif player1Choice == "attack":
                       willStruggle = True
                       for moveNum in range(5):
                           if self.team1.activePokemon.Moves[moveNum].currentPP > 0 and (moveNum + 1) not in self.team1.activePokemon.volatile["Blocked Moves"]:
                               willStruggle = False
                       if willStruggle:
                           print(self.team1.activePokemon.pokemonName + " has run out of moves!")
                           team1Move = 5
                           priority1 = 0
                       else:
                           team1Move = int(input("Choose a move "))
                           while self.team1.activePokemon.Moves[team1Move - 1].currentPP <= 0 or team1Move in self.team1.activePokemon.volatile["Blocked Moves"]:
                               team1Move = int(input("The move has no PP!\nChoose a Move"))
                           priority1 = self.team1.activePokemon.Moves[team1Move - 1].priority
        elif self.team1.activePokemon.recharge == -1:
            player1Choice = "attack"
            team1Move =  self.team1.activePokemon.chargeMove + 1
            priority1 = 0
        else:
            player1Choice = "attack"
            team1Move = 1
            priority1 = 0
            
        if self.team2.activePokemon.recharge == 0:
            if not computer:
                print("\n" + self.team2.activePokemon.pokemonName + "\n")
                self.team2.activePokemon.showMoves()
                if self.team1.activePokemon.volatile["Trap"] > 0:
                    player2Choice == "attack"
                    team2Move = int(input("Choose a move "))
                    while self.team2.activePokemon.Moves[team2Move - 1].currentPP <= 0 or team2Move in self.team2.activePokemon.volatile["Blocked Moves"]:
                        team2Move = int(input("The move has no PP!\nChoose a Move "))
                    priority2 = self.team2.activePokemon.Moves[team2Move - 1].priority
                else:
                    while not player2Choice in ["attack", "switch"]:
                        player2Choice = str(input("Would you like to attack or switch? "))
                        if player2Choice == "switch":
                            priority2 = 6
                            self.team2.showTeam()
                            player2Switch = int(input("Who would you like to switch to? "))
                        elif player2Choice == "attack":
                            willStruggle = True
                            for moveNum in range(5):
                                if self.team2.activePokemon.Moves[moveNum].currentPP > 0 and (moveNum + 1) not in self.team2.activePokemon.volatile["Blocked Moves"]:
                                    willStruggle = False
                            if willStruggle:
                                print(self.team2.activePokemon.pokemonName + " has run out of moves!")
                                team2Move = 5
                                priority2 = 0
                            else:
                                team2Move = int(input("Choose a move "))
                                while self.team2.activePokemon.Moves[team2Move - 1].currentPP <= 0 or team2Move in self.team2.activePokemon.volatile["Blocked Moves"]:
                                    team2Move = int(input("The move has no PP!\nChoose a Move"))
                                priority2 = self.team2.activePokemon.Moves[team2Move - 1].priority
            else:
                strongestAttack = {5 : -2}
                for attack in range(4):
                    if self.team2.activePokemon.Moves[attack].currentPP > 0 and (attack + 1) not in self.team2.activePokemon.volatile["Blocked Moves"]:
                        aveDamage = 0
                        for i in range(32):
                            damage, unimportant = self.damageCalc(attack + 1, 2)
                            aveDamage += damage
                        aveDamage /= 32
                        strongestAttack[attack + 1] = int(aveDamage/self.team1.activePokemon.Stats["HP"] * 64)
                        if aveDamage > self.team1.activePokemon.currentHp:
                            strongestAttack[attack + 1] *= 3 
                            if self.team2.activePokemon.Moves[attack].priority >= 1:
                                strongestAttack[attack + 1] *= 2
                        if self.team2.activePokemon.Moves[attack].moveName in ["U-turn", "Volt Switch", "Flip Turn"] and self.team2.alivePokemon > 1:
                            strongestAttack[attack + 1] *= 1.5
                        elif self.team2.activePokemon.Moves[attack].charge in ["Charge", "Recharge"] and self.team2.activePokemon.currentHp > .5 * self.team2.activePokemon.Stats["HP"]:
                            strongestAttack[attack + 1] *= .5
                        elif self.team2.activePokemon.Moves[attack].phySpe == "Status":
                            if self.team2.activePokemon.Moves[attack].healing > 0:
                                strongestAttack[attack + 1] = self.team2.activePokemon.Stats["HP"] - self.team2.activePokemon.currentHp
                            elif self.team2.activePokemon.Moves[attack].stat in ["Sleep", "Burn", "Poison", "Badly Poison", "Paralyze"] and self.team1.activePokemon.status == "Healthy" and not (self.team1.activePokemon.Type1.typeName in ["Fire", "Poison", "Electric", "Steel"] or self.team1.activePokemon.Type2.typeName in ["Fire", "Poison", "Electric", "Steel"]) and self.team2.activePokemon.turnOut <= 2:
                                strongestAttack[attack + 1] = (self.team2.activePokemon.Moves[attack].accuracy * self.team2.activePokemon.currentHp / self.team2.activePokemon.Stats["HP"]) / 2
                            elif self.team2.activePokemon.Moves[attack].stat in ["Sleep", "Burn", "Poison", "Badly Poison", "Paralyze"] and not self.team1.activePokemon.status == "Healthy":
                                strongestAttack[attack + 1] = -1
                mostDamage = -2
                for powers in strongestAttack:
                    if strongestAttack[powers] >= mostDamage:
                        mostDamage = strongestAttack[powers]
                        mostPowerfulMove = powers
                team2Move = mostPowerfulMove
                switchChance = randint(1, 4)
                if strongestAttack[powers] < 8 and self.team2.alivePokemon > 1 and switchChance == 1 and self.team2.activePokemon.volatile["Trap"] == 0:
                    player2Choice = "switch"
                    player2SwitchList = []
                    for pokemonSlot in range(6):
                        mostHP = 0
                        for pokemonSlot2 in range(6):
                            if self.team2.pokemonList[pokemonSlot2].currentHp > mostHP and pokemonSlot not in player2SwitchList:
                                mostHP = self.team2.pokemonList[pokemonSlot2].currentHp
                                healthiest = pokemonSlot2
                        player2SwitchList.append(healthiest + 1)
                    count = 0
                    player2Switch = player2SwitchList[0]
                    while self.team2.pokemonList[player2SwitchList[count] - 1] == self.team2.activePokemon or self.team2.pokemonList[player2SwitchList[count] - 1].currentHp <= 0:
                        print(player2Switch[count])
                        player2Switch = player2SwitchList[count]
                        count += 1
                    priority2 = 6
                else:
                    player2Choice = "attack"
                    priority2 = self.team2.activePokemon.Moves[team2Move - 1].priority
        elif self.team2.activePokemon.recharge == -1:
            player2Choice = "attack"
            team2Move =  self.team2.activePokemon.chargeMove + 1
            priority2 = 0
        else:
            player2Choice = "attack"
            team2Move = 1
            priority2 = 0
        
        if self.team1.activePokemon.status == "Paralyze":
            pokemon1Para = .5
        else:
            pokemon1Para = 1
        if self.team2.activePokemon.status == "Paralyze":
            pokemon2Para = .5
        else:
            pokemon2Para = 1
        
        if player1Choice == "switch":
            self.team1.Switch(player1Switch)
        if player2Choice == "switch":
            self.team2.Switch(player2Switch)
        
        if not self.team1.mega:
            self.team1.megaEvolve(megaDict, megaList)
        if not self.team2.mega:
            self.team2.megaEvolve(megaDict, megaList)
        
        if self.team1.activePokemon.Stats["Speed"] * self.team1.activePokemon.statModifier["Speed"] * pokemon1Para > self.team2.activePokemon.Stats["Speed"] * self.team2.activePokemon.statModifier["Speed"] * pokemon2Para and priority1 >= priority2:
            if player1Choice == "attack":
                self.Attack(team1Move, priority1, priority2, 1, False, computer)
            if alive2 == self.team2.alivePokemon:
                if player2Choice == "attack":
                    self.Attack(team2Move, priority2, priority1, 2, computer)
        elif self.team1.activePokemon.Stats["Speed"] * self.team1.activePokemon.statModifier["Speed"] * pokemon1Para < self.team2.activePokemon.Stats["Speed"] * self.team2.activePokemon.statModifier["Speed"] * pokemon2Para and priority1 <= priority2:
            if player2Choice == "attack":
                self.Attack(team2Move, priority2, priority1, 2, computer)
            if alive1 == self.team1.alivePokemon:
                if player1Choice == "attack":
                    self.Attack(team1Move, priority1, priority2, 1, False, computer)
        else:
            if priority1 > priority2:
                speedTie = 1
            elif priority1 < priority2:
                speedTie = 0
            else:
                speedTie = randint(0, 1)
            if speedTie == 0:
                if player2Choice == "attack":
                    self.Attack(team2Move, priority2, priority1, 2, computer)
                if alive1 == self.team1.alivePokemon:
                    if player1Choice == "attack":
                        self.Attack(team1Move, priority1, priority2, 1, False, computer)
            else:
                if player1Choice == "attack":
                    self.Attack(team1Move, priority1, priority2, 1, False, computer)
                if alive2 == self.team2.alivePokemon:
                    if player2Choice == "attack":
                        self.Attack(team2Move, priority2, priority1, 2, computer)
        
        if player1Choice == "attack" and self.team1.activePokemon.intangibility:
            if self.team1.activePokemon.Moves[team1Move - 1].moveName in ["Protect", "Detect"]:
                self.team1.activePokemon.intangibility = False
        if player2Choice == "attack" and self.team2.activePokemon.intangibility:
            if self.team2.activePokemon.Moves[team2Move - 1].moveName in ["Protect", "Detect"]:
                self.team2.activePokemon.intangibility = False
        
        if self.team1.activePokemon.item.effect in ["Heal", "Boost"] and not self.team1.activePokemon.item.consumed:
            if self.team1.activePokemon.item.multiplier == 1.5:
                if self.team1.activePokemon.currentHp < .25 * self.team1.activePokemon.Stats["HP"]:
                    self.team1.activePokemon.modifyStat(self.team1.activePokemon.item.effect2, 1)
                    if self.team1.activePokemon.item.consumable:
                        self.team1.activePokemon.Consume()
                    print(self.team1.activePokemon.pokemonName + " boosted its " + self.team1.activePokemon.item.effect2 + " with its berry!")
            elif self.team1.activePokemon.item.multiplier > 1:
                if self.team1.activePokemon.currentHp < .5 * self.team1.activePokemon.Stats["HP"]:
                    self.team1.activePokemon.currentHp += self.team1.activePokemon.item.multiplier
                    if self.team1.activePokemon.item.consumable:
                        self.team1.activePokemon.item.Consume()
                    print(self.team1.activePokemon.pokemonName + " restored health with its " + self.team1.activePokemon.item.itemName + "!")
            elif self.team1.activePokemon.item.multiplier > .25:
                if self.team1.activePokemon.currentHp < .25 * self.team1.activePokemon.Stats["HP"]:
                    self.team1.activePokemon.currentHp += floor(self.team1.activePokemon.item.multiplier * self.team1.activePokemon.Stats["HP"])
                    if self.team1.activePokemon.item.consumable:
                        self.team1.activePokemon.item.Consume()
                    print(self.team1.activePokemon.pokemonName + " restored health with its " + self.team1.activePokemon.item.itemName + "!")
                    if self.team1.activePokemon.item.secondEffect == self.team1.activePokemon.minusNature:
                        self.team1.activePokemon.changeStatus("Confuse")
            else:
                if self.team1.activePokemon.currentHp < .5 * self.team1.activePokemon.Stats["HP"] or not self.team1.activePokemon.item.consumable:
                    self.team1.activePokemon.currentHp += floor(self.team1.activePokemon.item.multiplier * self.team1.activePokemon.Stats["HP"])
                    if self.team1.activePokemon.item.consumable:
                        self.team1.activePokemon.item.Consume()
                    print(self.team1.activePokemon.pokemonName + " restored health with its " + self.team1.activePokemon.item.itemName + "!")
            if self.team1.activePokemon.currentHp > self.team1.activePokemon.Stats["HP"]:
                self.team1.activePokemon.currentHp = self.team1.activePokemon.Stats["HP"]
            
        if self.team1.activePokemon.status == "Poison":
            if self.team1.activePokemon.volatile["Badly Poison"] > 0:
                self.team1.activePokemon.currentHp -= ceil(self.team1.activePokemon.Stats["HP"] * (1/16) *
                                           self.team1.activePokemon.volatile["Badly Poison"])
                self.team1.activePokemon.volatile["Badly Poison"] += 1
            else:
                self.team1.activePokemon.currentHp -= ceil(self.team1.activePokemon.Stats["HP"] * (1/8))
            print(self.team1.activePokemon.pokemonName + " was hurt by poison!")
        elif self.team1.activePokemon.status == "Burn":
            self.team1.activePokemon.currentHp -= ceil(self.team1.activePokemon.Stats["HP"] * (1/16))
            print(self.team1.activePokemon.pokemonName + " was hurt by its burn!")
        if self.team1.activePokemon.volatile["Trap"] != 0:
            self.team1.activePokemon.currentHp -= floor(self.team1.activePokemon.Stats["HP"] * (1/8))
            self.team1.activePokemon.volatile["Trap"] -= 1
            print(self.team1.activePokemon.pokemonName + " was hurt by the opponent's trap!")
        
        if self.team2.activePokemon.status == "Poison":
            if self.team2.activePokemon.volatile["Badly Poison"] > 0:
                self.team2.activePokemon.currentHp -= ceil(self.team2.activePokemon.Stats["HP"] * (1/16) *
                                           self.team2.activePokemon.volatile["Badly Poison"])
                self.team2.activePokemon.volatile["Badly Poison"] += 1
            else:
                self.team2.activePokemon.currentHp -= ceil(self.team2.activePokemon.Stats["HP"] * (1/8))
            print(self.team2.activePokemon.pokemonName + " was hurt by poison!")
        elif self.team2.activePokemon.status == "Burn":
            self.team2.activePokemon.currentHp -= ceil(self.team2.activePokemon.Stats["HP"] * (1/16))
            print(self.team2.activePokemon.pokemonName + " was hurt by its burn!")
        if self.team2.activePokemon.volatile["Trap"] != 0:
            self.team2.activePokemon.currentHp -= floor(self.team2.activePokemon.Stats["HP"] * (1/8))
            self.team2.activePokemon.volatile["Trap"] -= 1
            print(self.team2.activePokemon.pokemonName + " was hurt by the opponent's trap!")
        
        if self.weather[0] != "Clear":
            self.weather[1] -= 1
            if self.weather[1] > 0:
                if self.weather[0] == "Hail" and not (self.team1.activePokemon.Type1.typeName == "Ice" or self.team1.activePokemon.Type2.typeName == "Ice"):
                    self.team1.activePokemon.currentHp -= int(self.team1.activePokemon.Stats["HP"] / 16)
                    print(self.team1.activePokemon.pokemonName + " was buffeted by Hail!")
                if self.weather[0] == "Hail" and not (self.team1.activePokemon.Type2.typeName == "Ice" or self.team2.activePokemon.Type2.typeName == "Ice"):
                    self.team2.activePokemon.currentHp -= int(self.team2.activePokemon.Stats["HP"] / 16)
                    print(self.team2.activePokemon.pokemonName + " was buffeted by Hail!")
                if self.weather[0] == "Sandstorm" and not (self.team1.activePokemon.Type1.typeName in ["Rock", "Steel", "Ground"] or self.team1.activePokemon.Type2.typeName in ["Rock", "Steel", "Ground"]):
                    self.team1.activePokemon.currentHp -= int(self.team1.activePokemon.Stats["HP"] / 16)
                    print(self.team1.activePokemon.pokemonName + " was buffeted by Sandstorm!")
                if self.weather[0] == "Sandstorm" and not (self.team1.activePokemon.Type2.typeName in ["Rock", "Steel", "Ground"] or self.team2.activePokemon.Type2.typeName in ["Rock", "Steel", "Ground"]):
                    self.team2.activePokemon.currentHp -= int(self.team2.activePokemon.Stats["HP"] / 16)
                    print(self.team2.activePokemon.pokemonName + " was buffeted by Sandstorm!")
            else:
                self.weather[0] = "Clear"
                print("The weather cleared up!")
        
        if self.team1.activePokemon.currentHp <= 0:
            if self.team1.alivePokemon > 0:
                self.team1.activePokemon.currentHp = 0
                print(self.team1.activePokemon.pokemonName + " fainted!")
                self.team1.alivePokemon -= 1
                if self.team1.alivePokemon > 0:
                    self.team1.showTeam()
                    while self.team1.activePokemon.currentHp <= 0:
                        position = int(input("\nWho would you like to switch to? "))
                        self.team1.Switch(position)
        
        if self.team2.activePokemon.currentHp <= 0:
            if self.team2.alivePokemon > 0:
                self.team2.activePokemon.currentHp = 0
                print(self.team2.activePokemon.pokemonName + " fainted!") 
                self.team2.alivePokemon -= 1
                if self.team2.alivePokemon > 0:
                    while self.team2.activePokemon.currentHp <= 0:
                         if not computer:
                             self.team2.showTeam()
                             position = int(input("\nWho would you like to switch to? "))
                         else:
                            position = randint(1, 6)
                            while self.team2.pokemonList[position - 1].currentHp == 0:
                                position = randint(1, 6)
                         self.team2.Switch(position)
                         
        if self.team1.reflect > 0:
            self.team1.reflect -= 1
            if self.team1.reflect == 0:
                print("Your Reflect wore off!")
        if self.team2.reflect > 0:
            self.team2.reflect -= 1
            if self.team2.reflect == 0:
                print("The opponent's Reflect wore off!")
        if self.team1.lightScreen > 0:
            self.team1.lightScreen -= 1
            if self.team1.lightScreen == 0:
                print("Your Light Screen wore off!")
        if self.team2.lightScreen > 0:
            self.team2.lightScreen -= 1
            if self.team2.lightScreen == 0:
                print("The opponent's Light Screen wore off!")
            
        
def Pokedex():
    infile = pd.read_excel('Pokemon Simulator Stats.xlsx', 'Sheet1')
    
    pokedexDict = {}
    pokemonName = []
    pokemonType1 = []
    pokemonType2 = []
    pokemonHp = []
    pokemonAt = []
    pokemonDe = []
    pokemonSa = []
    pokemonSd = []
    pokemonSp = []
    
    for strName in infile["Name"]:
        pokemonName.append(strName)
        
    for strType1 in infile["Type 1"]:
        pokemonType1.append(strType1)
        
    for strType2 in infile["Type 2"]:
        pokemonType2.append(strType2)
    
    for intHP in infile["HP"]:
        pokemonHp.append(int(intHP))
        
    for intAt in infile["Attack"]:
        pokemonAt.append(int(intAt))
        
    for intDe in infile["Defense"]:
        pokemonDe.append(int(intDe))
        
    for intSa in infile["Special Attack"]:
        pokemonSa.append(int(intSa))
        
    for intSd in infile["Special Defense"]:
        pokemonSd.append(int(intSd))
        
    for intSp in infile["Speed"]:
        pokemonSp.append(int(intSp))
        
    for pokemonNum in range(len(pokemonName)):
        pokemonObj = Pokemon(pokemonName[pokemonNum], pokemonType1[pokemonNum], pokemonType2[pokemonNum])
        pokemonObj.setBaseStat("HP", pokemonHp[pokemonNum])
        pokemonObj.setBaseStat("Attack", pokemonAt[pokemonNum])
        pokemonObj.setBaseStat("Defense", pokemonDe[pokemonNum])
        pokemonObj.setBaseStat("Special Attack", pokemonSa[pokemonNum])
        pokemonObj.setBaseStat("Special Defense", pokemonSd[pokemonNum])
        pokemonObj.setBaseStat("Speed", pokemonSp[pokemonNum])
        pokedexDict[pokemonName[pokemonNum]] = pokemonObj
        
    return pokedexDict, pokemonName

def MoveList():
    infile = pd.read_excel('Pokemon Simulator Stats.xlsx', 'Sheet2')
    
    moveDict = {}
    moveName = []
    moveType = []
    movePower = []
    moveAccuracy = []
    movePP = []
    movePhySpe = []
    moveHealing = []
    moveChance = []
    moveStat = []
    moveTarget = []
    moveStages = []
    moveHitTimes = []
    movePriority = []
    moveCharge = []
    moveCrit = []
    moveSound = []
    moveFeint = []
    
    for strName in infile["Move"]:
        moveName.append(strName)
        
    for strType in infile["Type"]:
        moveType.append(strType)
    
    for intPower in infile["Power"]:
        movePower.append(int(intPower))
        
    for intAccuracy in infile["Accuracy"]:
        moveAccuracy.append(int(intAccuracy))
        
    for intPP in infile["PP"]:
        movePP.append(int(intPP))
        
    for strPhySpec in infile["Physical"]:
        movePhySpe.append(strPhySpec)
        
    for floatHealing in infile["Healing"]:
        moveHealing.append(round(float(floatHealing), 2))
        
    for intChance in infile["Secondary Chance"]:
        moveChance.append(int(intChance))
        
    for strStat in infile["Stat"]:
        moveStat.append(strStat)
    
    for strTarget in infile["Target"]:
        moveTarget.append(strTarget)
        
    for strStages in infile["Stages"]:
        moveStages.append(str(strStages))
        
    for strHits in infile["Hit Times"]:
        moveHitTimes.append(str(strHits))
    
    for intPriority in infile["Priority"]:
        movePriority.append(int(intPriority))
        
    for strCharge in infile["Charge"]:
        moveCharge.append(strCharge)
        
    for strCrit in infile["Crit"]:
        moveCrit.append(strCrit)
        
    for boolSound in infile["Sound"]:
        moveSound.append(bool(boolSound))
        
    for boolFeint in infile["Feint"]:
        moveFeint.append(bool(boolFeint))
    
    struggleRemoved = False
    
    for move in range(len(moveName)):
        if struggleRemoved:
            moveDict[moveName[move - 1]] = Move(moveName[move - 1], moveType[move - 1], 
                    movePower[move - 1], moveAccuracy[move - 1], movePP[move - 1], 
                    movePhySpe[move - 1], moveHealing[move - 1], moveChance[move - 1], 
                    moveStat[move - 1], moveTarget[move - 1], moveStages[move - 1], 
                    moveHitTimes[move - 1], movePriority[move - 1], 
                    moveCharge[move - 1], moveCrit[move - 1], moveSound[move - 1], 
                    moveFeint[move - 1])
        elif moveName[move] == "Struggle":
            struggle = Move(moveName[move], moveType[move], movePower[move],
                moveAccuracy[move], movePP[move], movePhySpe[move], 
                moveHealing[move], moveChance[move], moveStat[move], 
                moveTarget[move], moveStages[move], moveHitTimes[move], 
                movePriority[move], moveCharge[move], moveCrit[move], 
                moveSound[move], moveFeint[move])
            moveName.pop(move)
            moveType.pop(move)
            movePower.pop(move)
            moveAccuracy.pop(move)
            movePP.pop(move)
            movePhySpe.pop(move)
            moveHealing.pop(move)
            moveChance.pop(move)
            moveStat.pop(move)
            moveTarget.pop(move)
            moveStages.pop(move)
            moveHitTimes.pop(move)
            movePriority.pop(move)
            moveCharge.pop(move)
            moveCrit.pop(move)
            moveSound.pop(move)
            moveFeint.pop(move)
            struggleRemoved = True
        else:
            moveDict[moveName[move]] = Move(moveName[move], moveType[move], 
                    movePower[move], moveAccuracy[move], movePP[move], 
                    movePhySpe[move], moveHealing[move], moveChance[move], 
                    moveStat[move], moveTarget[move], moveStages[move], 
                    moveHitTimes[move], movePriority[move], moveCharge[move], 
                    moveCrit[move], moveSound[move], moveFeint[move])
        
    return moveDict, moveName, struggle

def ItemList():
    infile = pd.read_excel('Pokemon Simulator Stats.xlsx', 'Sheet3')
    
    itemDict = {}
    itemSpecialtyDict = {}
    itemName = []
    itemEffect = []
    itemsecondEffect = []
    itemMultiplier = []
    itemConsumable = []
    itemSpecialty = []
    itemNormalName = []
    itemSpecialtyName = []
    itemFling = []
    
    for strName in infile["Item"]:
        itemName.append(strName)
        
    for strEffect in infile["Effect"]:
        itemEffect.append(strEffect)
        
    for strsecondEffect in infile["Second Effect"]:
        itemsecondEffect.append(strsecondEffect)
    
    for floatMultiplier in infile["Multiplier"]:
        itemMultiplier.append(round(floatMultiplier, 4))
        
    for boolConsume in infile["Consumable"]:
        itemConsumable.append(bool(boolConsume))
        
    for strSpecialty in infile["Signature"]:
        itemSpecialty.append(strSpecialty)
        
    for intFling in infile["Fling"]:
        itemFling.append(int(intFling))
    
    for item in range(len(itemName)):
        if itemSpecialty[item] == "False":
            itemDict[itemName[item]] = Item(itemName[item], itemConsumable[item], 
                    itemEffect[item], itemsecondEffect[item], itemMultiplier[item],
                    itemFling[item])
            itemNormalName.append(itemName[item])
        else:
            if itemSpecialty[item] not in itemSpecialtyDict:
                itemSpecialtyDict[itemSpecialty[item]] = {}        
            itemSpecialtyDict[itemSpecialty[item]][itemName[item]] = Item(itemName[item], itemConsumable[item], 
                       itemEffect[item], itemsecondEffect[item], 
                       itemMultiplier[item], itemFling[item])
            itemSpecialtyName.append(itemName[item])
                
    return itemDict, itemSpecialtyDict, itemNormalName, itemSpecialtyName

def Megas(pokemonDict):
    infile = pd.read_excel('Pokemon Simulator Stats.xlsx', 'Sheet4')
    
    pokedexDict = {}
    pokemonName = []
    pokemonLabel = []
    pokemonItem = []
    pokemonType1 = []
    pokemonType2 = []
    pokemonAt = []
    pokemonDe = []
    pokemonSa = []
    pokemonSd = []
    pokemonSp = []
    
    for strName in infile["Pokemon"]:
        pokemonName.append(strName)
        
    for strLabel in infile["Label"]:
        if strLabel == "None":
            pokemonLabel.append("")
        else:
            pokemonLabel.append(" " + strLabel)
            
    for strItem in infile["Item"]:
        pokemonItem.append(strItem)
    
    for strType1 in infile["Type 1"]:
        pokemonType1.append(strType1)
        
    for strType2 in infile["Type 2"]:
        pokemonType2.append(strType2)
        
    for intAt in infile["Attack"]:
        pokemonAt.append(int(intAt))
        
    for intDe in infile["Defense"]:
        pokemonDe.append(int(intDe))
        
    for intSa in infile["Special Attack"]:
        pokemonSa.append(int(intSa))
        
    for intSd in infile["Special Defense"]:
        pokemonSd.append(int(intSd))
        
    for intSp in infile["Speed"]:
        pokemonSp.append(int(intSp))
    
    for pokemonNum in range(len(pokemonName)):
        pokemonObj = Pokemon("Mega " + pokemonName[pokemonNum] + pokemonLabel[pokemonNum], 
                             pokemonType1[pokemonNum], pokemonType2[pokemonNum])
        pokemonObj.setBaseStat("HP", pokemonDict[pokemonName[pokemonNum]].BaseStats["HP"])
        pokemonObj.setBaseStat("Attack", pokemonAt[pokemonNum])
        pokemonObj.setBaseStat("Defense", pokemonDe[pokemonNum])
        pokemonObj.setBaseStat("Special Attack", pokemonSa[pokemonNum])
        pokemonObj.setBaseStat("Special Defense", pokemonSd[pokemonNum])
        pokemonObj.setBaseStat("Speed", pokemonSp[pokemonNum])
        pokedexDict[pokemonName[pokemonNum] + pokemonLabel[pokemonNum]] = [pokemonObj, pokemonItem[pokemonNum]]
        
    return pokedexDict, pokemonName

def test():
    pokemonDict, pokemonList = Pokedex()
    moveDict, moveList, struggle = MoveList()
    itemDict, itemSpecialtyDict, itemNormalName, itemSpecialtyName = ItemList()
    megaDict, megaList = Megas(pokemonDict)
    
    '''pokemon1 = copy.deepcopy(pokemonDict["Charizard"])'''
    pokemon1 = copy.deepcopy(pokemonDict[choice(pokemonList)])
    pokemon1.setStats(50, choice(["Attack", "Defense", "Special Attack", 
                                 "Special Defense", "Speed"]), 
            choice(["Attack", "Defense", "Special Attack", "Special Defense", 
                   "Speed"]), [randint(0,31), randint(0,31), randint(0,31),
                          randint(0,31), randint(0,31), randint(0,31)], 
                   [randint(0, 252), randint(0, 252), randint(0, 252), randint(0, 252),
                    randint(0, 252), randint(0, 252)])
    pokemon1.newMove(copy.deepcopy(moveDict["Fling"]))
    '''pokemon1.newMove(copy.deepcopy(moveDict["Sunny Day"]))'''
    '''pokemon1.newMove(copy.deepcopy(moveDict[choice(moveList)]))'''
    pokemon1.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon1.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon1.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    '''pokemon1.newItem(itemDict["Shuca Berry"])'''
    if pokemon1.pokemonName in itemSpecialtyDict:
        signatureItem = choice(itemSpecialtyName)
        while signatureItem not in itemSpecialtyDict[pokemon1.pokemonName]:
            signatureItem = choice(itemSpecialtyName)
        pokemon1.newItem(copy.deepcopy(itemSpecialtyDict[pokemon1.pokemonName][signatureItem]))
    else:
        pokemon1.newItem(copy.deepcopy(itemDict[choice(itemNormalName)]))
    pokemon1.replaceMove(struggle, 5)
    
    pokemon2 = copy.deepcopy(pokemonDict[choice(pokemonList)])
    pokemon2.setStats(50, choice(["Attack", "Defense", "Special Attack", 
                                 "Special Defense", "Speed"]), 
            choice(["Attack", "Defense", "Special Attack", "Special Defense", 
                   "Speed"]), [randint(0,31), randint(0,31), randint(0,31),
                          randint(0,31), randint(0,31), randint(0,31)], 
                   [randint(0, 252), randint(0, 252), randint(0, 252), randint(0, 252),
                    randint(0, 252), randint(0, 252)])
    '''pokemon2.newMove(copy.deepcopy(moveDict["Hyper Voice"]))'''
    pokemon2.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon2.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon2.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon2.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    if pokemon2.pokemonName in itemSpecialtyDict:
        signatureItem = choice(itemSpecialtyName)
        while signatureItem not in itemSpecialtyDict[pokemon2.pokemonName]:
            signatureItem = choice(itemSpecialtyName)
        pokemon1.newItem(copy.deepcopy(itemSpecialtyDict[pokemon2.pokemonName][signatureItem]))
    else:
        pokemon2.newItem(copy.deepcopy(itemDict[choice(itemNormalName)]))
    pokemon2.replaceMove(struggle, 5)
    
    pokemon3 = copy.deepcopy(pokemonDict[choice(pokemonList)])
    pokemon3.setStats(50, choice(["Attack", "Defense", "Special Attack", 
                                 "Special Defense", "Speed"]), 
            choice(["Attack", "Defense", "Special Attack", "Special Defense", 
                   "Speed"]), [randint(0,31), randint(0,31), randint(0,31),
                          randint(0,31), randint(0,31), randint(0,31)], 
                   [randint(0, 252), randint(0, 252), randint(0, 252), randint(0, 252),
                    randint(0, 252), randint(0, 252)])
    pokemon3.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon3.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon3.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon3.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    if pokemon3.pokemonName in itemSpecialtyDict:
        signatureItem = choice(itemSpecialtyName)
        while signatureItem not in itemSpecialtyDict[pokemon3.pokemonName]:
            signatureItem = choice(itemSpecialtyName)
        pokemon3.newItem(copy.deepcopy(itemSpecialtyDict[pokemon3.pokemonName][signatureItem]))
    else:
        pokemon3.newItem(copy.deepcopy(itemDict[choice(itemNormalName)]))
    pokemon3.replaceMove(struggle, 5)
    
    pokemon4 = copy.deepcopy(pokemonDict[choice(pokemonList)])
    pokemon4.setStats(50, choice(["Attack", "Defense", "Special Attack", 
                                 "Special Defense", "Speed"]), 
            choice(["Attack", "Defense", "Special Attack", "Special Defense", 
                   "Speed"]), [randint(0,31), randint(0,31), randint(0,31),
                          randint(0,31), randint(0,31), randint(0,31)], 
                   [randint(0, 252), randint(0, 252), randint(0, 252), randint(0, 252),
                    randint(0, 252), randint(0, 252)])
    pokemon4.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon4.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon4.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon4.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    if pokemon4.pokemonName in itemSpecialtyDict:
        signatureItem = choice(itemSpecialtyName)
        while signatureItem not in itemSpecialtyDict[pokemon4.pokemonName]:
            signatureItem = choice(itemSpecialtyName)
        pokemon4.newItem(copy.deepcopy(itemSpecialtyDict[pokemon4.pokemonName][signatureItem]))
    else:
        pokemon4.newItem(copy.deepcopy(itemDict[choice(itemNormalName)]))
    pokemon4.replaceMove(struggle, 5)
    
    pokemon5 = copy.deepcopy(pokemonDict[choice(pokemonList)])
    pokemon5.setStats(50, choice(["Attack", "Defense", "Special Attack", 
                                 "Special Defense", "Speed"]), 
            choice(["Attack", "Defense", "Special Attack", "Special Defense", 
                   "Speed"]), [randint(0,31), randint(0,31), randint(0,31),
                          randint(0,31), randint(0,31), randint(0,31)], 
                   [randint(0, 252), randint(0, 252), randint(0, 252), randint(0, 252),
                    randint(0, 252), randint(0, 252)])
    pokemon5.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon5.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon5.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon5.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    if pokemon5.pokemonName in itemSpecialtyDict:
        signatureItem = choice(itemSpecialtyName)
        while signatureItem not in itemSpecialtyDict[pokemon5.pokemonName]:
            signatureItem = choice(itemSpecialtyName)
        pokemon5.newItem(copy.deepcopy(itemSpecialtyDict[pokemon5.pokemonName][signatureItem]))
    else:
        pokemon5.newItem(copy.deepcopy(itemDict[choice(itemNormalName)]))
    pokemon5.replaceMove(struggle, 5)
    
    pokemon6 = copy.deepcopy(pokemonDict[choice(pokemonList)])
    pokemon6.setStats(50, choice(["Attack", "Defense", "Special Attack", 
                                 "Special Defense", "Speed"]), 
            choice(["Attack", "Defense", "Special Attack", "Special Defense", 
                   "Speed"]), [randint(0,31), randint(0,31), randint(0,31),
                          randint(0,31), randint(0,31), randint(0,31)], 
                   [randint(0, 252), randint(0, 252), randint(0, 252), randint(0, 252),
                    randint(0, 252), randint(0, 252)])
    pokemon6.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon6.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon6.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon6.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    if pokemon6.pokemonName in itemSpecialtyDict:
        signatureItem = choice(itemSpecialtyName)
        while signatureItem not in itemSpecialtyDict[pokemon6.pokemonName]:
            signatureItem = choice(itemSpecialtyName)
        pokemon6.newItem(copy.deepcopy(itemSpecialtyDict[pokemon6.pokemonName][signatureItem]))
    else:
        pokemon6.newItem(copy.deepcopy(itemDict[choice(itemNormalName)]))
    pokemon6.replaceMove(struggle, 5)
    
    pokemon7 = copy.deepcopy(pokemonDict[choice(pokemonList)])
    pokemon7.setStats(50, choice(["Attack", "Defense", "Special Attack", 
                                 "Special Defense", "Speed"]), 
            choice(["Attack", "Defense", "Special Attack", "Special Defense", 
                   "Speed"]), [randint(0,31), randint(0,31), randint(0,31),
                          randint(0,31), randint(0,31), randint(0,31)], 
                   [randint(0, 252), randint(0, 252), randint(0, 252), randint(0, 252),
                    randint(0, 252), randint(0, 252)])
    pokemon7.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon7.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon7.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon7.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    if pokemon7.pokemonName in itemSpecialtyDict:
        signatureItem = choice(itemSpecialtyName)
        while signatureItem not in itemSpecialtyDict[pokemon7.pokemonName]:
            signatureItem = choice(itemSpecialtyName)
        pokemon7.newItem(copy.deepcopy(itemSpecialtyDict[pokemon7.pokemonName][signatureItem]))
    else:
        pokemon7.newItem(copy.deepcopy(itemDict[choice(itemNormalName)]))
    pokemon7.replaceMove(struggle, 5)
    
    pokemon8 = copy.deepcopy(pokemonDict[choice(pokemonList)])
    pokemon8.setStats(50, choice(["Attack", "Defense", "Special Attack", 
                                 "Special Defense", "Speed"]), 
            choice(["Attack", "Defense", "Special Attack", "Special Defense", 
                   "Speed"]), [randint(0,31), randint(0,31), randint(0,31),
                          randint(0,31), randint(0,31), randint(0,31)], 
                   [randint(0, 252), randint(0, 252), randint(0, 252), randint(0, 252),
                    randint(0, 252), randint(0, 252)])
    pokemon8.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon8.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon8.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon8.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    if pokemon8.pokemonName in itemSpecialtyDict:
        signatureItem = choice(itemSpecialtyName)
        while signatureItem not in itemSpecialtyDict[pokemon8.pokemonName]:
            signatureItem = choice(itemSpecialtyName)
        pokemon8.newItem(copy.deepcopy(itemSpecialtyDict[pokemon8.pokemonName][signatureItem]))
    else:
        pokemon8.newItem(copy.deepcopy(itemDict[choice(itemNormalName)]))
    pokemon8.replaceMove(struggle, 5)
    
    pokemon9 = copy.deepcopy(pokemonDict[choice(pokemonList)])
    pokemon9.setStats(50, choice(["Attack", "Defense", "Special Attack", 
                                 "Special Defense", "Speed"]), 
            choice(["Attack", "Defense", "Special Attack", "Special Defense", 
                   "Speed"]), [randint(0,31), randint(0,31), randint(0,31),
                          randint(0,31), randint(0,31), randint(0,31)], 
                   [randint(0, 252), randint(0, 252), randint(0, 252), randint(0, 252),
                    randint(0, 252), randint(0, 252)])
    pokemon9.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon9.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon9.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon9.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    if pokemon9.pokemonName in itemSpecialtyDict:
        signatureItem = choice(itemSpecialtyName)
        while signatureItem not in itemSpecialtyDict[pokemon9.pokemonName]:
            signatureItem = choice(itemSpecialtyName)
        pokemon9.newItem(copy.deepcopy(itemSpecialtyDict[pokemon9.pokemonName][signatureItem]))
    else:
        pokemon9.newItem(copy.deepcopy(itemDict[choice(itemNormalName)]))
    pokemon9.replaceMove(struggle, 5)
    
    pokemon10 = copy.deepcopy(pokemonDict[choice(pokemonList)])
    pokemon10.setStats(50, choice(["Attack", "Defense", "Special Attack", 
                                 "Special Defense", "Speed"]), 
            choice(["Attack", "Defense", "Special Attack", "Special Defense", 
                   "Speed"]), [randint(0,31), randint(0,31), randint(0,31),
                          randint(0,31), randint(0,31), randint(0,31)], 
                   [randint(0, 252), randint(0, 252), randint(0, 252), randint(0, 252),
                    randint(0, 252), randint(0, 252)])
    pokemon10.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon10.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon10.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon10.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    if pokemon10.pokemonName in itemSpecialtyDict:
        signatureItem = choice(itemSpecialtyName)
        while signatureItem not in itemSpecialtyDict[pokemon10.pokemonName]:
            signatureItem = choice(itemSpecialtyName)
        pokemon10.newItem(copy.deepcopy(itemSpecialtyDict[pokemon10.pokemonName][signatureItem]))
    else:
        pokemon10.newItem(copy.deepcopy(itemDict[choice(itemNormalName)]))
    pokemon10.replaceMove(struggle, 5)
    
    pokemon11 = copy.deepcopy(pokemonDict[choice(pokemonList)])
    pokemon11.setStats(50, choice(["Attack", "Defense", "Special Attack", 
                                 "Special Defense", "Speed"]), 
            choice(["Attack", "Defense", "Special Attack", "Special Defense", 
                   "Speed"]), [randint(0,31), randint(0,31), randint(0,31),
                          randint(0,31), randint(0,31), randint(0,31)], 
                   [randint(0, 252), randint(0, 252), randint(0, 252), randint(0, 252),
                    randint(0, 252), randint(0, 252)])
    pokemon11.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon11.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon11.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon11.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    if pokemon11.pokemonName in itemSpecialtyDict:
        signatureItem = choice(itemSpecialtyName)
        while signatureItem not in itemSpecialtyDict[pokemon11.pokemonName]:
            signatureItem = choice(itemSpecialtyName)
        pokemon11.newItem(copy.deepcopy(itemSpecialtyDict[pokemon11.pokemonName][signatureItem]))
    else:
        pokemon11.newItem(copy.deepcopy(itemDict[choice(itemNormalName)]))
    pokemon11.replaceMove(struggle, 5)
    
    pokemon12 = copy.deepcopy(pokemonDict[choice(pokemonList)])
    pokemon12.setStats(50, choice(["Attack", "Defense", "Special Attack", 
                                 "Special Defense", "Speed"]), 
            choice(["Attack", "Defense", "Special Attack", "Special Defense", 
                   "Speed"]), [randint(0,31), randint(0,31), randint(0,31),
                          randint(0,31), randint(0,31), randint(0,31)], 
                   [randint(0, 252), randint(0, 252), randint(0, 252), randint(0, 252),
                    randint(0, 252), randint(0, 252)])
    pokemon12.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon12.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon12.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    pokemon12.newMove(copy.deepcopy(moveDict[choice(moveList)]))
    if pokemon12.pokemonName in itemSpecialtyDict:
        signatureItem = choice(itemSpecialtyName)
        while signatureItem not in itemSpecialtyDict[pokemon12.pokemonName]:
            signatureItem = choice(itemSpecialtyName)
        pokemon12.newItem(copy.deepcopy(itemSpecialtyDict[pokemon12.pokemonName][signatureItem]))
    else:
        pokemon12.newItem(copy.deepcopy(itemDict[choice(itemNormalName)]))
    pokemon12.replaceMove(struggle, 5)
    
    testTeam = Team()
    testTeam.addPokemon(pokemon1)
    testTeam.addPokemon(pokemon3)
    testTeam.addPokemon(pokemon5)
    testTeam.addPokemon(pokemon7)
    testTeam.addPokemon(pokemon9)
    testTeam.addPokemon(pokemon11)
    testTeam.showTeam()
    print()
    
    testTeam2 = Team()
    testTeam2.addPokemon(pokemon2)
    testTeam2.addPokemon(pokemon4)
    testTeam2.addPokemon(pokemon6)
    testTeam2.addPokemon(pokemon8)
    testTeam2.addPokemon(pokemon10)
    testTeam2.addPokemon(pokemon12)
    testTeam2.showTeam()
    print()
    
    testBattle = Battle(testTeam, testTeam2)
    testBattle.typeMatchup()
    testBattle.fixType()
    
    while testTeam.alivePokemon > 0 and testTeam2.alivePokemon > 0:
        testBattle.Turn(megaDict, megaList, True)
        if testTeam.alivePokemon == 0:
            print("Team 2 wins!")
        elif testTeam2.alivePokemon == 0:
            print("Team 1 wins!")

test()
