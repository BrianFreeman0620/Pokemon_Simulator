from graphics import Point, Text
from math import floor
from random import choice, randint
import copy

from Item_Pokemon import Item
from Type_Pokemon import Type

# The Pokemon class is the pokemon with all related traits
class Pokemon:
    
    def __init__(self, pokemonName, ability, evolve, mass, typeName1, typeName2 = "None", gender = ["Male"], win = None):
        self.win = win
        
        self.pokemonName = pokemonName
        self.crunchName = "None"
        self.ability = ability
        # Mass is a list with the mass as a float and if the mass
        # can be used in weight related calculations
        self.mass = mass
        self.currentMass = mass[0]
        self.Type1 = Type(typeName1)
        self.Type2 = Type(typeName2)
        # Temporary types are stored if a pokemon's types changes
        self.tempType1 = Type(typeName1)
        self.tempType2 = Type(typeName2)
        # Used for level adjustment when creating pokemon and the item Eviolite
        if evolve == "Yes":
            self.evolve = False
        else:
            self.evolve = True
        
        #4 Moves, Struggle, Temporary Move, Z-Move
        self.Moves = [None, None, None, None, None, None, None]
        self.guaranteedMove = "None"
        # The following are traits that are temporarily set until changed
        # by a later function
        self.Level = 5
        self.BaseStats = {"HP" : 48, "Attack" : 48, "Defense" : 48,
                      "Special Attack": 48, "Special Defense": 48, 
                      "Speed" : 48}
        self.Stats = {"HP" : 20, "Attack" : 10, "Defense" : 10,
                      "Special Attack": 10, "Special Defense": 10, 
                      "Speed" : 10}
        self.IV = [15, 15, 15, 15, 15, 15]
        self.EV = [0, 0, 0, 0, 0, 0]
        self.currentHp = 20
        # Temporary modifiers for speed, damage, and hit chance calculations
        self.statModifier = {"Attack" : 1, "Defense" : 1,
                      "Special Attack": 1, "Special Defense": 1, 
                      "Speed" : 1, "Accuracy": 1, "Evasion": 1}
        # Used in boosting and lowering stats
        self.plusNature = "HP"
        self.minusNature = "HP"
        # The following traits are used to keep track of semipermanent and
        # temporary status inflictions
        self.status = "Healthy"
        self.volatile = {"Flinch" : 0, "Confuse" : 0, "Badly Poison" : 0, "Trap" : 0,
                         "Block Condition" : "None", "Blocked Moves" : [5], 
                         "Intangible" : " ", "Substitute" : 0, "Infatuation" : 0, 
                         "Pumped" : 0, "Perish" : 0, "Drowsy" : 0, "Aqua Ring" : 0}
        self.sleepCounter = 0
        # Initializes an item with no effect
        self.item = Item("None", False, "None", "None", 1, 0)
        self.item.Consume()
        
        self.turnOut = 0
        # The following are used for moves that require multiple turns to use
        self.recharge = 0
        self.chargeMove = None
        # The following are used for checking if a pokemon can be attacked
        self.intangibility = False
        self.intangibleOdds = 1
        # The following are used to store information of a pokemon's current form
        self.transformed = False
        self.tempPokemon = None
        self.currentForm = "Base"
        # The following allows a pokemon to have a gender, or lack one in
        # certain cases
        self.gender = "Male"
        self.genderRatio = gender
        # The following are traits related to specific moves and abilities
        self.hiddenPower = "Dark"
        self.photonGeyser = "Special"
        self.boosterEnergy = [1, None, False]
        self.flashFire = False
        self.protean = False
        self.illusion = True
        self.roosted = False
        self.rageFist = 1
        # Randomly decides if a pokemon is a special color
        shiny = randint(1, 100)
        if shiny == 50:
            self.shiny = True
        else:
            self.shiny = False
    
    # Allows the pokemon to work in the graphics window
    def addToWin(self, win):
        self.win = win
    
    # Writes a string to the graphics window
    def drawCurrentText(self, text):
        self.currentText = Text(Point(250,75), text)
        textSize = int(600/len(text))
        if textSize >= 12:
            textSize = 12
        elif textSize <= 6:
            textSize = 6
        self.currentText.setSize(textSize)
        self.currentText.draw(self.win)
        self.win.getMouse()
        self.currentText.undraw()
    
    # Changes the base stat value
    def setBaseStat(self, statName, baseStat):
        if statName in self.Stats:
            self.BaseStats[statName] = baseStat
    
    # Changes the types and whether the change is permanent
    def changeType(self, newType1, newType2, permanent):
        self.Type1 = Type(newType1)
        self.Type2 = Type(newType2)
        if permanent:
            self.tempType1 = Type(newType1)
            self.tempType2 = Type(newType2)
    
    # If the conditions are met, Mega Evolves a pokemon
    def megaEvolve(self, megaDict, megaList):
        for megaPokemon in megaList:
            if self.pokemonName == megaPokemon:
                tempHp = self.currentHp
                try:
                    # Used for most megas to change the type, ability, and stats
                    if self.item.effect[0] == "Mega" and megaDict[self.pokemonName][1] == self.item.itemName:
                        self.setBaseStat("HP", megaDict[self.pokemonName][0].BaseStats["HP"])
                        self.setBaseStat("Attack", megaDict[self.pokemonName][0].BaseStats["Attack"])
                        self.setBaseStat("Defense", megaDict[self.pokemonName][0].BaseStats["Defense"])
                        self.setBaseStat("Special Attack", megaDict[self.pokemonName][0].BaseStats["Special Attack"])
                        self.setBaseStat("Special Defense", megaDict[self.pokemonName][0].BaseStats["Special Defense"])
                        self.setBaseStat("Speed", megaDict[self.pokemonName][0].BaseStats["Speed"])
                        
                        self.setStats(self.Level, self.plusNature, self.minusNature,
                                      self.IV, self.EV)
                        self.currentHp = tempHp
                        self.changeType(megaDict[self.pokemonName][0].Type1.typeName, megaDict[self.pokemonName][0].Type2.typeName, True)
                        self.ability = megaDict[self.pokemonName][0].ability
                        self.mass = megaDict[self.pokemonName][0].mass
                        self.currentMass = megaDict[self.pokemonName][0].mass[0]
                        
                        self.pokemonName = megaDict[self.pokemonName][0].pokemonName
                        
                        return True
                except:
                    # Used for Mega Charizard X and Mega Mewtwo X
                    if self.item.effect[0] == "Mega" and megaDict[self.pokemonName + " X"][1] == self.item.itemName:
                        self.setBaseStat("HP", megaDict[self.pokemonName + " X"][0].BaseStats["HP"])
                        self.setBaseStat("Attack", megaDict[self.pokemonName + " X"][0].BaseStats["Attack"])
                        self.setBaseStat("Defense", megaDict[self.pokemonName + " X"][0].BaseStats["Defense"])
                        self.setBaseStat("Special Attack", megaDict[self.pokemonName + " X"][0].BaseStats["Special Attack"])
                        self.setBaseStat("Special Defense", megaDict[self.pokemonName + " X"][0].BaseStats["Special Defense"])
                        self.setBaseStat("Speed", megaDict[self.pokemonName + " X"][0].BaseStats["Speed"])
                        
                        self.setStats(self.Level, self.plusNature, self.minusNature,
                                      self.IV, self.EV)
                        self.currentHp = tempHp
                        self.changeType(megaDict[self.pokemonName + " X"][0].Type1.typeName, megaDict[self.pokemonName + " X"][0].Type2.typeName, True)
                        self.ability = megaDict[self.pokemonName + " X"][0].ability
                        self.mass = megaDict[self.pokemonName + " X"][0].mass
                        self.currentMass = megaDict[self.pokemonName + " X"][0].mass[0]
                        
                        self.pokemonName = megaDict[self.pokemonName + " X"][0].pokemonName
                        
                        return True
                    # Used for Mega Charizard Y and Mega Mewtwo Y
                    elif self.item.effect[0] == "Mega" and megaDict[self.pokemonName + " Y"][1] == self.item.itemName:
                        self.setBaseStat("HP", megaDict[self.pokemonName + " Y"][0].BaseStats["HP"])
                        self.setBaseStat("Attack", megaDict[self.pokemonName + " Y"][0].BaseStats["Attack"])
                        self.setBaseStat("Defense", megaDict[self.pokemonName + " Y"][0].BaseStats["Defense"])
                        self.setBaseStat("Special Attack", megaDict[self.pokemonName + " Y"][0].BaseStats["Special Attack"])
                        self.setBaseStat("Special Defense", megaDict[self.pokemonName + " Y"][0].BaseStats["Special Defense"])
                        self.setBaseStat("Speed", megaDict[self.pokemonName + " Y"][0].BaseStats["Speed"])
                        
                        self.setStats(self.Level, self.plusNature, self.minusNature,
                                      self.IV, self.EV)
                        self.currentHp = tempHp
                        self.changeType(megaDict[self.pokemonName + " Y"][0].Type1.typeName, megaDict[self.pokemonName + " Y"][0].Type2.typeName, True)
                        self.ability = megaDict[self.pokemonName + " Y"][0].ability
                        self.mass = megaDict[self.pokemonName + " Y"][0].mass
                        self.currentMass = megaDict[self.pokemonName + " Y"][0].mass[0]
                        
                        self.pokemonName = megaDict[self.pokemonName + " Y"][0].pokemonName
                        
                        return True
            
        return False
    
    # Changes the form of a pokemon
    def changeForm(self, weather, activate = False):
        tempHp = self.currentHp
        # Changes Necrozma to Ultra Necrozma
        if "Ultranecrozium" in self.item.itemName and activate:
            self.setBaseStat("Attack", 167)
            self.setBaseStat("Defense", 97)
            self.setBaseStat("Special Attack", 167)
            self.setBaseStat("Special Defense", 97)
            self.setBaseStat("Speed", 129)
            self.setStats(self.Level, self.plusNature, self.minusNature,
                          self.IV, self.EV)
            self.currentHp = tempHp
            self.changeType("Psychic", "Dragon", True)
            self.pokemonName = "Necrozma (Ultra)"
            self.mass = [230.0, True]
        
        if self.ability.effect[0] == "Specialty":
            # Changes Wishiwashi to a different form depending on remaining HP
            if self.ability.abilityName == "Schooling":
                if self.currentHp <= floor(.25 * self.Stats["HP"]):
                    self.setBaseStat("Attack", 20)
                    self.setBaseStat("Defense", 20)
                    self.setBaseStat("Special Attack", 25)
                    self.setBaseStat("Special Defense", 25)
                    self.setBaseStat("Speed", 40)
                    self.setStats(self.Level, self.plusNature, self.minusNature,
                                  self.IV, self.EV)
                    self.currentHp = tempHp
                    self.pokemonName = "Wishiwashi (Solo)"
                    self.mass = [0.3, True]
                else:
                    self.setBaseStat("Attack", 140)
                    self.setBaseStat("Defense", 130)
                    self.setBaseStat("Special Attack", 140)
                    self.setBaseStat("Special Defense", 135)
                    self.setBaseStat("Speed", 30)
                    self.setStats(self.Level, self.plusNature, self.minusNature,
                                  self.IV, self.EV)
                    self.currentHp = tempHp
                    self.pokemonName = "Wishiwashi (Schooling)"
                    self.mass = [78.6, True]
            elif self.ability.abilityName in ["Power Construct", "Shields Down", "Zen Mode"]:
                if self.currentHp <= floor(.5 * self.Stats["HP"]):
                    # Changes Zygarde to Zygarde Complete
                    if self.ability.abilityName == "Power Construct":
                        self.currentForm = "Complete"
                        currentFullHP = self.Stats["HP"]
                        self.setBaseStat("HP", 216)
                        self.setBaseStat("Attack", 100)
                        self.setBaseStat("Defense", 121)
                        self.setBaseStat("Special Attack", 91)
                        self.setBaseStat("Special Defense", 95)
                        self.setBaseStat("Speed", 85)
                        self.setStats(self.Level, self.plusNature, self.minusNature,
                                      self.IV, self.EV)
                        self.currentHp = int(tempHp * self.Stats["HP"] / currentFullHP)
                        self.pokemonName = "Zygarde (Complete)"
                        self.mass = [610.0, True]
                    # Changes Minior Meteor to Minior Core
                    elif self.ability.abilityName == "Shields Down":
                        self.setBaseStat("Attack", 100)
                        self.setBaseStat("Defense", 60)
                        self.setBaseStat("Special Attack", 100)
                        self.setBaseStat("Special Defense", 60)
                        self.setBaseStat("Speed", 120)
                        self.setStats(self.Level, self.plusNature, self.minusNature,
                                      self.IV, self.EV)
                        self.currentHp = tempHp
                        self.pokemonName = "Minior (Core)"
                        self.mass = [0.3, True]
                    # Changes Darmanitan to its corresponding Zen Mode
                    elif self.ability.abilityName == "Zen Mode":
                        if self.Type1.typeName == "Ice":
                            self.setBaseStat("Attack", 160)
                            self.setBaseStat("Defense", 55)
                            self.setBaseStat("Special Attack", 30)
                            self.setBaseStat("Special Defense", 55)
                            self.setBaseStat("Speed", 135)
                            self.setStats(self.Level, self.plusNature, self.minusNature,
                                          self.IV, self.EV)
                            self.currentHp = tempHp
                            self.changeType("Ice", "Fire", True)
                            self.pokemonName = "Darmanitan (Galarian Zen)"
                        else:
                            self.setBaseStat("Attack", 30)
                            self.setBaseStat("Defense", 105)
                            self.setBaseStat("Special Attack", 140)
                            self.setBaseStat("Special Defense", 105)
                            self.setBaseStat("Speed", 55)
                            self.setStats(self.Level, self.plusNature, self.minusNature,
                                          self.IV, self.EV)
                            self.currentHp = tempHp
                            self.changeType("Fire", "Psychic", True)
                            self.pokemonName = "Darmanitan (Zen)"
                else:
                    # Used to force Power Construct Zygarde to start in its 50% form
                    if self.ability.abilityName == "Power Construct":
                        if not self.currentForm == "Complete":
                            currentFullHP = self.Stats["HP"]
                            self.setBaseStat("HP", 108)
                            self.setBaseStat("Attack", 100)
                            self.setBaseStat("Defense", 121)
                            self.setBaseStat("Special Attack", 81)
                            self.setBaseStat("Special Defense", 95)
                            self.setBaseStat("Speed", 95)
                            self.setStats(self.Level, self.plusNature, self.minusNature,
                                          self.IV, self.EV)
                            self.currentHp = int(tempHp * self.Stats["HP"] / currentFullHP)
                            self.pokemonName = "Zygarde"
                            self.mass = [305.0, True]
                    # Changes Minior Shield to Minior Meteor
                    elif self.ability.abilityName == "Shields Down":
                        self.setBaseStat("Attack", 60)
                        self.setBaseStat("Defense", 100)
                        self.setBaseStat("Special Attack", 60)
                        self.setBaseStat("Special Defense", 100)
                        self.setBaseStat("Speed", 60)
                        self.setStats(self.Level, self.plusNature, self.minusNature,
                                      self.IV, self.EV)
                        self.currentHp = tempHp
                        self.pokemonName = "Minior (Meteor)"
                        self.mass = [40.0, True]
                    # Changes Darmanitan Zen Mode to its corresponding base form
                    elif self.ability.abilityName == "Zen Mode":
                        self.setBaseStat("Attack", 140)
                        self.setBaseStat("Defense", 55)
                        self.setBaseStat("Special Attack", 30)
                        self.setBaseStat("Special Defense", 55)
                        self.setBaseStat("Speed", 95)
                        self.setStats(self.Level, self.plusNature, self.minusNature,
                                      self.IV, self.EV)
                        self.currentHp = tempHp
                        self.changeType(self.Type1.typeName, "None", True)
                        if self.Type1.typeName == "Ice":
                            self.pokemonName = "Darmanitan (Galarian)"
                        else:
                            self.pokemonName = "Darmanitan"
            # Changes Greninja to Ash Greninja
            elif self.ability.abilityName == "Battle Bond":
                if self.currentForm == "Base" and not activate:
                    self.setBaseStat("Attack", 95)
                    self.setBaseStat("Defense", 67)
                    self.setBaseStat("Special Attack", 103)
                    self.setBaseStat("Special Defense", 71)
                    self.setBaseStat("Speed", 122)
                    self.setStats(self.Level, self.plusNature, self.minusNature,
                                  self.IV, self.EV)
                    self.currentHp = tempHp
                    self.pokemonName = "Greninja"
                else:
                    self.currentForm == "Ash"
                    self.setBaseStat("Attack", 145)
                    self.setBaseStat("Defense", 67)
                    self.setBaseStat("Special Attack", 153)
                    self.setBaseStat("Special Defense", 71)
                    self.setBaseStat("Speed", 132)
                    self.setStats(self.Level, self.plusNature, self.minusNature,
                                  self.IV, self.EV)
                    self.currentHp = tempHp
                    self.pokemonName = "Greninja (Ash)"
                    self.drawCurrentText("Greninja transformed to Ash Greninja!")
           # Changes Castform to its corresponding weather form
            elif self.ability.abilityName == "Forecast":
                if weather == "Sunny Day":
                    self.changeType("Fire", "None", False)
                    self.pokemonName = "Castform (Sunny)"
                elif weather == "Rain Dance":
                    self.changeType("Water", "None", False)
                    self.pokemonName = "Castform (Rainy)"
                elif weather == "Hail":
                    self.changeType("Ice", "None", False)
                    self.pokemonName = "Castform (Snowy)"
                else:
                    self.changeType("Normal", "None", True)
                    self.pokemonName = "Castform"
            # Changes Aegislash between its Blade and Shield forms
            elif self.ability.abilityName == "Stance Change" and activate:
                if self.currentForm == "Base":
                    self.currentForm = "Blade"
                    self.setBaseStat("Attack", 140)
                    self.setBaseStat("Defense", 50)
                    self.setBaseStat("Special Attack", 140)
                    self.setBaseStat("Special Defense", 50)
                    self.setStats(self.Level, self.plusNature, self.minusNature,
                                  self.IV, self.EV)
                    self.currentHp = tempHp
                    self.pokemonName = "Aegislash (Blade)"
                else:
                    self.currentForm = "Base"
                    self.setBaseStat("Attack", 50)
                    self.setBaseStat("Defense", 140)
                    self.setBaseStat("Special Attack", 50)
                    self.setBaseStat("Special Defense", 140)
                    self.setStats(self.Level, self.plusNature, self.minusNature,
                                  self.IV, self.EV)
                    self.currentHp = tempHp
                    self.pokemonName = "Aegislash (Shield)"
            # Changes Eiscue between its Ice and No Ice forms
            elif self.ability.abilityName == "Ice Face":
                if activate:
                    self.currentForm = "No Ice"
                    self.setBaseStat("Defense", 70)
                    self.setBaseStat("Special Defense", 50)
                    self.setBaseStat("Speed", 130)
                    self.currentHP = tempHp
                    self.pokemonName = "Eiscue (No Ice)"
                elif weather == "Hail":
                    self.currentForm = "Base"
                    self.setBaseStat("Defense", 110)
                    self.setBaseStat("Special Defense", 90)
                    self.setBaseStat("Speed", 50)
                    self.currentHP = tempHp
                    self.pokemonName = "Eiscue (Ice)"
            # Changes Mimikyu to busted
            elif self.ability.abilityName == "Disguise":
                if activate:
                    self.currentForm = "Busted"
            # Changes Cramorant bewteen its forms
            elif self.ability.abilityName == "Gulp Missile" and activate:
                if self.currentForm == "Base":
                    if (tempHp/self.Stats["HP"]) > .5:
                        self.currentForm = "Gulping"
                    else:
                        self.currentForm = "Gorging"
                else:
                    self.currentForm = "Base"
            # Changes Meloetta Aria to Meloetta Pirouette
            elif self.pokemonName == "Meloetta (Aria)" and activate:
                self.setBaseStat("Attack", 128)
                self.setBaseStat("Defense", 90)
                self.setBaseStat("Special Attack", 77)
                self.setBaseStat("Special Defense", 77)
                self.setBaseStat("Speed", 128)
                self.setStats(self.Level, self.plusNature, self.minusNature,
                              self.IV, self.EV)
                self.currentHp = tempHp
                self.changeType("Normal", "Fighting", True)
                self.pokemonName = "Meloetta (Pirouette)"
            # Changes Palafin to Palafin Hero
            elif self.pokemonName == "Palafin" and activate:
                self.setBaseStat("Attack", 160)
                self.setBaseStat("Defense", 97)
                self.setBaseStat("Special Attack", 106)
                self.setBaseStat("Special Defense", 87)
                self.setBaseStat("Speed", 100)
                self.setStats(self.Level, self.plusNature, self.minusNature,
                              self.IV, self.EV)
                self.currentHp = tempHp
                self.pokemonName = "Palafin (Hero)"
                self.mass = [97.4, True]
            # Alternates Morpeko between forms
        elif self.pokemonName == "Morpeko":
            if self.currentForm == "Base":
                self.currentForm == "Hangry"
            else:
                self.currentForm == "Base"
        self.currentMass = copy.deepcopy(self.mass[0])
    
    # Sets the stat values used in attacking, defending, and speed
    def setStats(self, level, posNature = "HP", negNature = "HP", 
                 IV = [15,15,15,15,15,15], EV = [0,0,0,0,0,0]):
        self.Level = level
        counter = 0
        boosterStat = None
        boosterValue = 0
        # Checks if the held item is a power item, which the EV values are overridden
        # for the max value of 252
        if "Raise" in self.item.secondEffect:
            if self.item.secondEffect == "Raise HP":
                powerStat = 0
                fixedStat = "HP"
            elif self.item.secondEffect == "Raise Attack":
                powerStat = 1
                fixedStat = "Attack"
            elif self.item.secondEffect == "Raise Defense":
                powerStat = 2
                fixedStat = "Defense"
            elif self.item.secondEffect == "Raise Special Attack":
                powerStat = 3
                fixedStat = "Special Attack"
            elif self.item.secondEffect == "Raise Special Defense":
                powerStat = 4
                fixedStat = "Special Defense"
            else:
                powerStat = 5
                fixedStat = "Speed"
            EV[powerStat] = 252
            
            evTotal = 0
            for evPosition in range(len(EV)):
                if not evPosition == powerStat:
                    evTotal += EV[evPosition]
            if evTotal > 258:
                evFix = 258/evTotal
            else:
                evFix = 1
        else:
            evTotal = 0
            powerStat = 6
            fixedStat = "None"
            for evValue in EV:
                evTotal += evValue
            if evTotal > 510:
                evFix = 510 / evTotal
            else:
                evFix = 1
        for stat in self.BaseStats:
            if stat == "HP":
                # Shedinja is forced to have 1 HP as the calculations would fail
                # to correctly give it the right stat
                if self.pokemonName == "Shedinja":
                    self.Stats["HP"] = 1
                    self.currentHp = 1
                elif powerStat == 0:
                    self.Stats["HP"] = int((2 * self.BaseStats[stat] + IV[counter] 
                    + (EV[counter]/4)) * level / 100) + level + 10
                    self.currentHp = self.Stats["HP"]
                else:
                    self.Stats["HP"] = int((2 * self.BaseStats[stat] + IV[counter] 
                    + (floor(EV[counter] * evFix)/4)) * level / 100) + level + 10
                    self.currentHp = self.Stats["HP"]
            # Runs if positive nature to give a slight boost
            elif posNature == stat and posNature != negNature:
                if powerStat == 6 or not stat == fixedStat:
                    self.Stats[stat] = int((int((2 * self.BaseStats[stat] 
                    + IV[counter] + (floor(EV[counter] * evFix)/4)) * level / 100) 
                        + 5) * 1.1)
                else:
                    self.Stats[stat] = int((int((2 * self.BaseStats[stat] 
                    + IV[counter] + (EV[counter]/4)) * level / 100) 
                        + 5) * 1.1)
                self.plusNature = posNature
            # Runs if negative nature to take a slight deduction
            elif negNature == stat and posNature != negNature:
                if powerStat == 6 or not stat == fixedStat:
                    self.Stats[stat] = int((int((2 * self.BaseStats[stat] 
                    + IV[counter] + (floor(EV[counter] * evFix)/4)) * level / 100) 
                        + 5) * .9)
                else:
                    self.Stats[stat] = int((int((2 * self.BaseStats[stat] 
                    + IV[counter] + (EV[counter]/4)) * level / 100) 
                        + 5) * .9)
                self.minusNature = negNature
            else:
                if powerStat == 6 or not stat == fixedStat:
                    self.Stats[stat] = int((int((2 * self.BaseStats[stat] 
                    + IV[counter] + (floor(EV[counter] * evFix)/4)) * level / 100) 
                        + 5))
                else:
                    self.Stats[stat] = int((int((2 * self.BaseStats[stat] 
                    + IV[counter] + (EV[counter]/4)) * level / 100) 
                        + 5))
            # Finds the highest stat for Protosynthesis and Quark Drive
            if not stat == "HP" and boosterValue < self.Stats[stat]:
                boosterStat = stat
                boosterValue = self.Stats[stat]
                if stat == "Speed":
                    self.boosterEnergy = [1.5, boosterStat, False]
                else:
                    self.boosterEnergy = [1.3, boosterStat, False]
            counter += 1
        self.IV = IV
        self.EV = EV
        self.hiddenPowerCalculator()
        if self.Stats["Special Attack"] >= self.Stats["Attack"]:
            self.photonGeyser = "Special"
        else:
            self.photonGeyser = "Physical"
    
    # Boosts the corresponding stat if Protosynthesis or Quark Drive conditions
    # are met
    def energyBoost(self, weather, terrain):
        if self.ability.effect[0] == "Booster Energy":
            if weather == self.ability.effect[1] or terrain == self.ability.effect[1]:
                self.boosterEnergy[2] = True
            elif self.item.itemName == self.ability.effect[0] and not self.item.consumed:
                self.boosterEnergy[2] = True
                self.item.Consume()
            else:
                self.boosterEnergy[2] = False
    
    # Adds a new move that can be selected
    def newMove(self, newMove):
        for move in range(4):
            if self.Moves[move] == None:
                self.Moves[move] = newMove
                # The following have special conditions for type and category
                if self.Moves[move].moveName == "Hidden Power":
                    self.Moves[move].moveType = Type(self.hiddenPower)
                elif self.Moves[move].moveName == "Photon Geyser":
                    self.Moves[move].phySpe = self.photonGeyser
                elif self.Moves[move].moveName == "Raging Bull" and "Tauros" in self.pokemonName:
                    if self.pokemonName == "Tauros (Paldea)":
                        self.Moves[move].moveType = Type("Fighting")
                    elif self.pokemonName == "Tauros (Blaze)":
                        self.Moves[move].moveType = Type("Fire")
                    elif self.pokemonName == "Tauros (Aqua)":
                        self.Moves[move].moveType = Type("Water")
                break
    
    # Uses the IV values to determine the Hidden Power type
    def hiddenPowerCalculator(self):
        typeList = ["Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost",
                    "Steel", "Fire", "Water", "Grass", "Electric", "Psychic", "Ice",
                    "Dragon", "Dark"]
        hiddenPowerSum = 0
        counter = 0
        tempStats = [self.IV[0], self.IV[1], self.IV[2], self.IV[5], self.IV[3], self.IV[4]]
        
        for ivNumber in tempStats:
            if ivNumber%2 == 0:
                hiddenPowerSum += (2**counter) * 0
            else:
                hiddenPowerSum += (2**counter) * 1
            counter += 1
        hiddenPowerValue = floor(hiddenPowerSum*5/21)
        self.hiddenPower = typeList[hiddenPowerValue]
    
    # Replaces one of the current moves with a new one
    def replaceMove(self, newMove, position):
        self.Moves[position - 1] = newMove
    
    # Replaces the item for a new one
    def newItem(self, item, zMoveDict = {}):
        self.item = item
        if self.ability.abilityName == "Klutz" and not self.item.fling == 0:
            self.item.klutz = True
            self.item.Consume()
    
    # Temporarily changes a stat
    def modifyStat(self, stat, modifier, targetSelf):
        normalStats = [1/4, 2/7, 1/3, 2/5, 1/2, 2/3, 1, 3/2, 2, 5/2, 3, 7/2, 4]
        accuracyStats = [1/3, 3/8, 3/7, 1/2, 3/5, 3/4, 1, 4/3, 5/3, 2, 7/3, 8/3, 3]
        
        statSplit = stat.split("/")
        modifierSplit = modifier.split("/")
        # Picks a random stat when acupressure is used
        if statSplit == ["Acupressure"]:
            statSplit = [choice(["Attack", "Defense", "Special Attack", "Special Defense", "Speed", "Accuracy", "Evasion"])]
        
        for statNumber in range(len(statSplit)):
            # Doubles stat change if ability is Simple
            if self.ability.abilityName == "Simple":
                modifierSplit[statNumber] *= 2
            # Checks if the stat is accuracy related or not
            if statSplit[statNumber] in ["Attack", "Defense", "Special Attack", "Special Defense", "Speed"]:
                for i in range(13):
                    if round(self.statModifier[statSplit[statNumber]], 2) == round(normalStats[i], 2):
                        if self.ability.abilityName == "Contrary":
                            newModifier = int(modifierSplit[statNumber]) - i
                        else:
                            newModifier = int(modifierSplit[statNumber]) + i
                # Checks if the modifier is out of range
                if newModifier < 0:
                    newModifier = 0
                elif newModifier > 12:
                    newModifier = 12
                self.statModifier[statSplit[statNumber]] = normalStats[newModifier]
            elif statSplit[statNumber] in ["Accuracy", "Evasion"]:
                for i in range(13):
                    if round(self.statModifier[statSplit[statNumber]], 2) == round(accuracyStats[i], 2):
                        if self.ability.abilityName == "Contrary":
                            newModifier = int(modifierSplit[statNumber]) - i
                        else:
                            newModifier = int(modifierSplit[statNumber]) + i
                if newModifier < 0:
                    newModifier = 0
                elif newModifier > 12:
                    newModifier = 12
                self.statModifier[statSplit[statNumber]] = accuracyStats[newModifier]
            if not (statSplit[statNumber] == "None" or statSplit[statNumber] == None or str(statSplit[statNumber]) == "nan"):
                # Lowers a stat by 1 stage
                if int(modifierSplit[statNumber]) == -1 or (int(modifierSplit[statNumber]) == 1 and self.ability.abilityName == "Contrary"):
                    self.drawCurrentText(self.pokemonName + "'s " + statSplit[statNumber] + " was lowered!")
                    # Raises a stat by 2 if Defiant conditions are met
                    if self.ability.effect[0] == "Defiant" and not targetSelf:
                        self.drawCurrentText(self.pokemonName + " defiantly rose its ", self.ability.effect[1])
                        self.modifyStat(self.ability.effect[1], [2], True)
                # Lowers a stat by 2+ stages
                elif int(modifierSplit[statNumber]) < -1 or (int(modifierSplit[statNumber]) > 1 and self.ability.abilityName == "Contrary"):
                    self.drawCurrentText(self.pokemonName + "'s " + statSplit[statNumber] + " was drastically lowered!")
                    if self.ability.effect[0] == "Defiant" and not targetSelf:
                        self.drawCurrentText(self.pokemonName + " defiantly rose its ", self.ability.effect[1])
                        self.modifyStat(self.ability.effect[1], [2], True)
                # Raises a stat by 1 stage
                elif int(modifierSplit[statNumber]) == 1 or (int(modifierSplit[statNumber]) == -1 and self.ability.abilityName == "Contrary"):
                    self.drawCurrentText(self.pokemonName + "'s " + statSplit[statNumber] + " was raised!")
                # Maxes a stat
                elif int(modifierSplit[statNumber])%12 == 0:
                    self.drawCurrentText(self.pokemonName + " maximized its " + statSplit[statNumber] + "!")
                # Raises a stat by 2+ stages
                elif int(modifierSplit[statNumber]) > 1 or (int(modifierSplit[statNumber]) < -1 and self.ability.abilityName == "Contrary"):
                    self.drawCurrentText(self.pokemonName + "'s " + statSplit[statNumber] + " was sharply raised!")
    
    # Changes status and volatile conditions
    def changeStatus(self, status, corrosion = False):
        success = False
        # Chacks if the status is one of the special cases with multiple outcomes
        if status == "Tri Attack":
            triAttackStatus = randint(1, 3)
            if triAttackStatus == 1:
                status = "Burn"
            elif triAttackStatus == 2:
                status = "Freeze"
            else:
                status = "Paralyze"
        elif status == "Dire Claw":
            direClawStatus = randint(1, 4)
            if direClawStatus < 3:
                status = "Poison"
            elif direClawStatus == 3:
                status = "Sleep"
            else:
                status = "Paralyze"
        
        if not(status in self.ability.effect[1] and self.ability.effect[0] == "Immunity" and self.ability.effect[2] == "Status"):  
            # Volatile conditions that do not trap
            if status in ["Flinch", "Confuse", "Infatuation", "Pumped", "Perish", "Drowsy", "Aqua Ring"]:
                if self.volatile[status] == 0:
                    success = True
                    self.volatile[status] = 1
            # Trapping conditions that do damage
            elif status == "Trap":
                success = True
                self.volatile[status] = 4
            # Trapping conditions that do not do damage
            elif status in ["Mean Look", "Octolock", "Ingrain"]:
                success = True
                self.volatile["Block Condition"] = status
            # Poison status conditions
            elif status == "Poison" or status == "Badly Poison":
                if (self.Type1.typeName == "Poison" or self.Type2.typeName == "Poison" or self.Type1.typeName == "Steel" or self.Type2.typeName == "Steel") and not corrosion:
                    pass
                else:
                    self.status = "Poison"
                    success = True
                    if status == "Badly Poison":
                        self.volatile[status] = 1
            else:
                # Fire types cannot be burned
                if self.Type1.typeName == "Fire" or self.Type2.typeName == "Fire":
                    if status != "Burn":
                        self.status = status
                        success = True
                # Electric types cannot be paralyzed
                elif self.Type1.typeName == "Electric" or self.Type2.typeName == "Electric":
                    if status != "Paralyze":
                        self.status = status
                        success = True
                # Ice types cannot be frozen
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
            
        # Displays a message of the successful status condition
        if success:
            if status == "Burn":
                self.drawCurrentText(self.pokemonName + " was burned!")
            elif status == "Poison":
                self.drawCurrentText(self.pokemonName + " was poisoned!")
            elif status == "Paralyze":
                self.drawCurrentText(self.pokemonName + " was paralyzed! It may be unable to move!")
            elif status == "Freeze":
                self.drawCurrentText(self.pokemonName + " was frozen solid!")
            elif status == "Sleep":
                self.drawCurrentText(self.pokemonName + " was put to sleep!")
            elif status == "Confuse":
                self.drawCurrentText(self.pokemonName + " was confused!")
            elif status == "Infatuation":
                self.drawCurrentText(self.pokemonName + " fell in love!")
            elif status == "Pumped":
                self.drawCurrentText(self.pokemonName + " is getting pumped!")
            elif status == "Perish":
                self.drawCurrentText("All Pokemon that heard this song will faint in 3 turns!")
            elif status == "Drowsy":
                self.drawCurrentText(self.pokemonName + " became drowsy!")
    
    # Randomly chooses a gender using the gender ratio
    def Gender(self):
        self.gender = choice(self.genderRatio)