from random import choice, randint
from math import ceil, floor, sqrt
from graphics import Circle, color_rgb, GraphWin, Line, Oval, Point, Polygon, Rectangle, Text
import pandas as pd
import copy

# Checks if a square is clicked
def Clicked(bottomLeft, topRight, point):
    bottomLeftX = bottomLeft.getX()
    bottomLeftY = bottomLeft.getY()
    topRightX = topRight.getX()
    topRightY = topRight.getY()
    pointX = point.getX()
    pointY = point.getY()
    
    if bottomLeftX < pointX and topRightX > pointX:
        if bottomLeftY < pointY and topRightY > pointY:
            return True
    return False

# Checks if a circle is clicked
def ClickedCircle(radius, center, point):
    centerX = center.getX()
    centerY = center.getY()
    pointX = point.getX()
    pointY = point.getY()
    
    distance = sqrt( (centerX - pointX) ** 2 + (centerY - pointY) ** 2 )
    
    if distance <= radius:
        return True
    else:
        return False

# The Type class defines the type of pokemon and moves
class Type:
    
    def __init__(self, typeName):
        self.typeName = typeName
        self.effectDict = {}
    
    # Sets the type effectiveness when attacking
    def setEffectiveness(self, typeName, damageMult):
        self.effectDict[typeName] = damageMult

# The Move class is used for moves that a pokemon knows and can call
class Move:
    
    def __init__(self, moveName, typeName, power, accuracy, pp, phySpe, healing,
                 chance, stat, target, stages, hitTimes, priority, charge, crit, 
                 sound, feint, contact, punching, slicing, zEffect, zTarget, zStages):
        self.moveName = moveName
        self.moveType = Type(typeName)
        self.power = power
        self.accuracy = accuracy
        # The following traits keep track of how many times a move can be used
        self.pp = pp
        self.currentPP = pp
        # Can be Physical, Special, or Status
        self.phySpe = phySpe
        # self.healing is used for moves that heal and hurt the user
        self.healing = healing
        # The following traits are used for secondary effects
        self.chance = chance
        self.stat = stat
        self.target = target
        self.stages = stages
        # The following traits are numbers for additional effects that are not
        # affected by succeeding a secondary effect chance
        self.hitTimes = hitTimes.split("/")
        self.priority = priority
        self.charge = charge
        self.crit = crit
        # The following traits are True or False
        self.sound = sound
        self.feint = feint
        self.contact = contact
        self.punching = punching
        self.slicing = slicing
        # The following traits are used for Z-Moves for status moves introduced
        # in generation 7 and earlier
        self.zEffect = zEffect
        self.zTarget = zTarget
        self.zStages = zStages
    
    # If the random integer is favorable, returns the type of secondary effect,
    # secondary effect name, the target, and how many stages
    def Secondary(self, serene):
        success = randint(1, 10)
        if serene:
            sereneBoost = 2
        else:
            sereneBoost = 1
        
        if success <= self.chance * sereneBoost:
            if self.stat in ["Flinch", "Confuse", "Trap", "Mean Look", "Octolock", "Ingrain", "Infatuation", "Pumped", "Perish", "Drowsy"]:
                return ["Volatile", self.stat, self.target, self.stages]
            elif self.stat in ["Burn", "Sleep", "Freeze", "Paralyze", "Poison",
                               "Rest", "Badly Poison", "Tri Attack", "Dire Claw", "Healthy"]:
                return ["Status", self.stat, self.target, self.stages]
            else:
                return ["Stat", self.stat, self.target, self.stages]
        else:
            return ["Failure"]

# A subclass of Move
class ZMove(Move):
    
    def __init__(self, moveName, typeName, power, phySpe, stat, target, stages, crit,
                 contact, sound, base, crystal, method, signature):
        # The following traits work the same as in Move
        self.moveName = moveName
        self.moveType = Type(typeName)
        self.power = power
        self.phySpe = phySpe
        self.stat = stat
        self.target = target
        self.stages = stages
        self.crit = crit
        self.contact = contact
        self.sound = sound
        # The following traits are used to figure out the conditions to allow
        # a Z-Move to be used
        self.base = base
        self.crystal = crystal
        self.method = method
        self.signature = signature
        # The following traits are consistant for all Z-Moves
        self.accuracy = 101
        self.pp = 1
        self.currentPP = 1
        self.healing = 0
        self.chance = 10
        self.hitTimes = ["1","1"]
        self.priority = 0
        self.charge = "None"
        self.feint = True
        self.punching = False
        self.slicing = False

# The Item class is used for held items        
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
        # Used if the pokemon's ability is klutz to prevent the item's usage
        self.klutz = None
    
    # Replaces the string function for items
    def __str__(self):
        if self.consumed and not self.klutz:
            return "None"
        else:
            itemWords = self.itemName.split(" ")
            newName = ""
            for word in itemWords:
                if not (word[0] == "(" or word[-1] == ")"):
                    newName += word + " "
            return newName
    
    # Prevents the usage of an item
    def Consume(self):
        self.consumed = True

# The Ability class is used for a pokemon's ability
class Ability:
    def __init__(self, abilityName, target, effect1, effect2, effect3, success):
        self.abilityName = abilityName
        self.target = target
        # Up to 3 effects are used
        self.effect = [effect1, effect2, effect3]
        self.success = success
        # The following are used to store a pokemon's ability when not in effect
        self.neutralizeState = 0
        self.trace = False
        self.tempAbility = [abilityName, target, [effect1, effect2, effect3], success]
    
    # Prevents the usage of an ability if the ability Neutralizing Gas is in play
    def neutralize(self):
        self.abilityName = "None"
        self.target = "None"
        self.effect = ["None", "None", "None"]
        self.success = 0
        self.neutralizeState = 1
    
    # Allows the usage of an ability if the ability Neutralizing Gas is removed
    # from play
    def deneutralize(self):
        self.abilityName = self.tempAbility[0]
        self.target = self.tempAbility[1]
        self.effect = self.tempAbility[2]
        self.success = self.tempAbility[3]
        self.neutralizeState = 0

# The Pokemon class is the pokemon with all related traits
class Pokemon:
    
    def __init__(self, pokemonName, ability, evolve, mass, typeName1, typeName2 = "None", gender = ["Male"], win = None):
        self.win = win
        
        self.pokemonName = pokemonName
        self.crunchName = "None"
        self.ability = ability
        # Mass is a list with the mass as a float, the units, and if the mass
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
                         "Pumped" : 0, "Perish" : 0, "Drowsy" : 0}
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
            self.mass = [230.0, "kG", True]
        
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
                    self.mass = [0.3, "kG", True]
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
                    self.mass = [78.6, "kG", True]
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
                        self.mass = [610.0, "kG", True]
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
                        self.mass = [0.3, "kG", True]
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
                            self.mass = [305.0, "kG", True]
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
                        self.mass = [40.0, "kG", True]
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
                self.mass = [97.4, "kG", True]
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
            if status in ["Flinch", "Confuse", "Infatuation", "Pumped", "Perish", "Drowsy"]:
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

# The Team class holds 6 pokemon
class Team():
    
    def __init__(self, win = None):
        self.win = win
        # The following keep track of the pokemon on the team
        self.pokemonList = [None, None, None, None, None, None]
        self.alivePokemon = 0
        self.activePokemon = None
        # The following keep track if special items have been used
        self.mega = False
        self.zMove = False
        # The following keep track of the conditions on the side of the field
        self.reflect = 0
        self.lightScreen = 0
        self.entryHazards = {"Spikes" : 0, "Toxic Spikes" : 0, "Stealth Rock" : 0,
                             "Sticky Web" : 0}
        self.textBoxBottomLeft = Point(0,0)
        self.textBoxTopRight = Point(500,150)
    
    # addToWin and drawCurrentText work the same as in the pokemon function
    # These functions will not change among classes
    def addToWin(self, win):
        self.win = win
        for pokemon in self.pokemonList:
            pokemon.addToWin(self.win)
            
    def drawCurrentText(self, text):
        self.currentText = Text(Point(250,75), text)
        self.currentText.draw(self.win)
        self.win.getMouse()
        self.currentText.undraw()
    
    # Adds a pokemon to the team if there is room
    def addPokemon(self, newPokemon):
        if self.alivePokemon < 6:
            for pokemonNumber in range(6):
                if self.pokemonList[pokemonNumber] == None:
                    self.pokemonList[pokemonNumber] = newPokemon
                    if pokemonNumber == 0:
                        self.activePokemon = self.pokemonList[pokemonNumber]
                    break
            self.alivePokemon += 1
    
    # Switches the current pokemon with the pokemon at position
    def Switch(self, position):
        if not self.pokemonList[position - 1] == None:
            if self.pokemonList[position - 1].currentHp > 0:
                # Removes the transformed effect from Imposter and Transform
                if self.activePokemon.transformed:
                    self.activePokemon.transformed = False
                    self.activePokemon.Stats = self.activePokemon.tempPokemon[0]
                    self.activePokemon.ability = self.activePokemon.tempPokemon[1]
                    self.activePokemon.changeType(self.activePokemon.tempPokemon[2], self.activePokemon.tempPokemon[3], True)
                    self.activePokemon.Moves = self.activePokemon.tempPokemon[4]
                # Removes the trace effect from Trace
                if self.activePokemon.ability.trace:
                    self.activePokemon.ability.abilityName = self.activePokemon.ability.tempAbility[0]
                    self.activePokemon.ability.target = self.activePokemon.ability.tempAbility[1]
                    self.activePokemon.ability.effect = self.activePokemon.ability.tempAbility[2]
                    self.activePokemon.ability.success = self.activePokemon.ability.tempAbility[3]
                    self.activePokemon.ability.trace = False
                # Aegislash becomes shield form
                if self.activePokemon.ability.abilityName == "Stance Change" and self.activePokemon.currentForm == "Blade":
                    self.activePokemon.changeForm("Unimportant", True)
                # Palafin becomes hero form
                elif self.activePokemon.ability.abilityName == "Zero to Hero" and self.activePokemon.pokemonName == "Palafin":
                    self.activePokemon.changeForm("Unimportant", True)
                # Resets volatile status conditions and badly poison count
                if self.activePokemon.volatile["Badly Poison"] > 0:
                    self.activePokemon.volatile = {"Flinch" : 0, "Confuse" : 0, "Badly Poison" : 1, "Trap" : 0, 
                                                   "Block Condition" : "None", "Blocked Moves" : [5], "Intangible" : " ", 
                                                   "Substitute" : 0, "Infatuation" : 0, "Pumped" : 0, "Perish" : 0, "Drowsy" : 0}
                # Resets volatile status conditions
                else:
                    self.activePokemon.volatile = {"Flinch" : 0, "Confuse" : 0, "Badly Poison" : 0, "Trap" : 0,
                                                   "Block Condition" : "None", "Blocked Moves" : [5], "Intangible" : " ", 
                                                   "Substitute" : 0, "Infatuation" : 0, "Pumped" : 0, "Perish" : 0, "Drowsy" : 0}
                # Resets stat modifiers
                self.activePokemon.statModifier = {"Attack" : 1, "Defense" : 1,
                      "Special Attack": 1, "Special Defense": 1, "Speed" : 1, 
                      "Accuracy": 1, "Evasion": 1}
                # Heals status conditions if ability is Natural Cure
                if self.activePokemon.ability.abilityName == "Natural Cure":
                    self.activePokemon.changeStatus("Healthy")
                    self.activePokemon.volatile["Badly Poison"] = 0
                # Heals HP if ability is Regenerator
                elif self.activePokemon.ability.abilityName == "Regenerator":
                    self.activePokemon.currentHp += floor(self.activePokemon.Stats["HP"] * .33)
                    if self.activePokemon.currentHp > self.activePokemon.Stats["HP"]:
                        self.activePokemon.currentHp = self.activePokemon.Stats["HP"]
                # Resets other traits
                self.activePokemon.currentMass = copy.deepcopy(self.activePokemon.mass[0])
                self.activePokemon.changeType(self.activePokemon.tempType1.typeName, self.activePokemon.tempType2.typeName, True)
                self.activePokemon.turnOut = 0
                self.activePokemon.protean = False
                self.activePokemon.flashFire = False
                self.activePokemon.illusion = True
                self.activePokemon.ability.deneutralize()
                self.activePokemon = self.pokemonList[position - 1]
                self.drawCurrentText("Switched to " + self.pokemonList[position - 1].pokemonName + "!")
                # Pokemon without the Heavy-Duty Boots item are affected by entry hazards
                if not self.activePokemon.item.itemName == "Heavy-Duty Boots":
                    if self.entryHazards["Spikes"] > 0 and not(self.activePokemon.Type1.typeName == "Flying" or self.activePokemon.Type2.typeName == "Flying" or self.activePokemon.ability.abilityName == "Levitate"):
                        if self.entryHazards["Spikes"] == 1:
                            self.activePokemon.currentHp -= round(self.activePokemon.Stats["HP"] / 8)
                        elif self.entryHazards["Spikes"] == 2:
                            self.activePokemon.currentHp -= round(self.activePokemon.Stats["HP"] / 6)
                        else:
                            self.activePokemon.currentHp -= round(self.activePokemon.Stats["HP"] / 4)
                        self.drawCurrentText(self.activePokemon.pokemonName + " was hurt by Spikes!")
                    if self.entryHazards["Stealth Rock"] == 1:
                        rockMatchUp = {"Bug" : 2, "Dark" : 1, "Dragon" : 1, "Electric" : 1, 
                                       "Fairy" : 1, "Fighting" : .5, "Fire" : 2, "Flying" : 2, 
                                       "Ghost" : 1, "Grass" : 1, "Ground" : .5, "Ice" : 2, 
                                       "Normal" : 1, "Poison" : 1, "Psychic" : 1, "Rock" : 1, 
                                       "Steel" : .5, "Water" : 1, "None" : 1}
                        self.activePokemon.currentHp -= round(self.activePokemon.Stats["HP"] / 8 * rockMatchUp[self.activePokemon.Type1.typeName] * rockMatchUp[self.activePokemon.Type2.typeName])
                        self.drawCurrentText("Pointed stones dug into " + self.activePokemon.pokemonName + "!")
                    if self.entryHazards["Toxic Spikes"] > 0 and not(self.activePokemon.Type1.typeName == "Flying" or self.activePokemon.Type2.typeName == "Flying" or self.activePokemon.ability.abilityName == "Levitate"):
                        if self.activePokemon.Type1.typeName == "Poison" or self.activePokemon.Type2.typeName == "Poison":
                            self.entryHazards["Toxic Spikes"] = 0
                            self.drawCurrentText("The toxic spikes disappeared under " + self.activePokemon.pokemonName + "'s feet!")
                        elif not(self.activePokemon.Type1.typeName == "Steel" or self.activePokemon.Type2.typeName == "Steel"):
                            if self.entryHazards["Toxic Spikes"] == 1:
                                self.activePokemon.changeStatus("Poison")
                            else:
                                self.activePokemon.changeStatus("Badly Poison")
                    if self.entryHazards["Sticky Web"] == 1 and not(self.activePokemon.Type1.typeName == "Flying" or self.activePokemon.Type2.typeName == "Flying" or self.activePokemon.ability.abilityName == "Levitate" or (self.activePokemon.ability.effect[0] == "Clear Body" and self.activePokemon.ability.effect[0] == "All")):
                        self.drawCurrentText(self.activePokemon.pokemonName + " got caught in a sticky web!")
                        self.activePokemon.modifyStat("Speed", "-1", False)
                    if self.activePokemon.currentHp <= 0:
                        self.drawCurrentText(self.activePokemon.pokemonName + " fainted!")
                        while self.pokemonList[position - 1].currentHp <= 0:
                            position = self.switchMenu()
                        self.Switch(position)
                # Displays a message if pokemon's ability is one of the ruin
                if self.activePokemon.currentHp > 0 and self.activePokemon.ability.effect[0] == "Ruin":
                    self.drawCurrentText(self.activePokemon.pokemonName + "'s " + self.activePokemon.ability.abilityName + " reduced all Pokemon's " + self.activePokemon.ability.effect[1] + "!")
                # Removes boost from Protosynthesis and Quark Drive
                if self.activePokemon.boosterEnergy[2]:
                    self.activePokemon.boosterEnergy[2] = False
   
    # Tries mega evolving the active pokemon             
    def megaEvolve(self, megaDict, megaList):
        tryMega = self.activePokemon.megaEvolve(megaDict, megaList)
        if tryMega:
            self.mega = True
            self.drawCurrentText("The Pokemon mega evolved into " + self.activePokemon.pokemonName + "!")
    
    # Runs a special switch menu that cannot be exited from
    def switchMenu(self):
        # Green is high HP pokemon
        # Yellow is medium HP pokemon
        # Red is low HP pokemon
        # Grey is fainted pokemon
        pokemonColorList = []
        for pokemon in self.pokemonList:
            if pokemon.currentHp >= pokemon.Stats["HP"] * .5:
                pokemonColorList.append("Green")
            elif pokemon.currentHp >= pokemon.Stats["HP"] * .125:
                pokemonColorList.append("Yellow")
            elif pokemon.currentHp <= 0:
                pokemonColorList.append("Grey")
            else:
                pokemonColorList.append("Red")
        # Pokemon 1
        pokemon1BoxBottomLeft = Point(0, 100)
        pokemon1BoxTopRight = Point(250, 150)
        pokemon1Box = Rectangle(pokemon1BoxBottomLeft, pokemon1BoxTopRight)
        pokemon1Box.setFill(pokemonColorList[0])
        pokemon1Box.setWidth(6)
        pokemon1Box.draw(self.win)
        pokemon1Text = Text(Point(125,125), self.pokemonList[0].pokemonName + " " + str(self.pokemonList[0].currentHp) + "/" + str(self.pokemonList[0].Stats["HP"]))
        pokemon1Text.setSize(10)
        pokemon1Text.draw(self.win)
        # Pokemon 2
        pokemon2BoxBottomLeft = Point(250, 100)
        pokemon2BoxTopRight = Point(500, 150)
        pokemon2Box = Rectangle(pokemon2BoxBottomLeft, pokemon2BoxTopRight)
        pokemon2Box.setFill(pokemonColorList[1])
        pokemon2Box.setWidth(6)
        pokemon2Box.draw(self.win)
        pokemon2Text = Text(Point(375,125), self.pokemonList[1].pokemonName + " " + str(self.pokemonList[1].currentHp) + "/" + str(self.pokemonList[1].Stats["HP"]))
        pokemon2Text.setSize(10)
        pokemon2Text.draw(self.win)
        # Pokemon 3
        pokemon3BoxBottomLeft = Point(0, 50)
        pokemon3BoxTopRight = Point(250, 100)
        pokemon3Box = Rectangle(pokemon3BoxBottomLeft, pokemon3BoxTopRight)
        pokemon3Box.setFill(pokemonColorList[2])
        pokemon3Box.setWidth(6)
        pokemon3Box.draw(self.win)
        pokemon3Text = Text(Point(125,75), self.pokemonList[2].pokemonName + " " + str(self.pokemonList[2].currentHp) + "/" + str(self.pokemonList[2].Stats["HP"]))
        pokemon3Text.setSize(10)
        pokemon3Text.draw(self.win)
        # Pokemon 4
        pokemon4BoxBottomLeft = Point(250, 50)
        pokemon4BoxTopRight = Point(500, 100)
        pokemon4Box = Rectangle(pokemon4BoxBottomLeft, pokemon4BoxTopRight)
        pokemon4Box.setFill(pokemonColorList[3])
        pokemon4Box.setWidth(6)
        pokemon4Box.draw(self.win)
        pokemon4Text = Text(Point(375,75), self.pokemonList[3].pokemonName + " " + str(self.pokemonList[3].currentHp) + "/" + str(self.pokemonList[3].Stats["HP"]))
        pokemon4Text.setSize(10)
        pokemon4Text.draw(self.win)
        # Pokemon 5
        pokemon5BoxBottomLeft = Point(0, 0)
        pokemon5BoxTopRight = Point(250, 50)
        pokemon5Box = Rectangle(pokemon5BoxBottomLeft, pokemon5BoxTopRight)
        pokemon5Box.setFill(pokemonColorList[4])
        pokemon5Box.setWidth(6)
        pokemon5Box.draw(self.win)
        pokemon5Text = Text(Point(125,25), self.pokemonList[4].pokemonName + " " + str(self.pokemonList[4].currentHp) + "/" + str(self.pokemonList[4].Stats["HP"]))
        pokemon5Text.setSize(10)
        pokemon5Text.draw(self.win)
        # Pokemon 6
        pokemon6BoxBottomLeft = Point(250, 0)
        pokemon6BoxTopRight = Point(500, 50)
        pokemon6Box = Rectangle(pokemon6BoxBottomLeft, pokemon6BoxTopRight)
        pokemon6Box.setFill(pokemonColorList[5])
        pokemon6Box.setWidth(6)
        pokemon6Box.draw(self.win)
        pokemon6Text = Text(Point(375,25), self.pokemonList[5].pokemonName + " " + str(self.pokemonList[5].currentHp) + "/" + str(self.pokemonList[5].Stats["HP"]))
        pokemon6Text.setSize(10)
        pokemon6Text.draw(self.win)
        # Runs until a pokemon is selected
        clickedPoint = self.win.getMouse()
        while not Clicked(self.textBoxBottomLeft, self.textBoxTopRight, clickedPoint):
            clickedPoint = self.win.getMouse()
        # Undraws the pokemon boxes
        pokemon1Box.undraw()
        pokemon1Text.undraw()
        pokemon2Box.undraw()
        pokemon2Text.undraw()
        pokemon3Box.undraw()
        pokemon3Text.undraw()
        pokemon4Box.undraw()
        pokemon4Text.undraw()
        pokemon5Box.undraw()
        pokemon5Text.undraw()
        pokemon6Box.undraw()
        pokemon6Text.undraw()
        # Sends out the correct pokemon
        if Clicked(pokemon1BoxBottomLeft, pokemon1BoxTopRight, clickedPoint):
            if self.pokemonList[0].currentHp <= 0:
                return self.switchMenu()
            else:
                position = "1"
        elif Clicked(pokemon2BoxBottomLeft, pokemon2BoxTopRight, clickedPoint):
            if self.pokemonList[1].currentHp <= 0:
                return self.switchMenu()
            else:
                position = "2"
        elif Clicked(pokemon3BoxBottomLeft, pokemon3BoxTopRight, clickedPoint):
            if self.pokemonList[2].currentHp <= 0:
                return self.switchMenu()
            else:
                position = "3"
        elif Clicked(pokemon4BoxBottomLeft, pokemon4BoxTopRight, clickedPoint):
            if self.pokemonList[3].currentHp <= 0:
                return self.switchMenu()
            else:
                position = "4"
        elif Clicked(pokemon5BoxBottomLeft, pokemon5BoxTopRight, clickedPoint):
            if self.pokemonList[4].currentHp <= 0:
                return self.switchMenu()
            else:
                position = "5"
        elif Clicked(pokemon6BoxBottomLeft, pokemon6BoxTopRight, clickedPoint):
            if self.pokemonList[5].currentHp <= 0:
                return self.switchMenu()
            else:
                position = "6"
        return position
# The Battle class is the main class used, with two teams of pokemon and conditions
# impacting both         
class Battle():
    
    def __init__(self, Team1, Team2, win):
        self.win = win
        # The two team objects
        self.team1 = Team1
        self.team2 = Team2
        # The following are the current field condtion along with how long they
        # will last
        self.weather = ["Clear", 0]
        self.terrain = ["Clear", 0]
        # If true, then weather will not be taken into consideration
        self.cloudNine = False
        # The names of the last move used
        self.lastMove = [None, None]
        # Adds teams to window
        self.team1.addToWin(self.win)
        self.team2.addToWin(self.win)
        # Text box with information seeable to user
        self.textBoxBottomLeft = Point(3,3)
        self.textBoxTopRight = Point(497, 147)
        self.textBox = Rectangle(self.textBoxBottomLeft, self.textBoxTopRight)
        self.textBox.setWidth(6)
        self.textBox.draw(self.win)
        # The HP bar for both pokemon
        self.pokemon1HPBar = Rectangle(Point(277, 172), Point(411, 188))
        self.pokemon1HPBar.setFill("Grey")
        self.pokemon1HPBar.setWidth(0)
        self.pokemon1HPBar.draw(self.win)
        self.pokemon1CurrentHP = Rectangle(Point(0,0), Point(0,0))
        self.HPText = Text(Point(0,0), "")
        self.pokemon2HPBar = Rectangle(Point(61, 362), Point(195, 378))
        self.pokemon2HPBar.setFill("Grey")
        self.pokemon2HPBar.setWidth(0)
        self.pokemon2HPBar.draw(self.win)
        self.pokemon2CurrentHP = Rectangle(Point(0,0), Point(0,0))
        # Picture of both teams' active pokemon
        self.pokemon11Picture = Rectangle(Point(0,0), Point(0,0))
        self.pokemon12Picture = Rectangle(Point(0,0), Point(0,0))
        self.pokemon21Picture = Rectangle(Point(0,0), Point(0,0))
        self.pokemon22Picture = Rectangle(Point(0,0), Point(0,0))
        self.pokemon31Picture = Rectangle(Point(0,0), Point(0,0))
        self.pokemon32Picture = Rectangle(Point(0,0), Point(0,0))
        self.pokemon1Name = Text(Point(0,0), "")
        self.pokemon2Name = Text(Point(0,0), "")
        # Status condition of both active pokemon
        self.statusBar1 = Rectangle(Point(0,0), Point(0,0))
        self.statusBar2 = Rectangle(Point(0,0), Point(0,0))
        self.statusText1 = Text(Point(0,0), "")
        self.statusText2 = Text(Point(0,0), "")
        # The pokeballs for both teams that show the condition of each pokemon
        self.pokeball11 = Circle(Point(282, 198), 5)
        self.pokeball12 = Circle(Point(297, 198), 5)
        self.pokeball13 = Circle(Point(312, 198), 5)
        self.pokeball14 = Circle(Point(327, 198), 5)
        self.pokeball15 = Circle(Point(342, 198), 5)
        self.pokeball16 = Circle(Point(357, 198), 5)
        self.pokeball21 = Circle(Point(66, 352), 5)
        self.pokeball22 = Circle(Point(81, 352), 5)
        self.pokeball23 = Circle(Point(96, 352), 5)
        self.pokeball24 = Circle(Point(111, 352), 5)
        self.pokeball25 = Circle(Point(126, 352), 5)
        self.pokeball26 = Circle(Point(141, 352), 5)
        self.pokeballList = [self.pokeball11, self.pokeball12, self.pokeball13, 
                             self.pokeball14, self.pokeball15, self.pokeball16, 
                             self.pokeball21, self.pokeball22, self.pokeball23, 
                             self.pokeball24, self.pokeball25, self.pokeball26]
        # Gender symbols for both teams
        self.pokemon1GenderCircle = Circle(Point(0,0), 0)
        self.pokemon2GenderCircle = Circle(Point(0,0), 0)
        self.GenderLine11 = Line(Point(0,0), Point(0,0))
        self.GenderLine12 = Line(Point(0,0), Point(0,0))
        self.GenderLine13 = Line(Point(0,0), Point(0,0))
        self.GenderLine21 = Line(Point(0,0), Point(0,0))
        self.GenderLine22 = Line(Point(0,0), Point(0,0))
        self.GenderLine23 = Line(Point(0,0), Point(0,0))
        # Shiny symbols for both teams
        self.shiny1 = Polygon([Point(210, 184), Point(220, 184), Point(212, 176.5),
                                       Point(215, 187), Point(218, 176.5), Point(210, 184)])
        self.shiny1.setFill("Red")
        self.shiny1.setOutline("Red")
        self.shiny2 = Polygon([Point(202, 374), Point(212, 374), Point(204, 366.5),
                                       Point(207, 377), Point(209, 366.5), Point(202, 374)])
        self.shiny2.setFill("Red")
        self.shiny2.setOutline("Red")
        # Level of both active pokemon
        self.Level1 = Text(Point(0,0), "")
        self.Level2 = Text(Point(0,0), "")
        # Mega symbol for both active Pokemon
        self.megaSymbol1 = Circle(Point(0,0), 0)
        self.megaSymbol2 = Circle(Point(0,0), 0)
        
    def drawCurrentText(self, text):
        self.currentText = Text(Point(250,75), text)
        self.currentText.draw(self.win)
        self.win.getMouse()
        self.currentText.undraw()
    # Adjusts the health bar to reflect remaining HP    
    def healthBar(self):
        # Undraws the health bar
        self.pokemon1CurrentHP.undraw()
        self.pokemon2CurrentHP.undraw()
        self.HPText.undraw()
        self.statusBar1.undraw()
        self.statusBar2.undraw()
        self.statusText1.undraw()
        self.statusText2.undraw()
        self.Level1.undraw()
        self.Level2.undraw()
        self.pokemon11Picture.undraw()
        self.pokemon21Picture.undraw()
        self.pokemon31Picture.undraw()
        self.pokemon12Picture.undraw()
        self.pokemon22Picture.undraw()
        self.pokemon32Picture.undraw()
        # Changes the color of the pokeballs to reflect status condition
        # Black means the pokemon has fainted
        # Grey means the pokemon has a status condition
        # Red means the pokemon is healthy
        # Yellow border means the active pokemon
        for pokemonNumber in range(6):
            self.pokeballList[pokemonNumber].undraw()
            self.pokeballList[pokemonNumber + 6].undraw()
            
            if self.team1.pokemonList[pokemonNumber].currentHp <= 0:
                self.pokeballList[pokemonNumber].setFill("Black")
            elif not self.team1.pokemonList[pokemonNumber].status == "Healthy":
                self.pokeballList[pokemonNumber].setFill("Grey")
            else:
                self.pokeballList[pokemonNumber].setFill("Red")
                
            if self.team2.pokemonList[pokemonNumber].currentHp <= 0:
                self.pokeballList[pokemonNumber + 6].setFill("Black")
            elif not self.team2.pokemonList[pokemonNumber].status == "Healthy":
                self.pokeballList[pokemonNumber + 6].setFill("Grey")
            else:
                self.pokeballList[pokemonNumber + 6].setFill("Red")
            
            if self.team1.pokemonList[pokemonNumber] == self.team1.activePokemon:
                self.pokeballList[pokemonNumber].setOutline("Yellow")
                self.pokeballList[pokemonNumber].setWidth(3)
            else:
                self.pokeballList[pokemonNumber].setOutline("Black")
                self.pokeballList[pokemonNumber].setWidth(1)
                
            if self.team2.pokemonList[pokemonNumber] == self.team2.activePokemon:
                self.pokeballList[pokemonNumber + 6].setOutline("Yellow")
                self.pokeballList[pokemonNumber + 6].setWidth(3)
            else:
                self.pokeballList[pokemonNumber + 6].setOutline("Black")
                self.pokeballList[pokemonNumber + 6].setWidth(1)
            
            self.pokeballList[pokemonNumber].draw(self.win)    
            self.pokeballList[pokemonNumber + 6].draw(self.win)
        # Changes the background color to reflect terrain
        if self.terrain[0] == "Grassy Terrain":
            self.win.setBackground(color_rgb(81,155,18))
        elif self.terrain[0] == "Psychic Terrain":
            self.win.setBackground(color_rgb(237,69,129))
        elif self.terrain[0] == "Electric Terrain":
            self.win.setBackground(color_rgb(252,188,12))
        elif self.terrain[0] == "Misty Terrain":
            self.win.setBackground(color_rgb(245,176,245))
        else:
            self.win.setBackground("White")
        # The bar is drawn depending on the remaining HP
        if self.team1.activePokemon.currentHp == self.team1.activePokemon.Stats["HP"]:
            currentHPValue = 16
        elif self.team1.activePokemon.currentHp <= self.team1.activePokemon.Stats["HP"] / 16:
            currentHPValue = .5
        else:
            currentHPValue = floor(self.team1.activePokemon.currentHp / self.team1.activePokemon.Stats["HP"] * 16)
        # Green means the pokemon has more than 1/2 of its HP remaining
        # Red means the pokemon has less than 1/32 of its HP remaining
        # Yellow means the pokemon has HP between 1/32 and 1/2
        self.pokemon1CurrentHP = Rectangle(Point(280, 175), Point(280 + currentHPValue * 8, 185))
        if currentHPValue >= 8:
            self.pokemon1CurrentHP.setFill("Green")
        elif currentHPValue <= .5:
            self.pokemon1CurrentHP.setFill("Red")
        else:
            self.pokemon1CurrentHP.setFill("Yellow")
        self.pokemon1CurrentHP.setWidth(0)
        self.pokemon1CurrentHP.draw(self.win)
        
        if self.team2.activePokemon.currentHp == self.team2.activePokemon.Stats["HP"]:
            currentHPValue = 16
        elif self.team2.activePokemon.currentHp <= self.team2.activePokemon.Stats["HP"] / 16:
            currentHPValue = .5
        else:
            currentHPValue = floor(self.team2.activePokemon.currentHp / self.team2.activePokemon.Stats["HP"] * 16)
            
        self.pokemon2CurrentHP = Rectangle(Point(64, 365), Point(64 + currentHPValue * 8, 375))
        if currentHPValue >= 8:
            self.pokemon2CurrentHP.setFill("Green")
        elif currentHPValue <= .5:
            self.pokemon2CurrentHP.setFill("Red")
        else:
            self.pokemon2CurrentHP.setFill("Yellow")
        self.pokemon2CurrentHP.setWidth(0)
        self.pokemon2CurrentHP.draw(self.win)
        
        self.HPText = Text(Point(450, 180), str(self.team1.activePokemon.currentHp) + "/" + str(self.team1.activePokemon.Stats["HP"]))
        self.HPText.draw(self.win)
        # Draws the status condition of the active pokemon
        if not self.team1.activePokemon.status == "Healthy":
            if self.team1.activePokemon.status in ["Sleep","Rest"]:
                statusText1 = "SLP"
                statusColor1 = [152,169,245]
            elif self.team1.activePokemon.status == "Poison":
                statusText1 = "PSN"
                if self.team1.activePokemon.volatile["Badly Poison"] > 0:
                    statusColor1 = [90, 30, 92]
                else:
                    statusColor1 = [115,38,117]
            elif self.team1.activePokemon.status == "Burn":
                statusText1 = "BRN"
                statusColor1 = [217,48,6]
            elif self.team1.activePokemon.status == "Paralyze":
                statusText1 = "PRZ"
                statusColor1 = [252,188,12]
            elif self.team1.activePokemon.status == "Freeze":
                statusText1 = "FRZ"
                statusColor1 = [173,234,254]
            self.statusBar1 = Rectangle(Point(241,172), Point(271,188))
            self.statusBar1.setFill(color_rgb(statusColor1[0], statusColor1[1], statusColor1[2]))
            self.statusBar1.setWidth(2)
            self.statusBar1.draw(self.win)
            
            self.statusText1 = Text(Point(256,180), statusText1)
            self.statusText1.setSize(10)
            self.statusText1.draw(self.win)
            
        if not self.team2.activePokemon.status == "Healthy":
            if self.team2.activePokemon.status in ["Sleep","Rest"]:
                statusText2 = "SLP"
                statusColor2 = [152,169,245]
            elif self.team2.activePokemon.status == "Poison":
                statusText2 = "PSN"
                if self.team2.activePokemon.volatile["Badly Poison"] > 0:
                    statusColor2 = [90, 30, 92]
                else:
                    statusColor2 = [115,38,117]
            elif self.team2.activePokemon.status == "Burn":
                statusText2 = "BRN"
                statusColor2 = [217,48,6]
            elif self.team2.activePokemon.status == "Paralyze":
                statusText2 = "PRZ"
                statusColor2 = [252,188,12]
            elif self.team2.activePokemon.status == "Freeze":
                statusText2 = "FRZ"
                statusColor2 = [173,234,254]
            self.statusBar2 = Rectangle(Point(25,362), Point(55,378))
            self.statusBar2.setFill(color_rgb(statusColor2[0], statusColor2[1], statusColor2[2]))
            self.statusBar2.setWidth(2)
            self.statusBar2.draw(self.win)
            
            self.statusText2 = Text(Point(40,370), statusText2)
            self.statusText2.setSize(10)
            self.statusText2.draw(self.win)
        # Draws the level of the active Pokemon    
        self.Level1 = Text(Point(382, 198), "LV: " + str(self.team1.activePokemon.Level))
        self.Level1.setSize(8)
        self.Level1.draw(self.win)
        self.Level2 = Text(Point(166, 352), "LV: " + str(self.team2.activePokemon.Level))
        self.Level2.setSize(8)
        self.Level2.draw(self.win)
        # Draws pokemon, hiding the pokemon's identity if Illusion
        if self.team1.activePokemon.ability.abilityName == "Illusion" and self.team1.activePokemon.illusion:
            for positionNumber in range(6):
                if self.team1.pokemonList[positionNumber].currentHp > 0:
                    illusionPokemon = self.team1.pokemonList[positionNumber]
            self.pokemon11Picture, self.pokemon21Picture, self.pokemon31Picture = self.pokemonPicture(1, illusionPokemon.Type1, illusionPokemon.Type2, illusionPokemon.shiny)
        else:
            self.pokemon11Picture, self.pokemon21Picture, self.pokemon31Picture = self.pokemonPicture(1, self.team1.activePokemon.Type1, self.team1.activePokemon.Type2, self.team1.activePokemon.shiny)
        self.pokemon11Picture.draw(self.win)
        self.pokemon21Picture.draw(self.win)
        self.pokemon31Picture.draw(self.win)
        if self.team2.activePokemon.ability.abilityName == "Illusion" and self.team2.activePokemon.illusion:
            for positionNumber in range(6):
                if self.team2.pokemonList[positionNumber].currentHp > 0:
                    illusionPokemon = self.team2.pokemonList[positionNumber]
            self.pokemon12Picture, self.pokemon22Picture, self.pokemon32Picture = self.pokemonPicture(2, illusionPokemon.Type1, illusionPokemon.Type2, illusionPokemon.shiny)
        else:
            self.pokemon12Picture, self.pokemon22Picture, self.pokemon32Picture = self.pokemonPicture(2, self.team2.activePokemon.Type1, self.team2.activePokemon.Type2, self.team2.activePokemon.shiny)
        self.pokemon12Picture.draw(self.win)
        self.pokemon22Picture.draw(self.win)
        self.pokemon32Picture.draw(self.win)
    # The main menu, which can pick attack, switch, or forfeit    
    def mainMenu(self):
        self.megaSymbol1.undraw()
        self.megaSymbol2.undraw()
        # Draws a symbol to show if a pokemon has mega evolved
        if "Mega " in self.team1.activePokemon.pokemonName:
            self.megaSymbol1 = Circle(Point(125, 225), 10)
            self.megaSymbol1.setFill("Blue")
            self.megaSymbol1.draw(self.win)
        if "Mega " in self.team2.activePokemon.pokemonName:
            self.megaSymbol2 = Circle(Point(375, 345), 10)
            self.megaSymbol2.setFill("Blue")
            self.megaSymbol2.draw(self.win)
        # Shows important information to the user
        informationBoxBottomLeft = Point(0,0)
        informationBoxTopRight = Point(500/3, 150)
        informationBox = Rectangle(informationBoxBottomLeft, informationBoxTopRight)
        informationBox.setWidth(6)
        informationBox.setFill("White")
        informationBox.draw(self.win)
        if "As One" in self.team1.activePokemon.ability.abilityName:
            abilityText = "As One"
        else:
            abilityText = str(self.team1.activePokemon.ability.abilityName)
        informationString = "Item: " + str(self.team1.activePokemon.item) + "\nAbility: " + abilityText + "\nWeather: " + str(self.weather[0]) + "\nTerrain: " + str(self.terrain[0])
        informationText = Text(Point(250/3, 75), informationString)
        informationText.setSize(11)
        informationText.draw(self.win)
        # Attack button
        attackBottomLeft = Point(500/3, 75)
        attackTopRight = Point(1000/3, 150)
        attackBox = Rectangle(attackBottomLeft, attackTopRight)
        attackBox.setWidth(6)
        attackBox.setFill("Red")
        attackBox.draw(self.win)
        attackText = Text(Point(250, 112.5), "Attack")
        attackText.setSize(25)
        attackText.draw(self.win)
        # Switch button
        switchBottomLeft = Point(1000/3, 75)
        switchTopRight = Point(500, 150)
        switchBox = Rectangle(switchBottomLeft, switchTopRight)
        switchBox.setWidth(6)
        switchBox.setFill("Green")
        switchBox.draw(self.win)
        switchText = Text(Point(1250/3, 112.5), "Switch")
        switchText.setSize(25)
        switchText.draw(self.win)
        # Forfeit button
        forfeitBottomLeft = Point(500/3, 0)
        forfeitTopRight = Point(500, 75)
        forfeitBox = Rectangle(forfeitBottomLeft, forfeitTopRight)
        forfeitBox.setWidth(6)
        forfeitBox.setFill("Blue")
        forfeitBox.draw(self.win)
        forfeitText = Text(Point(1000/3, 37.5), "Forfeit")
        forfeitText.setSize(25)
        forfeitText.draw(self.win)
        # Waits until a button has been clicked
        clickedPoint = self.win.getMouse()
        while not Clicked(self.textBoxBottomLeft, self.textBoxTopRight, clickedPoint):
            clickedPoint = self.win.getMouse()
        # Undraws all buttons
        attackBox.undraw()
        switchBox.undraw()
        forfeitBox.undraw()
        informationBox.undraw()
        attackText.undraw()
        switchText.undraw()
        forfeitText.undraw()
        informationText.undraw()
        # Changes menu
        if Clicked(attackBottomLeft, attackTopRight, clickedPoint):
            return self.attackMenu()
        elif Clicked(switchBottomLeft, switchTopRight, clickedPoint):
            return self.switchMenu()
        elif Clicked(informationBoxBottomLeft, informationBoxTopRight, clickedPoint):
            return self.mainMenu()
        else:
            self.forfeitMenu()
            return ["forfeit", 1]
    # Attack menu with 4 moves    
    def attackMenu(self, forfeit = False, megaEvolve = False, zMove = False):
        # The colors for each of the types for moves
        typeColorDict = {"Bug" : [169,185,28], "Dark" : [0,0,0], "Dragon" : [78,61,153],
                         "Electric" : [252,188,12], "Fairy" : [245,176,245], "Fighting" : [128,51,27],
                         "Fire" : [217,48,6], "Flying" : [152,169,245], "Ghost" : [75,75,152],
                         "Grass" : [81,155,18], "Ground" : [211,179,86], "Ice" : [173,234,254],
                         "Normal" : [173,165,148], "Poison" : [115,38,117], "Psychic" : [237,69,129],
                         "Rock" : [158,134,61], "Steel" : [131,131,144], "Water" : [33,132,228]}
        # Attack 1 box
        attack1BottomLeft = Point(0,100)
        attack1TopRight = Point(250,150)
        attack1Box = Rectangle(attack1BottomLeft, attack1TopRight)
        attack1Box.setWidth(6)
        attack1Box.setFill(color_rgb(typeColorDict[self.team1.activePokemon.Moves[0].moveType.typeName][0],
                                     typeColorDict[self.team1.activePokemon.Moves[0].moveType.typeName][1],
                                     typeColorDict[self.team1.activePokemon.Moves[0].moveType.typeName][2]))
        attack1Box.draw(self.win)
        
        attack1String = self.team1.activePokemon.Moves[0].moveName + " " + str(self.team1.activePokemon.Moves[0].currentPP) + "/" + str(self.team1.activePokemon.Moves[0].pp)
        attack1Text = Text(Point(125,125), attack1String)
        # Readjusts size and color for long names and dark color types
        if len(attack1String) > 20:
            attack1Text.setSize(10)
        if self.team1.activePokemon.Moves[0].moveType.typeName in ["Dark", "Fighting", "Ghost"]:
            attack1Text.setFill("White")
        attack1Text.draw(self.win)
        # Attack 2 box
        attack2BottomLeft = Point(250,100)
        attack2TopRight = Point(500,150)
        attack2Box = Rectangle(attack2BottomLeft, attack2TopRight)
        attack2Box.setWidth(6)
        attack2Box.setFill(color_rgb(typeColorDict[self.team1.activePokemon.Moves[1].moveType.typeName][0],
                                     typeColorDict[self.team1.activePokemon.Moves[1].moveType.typeName][1],
                                     typeColorDict[self.team1.activePokemon.Moves[1].moveType.typeName][2]))
        attack2Box.draw(self.win)
        
        attack2String = self.team1.activePokemon.Moves[1].moveName + " " + str(self.team1.activePokemon.Moves[1].currentPP) + "/" + str(self.team1.activePokemon.Moves[1].pp)
        attack2Text = Text(Point(375,125), attack2String)
        if len(attack2String) > 20:
            attack2Text.setSize(10)
        if self.team1.activePokemon.Moves[1].moveType.typeName in ["Dark", "Fighting", "Ghost"]:
            attack2Text.setFill("White")
        attack2Text.draw(self.win)
        # Attack 3 box
        attack3BottomLeft = Point(0,50)
        attack3TopRight = Point(250,100)
        attack3Box = Rectangle(attack3BottomLeft, attack3TopRight)
        attack3Box.setWidth(6)
        attack3Box.setFill(color_rgb(typeColorDict[self.team1.activePokemon.Moves[2].moveType.typeName][0],
                                     typeColorDict[self.team1.activePokemon.Moves[2].moveType.typeName][1],
                                     typeColorDict[self.team1.activePokemon.Moves[2].moveType.typeName][2]))
        attack3Box.draw(self.win)
        
        attack3String = self.team1.activePokemon.Moves[2].moveName + " " + str(self.team1.activePokemon.Moves[2].currentPP) + "/" + str(self.team1.activePokemon.Moves[2].pp)
        attack3Text = Text(Point(125,75), attack3String)
        if len(attack3String) > 20:
            attack3Text.setSize(10)
        if self.team1.activePokemon.Moves[2].moveType.typeName in ["Dark", "Fighting", "Ghost"]:
            attack3Text.setFill("White")
        attack3Text.draw(self.win)
        # Attack 4 box
        attack4BottomLeft = Point(250,50)
        attack4TopRight = Point(500,100)
        attack4Box = Rectangle(attack4BottomLeft, attack4TopRight)
        attack4Box.setWidth(6)
        attack4Box.setFill(color_rgb(typeColorDict[self.team1.activePokemon.Moves[3].moveType.typeName][0],
                                     typeColorDict[self.team1.activePokemon.Moves[3].moveType.typeName][1],
                                     typeColorDict[self.team1.activePokemon.Moves[3].moveType.typeName][2]))
        attack4Box.draw(self.win)
        
        attack4String = self.team1.activePokemon.Moves[3].moveName + " " + str(self.team1.activePokemon.Moves[3].currentPP) + "/" + str(self.team1.activePokemon.Moves[3].pp)
        attack4Text = Text(Point(375,75), attack4String)
        if len(attack4String) > 20:
            attack4Text.setSize(10)
        if self.team1.activePokemon.Moves[3].moveType.typeName in ["Dark", "Fighting", "Ghost"]:
            attack4Text.setFill("White")
        attack4Text.draw(self.win)
        # Creates a mega button if applicable
        if "Mega" in self.team1.activePokemon.item.effect:
            megaRadius = 40
            megaCenter = Point(250, 100)
            megaCircle = Circle(megaCenter, megaRadius)
            megaText = Text(Point(250, 100), "Mega")
            if self.team1.mega:
                megaCircle.setFill("Black")
                megaText.setFill("White")
            else:
                if megaEvolve:
                    megaCircle.setFill("Blue")    
                else:
                    megaCircle.setFill("White")
                megaText.setFill("Black")
            megaCircle.draw(self.win)
            megaText.draw(self.win)
            zMoveCircle = Circle(Point(0,0), 0)
            zMoveText = Text(Point(0, 0), "") 
        # Creates a z move button if applicable
        elif "Z-Move" in self.team1.activePokemon.item.effect:
            zMoveRadius = 40
            zMoveCenter = Point(250, 100)
            zMoveCircle = Circle(zMoveCenter, zMoveRadius)
            zMoveText = Text(Point(250, 100), "Z-Move")
            if self.team1.zMove:
                zMoveCircle.setFill("Black")
                zMoveText.setFill("White")
            else:
                zMoveBool = False
                moveNumber = []
                if self.team1.activePokemon.item.secondEffect == "Specialty":
                    self.team1.activePokemon.Moves[6] = self.zMoveSignatureDict[self.team1.activePokemon.item.itemName][0]
                    if self.team1.activePokemon.Moves[6].moveName == "Light That Burns the Sky":
                        self.team1.activePokemon.Moves[6].phySpe = self.team1.activePokemon.photonGeyser
                    for move in range(4):
                        if self.team1.activePokemon.Moves[move] == None:
                            pass
                        elif self.team1.activePokemon.Moves[6].base == self.team1.activePokemon.Moves[move].moveName:
                            zMoveBool = True
                            moveNumber.append(move)
                else:
                    for move in range(4):
                        if self.team1.activePokemon.Moves[move] == None:
                            pass
                        elif self.team1.activePokemon.item.secondEffect == self.team1.activePokemon.Moves[move].moveType.typeName:
                            zMoveBool = True
                            moveNumber.append(move)
                if zMoveBool:
                    if zMove:
                        zMoveCircle.setFill("Yellow")
                    else:
                        zMoveCircle.setFill("White")
                    zMoveText.setFill("BLack")
                else:
                    zMoveCircle.setFill("Black")
                    zMoveText.setFill("White")
            zMoveCircle.draw(self.win)
            zMoveText.draw(self.win)
            megaCircle = Circle(Point(0,0), 0)
            megaText = Text(Point(0, 0), "")
        else:
            megaCircle = Circle(Point(0,0), 0)
            megaText = Text(Point(0, 0), "")
            zMoveCircle = Circle(Point(0,0), 0)
            zMoveText = Text(Point(0, 0), "") 
        # Back button to cancel option
        backBoxBottomLeft = Point(0,0)
        backBoxTopRight = Point(500,50)
        backBox = Rectangle(backBoxBottomLeft, backBoxTopRight)
        backBox.setWidth(6)
        backBox.setFill("Blue")
        backBox.draw(self.win)
        # Forfeit button replaces back button if trapped
        if forfeit:
            backText = Text(Point(250, 25), "Forfeit")
        else:
            backText = Text(Point(250, 25), "Back")
        backText.draw(self.win)
        # Loops until an attack is chosen
        clickedPoint = self.win.getMouse()
        while not Clicked(self.textBoxBottomLeft, self.textBoxTopRight, clickedPoint):
            clickedPoint = self.win.getMouse()
        # Undraws attack buttons
        attack1Box.undraw()
        attack2Box.undraw()
        attack3Box.undraw()
        attack4Box.undraw()
        attack1Text.undraw()
        attack2Text.undraw()
        attack3Text.undraw()
        attack4Text.undraw()
        megaCircle.undraw()
        megaText.undraw()
        zMoveCircle.undraw()
        zMoveText.undraw()
        backBox.undraw()
        backText.undraw()
        # Returns to main menu if back button is clicked
        if Clicked(backBoxBottomLeft, backBoxTopRight, clickedPoint):
            if forfeit:
                self.forfeitMenu()
                return ["forfeit", 1]
            else:
                return self.mainMenu()
        # Uses the attack Struggle if cannot attack
        for move in range(5):
            if not (self.team1.activePokemon.Moves[move].currentPP <= 0 or (move + 1) in self.team1.activePokemon.volatile["Blocked Moves"]):
                break
            if move == 5:
                return ["attack", 5, megaEvolve, zMove]
        # Mega evolves if selected
        if "Mega" in self.team1.activePokemon.item.effect and not self.team1.mega:
            if ClickedCircle(megaRadius, megaCenter, clickedPoint):
                if not megaEvolve:
                    return self.attackMenu(False, True)
                else:
                    return self.attackMenu()
        # Uses z move if seleceted
        elif "Z-Move" in self.team1.activePokemon.item.effect and not self.team1.zMove:
            if ClickedCircle(zMoveRadius, zMoveCenter, clickedPoint):
                if not zMove:
                    return self.attackMenu(False, False, True)
                else:
                    return self.attackMenu()
        # Chooses correct move depending on selected button
        if Clicked(attack1BottomLeft, attack1TopRight, clickedPoint):
            if self.team1.activePokemon.Moves[0].currentPP <= 0 or 1 in self.team1.activePokemon.volatile["Blocked Moves"]:
                return self.attackMenu()
            else:
                return ["attack", 1, megaEvolve, zMove]
        elif Clicked(attack2BottomLeft, attack2TopRight, clickedPoint):
            if self.team1.activePokemon.Moves[1].currentPP <= 0 or 2 in self.team1.activePokemon.volatile["Blocked Moves"]:
                return self.attackMenu()
            else:
                return ["attack", 2, megaEvolve, zMove]
        elif Clicked(attack3BottomLeft, attack3TopRight, clickedPoint):
            if self.team1.activePokemon.Moves[2].currentPP <= 0 or 3 in self.team1.activePokemon.volatile["Blocked Moves"]:
                return self.attackMenu()
            else:
                return ["attack", 3, megaEvolve, zMove]
        else:
            if self.team1.activePokemon.Moves[3].currentPP <= 0 or 4 in self.team1.activePokemon.volatile["Blocked Moves"]:
                return self.attackMenu()
            else:
                return ["attack", 4, megaEvolve, zMove]
    # The switch menu which switches the active pokemon
    def switchMenu(self):
        pokemonColorList = []
        # White is active pokemon
        # Green is high HP pokemon
        # Yellow is medium HP pokemon
        # Red is low HP pokemon
        # Grey is fainted pokemon
        for pokemon in self.team1.pokemonList:
            if pokemon == self.team1.activePokemon:
                pokemonColorList.append("White")
            elif pokemon.currentHp >= pokemon.Stats["HP"] * .5:
                pokemonColorList.append("Green")
            elif pokemon.currentHp >= pokemon.Stats["HP"] * .125:
                pokemonColorList.append("Yellow")
            elif pokemon.currentHp <= 0:
                pokemonColorList.append("Grey")
            else:
                pokemonColorList.append("Red")
        # Pokemon 1      
        pokemon1BoxBottomLeft = Point(0, 112.5)
        pokemon1BoxTopRight = Point(250, 150)
        pokemon1Box = Rectangle(pokemon1BoxBottomLeft, pokemon1BoxTopRight)
        pokemon1Box.setFill(pokemonColorList[0])
        pokemon1Box.setWidth(6)
        pokemon1Box.draw(self.win)
        pokemon1Text = Text(Point(125,131.25), self.team1.pokemonList[0].pokemonName + " " + str(self.team1.pokemonList[0].currentHp) + "/" + str(self.team1.pokemonList[0].Stats["HP"]))
        pokemon1Text.setSize(10)
        pokemon1Text.draw(self.win)
        # Pokemon 2
        pokemon2BoxBottomLeft = Point(250, 112.5)
        pokemon2BoxTopRight = Point(500, 150)
        pokemon2Box = Rectangle(pokemon2BoxBottomLeft, pokemon2BoxTopRight)
        pokemon2Box.setFill(pokemonColorList[1])
        pokemon2Box.setWidth(6)
        pokemon2Box.draw(self.win)
        pokemon2Text = Text(Point(375,131.25), self.team1.pokemonList[1].pokemonName + " " + str(self.team1.pokemonList[1].currentHp) + "/" + str(self.team1.pokemonList[1].Stats["HP"]))
        pokemon2Text.setSize(10)
        pokemon2Text.draw(self.win)
        # Pokemon 3
        pokemon3BoxBottomLeft = Point(0, 75)
        pokemon3BoxTopRight = Point(250, 112.5)
        pokemon3Box = Rectangle(pokemon3BoxBottomLeft, pokemon3BoxTopRight)
        pokemon3Box.setFill(pokemonColorList[2])
        pokemon3Box.setWidth(6)
        pokemon3Box.draw(self.win)
        pokemon3Text = Text(Point(125,93.75), self.team1.pokemonList[2].pokemonName + " " + str(self.team1.pokemonList[2].currentHp) + "/" + str(self.team1.pokemonList[2].Stats["HP"]))
        pokemon3Text.setSize(10)
        pokemon3Text.draw(self.win)
        # Pokemon 4
        pokemon4BoxBottomLeft = Point(250, 75)
        pokemon4BoxTopRight = Point(500, 112.5)
        pokemon4Box = Rectangle(pokemon4BoxBottomLeft, pokemon4BoxTopRight)
        pokemon4Box.setFill(pokemonColorList[3])
        pokemon4Box.setWidth(6)
        pokemon4Box.draw(self.win)
        pokemon4Text = Text(Point(375,93.75), self.team1.pokemonList[3].pokemonName + " " + str(self.team1.pokemonList[3].currentHp) + "/" + str(self.team1.pokemonList[3].Stats["HP"]))
        pokemon4Text.setSize(10)
        pokemon4Text.draw(self.win)
        # Pokemon 5
        pokemon5BoxBottomLeft = Point(0, 37.5)
        pokemon5BoxTopRight = Point(250, 75)
        pokemon5Box = Rectangle(pokemon5BoxBottomLeft, pokemon5BoxTopRight)
        pokemon5Box.setFill(pokemonColorList[4])
        pokemon5Box.setWidth(6)
        pokemon5Box.draw(self.win)
        pokemon5Text = Text(Point(125,56.25), self.team1.pokemonList[4].pokemonName + " " + str(self.team1.pokemonList[4].currentHp) + "/" + str(self.team1.pokemonList[4].Stats["HP"]))
        pokemon5Text.setSize(10)
        pokemon5Text.draw(self.win)
        # Pokemon 6
        pokemon6BoxBottomLeft = Point(250, 37.5)
        pokemon6BoxTopRight = Point(500, 75)
        pokemon6Box = Rectangle(pokemon6BoxBottomLeft, pokemon6BoxTopRight)
        pokemon6Box.setFill(pokemonColorList[5])
        pokemon6Box.setWidth(6)
        pokemon6Box.draw(self.win)
        pokemon6Text = Text(Point(375,56.25), self.team1.pokemonList[5].pokemonName + " " + str(self.team1.pokemonList[5].currentHp) + "/" + str(self.team1.pokemonList[5].Stats["HP"]))
        pokemon6Text.setSize(10)
        pokemon6Text.draw(self.win)
        # Back button
        backBoxBottomLeft = Point(0,0)
        backBoxTopRight = Point(500, 37.5)
        backBox = Rectangle(backBoxBottomLeft, backBoxTopRight)
        backBox.setFill("Blue")
        backBox.setWidth(6)
        backBox.draw(self.win)
        backBoxText = Text(Point(250, 18.75), "Back")
        backBoxText.draw(self.win)
        # Loops until a pokemon is selected
        clickedPoint = self.win.getMouse()
        while not Clicked(self.textBoxBottomLeft, self.textBoxTopRight, clickedPoint):
            clickedPoint = self.win.getMouse()
        # Undraws pokemon boxes
        pokemon1Box.undraw()
        pokemon1Text.undraw()
        pokemon2Box.undraw()
        pokemon2Text.undraw()
        pokemon3Box.undraw()
        pokemon3Text.undraw()
        pokemon4Box.undraw()
        pokemon4Text.undraw()
        pokemon5Box.undraw()
        pokemon5Text.undraw()
        pokemon6Box.undraw()
        pokemon6Text.undraw()
        backBox.undraw()
        backBoxText.undraw()
        # Returns to main menu if back button is selected
        # Otherwise, switches pokemon if it has at least 1 remaining HP
        if Clicked(backBoxBottomLeft, backBoxTopRight, clickedPoint):
            return self.mainMenu()
        elif Clicked(pokemon1BoxBottomLeft, pokemon1BoxTopRight, clickedPoint):
            if self.team1.pokemonList[0].currentHp <= 0:
                return self.switchMenu()
            else:
                return ["switch", 1]
        elif Clicked(pokemon2BoxBottomLeft, pokemon2BoxTopRight, clickedPoint):
            if self.team1.pokemonList[1].currentHp <= 0:
                return self.switchMenu()
            else:
                return ["switch", 2]
        elif Clicked(pokemon3BoxBottomLeft, pokemon3BoxTopRight, clickedPoint):
            if self.team1.pokemonList[2].currentHp <= 0:
                return self.switchMenu()
            else:
                return ["switch", 3]
        elif Clicked(pokemon4BoxBottomLeft, pokemon4BoxTopRight, clickedPoint):
            if self.team1.pokemonList[3].currentHp <= 0:
                return self.switchMenu()
            else:
                return ["switch", 4]
        elif Clicked(pokemon5BoxBottomLeft, pokemon5BoxTopRight, clickedPoint):
            if self.team1.pokemonList[4].currentHp <= 0:
                return self.switchMenu()
            else:
                return ["switch", 5]
        else:
            if self.team1.pokemonList[5].currentHp <= 0:
                return self.switchMenu()
            else:
                return ["switch", 6]
    # Faints all pokemon when a team gives up
    def forfeitMenu(self):
        for pokemon in self.team1.pokemonList:
            pokemon.currentHp = 0
        
        self.team1.alivePokemon = 0
        self.team1.activePokemon.Moves[0].currentPP = 1
    # Creates the matchup chart for attacking types
    def typeMatchup(self):
        # Freeze-Dry, Flying Press, and None are specific to the named moves for
        # the first two and struggle for the last
        typeNameList = ["Bug", "Dark", "Dragon", "Electric", "Fairy", "Fighting",
                     "Fire", "Flying", "Ghost", "Grass", "Ground", "Ice", "Normal",
                     "Poison", "Psychic", "Rock", "Steel", "Water", "Freeze-Dry", 
                     "Flying Press","None"]
        # The numbers are the corresponding names in the previous list
        # 1 is neutal effective
        # 2 is super effective
        # .5 is resisted
        # 0 is no effect
        typeMatchupDict = {0:[1,2,1,1,.5,.5,.5,.5,.5,2,1,1,1,.5,2,1,.5,1,1,1,1],
                           1:[1,.5,1,1,.5,.5,1,1,2,1,1,1,1,1,2,1,1,1,1,1,1],
                           2:[1,1,2,1,0,1,1,1,1,1,1,1,1,1,1,1,.5,1,1,1,1],
                           3:[1,1,.5,.5,1,1,1,2,1,.5,0,1,1,1,1,1,1,2,1,1,1],
                           4:[1,2,2,1,1,2,.5,1,1,1,1,1,1,.5,1,1,.5,1,1,1,1],
                           5:[.5,2,1,1,.5,1,1,.5,0,1,1,2,2,.5,.5,2,2,1,1,1,1],
                           6:[2,1,.5,1,1,1,.5,1,1,2,1,2,1,1,1,.5,2,.5,1,1,1],
                           7:[2,1,1,.5,1,2,1,1,1,2,1,1,1,1,1,.5,.5,1,1,1,1],
                           8:[1,.5,1,1,1,1,1,1,2,1,1,1,0,1,2,1,1,1,1,1,1],
                           9:[.5,1,.5,1,1,1,.5,.5,1,.5,2,1,1,.5,1,2,.5,2,1,1,1],
                           10:[.5,1,1,2,1,1,2,0,1,.5,1,1,1,2,1,2,2,1,1,1,1],
                           11:[1,1,2,1,1,1,.5,2,1,2,2,.5,1,1,1,1,.5,.5,1,1,1],
                           12:[1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,.5,.5,1,1,1,1],
                           13:[1,1,1,1,2,1,1,1,.5,2,.5,1,1,.5,1,.5,0,1,1,1,1],
                           14:[1,0,1,1,1,2,1,1,1,1,1,1,1,2,.5,1,.5,1,1,1,1],
                           15:[2,1,1,1,1,.5,2,2,1,1,.5,2,1,1,1,1,.5,1,1,1,1],
                           16:[1,1,1,.5,2,1,.5,1,1,1,1,2,1,1,1,2,.5,.5,1,1,1],
                           17:[1,1,.5,1,1,1,2,1,1,.5,2,1,1,1,1,2,1,.5,1,1,1],
                           18:[1,1,2,1,1,1,.5,2,1,2,2,.5,1,1,1,1,.5,2,1,1,1],
                           19:[1,2,1,.5,.5,2,1,.5,0,2,1,2,2,.5,.5,1,1,1,1,1,1],
                           20:[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]}
        self.typeList = []
        for attacking in range(21):
            self.typeList.append(Type(typeNameList[attacking]))
            for defending in range(21):
                self.typeList[attacking].setEffectiveness(typeNameList[defending],
                        typeMatchupDict[attacking][defending])
    # Points the types for pokemon and moves to the same type object
    def fixType(self):
        # Team 1's pokemon
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
        # Team 2's pokemon
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
        # Regular Z-Moves                    
        for zMove in self.zMoveDict:
            for Type in self.typeList:
                if self.zMoveDict[zMove].moveType.typeName == Type.typeName:
                    self.zMoveDict[zMove].moveType = Type
        # Pokemon specific Z-Moves            
        for zMove in self.zMoveSignatureDict:
            for Type in self.typeList:
                if self.zMoveSignatureDict[zMove][0].moveType.typeName == Type.typeName:
                    self.zMoveSignatureDict[zMove][0].moveType = Type
    # Switches in pokemon 1, with pokemon 2 being the active pokemon for the opposing team
    def switchIn(self, pokemon1, pokemon2):
        # Removes extreme weather
        if not pokemon1.ability.abilityName in ["Primordial Sea", "Desolate Land", "Delta Stream"] and not pokemon2.ability.abilityName in ["Primordial Sea", "Desolate Land", "Delta Stream"] and self.weather[1] > 10:
            self.weather = ["Clear", 0]
            self.drawCurrentText("The extreme weather vanished!")
        if pokemon1.ability.effect[0] == "Cloud Nine" and not pokemon2.ability.effect[0] == "Cloud Nine":
            self.cloudNine = False
        # Undraws pokemon 1
        self.pokemon11Picture.undraw()
        self.pokemon21Picture.undraw()
        self.pokemon31Picture.undraw()
        self.megaSymbol1.undraw()
        # Undraws pokemon 2
        self.pokemon12Picture.undraw()
        self.pokemon22Picture.undraw()
        self.pokemon32Picture.undraw()
        self.megaSymbol2.undraw()
        # Runs if team 1 switched in a pokemon
        if self.team1.activePokemon == pokemon1:
            self.pokemon1Name.undraw()
            self.pokemon1CurrentHP.undraw()
            self.pokemon1GenderCircle.undraw()
            self.GenderLine11.undraw()
            self.GenderLine12.undraw()
            self.GenderLine13.undraw()
            self.shiny1.undraw()
            # Changes Arceus' type to its plate
            if pokemon1.ability.abilityName == "Multitype":
                if "Plate" in pokemon1.item.itemName:
                    pokemon1.changeType(pokemon1.item.effect[0], "None", False)
                elif pokemon1.item.effect == "Z-Move":
                    pokemon1.changeType(pokemon1.item.secondEffect, "None", False)
                else:
                    pokemon1.changeType("Normal", "None", False)
            # Changes Silvally's type to its memory
            elif pokemon1.ability.abilityName == "RKS System":
                if "Memory" in pokemon1.item.itemName:
                    pokemon1.changeType(pokemon1.item.effect[0], "None", False)
                elif pokemon1.item.effect == "Z-Move":
                    pokemon1.changeType(pokemon1.item.secondEffect, "None", False)
                else:
                    pokemon1.changeType("Normal", "None", False)
            # Illusion pokemon look like the last alive pokemon on the team
            if pokemon1.ability.abilityName == "Illusion" and pokemon1.illusion:
                for positionNumber in range(6):
                    if self.team1.pokemonList[positionNumber].currentHp > 0:
                        illusionPokemon = self.team1.pokemonList[positionNumber]
                self.pokemon11Picture, self.pokemon21Picture, self.pokemon31Picture = self.pokemonPicture(1, illusionPokemon.Type1, illusionPokemon.Type2, illusionPokemon.shiny)
                pokemonName1List = illusionPokemon.pokemonName.split(" ")
            else:
                self.pokemon11Picture, self.pokemon21Picture, self.pokemon31Picture = self.pokemonPicture(1, pokemon1.Type1, pokemon1.Type2, pokemon1.shiny)
                pokemonName1List = self.team1.activePokemon.pokemonName.split(" ")
            # Draws new pokemon 1
            self.pokemon11Picture.draw(self.win)
            self.pokemon21Picture.draw(self.win)
            self.pokemon31Picture.draw(self.win)
            if pokemon2.ability.abilityName == "Illusion" and pokemon2.illusion:
                for positionNumber in range(6):
                    if self.team2.pokemonList[positionNumber].currentHp > 0:
                        illusionPokemon = self.team2.pokemonList[positionNumber]
                self.pokemon12Picture, self.pokemon22Picture, self.pokemon32Picture = self.pokemonPicture(2, illusionPokemon.Type1, illusionPokemon.Type2, illusionPokemon.shiny)
            else:
                self.pokemon12Picture, self.pokemon22Picture, self.pokemon32Picture = self.pokemonPicture(2, pokemon2.Type1, pokemon2.Type2, pokemon2.shiny)
            # Redraws new pokemon 2
            self.pokemon12Picture.draw(self.win)
            self.pokemon22Picture.draw(self.win)
            self.pokemon32Picture.draw(self.win)
            # Writes the pokemon's name, removing specific form information that
            # would take up space
            if pokemonName1List[0] == "Mega":
                pokemon1Name = pokemonName1List[1]
            elif pokemonName1List[0] in ["Tapu", "Mr.", "Mime", "Type:", "Iron", "Great", "Scream", "Flutter", "Slither", 
                                         "Sandy", "Brute", "Roaring", "Walking"]:
                pokemon1Name = pokemonName1List[0] + " " + pokemonName1List[1]
            elif not pokemon1.crunchName == "None":
                pokemon1Name = pokemon1.crunchName
            else:
                pokemon1Name = pokemonName1List[0]
            self.pokemon1Name = Text(Point(125 + 5 * len(pokemon1Name), 180), pokemon1Name)
            self.pokemon1Name.setSize(9)
            self.pokemon1Name.draw(self.win)
            # Draws gender symbol
            if pokemon1.gender in ["Male", "Female"]:
                self.pokemon1GenderCircle = Circle(Point(230, 180), 5)
                self.pokemon1GenderCircle.setWidth(2)
                if pokemon1.gender == "Male":
                    self.pokemon1GenderCircle.setOutline("Blue")
                    
                    self.GenderLine11 = Line(Point(230, 180), Point(237, 187))
                    self.GenderLine11.setFill("Blue")
                    self.GenderLine11.draw(self.win)
                    
                    self.GenderLine12 = Line(Point(233, 187), Point(237, 187))
                    self.GenderLine12.setFill("Blue")
                    self.GenderLine12.draw(self.win)
                    
                    self.GenderLine13 = Line(Point(237, 183), Point(237, 187))
                    self.GenderLine13.setFill("Blue")
                    self.GenderLine13.draw(self.win)
                else:
                    self.pokemon1GenderCircle.setOutline("Pink")
                    
                    self.GenderLine11 = Line(Point(230, 175), Point(230, 165))
                    self.GenderLine11.setFill("Pink")
                    self.GenderLine11.draw(self.win)
                    
                    self.GenderLine12 = Line(Point(225, 167.5), Point(235, 167.5))
                    self.GenderLine12.setFill("Pink")
                    self.GenderLine12.draw(self.win)
                self.pokemon1GenderCircle.setFill("White")
                self.pokemon1GenderCircle.draw(self.win)
            if "Mega " in pokemon1.pokemonName:
                self.megaSymbol1 = Circle(Point(125, 225), 10)
                self.megaSymbol1.setFill("Blue")
                self.megaSymbol1.draw(self.win)
            # Draws shiny symbol
            if pokemon1.shiny:
                self.shiny1.draw(self.win)
            # Draws HP bar
            self.healthBar()
        # Runs if team 2 switched in a pokemon
        # All code is the same just for the opposite team
        else:
            self.pokemon2Name.undraw()
            self.pokemon2CurrentHP.undraw()
            self.pokemon2GenderCircle.undraw()
            self.GenderLine21.undraw()
            self.GenderLine22.undraw()
            self.GenderLine23.undraw()
            self.shiny2.undraw()
            
            if pokemon1.ability.abilityName == "Multitype":
                if "Plate" in pokemon1.item.itemName:
                    pokemon1.changeType(pokemon1.item.effect[0], "None", False)
                elif pokemon1.item.effect == "Z-Move":
                    pokemon1.changeType(pokemon1.item.secondEffect, "None", False)
                else:
                    pokemon1.changeType("Normal", "None", False)
            elif pokemon1.ability.abilityName == "RKS System":
                if "Memory" in pokemon1.item.itemName:
                    pokemon1.changeType(pokemon1.item.effect[0], "None", False)
                elif pokemon1.item.effect == "Z-Move":
                    pokemon1.changeType(pokemon1.item.secondEffect, "None", False)
                else:
                    pokemon1.changeType("Normal", "None", False)
            if pokemon1.ability.abilityName == "Illusion" and pokemon1.illusion:
                for positionNumber in range(6):
                    if self.team1.pokemonList[positionNumber].currentHp > 0:
                        illusionPokemon = self.team1.pokemonList[positionNumber]
                self.pokemon11Picture, self.pokemon21Picture, self.pokemon31Picture = self.pokemonPicture(1, illusionPokemon.Type1, illusionPokemon.Type2, illusionPokemon.shiny)
            else:
                self.pokemon11Picture, self.pokemon21Picture, self.pokemon31Picture = self.pokemonPicture(1, pokemon1.Type1, pokemon1.Type2, pokemon1.shiny)
            self.pokemon11Picture.draw(self.win)
            self.pokemon21Picture.draw(self.win)
            self.pokemon31Picture.draw(self.win)
            if pokemon2.ability.abilityName == "Illusion" and pokemon2.illusion:
                for positionNumber in range(6):
                    if self.team2.pokemonList[positionNumber].currentHp > 0:
                        illusionPokemon = self.team2.pokemonList[positionNumber]
                self.pokemon12Picture, self.pokemon22Picture, self.pokemon32Picture = self.pokemonPicture(2, illusionPokemon.Type1, illusionPokemon.Type2, illusionPokemon.shiny)
                pokemonName2List = illusionPokemon.pokemonName.split(" ")
            else:
                self.pokemon12Picture, self.pokemon22Picture, self.pokemon32Picture = self.pokemonPicture(2, pokemon2.Type1, pokemon2.Type2, pokemon2.shiny)
                pokemonName2List = self.team2.activePokemon.pokemonName.split(" ")
            self.pokemon12Picture.draw(self.win)
            self.pokemon22Picture.draw(self.win)
            self.pokemon32Picture.draw(self.win)
            if pokemonName2List[0] == "Mega":
                pokemon2Name = pokemonName2List[1]
            elif pokemonName2List[0] in ["Tapu", "Mr.", "Mime", "Type:", "Iron", "Great", "Scream", "Flutter", "Slither", 
                                         "Sandy", "Brute", "Roaring", "Walking"]:
                pokemon2Name = pokemonName2List[0] + " " + pokemonName2List[1]
            elif not pokemon1.crunchName == "None":
                pokemon2Name = pokemon1.crunchName
            else:
                pokemon2Name = pokemonName2List[0]
            self.pokemon2Name = Text(Point(375 - 5 * len(pokemon2Name), 370), pokemon2Name)
            self.pokemon2Name.setSize(9)
            self.pokemon2Name.draw(self.win)
            
            if pokemon1.gender in ["Male", "Female"]:
                self.pokemon2GenderCircle = Circle(Point(14, 370), 5)
                self.pokemon2GenderCircle.setWidth(2)
                if pokemon1.gender == "Male":
                    self.pokemon2GenderCircle.setOutline("Blue")
                    
                    self.GenderLine21 = Line(Point(14, 370), Point(21, 377))
                    self.GenderLine21.setFill("Blue")
                    self.GenderLine21.draw(self.win)
                    
                    self.GenderLine22 = Line(Point(17, 377), Point(21, 377))
                    self.GenderLine22.setFill("Blue")
                    self.GenderLine22.draw(self.win)
                    
                    self.GenderLine23 = Line(Point(21, 373), Point(21, 377))
                    self.GenderLine23.setFill("Blue")
                    self.GenderLine23.draw(self.win)
                else:
                    self.pokemon2GenderCircle.setOutline("Pink")
                    
                    self.GenderLine21 = Line(Point(14, 365), Point(14, 355))
                    self.GenderLine21.setFill("Pink")
                    self.GenderLine21.draw(self.win)
                    
                    self.GenderLine22 = Line(Point(9, 357.5), Point(19, 357.5))
                    self.GenderLine22.setFill("Pink")
                    self.GenderLine22.draw(self.win)
                self.pokemon2GenderCircle.setFill("White")
                self.pokemon2GenderCircle.draw(self.win)
            if "Mega " in pokemon2.pokemonName:
                self.megaSymbol2 = Circle(Point(375, 325), 10)
                self.megaSymbol2.setFill("Blue")
                self.megaSymbol2.draw(self.win)
            
            if pokemon1.shiny:
                self.shiny2.draw(self.win)
                
            self.healthBar()
        # Frees trapped pokemon and removes infatuation
        pokemon2.volatile["Trap"] = 0
        pokemon2.volatile["Block Condition"] = "None"
        pokemon2.volatile["Infatuation"] = 0
        # Decreases mass if holding the item Float Stone
        if pokemon1.item.itemName == "Float Stone":
            pokemon1.currentMass *= .5
        # Turns off abilities if either pokemon has the ability Neutralizing Gas
        if pokemon1.ability.abilityName == "Neutralizing Gas" and not (pokemon2.ability.abilityName == "Neutralizing Gas"):
            if pokemon1.ability == "Klutz":
                pokemon1.item.consumed = False
            pokemon2.ability.neutralize()
            self.drawCurrentText("Neutralizing gas filled the area!")
        elif pokemon2.ability.abilityName == "Neutralizing Gas" and not (pokemon1.ability.abilityName == "Neutralizing Gas"):
            if pokemon2.ability == "Klutz":
                pokemon2.item.consumed = False
            pokemon1.ability.neutralize()
        else:
            # Turns off neutralizing gas if neither pokemon have it as an ability
            if pokemon2.ability.neutralizeState == 1:
                pokemon2.ability.deneutralize()
                if pokemon1.ability == "Klutz":
                    pokemon1.item.Consume()
                self.switchIn(pokemon2, pokemon1)
            # Activates switch in abilites
            if pokemon1.ability.effect[0] == "Activate":
                if pokemon1.ability.target == "Opponent":
                    # Transforms pokemon with the ability Imposter
                    if pokemon1.ability.abilityName == "Imposter":
                        if not (pokemon1.transformed or pokemon2.transformed):
                            pokemon1.tempPokemon = [pokemon1.Stats, pokemon1.ability, pokemon1.tempType1.typeName, pokemon1.tempType2.typeName, pokemon1.Moves]
                            pokemon1.Stats = copy.deepcopy(pokemon2.Stats)
                            pokemon1.Stats["HP"] = pokemon1.tempPokemon[0]["HP"]
                            pokemon1.ability = pokemon2.ability
                            pokemon1.changeType(pokemon2.tempType1.typeName, pokemon2.tempType2.typeName, False)
                            pokemon1.Moves = copy.deepcopy(pokemon2.Moves)
                            for movePP in range(4):
                                pokemon1.Moves[movePP].currentPP = 5
                            pokemon1.transformed = True
                            self.drawCurrentText(pokemon1.pokemonName + " transformed into " + pokemon2.pokemonName + "!")
                            self.switchIn(pokemon1, pokemon2)
                    # Lowers stat of opposing pokemon as long as the ability does not
                    # cancel out Intimidate
                    elif not (pokemon1.ability.abilityName == "Intimidate" and (pokemon2.ability.abilityName in ["Inner Focus", "Oblivious", "Scrappy", "Own Tempo", "Hyper Cutter"] or (pokemon2.ability.effect[0] == "Clear Body" and pokemon2.ability.effect[1] == "All"))):
                        pokemon2.modifyStat(pokemon1.ability.effect[1], str(int(pokemon1.ability.success)), False)
                        # Rattled pokemon boost speed after being Intimidated
                        if pokemon1.ability.abilityName == "Intimidate" and pokemon2.ability.abilityName == "Rattled":
                            pokemon2.modifyStat("Speed", "1", True)
                # Changes the weather
                elif pokemon1.ability.effect[2] == "Weather":
                    if self.weather[0] != pokemon1.ability.effect[1] and not pokemon1.ability.abilityName in ["Primordial Sea", "Desolate Land", "Delta Stream"] and not pokemon2.ability.abilityName in ["Primordial Sea", "Desolate Land", "Delta Stream"]:
                        if pokemon1.ability.effect[1] in pokemon1.item.effect and not pokemon1.item.consumed:
                            self.weather = [pokemon1.ability.effect[1], 8]
                        else:
                            self.weather = [pokemon1.ability.effect[1], 5]
                        if self.weather[0] == "Rain Dance":
                            self.drawCurrentText("It started to rain!")
                        elif self.weather[0] == "Sunny Day":
                            self.drawCurrentText("The sunlight turned harsh!")
                        elif self.weather[0] == "Hail":
                            self.drawCurrentText("It started to hail!")
                        elif self.weather[0] == "Sandstorm":
                            self.drawCurrentText("A sandstorm kicked up!")
                    # Weather does not change if extreme weather is active
                    elif pokemon2.ability.abilityName in ["Primordial Sea", "Desolate Land", "Delta Stream"] and not pokemon1.ability.abilityName in ["Primordial Sea", "Desolate Land", "Delta Stream"]:
                        self.drawCurrentText(pokemon2.pokemonName + "'s " + pokemon2.ability.abilityName + " prevented the weather from changing!")
                    # Changes to extreme weather
                    elif pokemon1.ability.abilityName in ["Primordial Sea", "Desolate Land", "Delta Stream"]:
                        self.weather = [pokemon1.ability.effect[1], 999]
                        if pokemon1.ability.abilityName == "Primordial Sea":
                            self.drawCurrentText("A heavy rain began to fall!")
                        elif pokemon1.ability.abilityName == "Desolate Land":
                            self.drawCurrentText("The sunlight turned extremely harsh!")
                        else:
                            self.drawCurrentText("A mysterious air current is protecting Flying Pokemon!")
                # Removes light screen and reflect from the opponent
                elif pokemon1.ability.effect[1] == "Screens":
                    self.team1.reflect = 0
                    self.team1.lightScreen = 0
                    self.team2.reflect = 0
                    self.team2.lightScreen = 0
                # Changes the terrain
                elif pokemon1.ability.effect[2] == "Terrain":
                    if self.terrain[0] != pokemon1.ability.effect[1]:
                        if pokemon1.item.itemName == "Terrain Extender":
                            self.terrain = [pokemon1.ability.effect[1], 8]
                        else:
                            self.terrain = [pokemon1.ability.effect[1], 5]
                        self.drawCurrentText(pokemon1.pokemonName + " created a " + pokemon1.ability.abilityName + "!")
                        # Mimicry changes Galarian Stunfisk depending on terrain
                        if pokemon2.ability.abilityName == "Mimicry":
                            if self.terrain[0] == "Grassy Terrain":
                                newType = "Grass"
                            elif self.terrain[0] == "Misty Terrain":
                                newType = "Fairy"
                            elif self.terrain[0] == "Electric Terrain":
                                newType = "Electric"
                            elif self.terrain[0] == "Psychic Terrain":
                                newType = "Psychic"
                            pokemon2.changeType(newType, "None", False)
                # Boosts pokemon 1's stat upon switchin in
                elif pokemon1.ability.effect[1] == "Boost":
                    if pokemon1.ability.abilityName == "Download":
                        if pokemon2.Stats["Defense"] * pokemon2.statModifier["Defense"] <= pokemon2.Stats["Special Defense"] * pokemon2.statModifier["Special Defense"]:
                            pokemon1.modifyStat("Special Attack", "1", True)
                        else:
                            pokemon1.modifyStat("Attack", "1", True)
                    else:
                        pokemon1.modifyStat(pokemon1.ability.effect[2], "1", True)
                # Warns about the opponent's strongest move
                elif pokemon1.ability.effect[1] == "Warning":
                    strongestMove = 0
                    strongestPosition = 0
                    for moveNumber in range(4):
                        if pokemon2.Moves[moveNumber].stat in ["Level Damage", "Set Damage"] or pokemon2.Moves[moveNumber].moveName in ["Electro Ball", "Flail", "Fling", "Gyro Ball", "Reversal", "Trump Card"]:
                            power = 80
                        else:
                            power = pokemon2.Moves[moveNumber].power
                        if strongestMove < power:
                            strongestMove = power
                            strongestPosition = moveNumber
                        elif strongestMove == power and randint(0,1) == 1:
                            strongestMove = power
                            strongestPosition = moveNumber
                    self.drawCurrentText(pokemon1.pokemonName + " was warned about " + pokemon2.Moves[strongestPosition].moveName + "!")
                # Shudders if the opponent has any OHKO or super effective moves
                elif pokemon1.ability.effect[1] == "Shudder":
                    for moveNumber in range(4):
                        if pokemon2.Moves[moveNumber].stat == "OHKO":
                            self.drawCurrentText(pokemon1.pokemonName + " shuddered!")
                            break
                        else:
                            if pokemon1.Type2 == None:
                                typeEffect = pokemon2.Moves[moveNumber].moveType.effectDict[pokemon1.Type1.typeName]
                            else:
                                typeEffect = pokemon2.Moves[moveNumber].moveType.effectDict[pokemon1.Type1.typeName] * pokemon2.Moves[moveNumber].moveType.effectDict[pokemon1.Type2.typeName]
                            if typeEffect > 1 and pokemon2.Moves[moveNumber].power > 0:
                                self.drawCurrentText(pokemon1.pokemonName + " shuddered!")
                                break
                # Frisks the opponent's item
                elif pokemon1.ability.effect[0] == "Item" and not pokemon2.item.consumed:
                    self.drawCurrentText(pokemon2.pokemonName + " had its " + pokemon2.item.itemName + " frisked!")
                # Traces the opponent's abilit
                elif pokemon1.ability.abilityName == "Trace":
                    pokemon1.ability.tempAbility = [pokemon1.ability.abilityName, pokemon1.ability.target,
                                                    pokemon1.ability.effect, pokemon1.ability.success]
                    pokemon1.ability.abilityName = pokemon2.ability.abilityName
                    pokemon1.ability.target = pokemon2.ability.target
                    pokemon1.ability.effect = pokemon2.ability.effect
                    pokemon1.ability.success = pokemon2.ability.success
                    pokemon1.ability.trace = True
                    self.drawCurrentText(pokemon1.pokemonName + " traced " + pokemon1.ability.abilityName + "!")
                    self.switchIn(pokemon1, pokemon2)
                # Adjusts mass
                elif pokemon1.ability.effect[0] == "Mass":
                    pokemon1.currentMass *= pokemon1.ability.success
                # Eliminates the effects of weather
                elif pokemon1.ability.effect[0] == "Cloud Nine":
                    self.cloudNine = True
                    self.drawCurrentText("The effects of weather were locked!")
            # Displays a message to show what ability the switched in team's  
            # active pokemon has
            elif pokemon1.ability.effect[0] == "Mold Breaker":
                self.drawCurrentText(pokemon1.pokemonName + " breaks the mold!")
            elif pokemon1.ability.abilityName == "Pressure":
                self.drawCurrentText(pokemon1.pokemonName + " is exerting its pressure!")
            elif pokemon1.ability.abilityName == "Unnerve" or "As One" in pokemon1.ability.abilityName:
                self.drawCurrentText(pokemon2.pokemonName + " is too nervous to eat berries!")
            elif pokemon1.ability.abilityName == "Supreme Overlord":
                self.drawCurrentText(pokemon1.pokemonName + " is avenging its fallen teammates!")
            elif pokemon1.ability.abilityName == "Slow Start":
                self.drawCurrentText(pokemon1.pokemonName + " couldn't get going!")
            # Boosts stat
            elif pokemon1.ability.effect[0] == "Booster Energy":
                if self.cloudNine:
                    pokemon1.energyBoost("None", self.terrain[0])
                else:
                    pokemon1.energyBoost(self.weather[0], self.terrain[0])
                if pokemon1.boosterEnergy[2]:
                    self.drawCurrentText(pokemon1.pokemonName + " boosted its " + pokemon1.boosterEnergy[1] + " with its " + pokemon1.ability.abilityName + "!")
            # Traps the opponent
            elif pokemon1.ability.effect[0] == "Trapping" and not (pokemon2.Type1.typeName == "Ghost" or pokemon2.Type2.typeName == "Ghost"):
                if pokemon1.ability.effect[1] == "Steel" and (pokemon2.Type1.typeName == "Steel" or pokemon2.Type2.typeName == "Steel"):
                    pokemon2.volatile["Block Condition"] = "Mean Look"
                elif pokemon1.ability.effect[1] == "Ground" and not (pokemon2.Type1.typeName == "Flying" or pokemon2.Type2.typeName == "Flying" or pokemon2.ability.abilityName == "Levitatie"):
                    pokemon2.volatile["Block Condition"] = "Mean Look"
                elif pokemon1.ability.abilityName == "Shadow Tag":
                    pokemon2.volatile["Block Condition"] = "Mean Look"
    # Creates a picture using the pokemon's types and shiny value                
    def pokemonPicture(self, teamNumber, type1, type2, shiny):
        typeColorDict = {"Bug" : [169,185,28], "Dark" : [0,0,0], "Dragon" : [78,61,153],
                         "Electric" : [252,188,12], "Fairy" : [245,176,245], "Fighting" : [128,51,27],
                         "Fire" : [217,48,6], "Flying" : [152,169,245], "Ghost" : [75,75,152],
                         "Grass" : [81,155,18], "Ground" : [211,179,86], "Ice" : [173,234,254],
                         "Normal" : [173,165,148], "Poison" : [115,38,117], "Psychic" : [237,69,129],
                         "Rock" : [158,134,61], "Steel" : [131,131,144], "Water" : [33,132,228]}
        # Saves types as a string
        type1Name = type1.typeName
        if type2.typeName == "None":
            type2Name = type1.typeName
        else:
            type2Name = type2.typeName
        # Picks colors based on types
        type1ColorList = typeColorDict[type1Name]
        type2ColorList = typeColorDict[type2Name]
        if shiny:
            type1ColorList = [252 - type1ColorList[0], 252 - type1ColorList[1], 252 - type1ColorList[2]]
            type2ColorList = [252 - type2ColorList[0], 252 - type2ColorList[1], 252 - type2ColorList[2]]
        type1Color = color_rgb(type1ColorList[0], type1ColorList[1], type1ColorList[2])
        type2Color = color_rgb(type2ColorList[0], type2ColorList[1], type2ColorList[2])
        # Bug type
        if type1Name == "Bug":
            pokemon1Picture = Circle(Point(75,210), 50)
            pokemon1Picture.setFill(type2Color)
            
            pokemon2Picture = Line(Point(30, 230), Point(120, 230))
            pokemon2Picture.setWidth(3)
            
            pokemon3Picture = Line(Point(75, 160), Point(75, 230))
            pokemon3Picture.setWidth(3)
            
            if type1Name == type2Name:
                pokemon2Picture.setFill("Black")
                pokemon3Picture.setFill("Black")    
            else:
                pokemon2Picture.setFill(type1Color)
                pokemon3Picture.setFill(type1Color)
        # Dark type
        elif type1Name == "Dark":
            pokemon1Picture = Circle(Point(75,210), 50)
            pokemon1Picture.setFill(type2Color)
            
            pokemon2Picture = Circle(Point(75,235), 25)
            pokemon2Picture.setFill("White")
            
            pokemon3Picture =  Rectangle(Point(0,0), Point(0,0))
        # Dragon type
        elif type1Name == "Dragon":
            if teamNumber == 1:
                pokemon1Picture = Oval(Point(75,200), Point(125, 260))
                pokemon1Picture.setFill(type2Color)
                
                pokemon2Picture = Oval(Point(45,160), Point(105, 230))
                pokemon2Picture.setFill(type2Color)
                
                pokemon3Picture = Polygon(Point(65, 210), Point(65, 250), Point(25, 230), Point(55, 225), Point(30, 220))
                pokemon3Picture.setFill(type2Color)
                
            else:
                pokemon1Picture = Oval(Point(45,160), Point(105, 230))
                pokemon1Picture.setFill(type2Color)
                
                pokemon2Picture = Oval(Point(75,200), Point(25, 260))
                pokemon2Picture.setFill(type2Color)
                
                pokemon3Picture = Polygon(Point(85, 210), Point(85, 250), Point(125, 230), Point(95, 225), Point(120, 220))
                pokemon3Picture.setFill(type2Color)
        # Electric type
        elif type1Name == "Electric":
            pokemon1Picture = Polygon(Point(25, 160), Point(110, 230), Point(75, 230), Point(125, 260), Point(95, 260), Point(25, 218), Point(75, 218))
            pokemon1Picture.setFill(type2Color)
            
            pokemon2Picture =  Rectangle(Point(0,0), Point(0,0))
            pokemon3Picture =  Rectangle(Point(0,0), Point(0,0))
        # Fairy Type
        elif type1Name == "Fairy":
            pokemon1Picture = Circle(Point(100, 235), 25)
            pokemon1Picture.setFill(type2Color)
            pokemon1Picture.setOutline(type2Color)
            
            pokemon2Picture = Circle(Point(50, 235), 25)
            pokemon2Picture.setFill(type2Color)
            pokemon2Picture.setOutline(type2Color)
            
            pokemon3Picture =  Polygon(Point(25, 235), Point(125, 235), Point(75, 160))
            pokemon3Picture.setFill(type2Color)
            pokemon3Picture.setOutline(type2Color)
       # Fighting type
        elif type1Name == "Fighting":
            pokemon1Picture = Circle(Point(75,210), 40)
            pokemon1Picture.setFill(type2Color)
            
            pokemon2Picture = Circle(Point(100,195), 20)
            pokemon2Picture.setFill(type2Color)
            pokemon2Picture.setWidth(3)

            pokemon3Picture =  Rectangle(Point(0,0), Point(0,0))
        # Fire type
        elif type1Name == "Fire":
            pokemon1Picture = Circle(Point(75,200), 40)
            pokemon1Picture.setFill(type2Color)
            pokemon1Picture.setOutline(type2Color)
                
            pokemon2Picture = Circle(Point(75,190), 30)
            if type1Name == type2Name:
                pokemon2Picture.setFill("Yellow")
                pokemon2Picture.setOutline("Yellow")
            else:
                pokemon2Picture.setFill(type1Color)
                pokemon2Picture.setOutline(type1Color)
            
            pokemon3Picture = Polygon(Point(40,190), Point(55,255), Point(65, 225), Point(75, 275), Point(85, 225), Point(95, 255), Point(110, 190), Point(75, 220))
            pokemon3Picture.setFill(type2Color)
            pokemon3Picture.setOutline(type2Color)
        # Flying type
        elif type1Name == "Flying":
            if teamNumber == 1:
                pokemon1Picture = Oval(Point(45,160), Point(105, 230))
                pokemon1Picture.setFill(type2Color)
                
                pokemon2Picture = Oval(Point(75,200), Point(125, 260))
                pokemon2Picture.setFill(type2Color)
                
                pokemon3Picture = Oval(Point(75,180), Point(45, 210))
                pokemon3Picture.setFill(type2Color)
                pokemon3Picture.setWidth(2)
                
            else:
                pokemon1Picture = Oval(Point(45,160), Point(105, 230))
                pokemon1Picture.setFill(type2Color)
                
                pokemon2Picture = Oval(Point(75,200), Point(25, 260))
                pokemon2Picture.setFill(type2Color)
                
                pokemon3Picture = Oval(Point(75,180), Point(105, 210))
                pokemon3Picture.setFill(type2Color)
                pokemon3Picture.setWidth(2)
        # Ghost type
        elif type1Name == "Ghost":
            pokemon1Picture = Circle(Point(75,220), 35)
            pokemon1Picture.setFill(type2Color)
            pokemon1Picture.setOutline(type2Color)
            
            pokemon2Picture = Circle(Point(75,220), 15)
            if type1Name == type2Name:    
                pokemon2Picture.setFill("White")
            else:
                pokemon2Picture.setFill(type1Color)
            
            pokemon3Picture = Polygon(Point(40, 230), Point(55, 170), Point(65, 195), Point(75, 160), Point(85, 195), Point(95, 170), Point(110, 230), Point(75, 200))
            pokemon3Picture.setFill(type2Color)
            pokemon3Picture.setOutline(type2Color)
        # Grass type
        elif type1Name == "Grass":
            pokemon1Picture = Polygon(Point(35, 160), Point(25, 225), Point(45, 175), Point(50, 200), Point(60, 170), Point(75, 260), Point(90, 170), Point(100, 200), Point(105, 175), Point(125, 225), Point(115, 160))
            pokemon1Picture.setFill(type2Color)
            
            pokemon2Picture =  Rectangle(Point(0,0), Point(0,0))
            pokemon3Picture =  Rectangle(Point(0,0), Point(0,0))
        # Ground type
        elif type1Name == "Ground":
            pokemon1Picture = Polygon(Point(25, 160), Point(50, 230), Point(75, 160))
            pokemon1Picture.setFill(type2Color)
            
            pokemon2Picture = Polygon(Point(120, 160), Point(100, 220), Point(80, 160))
            pokemon2Picture.setFill(type2Color)
            
            pokemon3Picture = Polygon(Point(45, 160), Point(75, 260), Point(105, 160))
            pokemon3Picture.setFill(type2Color)
        # Ice type
        elif type1Name == "Ice":
            pokemon1Picture = Polygon(Point(70, 215), Point(75, 260), Point(80, 215), Point(125, 210), Point(80, 205), Point(75, 160), Point(70, 205), Point(25, 210))
            pokemon1Picture.setFill(type2Color)
            
            pokemon2Picture = Circle(Point(75, 210), 20)
            pokemon2Picture.setFill(type2Color)
            
            pokemon3Picture = Circle(Point(75, 210), 10)
            pokemon3Picture.setFill("White")
        # Normal type
        elif type1Name == "Normal":
            pokemon1Picture = Circle(Point(75, 210), 50)
            pokemon1Picture.setFill(type2Color)
            
            pokemon2Picture = Circle(Point(75, 210), 30)
            if type1Name == type2Name:
                pokemon2Picture.setFill("White")    
            else:
                pokemon2Picture.setFill(type1Color)
            
            pokemon3Picture =  Rectangle(Point(0,0), Point(0,0))
        # Poison type
        elif type1Name == "Poison":
            pokemon1Picture = Polygon(Point(25, 160), Point(75, 260), Point(125, 160))
            pokemon1Picture.setFill(type2Color)
            
            pokemon2Picture = Oval(Point(65, 230), Point(85, 190))
            pokemon3Picture = Circle(Point(75, 175), 10)
            
            if type1Name == type2Name:
                pokemon2Picture.setFill("Black")
                pokemon3Picture.setFill("Black")
            else:
                pokemon2Picture.setFill(type1Color)
                pokemon3Picture.setFill(type1Color)
                pokemon2Picture.setOutline(type1Color)
                pokemon3Picture.setOutline(type1Color)
        # Psychic type
        elif type1Name == "Psychic":
            pokemon1Picture = Oval(Point(25, 180), Point(125, 240))
            pokemon1Picture.setFill(type1Color)
            
            pokemon2Picture = Oval(Point(30, 190), Point(120, 230))
            pokemon2Picture.setFill("White")
            
            pokemon3Picture = Oval(Point(65, 230), Point(85, 190))
            pokemon3Picture.setFill(type2Color)
        # Rock type
        elif type1Name == "Rock":
            pokemon1Picture = Polygon(Point(50, 260), Point(100, 260), Point(125, 235), Point(125, 185), Point(100, 160), Point(50, 160), Point(25, 185), Point(25, 235))
            pokemon1Picture.setFill(type2Color)
            
            pokemon2Picture = Polygon(Point(50, 260), Point(75, 260), Point(100, 235), Point(100, 210), Point(75, 185), Point(50, 185), Point(25, 210), Point(25, 235))
            pokemon2Picture.setFill(type1Color)
            
            pokemon3Picture = Polygon(Point(100, 210), Point(125, 185), Point(100, 160), Point(75,185))
            pokemon3Picture.setFill(type2Color)
            if type2Name in ["Dark", "Fighting", "Ghost"]:
                pokemon3Picture.setOutline("White")
        # Steel type
        elif type1Name == "Steel":
            pokemon1Picture = Rectangle(Point(25, 160), Point(125, 260))
            pokemon1Picture.setFill(type2Color)
            
            pokemon2Picture = Rectangle(Point(45, 180), Point(105, 200))
            pokemon3Picture = Polygon(Point(65, 235), Point(45, 235), Point(45, 215), Point(65, 215), Point(85, 215), Point(85, 235), Point(105, 235), Point(105, 215), Point(65, 215))
            pokemon2Picture.setOutline(type2Color)
            pokemon3Picture.setOutline(type2Color)
            if type1Color == type2Color:
                pokemon2Picture.setFill("Yellow")
                pokemon3Picture.setFill("Yellow")
            else:
                pokemon2Picture.setFill(type1Color)
                pokemon3Picture.setFill(type1Color)
        # Water type
        else:
            if teamNumber == 1:
                pokemon1Picture = Oval(Point(50, 170), Point(125, 250))
                pokemon2Picture = Polygon(Point(50, 210), Point(25, 260), Point(25, 160))   
                pokemon3Picture = Circle(Point(105, 225), 5)
            else:
                pokemon1Picture = Oval(Point(25, 170), Point(100, 250))
                pokemon2Picture = Polygon(Point(100, 210), Point(125, 260), Point(125, 160))   
                pokemon3Picture = Circle(Point(45, 225), 5)
            
            pokemon1Picture.setFill(type2Color)
            pokemon2Picture.setFill(type2Color)
            if type1Color == type2Color:
                pokemon3Picture.setFill("Black")
            else:
                pokemon3Picture.setFill(type1Color)
        # Moves the picture if team 2
        if teamNumber == 2:
            pokemon1Picture.move(350, 130)
            pokemon2Picture.move(350, 130)
            pokemon3Picture.move(350, 130)
            
        return pokemon1Picture, pokemon2Picture, pokemon3Picture
    # Calculates the damage of an attack
    def damageCalc(self, moveNumber, playerNum, analytic):
        # Shifts the move number over 1
        moveNumber -= 1
        # Sets attacker and defender using player number
        if playerNum == 1:
            pokemon1 = self.team1.activePokemon
            team1 = self.team1
            pokemon2 = self.team2.activePokemon
            team2 = self.team2
            selfLastMove = self.lastMove[0]
            oppLastMove = self.lastMove[1]
        else:
            pokemon1 = self.team2.activePokemon
            team1 = self.team2
            pokemon2 = self.team1.activePokemon
            team2 = self.team1
            selfLastMove = self.lastMove[1]
            oppLastMove = self.lastMove[0]
        # Changes Judgment type to match plate type
        if pokemon1.Moves[moveNumber].moveName == "Judgment" and "Plate" in pokemon1.item.itemName:
            for pokemonType in self.typeList:
                if pokemonType.typeName in pokemon1.item.effect:
                    moveType = pokemonType
                    abilityBoost = 1
                    break
        # Changes Techno Blast type to match drive type
        elif pokemon1.Moves[moveNumber].moveName == "Techno Blast" and "Drive" in pokemon1.item.itemName:
            for pokemonType in self.typeList:
                if pokemonType.typeName in pokemon1.item.effect:
                    moveType = pokemonType
                    abilityBoost = 1
                    break
        # Changes Multi-Attack type to match memory type
        elif pokemon1.Moves[moveNumber].moveName == "Multi-Attack" and "Memory" in pokemon1.item.itemName:
            for pokemonType in self.typeList:
                if pokemonType.typeName in pokemon1.item.effect:
                    moveType = pokemonType
                    abilityBoost = 1
                    break
        # Changes Ivy Cudgel type to match mask
        elif pokemon1.Moves[moveNumber].moveName == "Ivy Cudgel" and pokemon1.item.itemName in ["Cornerstone Mask", "Hearthflame Mask", "Wellspring Mask"]:
            if pokemon1.item.itemName == "Cornerstone Mask":
                maskType = "Rock"
            elif pokemon1.item.itemName == "Hearthflame Mask":
                maskType = "Fire"
            else:
                maskType = "Water"
            for pokemonType in self.typeList:
                if pokemonType.typeName == maskType:
                    moveType = pokemonType
                    abilityBoost = 1
                    break
        # Changes type according to the ability
        elif pokemon1.ability.effect[0] == "Type":
            # -Ate abilities such as Galvanize and Pixilate
            if pokemon1.ability.effect[2] == "Normal":
                if pokemon1.Moves[moveNumber].moveType.typeName == "Normal":
                    for pokemonType in self.typeList:
                        if pokemonType.typeName == pokemon1.ability.effect[1]:
                            moveType = pokemonType
                            abilityBoost = 1.2
                            break
                else:
                    moveType = pokemon1.Moves[moveNumber].moveType
                    abilityBoost = 1
            # Type boost abilities like Dragon's Maw and Steelworker
            elif pokemon1.ability.effect[2] == "Boost":
                moveType = pokemon1.Moves[moveNumber].moveType
                if pokemon1.Moves[moveNumber].moveType.typeName == pokemon1.ability.effect[1]:
                    abilityBoost = pokemon1.ability.success
                else:
                    abilityBoost = 1
            # Normalize
            elif pokemon1.ability.effect[2] == "All":
                for pokemonType in self.typeList:
                    if pokemonType.typeName == "Normal":
                        moveType = pokemonType
                        abilityBoost = 1.2
                        break
            # Liquid Voice
            elif pokemon1.ability.effect[2] == "Sound":
                if pokemon1.Moves[moveNumber].sound:
                    for pokemonType in self.typeList:
                        if pokemonType.typeName == pokemon1.ability.effect[1]:
                            moveType = pokemonType
                            abilityBoost = 1
                            break
                else:
                    moveType = pokemon1.Moves[moveNumber].moveType
                    abilityBoost = 1
        # Reckless
        elif pokemon1.ability.abilityName == "Reckless" and pokemon1.Moves[moveNumber].healing < 0:
            moveType = pokemon1.Moves[moveNumber].moveType
            abilityBoost = 1.2
        # Pinch abilities such as Blaze and Swarm
        elif pokemon1.ability.effect[0] == "Pinch" and pokemon1.currentHp <= pokemon1.Stats["HP"] * (1/3) and pokemon1.Moves[moveNumber].moveType == pokemon1.ability.effect[1]:
            moveType = pokemon1.Moves[moveNumber].moveType
            abilityBoost = 1.5
        # Defeatist
        elif pokemon1.ability.abilityName == "Defeatist" and pokemon1.currentHp <= pokemon1.Stats["HP"] * (1/2):
            moveType = pokemon1.Moves[moveNumber].moveType
            abilityBoost = .5
        # Sheer Force
        elif pokemon1.ability.abilityName == "Sheer Force"  and not pokemon1.Moves[moveNumber].phySpe == "Status" and (pokemon1.Moves[moveNumber].target == "Opponent" or not "-" in pokemon1.Moves[moveNumber].stages):
            moveType = pokemon1.Moves[moveNumber].moveType
            abilityBoost = 1.3
        # Rivalry
        elif pokemon1.ability.abilityName == "Rivalry":
            if pokemon1.gender == "None" or pokemon2.gender == "None":
                abilityBoost = 1
            elif pokemon1.gender == pokemon2.gender:
                abilityBoost = 1.25
            else:
                abilityBoost = .8
            moveType = pokemon1.Moves[moveNumber].moveType
        # Supreme Overlord
        elif pokemon1.ability.abilityName == "Supreme Overlord":
            moveType = pokemon1.Moves[moveNumber].moveType
            abilityBoost = 1 + (.1 * (6 - team1.alivePokemon))
        # Multiscale and Shadow Shield
        elif pokemon2.ability.effect[0] == "Multiscale" and pokemon2.currentHp == pokemon2.Stats["HP"]:
            moveType = pokemon1.Moves[moveNumber].moveType
            abilityBoost = .5
        # Guts
        elif pokemon1.ability.abilityName == "Guts" and not pokemon1.status == "Healthy" and pokemon1.Moves[moveNumber].phySpe == "Physical":
            moveType = pokemon1.Moves[moveNumber].moveType
            abilityBoost = 1.5
        # Flare Boost and Toxic Boost
        elif pokemon1.ability.effect[0] == "Flare Boost" and pokemon1.status in pokemon1.ability.effect[1] and pokemon1.Moves[moveNumber].phySpe == pokemon1.ability.effect[2]:
            moveType = pokemon1.Moves[moveNumber].moveType
            abilityBoost = 1.5
        # Slow Start
        elif pokemon1.ability.abilityName == "Slow Start" and pokemon1.turnOut < 6 and pokemon1.Moves[moveNumber].phySpe == "Physical":
            moveType = pokemon1.Moves[moveNumber].moveType
            abilityBoost = .5
        # Flash Fire
        elif pokemon1.flashFire and pokemon1.Moves[moveNumber].moveType == "Fire":
            moveType = "Fire"
            abilityBoost = 1.5
        else:
            moveType = pokemon1.Moves[moveNumber].moveType
            abilityBoost = 1
        # Changes Freeze-Dry and Flying Press to their special type
        if pokemon1.Moves[moveNumber].moveName in ["Freeze-Dry", "Flying Press"]:
            for pokemonType in self.typeList:
                if pokemonType.typeName == pokemon1.Moves[moveNumber].moveName:
                    moveType = pokemonType
        # Dark Aura, Fairy Aura, and Aura Break
        if pokemon1.ability.effect[0] == "Aura" or pokemon2.ability.effect[0] == "Aura":
            if pokemon1.ability.effect[0] == "Aura" and pokemon1.ability.effect[1] == moveType:
                if pokemon2.ability.abilityName == "Aura Break":
                    abilityBoost /= pokemon1.ability.success
                else:
                    abilityBoost *= pokemon1.ability.success
            elif pokemon2.ability.effect[0] == "Aura" and pokemon2.ability.effect[1] == moveType:
                if pokemon1.ability.abilityName == "Aura Break":
                    abilityBoost /= pokemon2.ability.success
                else:
                    abilityBoost *= pokemon2.ability.success
        # Protosynthesis and Quark Drive
        if pokemon1.Moves[moveNumber].phySpe == "Physical":
            if pokemon1.ability.effect[0] == "Booster Energy" and pokemon1.boosterEnergy[2] and pokemon1.boosterEnergy[1] == "Attack":
                abilityBoost *= pokemon1.boosterEnergy[0]
            if pokemon2.ability.effect[0] == "Booster Energy" and pokemon2.boosterEnergy[2] and pokemon2.boosterEnergy[1] == "Defense":
                abilityBoost /= pokemon2.boosterEnergy[0]
        elif pokemon1.Moves[moveNumber].phySpe == "Special":
            if pokemon1.ability.effect[0] == "Booster Energy" and pokemon1.boosterEnergy[2] and pokemon1.boosterEnergy[1] == "Special Attack":
                abilityBoost *= pokemon1.boosterEnergy[0]
            if pokemon2.ability.effect[0] == "Booster Energy" and pokemon2.boosterEnergy[2] and pokemon2.boosterEnergy[1] == "Special Defense":
                abilityBoost /= pokemon2.boosterEnergy[0]
        # Analytic        
        if analytic:
            if pokemon1.ability.abilityName == "Analytic":
                abilityBoost *= 1.3
        # Same type attack bonus
        if moveType.typeName == pokemon1.Type1.typeName or (moveType.typeName == "Flying Press" and pokemon1.Type1.typeName == "Fighting") or (moveType.typeName == "Freeze-Dry" and pokemon1.Type1.typeName == "Ice"):
            if pokemon1.ability.abilityName == "Adaptability":
                stab = 2
            else:
                stab = 1.5
        elif moveType.typeName == pokemon1.Type2.typeName or (moveType.typeName == "Flying Press" and pokemon1.Type2.typeName == "Fighting") or (moveType.typeName == "Freeze-Dry" and pokemon1.Type2.typeName == "Ice"):
            if pokemon1.ability.abilityName == "Adaptability":
                stab = 2
            else:
                stab = 1.5
        elif pokemon1.ability.effect[0] == "Protean" and not pokemon1.protean:
            stab = 1.5
        else:
            stab = 1
        # Type effectiveness, with no effect taking priority over other effectiveness
        if pokemon1.ability.abilityName in ["Mind's Eye", "Scrappy"] and moveType.typeName in ["Normal", "Fighting"] and pokemon2.Type1.typeName == "Ghost":
            typeEffect = 1
        else:
            typeEffect =  moveType.effectDict[pokemon2.Type1.typeName]
        if not pokemon2.Type2.typeName == "None":
            if not (pokemon1.ability.abilityName == "Scrappy" and moveType.typeName in ["Normal", "Fighting"] and pokemon2.Type2.typeName == "Ghost"):
                typeEffect *= moveType.effectDict[pokemon2.Type2.typeName]
        # Type Immmunity abilities
        if pokemon2.ability.effect[0] == "Type Immunity":
            if pokemon2.ability.effect[1] == moveType.typeName:
                typeEffect = 0
                if pokemon2.ability.abilityName == "Flash Fire":
                    pokemon2.flashFire = True
        # Wonder Guard only allows super effective hits
        if pokemon2.ability.abilityName == "Wonder Guard" and typeEffect <= 1:
            typeEffect = 0
        # Filter and Solid Rock
        if typeEffect > 1 and pokemon2.ability.effect[0] == "Filter":
            typeEffect *= .75
        # Tinted Lens
        if typeEffect < 1 and pokemon1.ability.abilityName == "Tinted Lens":
            typeEffect *= 2
        # Collision Course and Electro Drift
        if typeEffect > 1 and pokemon1.Moves[moveNumber].moveName in ["Collision Course", "Electro Drift"]:
            typeEffect *= 4/3
        # Set damage attacks such as Dragon Rage
        if pokemon1.Moves[moveNumber].stat == "Set Damage" and typeEffect > 0:
            damage = pokemon1.Moves[moveNumber].power
        # Level damage attacks such as Seismic Toss
        elif pokemon1.Moves[moveNumber].stat == "Level Damage" and typeEffect > 0:
            damage = pokemon1.Level
        # Psywave damage is between 1 damage and 1.5x the user's level
        elif pokemon1.Moves[moveNumber].moveName == "Psywave" and typeEffect > 0:
            damage = floor(pokemon1.Level * (randint(0, 100) + 50)/ 100)
            if damage < 1:
                damage = 1
        else:
            # Weather damage multiplier
            if self.weather[0] != "Clear" and not self.cloudNine:
                # Rain and Heavy Rain
                if self.weather[0] == "Rain Dance":
                    if pokemon1.Moves[moveNumber].moveName in ["Solar Beam", "Solar Blade"] or moveType.typeName == "Fire":
                        if (pokemon1.ability.abilityName == "Primordial Sea" or pokemon2.ability.abilityName == "Primordial Sea") and moveType.typeName == "Fire":
                            weatherBoost = 0
                        else:
                            weatherBoost = .5
                    elif moveType.typeName == "Water":
                        weatherBoost = 2
                    else:
                        weatherBoost = 1
                # Sun and Harsh Sunlight
                elif self.weather[0] == "Sunny Day":
                    if moveType.typeName == "Fire":
                        weatherBoost = 2
                    elif (pokemon1.ability.abilityName == "Desolate Land" or pokemon2.ability.abilityName == "Desolate Land") and moveType.typeName == "Water":
                        weatherBoost = 0
                    elif moveType.typeName == "Water":
                        weatherBoost = .5
                    else:
                        weatherBoost = 1
                # Hail
                elif self.weather[0] == "Hail":
                    if pokemon1.Moves[moveNumber].moveName in ["Solar Beam", "Solar Blade"]:
                        weatherBoost = .5
                    else:
                        weatherBoost = 1
                # Sandstorm
                elif self.weather[0] == "Sandstorm":
                    if pokemon1.Moves[moveNumber].moveName in ["Solar Beam", "Solar Blade"]:
                        weatherBoost = .5
                    else:
                        weatherBoost = 1
                    if (pokemon2.Type1.typeName == "Rock" or pokemon2.Type2.typeName == "Rock") and pokemon1.Moves[moveNumber].phySpe == "Special":
                        weatherBoost /= 1.5
                # Strong Winds
                elif self.weather[0] == "Delta Stream":
                    if moveType.typeName in ["Electric", "Ice", "Rock"]:
                        weatherBoost = .5
                    else:
                        weatherBoost = 1
            else:
                weatherBoost = 1
            # Physical attacks
            if pokemon1.Moves[moveNumber].phySpe == "Physical":
                # Facade
                if pokemon1.Moves[moveNumber].moveName == "Facade":
                    if pokemon1.status in ["Burn", "Paralyze", "Poison"]:
                        statusMult = 2
                    else:
                        statusMult = 1
                # Burn
                elif pokemon1.status == "Burn" and not pokemon1.ability.abilityName == "Guts":
                    statusMult = .5
                else:
                    statusMult = 1
                # Item boosts physical attack 
                if "Attack" in pokemon1.item.effect and not pokemon1.item.consumed:
                    itemMult = pokemon1.item.multiplier
                # Specialty items that boost attack
                elif moveType.typeName in pokemon1.item.effect and pokemon1.item.secondEffect in ["Attack", "Specialty"] and not pokemon1.item.consumed:
                    itemMult = pokemon1.item.multiplier
                # No item with Acrobatics
                elif pokemon1.item.consumed and pokemon1.Moves[moveNumber].moveName == "Acrobatics":
                    itemMult = 2
                # Punching Glove and punching attacks
                elif pokemon1.item.itemName == "Punching Glove" and pokemon1.Moves[moveNumber].punching:
                    itemMult = 1.1
                else:
                    itemMult = 1
                # Defense boosting item
                if "Defense" in pokemon2.item.effect and not pokemon2.item.consumed:
                    itemMult /= pokemon2.item.multiplier
                # Eviolite for not fully evolved pokemon
                elif "Evolve" in pokemon2.item.effect and pokemon2.evolve and not pokemon2.item.consumed:
                    itemMult /= 1.5
                # Knock off boosting items being removed
                if pokemon1.Moves[moveNumber].moveName == "Knock Off" and not pokemon2.item.consumed and not pokemon2.item.fling == 0:
                    itemMult *= 1.5
                # Wake-Up Slap doubling damage against resting and sleeping opponent
                if pokemon2.status == "Sleep" or pokemon2.status == "Rest":
                    if pokemon1.Moves[moveNumber].moveName == "Wake-Up Slap":
                        statusMult *= 2
                # Smelling Salts doubling damage against paralyzed opponent
                elif pokemon2.status == "Paralyze":
                    if pokemon1.Moves[moveNumber].moveName == "Smelling Salts":
                        statusMult *= 2
                # Magnitude randomly choosing a power
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
                # Gyro Ball using speed to decide power
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
                # Flail and Reversal using self remaining HP to decide power
                elif pokemon1.Moves[moveNumber].moveName in ["Flail", "Reversal"]:
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
                # Last Repects doing more damage for each fainted pokemon
                elif pokemon1.Moves[moveNumber].moveName == "Last Respects":
                    powerMult = 7 - team1.alivePokemon
                # Low Kick using opponent weight to decide power
                elif pokemon1.Moves[moveNumber].moveName == "Low Kick":
                    if pokemon2.mass[2]:
                        if pokemon2.currentMass <= 9.9:
                            powerMult = 1
                        elif pokemon2.currentMass >= 10.0 and pokemon2.currentMass <= 24.9:
                            powerMult = 2
                        elif pokemon2.currentMass >= 25.0 and pokemon2.currentMass <= 49.9:
                            powerMult = 3
                        elif pokemon2.currentMass >= 50.0 and pokemon2.currentMass <= 99.9:
                            powerMult = 4
                        elif pokemon2.currentMass >= 100.0 and pokemon2.currentMass <= 199.9:
                            powerMult = 5
                        elif pokemon2.currentMass >= 200.0:
                            powerMult = 6
                    else:
                        powerMult = 0
                # Heat Crash and Heavy Slam using self and opponent weight to
                # decide power
                elif pokemon1.Moves[moveNumber].moveName in ["Heat Crash", "Heavy Slam"]:
                    if pokemon1.mass[2]:
                        massRatio = round(pokemon2.currentMass/pokemon1.currentMass, 4)
                        if massRatio > .5:
                            powerMult = 2
                        elif massRatio > .3334:
                            powerMult = 3
                        elif massRatio > .25:
                            powerMult = 4
                        elif massRatio > 20:
                            powerMult = 5
                        else:
                            powerMult = 6
                    else:
                        powerMult = 0
                # Rage Fist does more damage the more the user has been hit
                elif pokemon1.Moves[moveNumber].moveName == "Rage Fist":
                    powerMult = pokemon1.rageFist
                else:
                    powerMult = 1
                # Technician boosting weak attacks
                if pokemon1.ability.abilityName == "Technician" and pokemon1.Moves[moveNumber].power <= 60:
                    powerMult *= 1.5
                # Charge from previous turn
                if selfLastMove == "Charge" and moveType.typeName == "Electric":
                    powerMult *= 2
                # Electric Terrain boosting electric moves
                if self.terrain[0] == "Electric Terrain" and moveType.typeName == "Electric" and not (pokemon1.Type1.typeName == "Flying" or pokemon1.Type2.typeName == "Flying" or pokemon1.ability.abilityName == "Levitate"):
                    powerMult *= 1.3
                # Psychic Terrain boosting psychic moves
                elif self.terrain[0] == "Psychic Terrain" and moveType.typeName == "Psychic" and not (pokemon1.Type1.typeName == "Flying" or pokemon1.Type2.typeName == "Flying" or pokemon1.ability.abilityName == "Levitate"):
                    powerMult *= 1.3
                # Grassy Terrain boost grass moves
                elif self.terrain[0] == "Grassy Terrain":
                    if moveType.typeName == "Grass" and not (pokemon1.Type1.typeName == "Flying" or pokemon1.Type2.typeName == "Flying" or pokemon1.ability.abilityName == "Levitate"):
                        powerMult *= 1.3
                    elif pokemon1.Moves[moveNumber].moveName in ["Bulldoze", "Earthquake", "Magnitude"]:
                        powerMult *= .5
                # Misty Terrain weakening dragon moves
                elif self.terrain[0] == "Misty Terrain" and moveType.typeName == "Dragon" and not (pokemon1.Type1.typeName == "Flying" or pokemon1.Type2.typeName == "Flying" or pokemon1.ability.abilityName == "Levitate"):
                    powerMult *= .5
                elif self.terrain[0] == "Misty Terrain" and pokemon1.Moves[moveNumber].moveName == "Misty Explosion":
                    powerMult *= 1.5
                # Attack boosting ability
                if pokemon1.ability.effect[1] == "Attack" and pokemon1.ability.effect[0] == "Stats":
                    abilityAttDef = pokemon1.ability.success
                else:
                    abilityAttDef = 1
                # Defense boosting ability
                if (pokemon2.ability.effect[1] == "Defense" and pokemon2.ability.effect[0] == "Stats") and not pokemon1.ability.effect[0] == "Mold Breaker":
                    abilityAttDef /= pokemon2.ability.success
                # Fluffy taking more damage from fire moves
                if (moveType == "Fire" and pokemon2.ability.abilityName == "Fluffy") and not pokemon1.ability.effect[0] == "Mold Breaker":
                    abilityBoost *= 2
                # Thick Fat taking less damage from fire and ice moves
                if (moveType in ["Ice", "Fire"] and pokemon2.abilityName == "Thick Fat") and not pokemon1.ability.effect[0] == "Mold Breaker":
                    abilityBoost /= 1.5
                # Heatproof taking less damage from fire moves
                if (moveType == "Fire" and pokemon2.ability.abilityName == "Heatproof") and not pokemon1.ability.effect[0] == "Mold Breaker":
                    abilityBoost /= 2
                # Tough Claws boosting contact moves
                if pokemon1.Moves[moveNumber].contact and pokemon1.ability.abilityName == "Tough Claws":
                    abilityBoost *= 1.3
                # Strong Jaw boosting bite moves
                if pokemon1.Moves[moveNumber].moveName in ["Bite", "Crunch", "Fire Fang",
                                 "Fishious Rend", "Hyper Fang", "Ice Fang", "Jaw Lock",
                                 "Poison Fang", "Psychic Fangs", "Thunder Fang"] and pokemon1.ability.abilityName == "Strong Jaw":
                    abilityBoost *= 1.5
                # Iron Fist boosting punching moves
                if pokemon1.Moves[moveNumber].punching and pokemon1.ability.abilityName == "Iron Fist":
                    abilityBoost *= 1.2
                # Sharpness boosting slicing moves
                if pokemon1.Moves[moveNumber].slicing and pokemon1.ability.abilityName == "Sharpness":
                    abilityBoost *= 1.5
                # Sand Force boosting rock, ground, and steel moves in Sandstorm
                if pokemon1.ability.abilityName == "Sand Force" and self.weather[0] == "Sandstorm" and moveType.moveName in ["Ground", "Rock", "Steel"] and not self.cloudNine:
                    abilityBoost *= 1.3
                # Orichalcum Pulse boosts attack in Sun
                elif pokemon1.ability.abilityName == "Orichalcum Pulse" and self.weather[0] == "Sunny Day" and not self.cloudNine:
                    abilityBoost *= 4/3
                # Ruin abilities boosting or weaking damage
                if pokemon1.ability.effect[0] == "Ruin" or pokemon2.ability.effect[0] == "Ruin":
                    if pokemon1.ability.effect[1] == "Defense" and not pokemon2.ability.effect[1] == "Attack":
                        abilityBoost *= 1.25
                    elif pokemon2.ability.effect[1] == "Defense" and not pokemon1.ability.effect[1] == "Attack":
                        abilityBoost *= .8
                # Unaware ignores stat changes on opponent
                if pokemon2.ability.abilityName == "Unaware":
                    pokemon1StatMult = 1
                else:
                    pokemon1StatMult = pokemon1.statModifier["Attack"]
                # Chip Away and Unaware ignores stat changes on opponent
                if pokemon1.Moves[moveNumber].stat == "Chip Away" or pokemon2.ability.abilityName == "Unaware":
                    pokemon2StatMult = 1
                # Applies opponent's defense modifier
                else:
                    pokemon2StatMult = pokemon2.statModifier["Defense"]
                # Calculates damage for Fling
                if pokemon1.Moves[moveNumber].moveName == "Fling":
                    if pokemon1.item.fling > 0 and not pokemon1.item.consumed:
                        damage = floor((floor(floor(floor(((2 * pokemon1.Level) / 5) + 2) * pokemon1.item.fling * powerMult
                              * (pokemon1.Stats["Attack"]/pokemon2.Stats["Defense"] * abilityAttDef)) / 50) 
                                + 2) * (stab * typeEffect * pokemon1StatMult /
                                   pokemon2StatMult * (randint(85, 100) / 100)
                                   * statusMult * itemMult * weatherBoost * abilityBoost))
                    else:
                        damage = 0
                # Calculates damage for Body Press
                elif pokemon1.Moves[moveNumber].moveName == "Body Press":
                    damage = floor((floor(floor(floor(((2 * pokemon1.Level) / 5) + 2) * pokemon1.Moves[moveNumber].power * powerMult
                          * (pokemon1.Stats["Defense"]/pokemon2.Stats["Defense"] * abilityAttDef)) / 50) 
                            + 2) * (stab * typeEffect * pokemon1.statModifier["Defense"] /
                               pokemon2StatMult * (randint(85, 100) / 100)
                               * statusMult * itemMult * weatherBoost * abilityBoost))
                # Calculates damage for attack using multipliers found earlier
                else:
                    damage = floor((floor(floor(floor(((2 * pokemon1.Level) / 5) + 2) * pokemon1.Moves[moveNumber].power * powerMult
                          * (pokemon1.Stats["Attack"]/pokemon2.Stats["Defense"] * abilityAttDef)) / 50) 
                            + 2) * (stab * typeEffect * pokemon1StatMult /
                               pokemon2StatMult * (randint(85, 100) / 100)
                               * statusMult * itemMult * weatherBoost * abilityBoost))
            # Special attacks
            else:
                # Many of the multipliers are found the same way as found in
                # physical attack
                if "Special Attack" in pokemon1.item.effect and not pokemon1.item.consumed:
                    itemMult = pokemon1.item.multiplier
                elif moveType.typeName in pokemon1.item.effect and pokemon1.item.secondEffect in ["Attack", "Specialty"] and not pokemon1.item.consumed:
                    itemMult = pokemon1.item.multiplier
                else:
                    itemMult = 1
                if "Special Defense" in pokemon2.item.effect and not pokemon2.item.consumed:
                    itemMult /= pokemon2.item.multiplier
                elif "Evolve" in pokemon2.item.effect and pokemon2.evolve and not pokemon2.item.consumed:
                    itemMult /= 1.5
                # Calculates power of Electro Ball using speed of both pokemon
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
                # Trump Card calculates power using remaining PP
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
                # Calculates power of Eruption, Water Spout, and Dragon Energy
                # using users remaining HP
                elif pokemon1.Moves[moveNumber].moveName in ["Eruption", "Water Spout", "Dragon Energy"]:
                    powerMult = pokemon1.currentHp / pokemon1.Stats["HP"]
                    if powerMult < (1/150):
                        powerMult = (1/150)
                # Calculates power of Grass Knot using opponent's mass
                elif pokemon1.Moves[moveNumber].moveName == "Grass Knot":
                    if pokemon2.mass[2]:
                        if pokemon2.currentMass <= 9.9:
                            powerMult = 1
                        elif pokemon2.currentMass >= 10.0 and pokemon2.currentMass <= 24.9:
                            powerMult = 2
                        elif pokemon2.currentMass >= 25.0 and pokemon2.currentMass <= 49.9:
                            powerMult = 3
                        elif pokemon2.currentMass >= 50.0 and pokemon2.currentMass <= 99.9:
                            powerMult = 4
                        elif pokemon2.currentMass >= 100.0 and pokemon2.currentMass <= 199.9:
                            powerMult = 5
                        elif pokemon2.currentMass >= 200.0:
                            powerMult = 6
                    else:
                        powerMult = 0
                else:
                    powerMult = 1
                if pokemon1.ability.abilityName == "Technician" and pokemon1.Moves[moveNumber].power <= 60:
                    powerMult *= 1.5
                if selfLastMove == "Charge" and pokemon1.Moves[moveNumber].moveType.typeName == "Electric":
                    powerMult *= 2
                if self.terrain[0] == "Electric Terrain" and moveType.typeName == "Electric" and not (pokemon1.Type1.typeName == "Flying" or pokemon1.Type2.typeName == "Flying" or pokemon1.ability.abilityName == "Levitate"):
                    powerMult *= 1.3
                    if pokemon1.Moves[moveNumber].moveName == "Rising Voltage":
                        powerMult *= 2
                elif self.terrain[0] == "Psychic Terrain" and moveType.typeName == "Psychic" and not (pokemon1.Type1.typeName == "Flying" or pokemon1.Type2.typeName == "Flying" or pokemon1.ability.abilityName == "Levitate"):
                    powerMult *= 1.3
                    if pokemon1.Moves[moveNumber].moveName == "Expanding Force":
                        powerMult *= 1.5
                elif self.terrain[0] == "Grassy Terrain":
                    if moveType.typeName == "Grass" and not (pokemon1.Type1.typeName == "Flying" or pokemon1.Type2.typeName == "Flying" or pokemon1.ability.abilityName == "Levitate"):
                        powerMult *= 1.3
                    elif pokemon1.Moves[moveNumber].moveName in ["Bulldoze", "Earthquake", "Magnitude"]:
                        powerMult *= .5
                elif self.terrain[0] == "Misty Terrain" and moveType.typeName == "Dragon" and not (pokemon1.Type1.typeName == "Flying" or pokemon1.Type2.typeName == "Flying" or pokemon1.ability.abilityName == "Levitate"):
                    powerMult *= .5
                elif self.terrain[0] == "Misty Terrain" and pokemon1.Moves[moveNumber].moveName == "Misty Explosion":
                    powerMult *= 1.5    
                if (pokemon2.ability.effect[1] == "Special Defense" and pokemon2.ability.effect[0] == "Stats") and not pokemon1.ability.effect[0] == "Mold Breaker":
                    abilityAttDef = pokemon2.ability.success
                else:
                    abilityAttDef = 1
                if (moveType == "Fire" and pokemon2.ability.abilityName == "Fluffy") and not pokemon1.ability.effect[0] == "Mold Breaker":
                    abilityBoost *= 2
                if (moveType in ["Ice", "Fire"] and pokemon2.abilityName == "Thick Fat") and not pokemon1.ability.effect[0] == "Mold Breaker":
                    abilityBoost /= 1.5
                if (moveType == "Fire" and pokemon2.ability.abilityName == "Heatproof") and not pokemon1.ability.effect[0] == "Mold Breaker":
                    abilityBoost /= 2
                if pokemon1.Moves[moveNumber].contact and pokemon1.ability.abilityName == "Tough Claws":
                    abilityBoost *= 1.3
                # Mega Launcher boosts pulse moves
                if pokemon1.Moves[moveNumber].moveName in ["Aura Sphere", "Dark Pulse",
                                 "Dragon Pulse", "Origin Pulse", "Terrain Pulse",
                                 "Water Pulse"] and pokemon1.ability.abilityName == "Mega Launcher":
                    abilityBoost *= 1.5
                if pokemon1.ability.effect[2] == "Weather" and pokemon1.ability.effect[0] == "Boost" and not self.cloudNine:
                    if pokemon1.ability.effect[1] == self.weather[0]:
                        if self.weather[0] == "Sandstorm" and moveType.typeName in ["Ground", "Rock", "Steel"]:
                            abilityBoost *= 1.3
                        # Solar Power boosts special moves in Sun
                        elif self.weather[0] == "Sunny Day":
                            abilityBoost *= 1.5
                # Hadron Engine boosts special attack in Electric Terrain
                if pokemon1.ability.abilityName == "Hadron Engine" and self.terrain[0] == "Electric Terrain":
                    abilityBoost *= 4/3
                # Minus and Plus boosts special moves if the opponent has the 
                # ability as well
                if pokemon1.ability.effect[0] == "Flux" and pokemon2.ability.effect[0] == "Flux":
                    abilityBoost *= 1.5
                # Ash Greninja boosts Water Shuriken's power
                if pokemon1.pokemonName == "Greninja (Ash)" and pokemon1.Moves[moveNumber].moveName == "Water Shuriken":
                    abilityBoost *= 4/3
                if pokemon1.Moves[moveNumber].slicing and pokemon1.ability.abilityName == "Sharpness":
                    abilityBoost *= 1.5
                if pokemon1.ability.effect[0] == "Ruin" or pokemon2.ability.effect[0] == "Ruin":
                    if pokemon1.ability.effect[1] == "Special Defense" and not pokemon2.ability.effect[1] == "Special Attack":
                        abilityBoost *= 1.25
                    elif pokemon2.ability.effect[1] == "Special Defense" and not pokemon1.ability.effect[1] == "Special Attack":
                        abilityBoost *= .8
                if pokemon2.ability.abilityName == "Unaware":
                    pokemon1StatMult = 1
                else:
                    pokemon1StatMult = pokemon1.statModifier["Special Attack"]
                # Calculates damage for special attack using multipliers found earlier 
                if pokemon1.Moves[moveNumber].moveName not in ["Secret Sword", "Psyshock", "Psystrike"]:
                    if pokemon1.Moves[moveNumber].stat == "Chip Away" or pokemon2.ability.abilityName == "Unaware":
                        pokemon2StatMult = 1
                    else:
                        pokemon2StatMult = pokemon2.statModifier["Special Defense"]
                    damage = floor((floor(floor(floor(((2 * pokemon1.Level) / 5) + 2) 
                    * pokemon1.Moves[moveNumber].power * powerMult * (pokemon1.Stats["Special Attack"] 
                    / pokemon2.Stats["Special Defense"] * abilityAttDef)) / 50) + 2) * (stab 
                        * typeEffect * pokemon1StatMult / pokemon2StatMult * (randint(85, 100) / 100) 
                        * itemMult * weatherBoost * abilityBoost))
                # Calculates damage for Secret Sword, Psyshock, and Psystrike
                # using physical defense                                                       
                else:
                    if pokemon1.Moves[moveNumber].stat == "Chip Away" or pokemon2.ability.abilityName == "Unaware":
                        pokemon2StatMult = 1
                    else:
                        pokemon2StatMult = pokemon2.statModifier["Defense"]
                    damage = floor((floor(floor(floor(((2 * pokemon1.Level) / 5) + 2) 
                    * pokemon1.Moves[moveNumber].power * powerMult * 
                    (pokemon1.Stats["Special Attack"] / pokemon2.Stats["Defense"] * abilityAttDef)) / 50) + 2) * 
                        (stab * typeEffect * pokemon1StatMult / pokemon2StatMult * (randint(85, 100) / 100) 
                         * itemMult * weatherBoost * abilityBoost))
                # Dream Eater only works on sleeping and resting opponent's
                if pokemon1.Moves[moveNumber].moveName == "Dream Eater":
                    if pokemon2.status == "Sleep" or pokemon2.status == "Rest":
                        pass
                    else:
                        typeEffect = 0
                        damage = 0
        # Fake Out and First Impression only work on turn 1
        if (pokemon1.turnOut > 1 and pokemon1.Moves[moveNumber].moveName in ["Fake Out", "First Impression"]) or (damage == 0 and pokemon1.Moves[moveNumber].moveName == "Fling"):
            damage = 0
        # Gigaton Hammer and Blood Moon cannot be used twice in a row
        elif selfLastMove == pokemon1.Moves[moveNumber].moveName and pokemon1.Moves[moveNumber].moveName in ["Blood Moon", "Gigaton Hammer"]:
            damage = 0
        # Increased priority moves cannot be used in Psychic Terrain
        elif self.terrain[0] == "Psychic Terrain" and pokemon1.Moves[moveNumber].priority > 0 and damage > 0 and not (pokemon2.Type1.typeName == "Flying" or pokemon2.Type2.typeName == "Flying" or pokemon2.ability.abilityName == "Levitate"):
            damage = 0
        # Steel Roller must be used when terrain is activy
        elif self.terrain[0] == "Clear" and pokemon1.Moves[moveNumber].moveName == "Steel Roller":
            damage = 0
        # Explosion fails if either pokemon has Damp
        elif (pokemon1.ability.abilityName == "Damp" or pokemon2.ability.abilityName == "Damp") and not pokemon1.ability.abilityName == "Mold Breaker" and pokemon1.Moves[moveNumber].moveName in ["Explosion", "Self-Destruct", "Misty Explosion", "Mind Blown"]:
            damage = 0
        # Bullet moves cannot be used on Bulletproof pokemon
        elif pokemon2.ability.abilityName == "Bulletproof" and not pokemon1.ability.abilityName == "Mold Breaker" and pokemon1.Moves[moveNumber].moveName in ["Acid Spray", "Aura Sphere", "Barrage", "Beak Blast", "Bullet Seed", 
                                                                                                                                    "Egg Bomb", "Electro Ball", "Energy Ball", "Focus Blast", "Gyro Ball", "Ice Ball", "Magnet Bomb", 
                                                                                                                                    "Mist Ball", "Mud Bomb", "Octazooka", "Pyro Ball", "Rock Blast", "Rock Wrecker", 
                                                                                                                                    "Searing Shot", "Seed Bomb", "Shadow Ball", "Sludge Bomb", "Weather Ball", "Zap Cannon"]:
            damage = 0
        # Sound moves cannot be used on Soundproof pokemon
        elif pokemon2.ability.abilityName == "Soundproof" and not pokemon1.ability.abilityName == "Mold Breaker" and pokemon1.Moves[moveNumber].sound:
            damage = 0
        # Wind moves cannot be used on Wind Rider pokemon
        elif pokemon2.ability.abilityName == "Wind Rider" and not pokemon1.ability.abilityName == "Mold Breaker" and pokemon1.Moves[moveNumber].moveName in ["Air Cutter", "Bleakwind Storm", "Blizzard", "Fairy Wind", "Gust",
                                                                                                                                                             "Heat Wave", "Hurricane", "Icy Wind", "Petal Blizzard", "Sandsear Storm",
                                                                                                                                                             "Springtide Storm", "Twister", "Wildbolt Storm"]:
            damage = 0
        # Attacks must do at least 1 damage
        elif damage < 1 and not damage == 0 and typeEffect > 0:
            damage = 1
        return damage, typeEffect
    # Pokemon 1 tries to use an attack    
    def Attack(self, moveList, moveDict, moveNumber, oppMoveNumber, priority1, priority2, analytic, stakeout, playerNum, computer, computer2 = False, bounce = False, callMove = "None"):
        # Sets the pokemon and team variables using the player number
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
        # Checks if the opponent has full HP
        if pokemon2.Stats["HP"] == pokemon2.currentHp:
            fullHP = True
        else:
            fullHP = False
        # Finds the damage and type effectiveness of the move 
        damage, typeEffect = self.damageCalc(moveNumber, playerNum, analytic)
        # Sets the last moves used for moves that require it
        if playerNum == 1:
            self.lastMove[0] = pokemon1.Moves[moveNumber - 1].moveName
            oppLastMove = self.lastMove[1]
        else:
            self.lastMove[1] = pokemon1.Moves[moveNumber - 1].moveName
            oppLastMove = self.lastMove[0]
        # Attempts to use a Z Move
        if not attackingTeam.zMove:
            # Uses a Z Move if the user's team has not used one yet and the item
            # matches the intended Z Move
            if pokemon1.item.secondEffect == pokemon1.Moves[moveNumber - 1].moveType.typeName and moveNumber == 7:
                attackingTeam.zMove = True
                self.drawCurrentText(pokemon1.pokemonName + " activated its Z Power!")
                # Applies the corresponding bonus stat change for status moves
                if pokemon1.Moves[moveNumber - 1].phySpe == "Status":
                    raiseStats = False
                    for statEffect in ["Attack", "Defense", "Special Attack", "Special Defense", "Speed", "Accuracy", "Evasion"]:
                        if statEffect in pokemon1.Moves[moveNumber - 1].zEffect:
                            raiseStats = True
                    if raiseStats:
                        pokemon1.modifyStat(pokemon1.Moves[moveNumber - 1].zEffect, pokemon1.Moves[moveNumber - 1].zStages, True)
                    else:
                        if pokemon1.Moves[moveNumber - 1].zEffect == "Pumped":
                            pokemon1.changeStatus("Pumped")
                        # Resets lowered stats
                        elif pokemon1.Moves[moveNumber - 1].zEffect == "Reset":
                            resetText = False
                            for stat in pokemon1.statModifier:
                                if pokemon1.statModifier[stat] < 1:
                                    pokemon1.statModifier[stat] = 1
                                    resetText = True
                            if resetText:
                                self.drawCurrentText(pokemon1.pokemonName + " had its lowered stats reset!")
                        # Fully heals HP
                        elif pokemon1.Moves[moveNumber - 1].zEffect == "Heal":
                            pokemon1.currentHp = pokemon1.Stats["HP"]
        # Changes Aegislash to blade form if using an attacking move
        # Changes Aegislash to shield form if using King's Shield
        if ((pokemon1.Moves[moveNumber - 1].power > 0 and pokemon1.currentForm == "Base") or (pokemon1.Moves[moveNumber - 1].moveName == "King's Shield" and pokemon1.currentForm == "Blade")) and pokemon1.ability.abilityName == "Stance Change":
            pokemon1.changeForm(self.weather[0], True)
        # Fails to hit if the damage if 0 and tries to use an attacking move
        if damage == 0 and pokemon1.Moves[moveNumber - 1].power > 0:
            hit = 0
        # Fails to hit if the opponent is in an intangible state
        elif pokemon2.intangibility:
            hit = 0
        # Bounces back the attack if the user is using a status move and the
        # opponent either has the ability Magic Bounce or used the move Magic Coat
        elif (pokemon2.ability.abilityName == "Magic Bounce" or (self.lastMove[2 - playerNum] == "Magic Coat" and priority2 == 4)) and pokemon1.Moves[moveNumber - 1].phySpe == "Status" and pokemon1.Moves[moveNumber - 1].target == "Opponent" and not bounce:
            hit = 142
            pokemon2.Moves[5] = copy.deepcopy(pokemon1.Moves[moveNumber - 1])
            pokemon2.Moves[5].currentPP = 1
            self.Attack(moveList, moveDict, 6, oppMoveNumber, priority2, priority1, False, False, 3 - playerNum, computer2, computer, True)
        # Good as Gold and Crafty Shield blocks status moves
        elif (pokemon2.ability.abilityName == "Good as Gold" or (self.lastMove[2 - playerNum] == "Crafty Shield" and priority2 == 3)) and pokemon1.Moves[moveNumber - 1].phySpe == "Status" and pokemon1.Moves[moveNumber - 1].target == "Opponent" and not bounce:
            hit = 141
        # No Guard guarantees a hit on either pokemon
        elif pokemon1.ability.abilityName == "No Guard" or pokemon2.ability.abilityName == "No Guard":
            hit = -1
        # Hail without Cloud Nine guarantees Blizzard will hit
        elif self.weather[0] == "Hail" and pokemon1.Moves[moveNumber - 1].moveName == "Blizzard" and not self.cloudNine:
            hit = -1
        # Rain without Cloud Nine guarantees Thunder and Hurricane will hit
        elif self.weather[0] == "Rain Dance" and pokemon1.Moves[moveNumber - 1].moveName in ["Thunder", "Hurricane"] and not self.cloudNine:
            hit = -1
        # Sun without Cloud Nine lowers the chance Thunder and Hurricane will hit
        elif self.weather[0] == "Sunny Day" and pokemon1.Moves[moveNumber - 1].moveName in ["Thunder", "Hurricane"] and not self.cloudNine:
            hit = randint(1, 140)
        # Prankster causes status move to fail against dark type pokemon
        elif (pokemon2.Type1.typeName == "Dark" or pokemon2.Type2.typeName == "Dark") and pokemon1.Moves[moveNumber - 1].phySpe == "Status" and pokemon1.Moves[moveNumber - 1].target == "Opponent" and pokemon1.ability.abilityName == "Prankster":
            hit = 141
        # Grass types and Overcoat are immune to spore and powder moves
        elif (pokemon2.Type1.typeName == "Grass" or pokemon2.Type2.typeName == "Grass" or pokemon2.ability.abilityName == "Overcoat") and pokemon1.Moves[moveNumber - 1].moveName in ["Cotton Spore", "Magic Powder", "Poison Powder", "Powder", "Rage Powder", "Sleep Powder", "Spore", "Stun Spore"]:
            hit = 141
        # OHKO moves are more likely to hit the higher level the user is compared
        # to the target
        elif pokemon1.Moves[moveNumber - 1].stat == "OHKO":
            # Sturdy or the target being a higher level prevents OHKO moves from hitting
            if pokemon1.Level < pokemon2.Level or pokemon2.ability.abilityName == "Sturdy":
                hit = 141
            else:
                hit = randint(1, 3000) / (pokemon1.Level - pokemon2.Level + 30)
        else:
            hit = randint(1, 100)
        # Glaive Rush causes moves to always hit the user and take double damage
        if not hit == 0 and not hit == 141 and oppLastMove == "Glaive Rush":
            hit = -1
            damage *= 2
        # Hustle lowers accuracy of physical moves
        if pokemon1.ability.abilityName == "Hustle" and pokemon1.Moves[moveNumber - 1].phySpe == "Attack":
            abilityAccuracy = .8
        # Compound Eyes and Victory Star increases accuaracy
        elif pokemon1.ability.abilityName == "Compound Eyes":
            abilityAccuracy = 1.3
        elif pokemon1.ability.abilityName == "Victory Star":
            abilityAccuracy = 1.1
        else:
            abilityAccuracy = 1
        # Tanlged Feet and confusion increases evasion   
        if pokemon2.ability.abilityName == "Tangled Feet" and pokemon2.volatile["Confuse"] > 0:
            abilityAccuracy *= .5
        # Wonder Skin increases evasion of status moves
        elif pokemon2.ability.abilityName == "Wonder Skin" and pokemon1.Moves[moveNumber - 1].phySpe == "Status":
            abilityAccuracy *= .5
        # Weather related evasion abilities when the weather matches
        elif pokemon2.ability.effect[0] == "Evasion" and self.weather[0] == pokemon2.ability.effect[1] and not self.cloudNine:
            abilityAccuracy *= .8
        # Unaware, Chip Away, and Sacred Sword ignore evasion changes 
        if pokemon1.Moves[moveNumber - 1].stat == "Chip Away" or pokemon1.ability.abilityName == "Unaware":
            pokemon2Evasion = 1
        else:
            pokemon2Evasion = pokemon2.statModifier["Evasion"]
        # Unaware ignores accuary changes
        if pokemon2.ability.abilityName == "Unaware":
            pokemon1Accuracy = 1
        else:
            pokemon1Accuracy = pokemon2.statModifier["Accuracy"]
        # Checks if the attack passes the accuracy test
        if not hit == 141 and (hit <= pokemon1.Moves[moveNumber - 1].accuracy * abilityAccuracy * pokemon1Accuracy / pokemon2Evasion or pokemon1.Moves[moveNumber - 1].accuracy == 101):
            beatStatus = True
            # Truant prevents attacking every other turn
            if pokemon1.ability.abilityName == "Truant" and pokemon1.turnOut%2 == 0:
                beatStatus = False
                pokemon1.recharge = 0
                self.drawCurrentText(pokemon1.pokemonName + " is loafing around!")
            # Skips turn if needs to recharge
            elif pokemon1.recharge == 1:
                beatStatus = False
                pokemon1.recharge = 0
                self.drawCurrentText(pokemon1.pokemonName + " must recharge!")
            # Checks if the pokemon unthaws
            elif pokemon1.status == "Freeze":
                unthaw = randint(1, 5)
                if pokemon1.Moves[moveNumber - 1].moveName in ["Flame Wheel", 
                                 "Sacred Fire", "Flare Blitz", "Scald",
                                 "Steam Eruption", "Burn Up", "Pyro Ball",
                                 "Scorching Sands"] or (self.weather[0] == "Sunny Day" and not self.cloudNine):
                    pokemon1.changeStatus("Healthy")
                    self.drawCurrentText(pokemon1.pokemonName + " used " + pokemon1.Moves[moveNumber -1].moveName +
                          " and thawed itself out!")
                elif unthaw != 1:
                    beatStatus = False
                    self.drawCurrentText(pokemon1.pokemonName + " is frozen solid!")
                else:
                    pokemon1.changeStatus("Healthy")
                    self.drawCurrentText(pokemon1.pokemonName + " thawed out!")
            # Checks if the pokemon is fully paralyzed
            elif pokemon1.status == "Paralyze":
                fullyPara = randint(1, 4)
                if fullyPara == 1:
                    beatStatus = False
                    self.drawCurrentText(pokemon1.pokemonName + " is fully paralyzed!")
            # Checks if the pokemon wakes up
            elif pokemon1.status == "Sleep":
                if self.terrain[0] == "Electric Terrain" and not (pokemon1.Type1.typeName == "Flying" or pokemon1.Type2.typeName == "Flying" or pokemon1.ability.abilityName == "Levitate"):
                    pokemon1.sleepCounter == 6
                if pokemon1.sleepCounter == 0:
                    beatStatus = False
                    if pokemon1.ability.abilityName == "Early Bird":
                        pokemon1.sleepCounter = 2
                    else:
                        pokemon1.sleepCounter = 1
                    self.drawCurrentText(pokemon1.pokemonName + " is fast asleep!")
                else:
                    wakeUp = randint(1, (7 - pokemon1.sleepCounter))
                    if wakeUp == 1:
                        pokemon1.changeStatus("Healthy")
                        self.drawCurrentText(pokemon1.pokemonName + " woke up!")
                    else:
                        beatStatus = False
                        if pokemon1.ability.abilityName == "Early Bird" and not pokemon1.sleepCounter == 5:
                            pokemon1.sleepCounter += 2
                        else:
                            pokemon1.sleepCounter += 1
                        self.drawCurrentText(pokemon1.pokemonName + " is fast asleep!")
            # Checks if the pokemon finishes resting
            elif pokemon1.status == "Rest":
                if self.terrain[0] == "Electric Terrain" and not (pokemon1.Type1.typeName == "Flying" or pokemon1.Type2.typeName == "Flying" or pokemon1.ability.abilityName == "Levitate"):
                    pokemon1.sleepCounter == 2
                if pokemon1.sleepCounter == 2:
                    pokemon1.changeStatus("Healthy")
                    self.drawCurrentText(pokemon1.pokemonName + " woke up!")
                else:
                    beatStatus = False
                    if pokemon1.ability.abilityName == "Early Bird":
                        pokemon1.sleepCounter += 2
                    else:
                        pokemon1.sleepCounter += 1
                    self.drawCurrentText(pokemon1.pokemonName + " is fast asleep!")
            # Multiplies weather speed
            weatherSpeed = 1
            if not self.weather[0] == "None" and not self.cloudNine:
                if self.weather[0] == pokemon1.ability.effect[1] and pokemon1.ability.effect[0] == "Speed":
                    weatherSpeed *= pokemon1.ability.success
                if self.weather[0] == pokemon2.ability.effect[1] and pokemon2.ability.effect[0] == "Speed":
                    weatherSpeed /= pokemon2.ability.succes
            # Multiplies terrain speed
            terrainSpeed = 1   
            if not self.terrain[0] == "None":
                if self.terrain[0] == pokemon1.ability.effect[1] and pokemon1.ability.effect[0] == "Speed":
                    terrainSpeed *= pokemon1.ability.success
                if self.terrain[0] == pokemon2.ability.effect[1] and pokemon2.ability.effect[0] == "Speed":
                    terrainSpeed /= pokemon2.ability.success
            # Multiplies Slow Start speed
            abilitySpeed = 1
            if pokemon1.ability.abilityName == "Slow Start" and pokemon1.turnOut < 6:
                abilitySpeed /= 2
            if pokemon2.ability.abilityName == "Slow Start" and pokemon2.turnOut < 6:
                abilitySpeed *= 2
            # Multiplies Quick Feet speed
            if pokemon1.ability.abilityName == "Quick Feet" and not pokemon1.status == "Healthy":
                abilitySpeed *= 3/2
            if pokemon2.ability.abilityName == "Quick Feet" and not pokemon2.status == "Healthy":
                abilitySpeed *= 2/3
            # Checks if the pokemon successfully passed all previous checks
            if beatStatus:
                # Checks if the pokemon flinches
                if pokemon1.volatile["Flinch"] == 1:
                    if pokemon1.Stats["Speed"] * pokemon1.statModifier["Speed"] * weatherSpeed * terrainSpeed * abilitySpeed < pokemon2.Stats["Speed"] * pokemon2.statModifier["Speed"] or priority1 < priority2:
                        beatStatus = False
                        self.drawCurrentText(pokemon1.pokemonName + " flinched!")
                        pokemon1.recharge = 0
                        if pokemon1.ability.abilityName == "Steadfast":
                            pokemon1.modifyStat("Speed", 1, True)
                    pokemon1.volatile["Flinch"] = 0
                # Checks if the pokemon is infatuated
                if pokemon1.volatile["Infatuation"] > 0 and beatStatus:
                    self.drawCurrentText(pokemon1.pokemonName + " is in love with " + pokemon2.pokemonName + "!")
                    beatAttract = randint(0, 1)
                    if beatAttract == 0:
                        beatStatus = False
                        self.drawCurrentText(pokemon1.pokemonName + " is immobilized by love!")
                # Checks if the pokemon is still confused
                if pokemon1.volatile["Confuse"] > 0 and beatStatus:
                    if pokemon1.volatile["Confuse"] == 6:
                        pokemon1.volatile["Confuse"] = 0
                        self.drawCurrentText(pokemon1.pokemonName + " snapped out of confusion!")
                    elif pokemon1.volatile ["Confuse"] > 1:
                        snapOut = randint(1, 4)
                        if snapOut == 1:
                            pokemon1.volatile["Confuse"] = 0
                            self.drawCurrentText(pokemon1.pokemonName + " snapped out of confusion!")
                        # If still confused, checks if the pokemon hitself in confusion
                        else:
                            pokemon1.volatile["Confuse"] += 1
                            self.drawCurrentText(pokemon1.pokemonName + " is confused!")
                            hitSelf = randint(1, 3)
                            if hitSelf == 1:
                                beatStatus = False
                                self.drawCurrentText(pokemon1.pokemonName + " hit themself in confusion!")
                                damage = floor((floor(floor(floor(((2 * pokemon1.Level) / 5) + 2) 
                                * 40 * (pokemon1.Stats["Attack"]/pokemon1.Stats["Defense"])) / 50) + 2) 
                                * (pokemon1.statModifier["Attack"] / pokemon1.statModifier["Defense"] * (randint(85, 100) / 100)))
                                pokemon1.currentHp -= damage
                                pokemon1.recharge = 0
                    else:
                        pokemon1.volatile["Confuse"] += 1
                        self.drawCurrentText(pokemon1.pokemonName + " is confused!")
                        hitSelf = randint(1, 3)
                        if hitSelf == 1:
                            beatStatus = False
                            self.drawCurrentText(pokemon1.pokemonName + " hit themself in confusion!")
                            damage = floor((floor(floor(floor(((2 * pokemon1.Level) / 5) + 2) 
                            * 40 * (pokemon1.Stats["Attack"]/pokemon1.Stats["Defense"])) / 50) + 2) 
                            * (pokemon1.statModifier["Attack"] / pokemon1.statModifier["Defense"] * (randint(85, 100) / 100)))
                            pokemon1.currentHp -= damage
                            pokemon1.recharge = 0
                # Starts charging up an attack
                if pokemon1.Moves[moveNumber - 1].charge == "Charge" and pokemon1.recharge == 0 and beatStatus:
                    if not (pokemon1.Moves[moveNumber - 1].moveName in ["Solar Beam", "Solar Blade"] and self.weather[0] == "Sunny Day" and not self.cloudNine):
                        pokemon1.recharge = -1
                        pokemon1.chargeMove = moveNumber - 1
                        self.drawCurrentText(pokemon1.pokemonName + " is preparing a " + pokemon1.Moves[moveNumber - 1].moveName + "!")
                        if pokemon1.Moves[moveNumber - 1].stat == "Intangible":
                            pokemon1.intangibility = True
                            pokemon1.volatile["Intangible"] = pokemon1.Moves[moveNumber - 1].moveName
                        if pokemon1.item.itemName == "Power Herb" and not pokemon1.item.consumed:
                            pokemon1.recharge = 0
                            pokemon1.intangibility = False
                            pokemon1.volatile["Intangible"] = " "
                            pokemon1.item.Consume()
                            self.drawCurrentText(pokemon1.pokemonName + "'s Power Herb instantly charged up the attack!")
                        else:
                            beatStatus = False
            else:
                pokemon1.recharge = 0
            # Fails to hit intangible targets         
            if pokemon2.intangibility:
                secondaryList = ["Failure"]
            # Fake Out and First Impression only work on the first turn
            elif pokemon1.turnOut > 1 and pokemon1.Moves[moveNumber - 1].moveName in ["Fake Out", "First Impression"]:
                self.drawCurrentText(pokemon1.Moves[moveNumber - 1].moveName + " only works on the first turn out!")
                secondaryList = ["Failure"]
            # Priority moves fail in Psychic Terrain
            elif self.terrain[0] == "Psychic Terrain" and pokemon1.Moves[moveNumber - 1].priority > 1 and pokemon1.Moves[moveNumber - 1].power > 0 and not (pokemon2.Type1.typeName == "Flying" or pokemon2.Type2.typeName == "Flying" or pokemon2.ability.abilityName == "Levitate"):
                self.drawCurrentText("Psychic Terrian blocks priority moves!")
                secondaryList = ["Failure"]
            # Steel Roller fails if not in terrain
            elif self.terrain[0] == "Clear" and pokemon1.Moves[moveNumber - 1].moveName == "Steel Roller":
                self.drawCurrentText("Steel Roller failed to remove terrain!")
                secondaryList = ["Failure"]
            # Explosion, Self-Destruct, and Misty Explosion fail if Damp
            elif (pokemon1.ability.abilityName == "Damp" or pokemon2.ability.abilityName == "Damp") and not pokemon1.ability.abilityName == "Mold Breaker" and pokemon1.Moves[moveNumber - 1].moveName in ["Explosion", "Self-Destruct", "Misty Explosion", "Mind Blown"]:
                self.drawCurrentText("Damp prevents Pokemon from exploding!")
                secondaryList = ["Failure"]
            # Bomb and ball moves fail if Bulletproof
            elif pokemon2.ability.abilityName == "Bulletproof" and not pokemon1.ability.abilityName == "Mold Breaker" and pokemon1.Moves[moveNumber - 1].moveName in ["Acid Spray", "Aura Sphere", "Barrage", "Beak Blast", "Bullet Seed", 
                                                                                                                                    "Egg Bomb", "Electro Ball", "Energy Ball", "Focus Blast", "Gyro Ball", "Ice Ball", "Magnet Bomb", 
                                                                                                                                    "Mist Ball", "Mud Bomb", "Octazooka", "Pyro Ball", "Rock Blast", "Rock Wrecker", 
                                                                                                                                    "Searing Shot", "Seed Bomb", "Shadow Ball", "Sludge Bomb", "Weather Ball", "Zap Cannon"]:
                self.drawCurrentText("Bulletproof protects against ball and bomb moves!")
                secondaryList = ["Failure"]
            elif pokemon2.ability.abilityName == "Wind Rider" and not pokemon1.ability.abilityName == "Mold Breaker" and pokemon1.Moves[moveNumber - 1].moveName in ["Air Cutter", "Bleakwind Storm", "Blizzard", "Fairy Wind", "Gust",
                                                                                                                                                                 "Heat Wave", "Hurricane", "Icy Wind", "Petal Blizzard", "Sandsear Storm",
                                                                                                                                                                 "Springtide Storm", "Twister", "Wildbolt Storm"]:
                self.drawCurrentText("Wind Rider protects against wind moves!")
                secondaryList = ["Failure"]
                pokemon1.modifyStat("Attack", "1", False)
            # Spore and powder moves fail on grass types
            elif (pokemon2.Type1.typeName == "Grass" or pokemon2.Type2.typeName == "Grass" or pokemon2.ability.abilityName == "Overcoat" or pokemon2.item.itemName == "Safety Goggles") and pokemon1.Moves[moveNumber - 1].moveName in ["Cotton Spore", "Magic Powder", "Poison Powder", "Powder", "Rage Powder", "Sleep Powder", "Spore", "Stun Spore"]:
                self.drawCurrentText("Spore and powder moves do not work on " + pokemon2.pokemonName + "!")
                secondaryList = ["Failure"]
            else:
                # Serene Grace doubles the chance of secondary effects
                if pokemon1.ability.abilityName == "Serene Grace":
                    secondaryList = pokemon1.Moves[moveNumber - 1].Secondary(True)
                # Sheer Force removes user's secondary effects
                elif pokemon1.ability.abilityName == "Sheer Force" and not pokemon1.Moves[moveNumber - 1].phySpe == "Status" and (pokemon1.Moves[moveNumber - 1].target == "Opponent" or not "-" in pokemon1.Moves[moveNumber - 1].stages):
                    secondaryList = ["Failure"]
                else:
                    secondaryList = pokemon1.Moves[moveNumber - 1].Secondary(False)
                # Shield Dust and Covert Cloak protect against secondary effects
                if (pokemon2.ability.abilityName == "Shield Dust" or pokemon2.item.itemName == "Covert Cloak") and not pokemon1.Moves[moveNumber - 1].phySpe == "Status" and pokemon1.Moves[moveNumber - 1].target == "Opponent":
                    secondaryList = ["Failure"]
                # Fire Fang, Ice Fang, and ThunderFang can flinch if the first 
                # secondary effect fails
                if secondaryList[0] == "Failure" and pokemon1.Moves[moveNumber - 1].moveName in ["Fire Fang", "Ice Fang", "Thunder Fang"]:
                    fangFlinch = randint(1, 10)
                    if fangFlinch == 1:
                        secondaryList = ["Volatile", "Flinch", "Opponent", 1]
            # Sets last move to None if failed to attack
            if not beatStatus:
                if playerNum == 1:
                    self.lastMove[0] = None
                else:
                    self.lastMove[1] = None
            else:
                # Protean changes user's type if it hasn't been activated
                if pokemon1.ability.effect[0] == "Protean" and not pokemon1.protean:
                    if not pokemon1.Moves[moveNumber - 1].moveType.typeName == pokemon1.Type1.typeName or not pokemon1.Type2.typeName == "None":
                        pokemon1.changeType(pokemon1.Moves[moveNumber - 1].moveType.typeName, "None", False)
                        pokemon1.protean = True
                        self.drawCurrentText(pokemon1.pokemonName + " changed its type to " + pokemon1.Type1.typeName + "!")
                # Certain moves are prevented from being used
                if (pokemon1.item.secondEffect == "Block" and not pokemon1.item.consumed) or pokemon1.ability.effect[2] == "Block":
                    blockedMoves = [5]
                    if "Choice" in pokemon1.item.itemName or pokemon1.ability.abilityName == "Gorilla Tactics":
                        for number in range(4):
                            if number + 1 != moveNumber:
                                blockedMoves.append(number + 1)
                    elif pokemon1.item.itemName == "Assault Vest":
                        for number in range(4):
                            if pokemon1.Moves[number].phySpe == "Status":
                                blockedMoves.append(number + 1)
                    pokemon1.volatile["Blocked Moves"] = blockedMoves
                # Runs if not charging a move
                if not pokemon1.chargeMove is None:
                    # Bounces back a move
                    if bounce:
                        self.drawCurrentText(pokemon1.pokemonName + " used " + pokemon1.Moves[moveNumber - 1].moveName + "!")
                        self.drawCurrentText("The attack was bounced back!")
                    # Calls for a different move
                    elif not callMove == "None":
                        self.drawCurrentText(pokemon1.pokemonName + " used " + callMove + "!")
                        self.drawCurrentText(pokemon1.pokemonName + " called for " + pokemon1.Moves[moveNumber - 1].moveName + "!")
                    # Decreases remaining PP
                    else:
                        if pokemon2.ability.abilityName == "Pressure":
                            pokemon1.Moves[pokemon1.chargeMove].currentPP -= 2
                        else:
                            pokemon1.Moves[pokemon1.chargeMove].currentPP -= 1
                        self.drawCurrentText(pokemon1.pokemonName + " used " + pokemon1.Moves[pokemon1.chargeMove].moveName + "!")
                    pokemon1.chargeMove = None
                    pokemon1.recharge = 0
                else:
                    if bounce:
                        self.drawCurrentText(pokemon1.pokemonName + " used " + pokemon1.Moves[moveNumber - 1].moveName + "!\nThe attack was bounced back!")
                    else:
                        if pokemon2.ability.abilityName == "Pressure":
                            pokemon1.Moves[moveNumber - 1].currentPP -= 2    
                        else:
                            pokemon1.Moves[moveNumber - 1].currentPP -= 1
                        self.drawCurrentText(pokemon1.pokemonName + " used " + pokemon1.Moves[moveNumber - 1].moveName + "!")
                        pokemon1.volatile["Intangible"] = " "
                # Checks if the protection move is successful
                if pokemon1.Moves[moveNumber - 1].stat == "Protect":
                    protectSuccess = randint(1, pokemon1.intangibleOdds)
                    if protectSuccess == 1:
                        pokemon1.intangibility = True
                        pokemon1.volatile["Intangible"] = "Protect"
                        pokemon1.intangibleOdds *= 3
                    else:
                        pokemon1.intangibility = False
                        pokemon1.intangibleOdds = 1
                else:
                    pokemon1.intangibility = False
                    pokemon1.intangibleOdds = 1
                # Runs if stat changes or any secondary effect not covered by 
                # status or volatile
                if secondaryList[0] == "Stat":
                    if secondaryList[2] == "Self":
                        # Teleports to a party member
                        if pokemon1.Moves[moveNumber - 1].moveName == "Teleport" and attackingTeam.alivePokemon > 1:
                            if not computer:
                                position = int(self.team1.switchMenu())
                            else:
                                position = randint(1, 6)
                                while attackingTeam.pokemonList[position - 1].currentHp <= 0  or attackingTeam.pokemonList[position - 1] == pokemon1:
                                    position = randint(1, 6)
                            attackingTeam.Switch(position)
                            self.switchIn(attackingTeam.activePokemon, defendingTeam.activePokemon)
                        # Growth doubles the stat boost in sun
                        elif pokemon1.Moves[moveNumber - 1].moveName == "Growth" and self.weather[0] == "Sunny Day" and not self.cloudNine:
                            pokemon1.modifyStat("Attack/Special Attack", "2/2", True)
                        # Tidy Up removes hazards and subsitute, while boosting attack and speed
                        elif pokemon1.Moves[moveNumber - 1].moveName == "Tidy Up":
                            attackingTeam.entryHazards = {"Spikes" : 0, "Toxic Spikes" : 0, 
                                                 "Stealth Rock" : 0, "Sticky Web" : 0}
                            defendingTeam.entryHazards = {"Spikes" : 0, "Toxic Spikes" : 0, 
                                                 "Stealth Rock" : 0, "Sticky Web" : 0}
                            attackingTeam.activePokemon.volatile["Substitute"] = 0
                            defendingTeam.activePokemon.volatile["Substitute"] = 0
                            pokemon1.modifyStat(secondaryList[1], secondaryList[3], True)
                        # Camoflauge changes type depending on terrain first, weather second
                        elif pokemon1.Moves[moveNumber - 1].moveName == "Camoflauge":
                            if self.terrain[0] == "Grassy Terrain":
                                newType = "Grass"
                            elif self.terrain[0] == "Misty Terrain":
                                newType = "Fairy"
                            elif self.terrain[0] == "Electric Terrain":
                                newType = "Electric"
                            elif self.terrain[0] == "Psychic Terrain":
                                newType = "Psychic"
                            elif not self.weather[0] == "Clear" and not self.cloudNine:
                                if self.weather[0] == "Sunny Day":
                                    newType = "Fire"
                                elif self.weather[0] == "Rain Dance":
                                    newType = "Water"
                                elif self.weather[0] == "Hail":
                                    newType = "Ice"
                                elif self.weather[0] == "Sandstorm":
                                    newType = "Ground"
                                elif self.weather[0] == "Delta Stream":
                                    newType = "Flying"
                            else:
                                newType = "Normal"
                            pokemon1.changeType(newType, "None", False)
                            self.drawCurrentText(pokemon1.pokemonName + " camoflauged itself to become " + newType + "!")
                        # Reflect Type changes type to target's type
                        elif pokemon1.Moves[moveNumber - 1].moveName == "Reflect Type":
                            pokemon1.changeType(pokemon2.Type1.typeName, pokemon2.Type2.typeName, False)
                        # Conversion changes type to one of user's moves
                        elif pokemon1.Moves[moveNumber - 1].moveName == "Conversion":
                            typeChoices = []
                            for typeNumber in range(4): 
                                if not (pokemon1.Moves[typeNumber].moveType.typeName == pokemon1.Type1.typeName or pokemon1.Moves[typeNumber].moveType.typeName == pokemon1.Type2.typeName):
                                    typeChoices.append(pokemon1.Moves[typeNumber].moveType.typeName)
                            if len(typeChoices) == 0:
                                self.drawCurrentText(pokemon1.pokemonName + " failed to convert itself to a new type!")
                            else:
                                newTypeName = choice(typeChoices)
                                pokemon1.changeType(newTypeName, "None", False)
                                self.drawCurrentText(pokemon1.pokemonName + " converted to the " + newTypeName + " type!")
                        # Metronome calls a random move not in the following list
                        elif pokemon1.Moves[moveNumber - 1].moveName == "Metronome":
                            metronomeMove = moveDict[choice(moveList)]
                            while metronomeMove.moveName in ["After You", "Apple Acid", "Armor Cannon", "Assist", "Astral Barrage", "Aura Wheel",
                                                             "Baneful Bunker", "Beak Blast", "Behemoth Bash", "Behemoth Blasde", "Belch", "Bestow",
                                                             "Blazing Torque", "Body Press", "Branch Pokemon", "Breaking Swipe", "Celebrate", 
                                                             "Chatter", "Chilling Water", "Chilly Reception", "Clangorous Soul", "Collision Course",
                                                             "Combat Torque", "Comeuppance", "Copycat", "Counter", "Covet", "Crafty Shield",
                                                             "Decorate", "Destiny Bond", "Detect", "Diamond Storm", "Doodle", "Double Iron Bash",
                                                             "Double Shock", "Dragon Ascent", "Dragon Energy", "Drum Beating", "Dynamax Cannon",
                                                             "Electro Drift", "Endure", "Eternabeam", "False Surrender", "Feint", "Fiery Wrath",
                                                             "Fleur Cannon", "Fillet Away", "Focus Punch", "Follow Me", "Freeze Shock", "Freezing Glare",
                                                             "Glacial Lance", "Grav Apple", "Helping Hands", "Hold Hands", "Hyper Drill",
                                                             "Hyperspace Fury", "Hyperspace Hole", "Ice Burn", "Instruct", "Jet Punch",
                                                             "Jungle Healing", "King's Shield", "Life Dew", "Light of Ruin", "Make it Rain",
                                                             "Magical Torque", "Mat Block", "Me First", "Meteor Assault", "Mimic", "Mind Blown",
                                                             "Mirror Coat", "Mirror Move", "Moongeist Beam", "Nature Power", "Nature's Madness",
                                                             "Noxious Torque", "Obstruct", "Order Up", "Origin Pulse", "Overdrive", 
                                                             "Photon Geyser", "Plasma Fists", "Population Bomb", "Pounce", "Power Shift",
                                                             "Precipice Blades", "Protect", "Pyro Ball", "Quash", "Quick Guard", "Rage Fist",
                                                             "Rage Powder", "Raging Bull", "Raging Fury", "Relic Song", "Revival Blessing",
                                                             "Ruination", "Salt Cure", "Secret Sword", "Shed Tail", "Shell Trap", "Silk Trap",
                                                             "Sketch", "Sleep Talk", "Snap Trap", "Snarl", "Snatch", "Snore", "Snowscape",
                                                             "Spectral Thief", "Spicy Extract", "Spiky Shield", "Spirit Break", "Spotlight",
                                                             "Steam Eruption", "Steel Beam", "Strange Steam", "Struggle", "Sunsteel Strike",
                                                             "Surging Strikes", "Switcheroo", "Techno Blast", "Tidy Up", "Thief",
                                                             "Thousand Arrows", "Thousand Waves", "Thunder Cage", "Thunderous Kick",
                                                             "Trailblaze", "Transform", "Trick", "Twin Beam", "V-create", "Wicked Blow",
                                                             "Wicked Torque", "Wide Guard"]:
                                metronomeMove = moveDict[choice(moveList)]
                            pokemon1.Moves[5] = copy.deepcopy(metronomeMove)
                            pokemon1.Moves[5].currentPP = 1
                            self.fixType()
                            self.Attack(moveList, moveDict, 6, oppMoveNumber, priority1, priority2, analytic, stakeout, playerNum, computer, computer2, False, "Metronome")
                        # Me First uses the opponent's next move with more power
                        elif pokemon1.Moves[moveNumber - 1].moveName == "Me First":
                            if not analytic and not pokemon2.Moves[oppMoveNumber - 1] in ["Beak Blast", "Belch", "Chatter", "Counter", "Covet", "Focus Punch", "Metal Burst", "Mirror Coat", "Shell Trap", "Struggle", "Thief"] and not pokemon2.Moves[oppMoveNumber].phySpe == "Status":
                                pokemon1.Moves[5] = copy.deepcopy(pokemon2.Moves[oppMoveNumber - 1])
                                pokemon1.Moves[5].currentPP = 1
                                pokemon1.Moves[5].power *= 1.5
                                self.Attack(moveList, moveDict, 6, oppMoveNumber, priority1, priority2, analytic, stakeout, playerNum, computer, computer2, False, "Me First")
                        # Copycat and Mirror Move copy the opponent's last move as long
                        # as it is not in the following list
                        elif pokemon1.Moves[moveNumber - 1].moveName in ["Copycat", "Mirror Move"]:
                            if not oppLastMove in ["Assist", "Baneful Bunker", "Beak Blast", "Behemoth Bash", "Behemoth Blade",
                                                                                  "Bestow", "Celebrate", "Chatter", "Circle Throw", "Copycat", "Counter",
                                                                                  "Covet", "Destiny Bond", "Detect", "Dragon Tail", "Dynamax Cannon",
                                                                                  "Endure", "Feint", "Focus Punch", "Follow Me", "Helping Hand", "Hold Hands",
                                                                                  "King's Shield", "Mat Block", "Me First", "Metronome", "Mimic", "Mirror Coat",
                                                                                  "Mirror Move", "Protect", "Rage Powder", "Roar", "Shell Trap", "Sketch",
                                                                                  "Sleep Talk", "Snatch", "Struggle", "Spiky Shield", "Spotlight", "Switcheroo",
                                                                                  "Thief", "Transform", "Trick", "Whirlwind", None]:
                                for opponentMove in pokemon2.Moves:
                                    if  opponentMove == None:
                                        self.drawCurrentText("No moves were copied!")
                                        break
                                    elif opponentMove.moveName == oppLastMove:
                                        pokemon1.Moves[5] = copy.deepcopy(opponentMove)
                                        pokemon1.Moves[5].currentPP = 1
                                        self.Attack(moveList, moveDict, 6, oppMoveNumber, priority1, priority2, analytic, stakeout, playerNum, computer, computer2, False, "Copycat")
                                        break
                            else:
                                self.drawCurrentText("No moves were copied!")
                        # Sketch permanently learns the opponent's last used move
                        elif pokemon1.Moves[moveNumber - 1].moveName == "Sketch":
                            for opponentMove in pokemon2.Moves:
                                if  opponentMove == None:
                                    self.drawCurrentText("No moves were sketched!")
                                    break
                                elif opponentMove.moveName == oppLastMove:
                                    pokemon1.Moves[5] = copy.deepcopy(opponentMove)
                                    pokemon1.Moves[moveNumber - 1].currentPP = pokemon1.Moves[moveNumber - 1].pp
                                    self.drawCurrentText(pokemon1.pokemonName + " sketched the move " + pokemon1.Moves[moveNumber - 1].moveName + "!")
                                    break
                            
                        else:
                            # Changes the user's stat
                            pokemon1.modifyStat(secondaryList[1], secondaryList[3], True)
                            # Autonomize decreases mass by 100
                            if pokemon1.Moves[moveNumber - 1].moveName == "Autotomize":
                                pokemon1.currentMass -= 100
                                if pokemon1.currentMass < 0.1:
                                    pokemon1.currentMass = 0.1
                                self.drawCurrentText(pokemon1.pokemonName + " became nimble!")
                    else:    
                        # Intangible, substituted from non-sound and Infiltrator, and 
                        # bounce fail to hit status moves
                        if not pokemon2.intangibility and not (pokemon2.volatile["Substitute"] > 0  and not (pokemon1.Moves[moveNumber - 1].sound or (pokemon1.ability.abilityName == "Infiltrator" and not pokemon1.Moves[moveNumber - 1].moveName == "Transform"))) or bounce:
                            if typeEffect > 0 or pokemon1.Moves[moveNumber - 1].power == 0:
                                # Transform changes the user to opponent, with HP
                                # staying the same and all PP being 5
                                if pokemon1.Moves[moveNumber - 1].moveName == "Transform" and not (pokemon1.transformed or pokemon2.transformed):
                                    pokemon1.tempPokemon = [pokemon1.Stats, pokemon1.ability, pokemon1.tempType1.typeName, pokemon1.tempType2.typeName, pokemon1.Moves]
                                    pokemon1.Stats = copy.deepcopy(pokemon2.Stats)
                                    pokemon1.Stats["HP"] = pokemon1.tempPokemon[0]["HP"]
                                    pokemon1.ability = pokemon2.ability
                                    pokemon1.changeType(pokemon2.Type1.typeName, pokemon2.Type2.typeName, False)
                                    pokemon1.Moves = copy.deepcopy(pokemon2.Moves)
                                    for movePP in range(4):
                                        pokemon1.Moves[movePP].currentPP = 5
                                    pokemon1.transformed = True
                                    self.drawCurrentText(pokemon1.pokemonName + " transformed into " + pokemon2.pokemonName + "!")
                                    self.switchIn(attackingTeam.activePokemon, defendingTeam.activePokemon)
                                # Sets up entry hazards
                                elif pokemon1.Moves[moveNumber - 1].stat == "Entry Hazard":
                                    if pokemon1.Moves[moveNumber - 1].moveName in ["Stealth Rock", "Sticky Web"]:
                                        defendingTeam.entryHazards[pokemon1.Moves[moveNumber - 1].moveName] = 1
                                    elif pokemon1.Moves[moveNumber - 1].moveName == "Spikes" and defendingTeam.entryHazards[pokemon1.Moves[moveNumber - 1].moveName] < 3:
                                        defendingTeam.entryHazards[pokemon1.Moves[moveNumber - 1].moveName] += 1
                                    elif pokemon1.Moves[moveNumber - 1].moveName == "Toxic Spikes" and defendingTeam.entryHazards[pokemon1.Moves[moveNumber - 1].moveName] < 2:
                                        defendingTeam.entryHazards[pokemon1.Moves[moveNumber - 1].moveName] += 1
                                # Changes the target to a water type
                                elif pokemon1.Moves[moveNumber - 1].moveName == "Soak" and not pokemon2.ability.abilityName in ["Multitype", "RKS System"]:
                                    pokemon2.changeType("Water", "None", False)
                                    self.drawCurrentText(pokemon2.pokemonName + " was soaked and became a Water type!")
                                # Changes the target to a psychic type
                                elif pokemon1.Moves[moveNumber - 1].moveName == "Magic Powder" and not pokemon2.ability.abilityName in ["Multitype", "RKS System"]:
                                    pokemon2.changeType("Psychic", "None", False)
                                    self.drawCurrentText(pokemon2.pokemonName + " was powdered and became a Psychic type!")
                                else:
                                    # Certain abilities prevent stats from being lowered
                                    if not (pokemon2.ability.effect[0] == "Clear Body" and (pokemon2.ability.effect[1] in secondaryList[1] or pokemon2.ability.effect[1] == "All")):
                                        pokemon2.modifyStat(secondaryList[1], secondaryList[3], False)
                                        # Parting Shot switches with a party member
                                        if pokemon1.Moves[moveNumber - 1].moveName == "Parting Shot" and attackingTeam.alivePokemon > 1:
                                            # Full heal only happens from Darkinium Z
                                            if moveNumber == 7:
                                                fullHeal = True
                                            else:
                                                fullHeal = False
                                            if not computer:
                                                position = int(self.team1.switchMenu())
                                            else:
                                                position = randint(1, 6)
                                                while attackingTeam.pokemonList[position - 1].currentHp <= 0  or attackingTeam.pokemonList[position - 1] == pokemon1:
                                                    position = randint(1, 6)
                                            attackingTeam.Switch(position)
                                            self.switchIn(attackingTeam.activePokemon, defendingTeam.activePokemon)
                                            if fullHeal:
                                                attackingTeam.activePokemon.currentHp = attackingTeam.activePokemon.Stats["HP"]
                                        # Defog removes screens, entry hazards, and terrain
                                        elif pokemon1.Moves[moveNumber - 1].moveName == "Defog":
                                            attackingTeam.entryHazards = {"Spikes" : 0, "Toxic Spikes" : 0, 
                                                                 "Stealth Rock" : 0, "Sticky Web" : 0}
                                            defendingTeam.entryHazards = {"Spikes" : 0, "Toxic Spikes" : 0, 
                                                                 "Stealth Rock" : 0, "Sticky Web" : 0}
                                            defendingTeam.reflect = 0
                                            defendingTeam.lightScreen = 0
                                            self.terrain = ["Clear", 0]
                                            if pokemon1.ability.abilityName == "Mimicry":
                                                pokemon1.changeType(pokemon1.tempType1, pokemon1.tempType2, True)
                                            if pokemon2.ability.abilityName == "Mimicry":
                                                pokemon2.changeType(pokemon2.tempType1, pokemon2.tempType2, True)
                # Status conditions
                elif secondaryList[0] == "Status":
                    # Misty Terrain prevents grounded pokemon from being statused
                    if self.terrain[0] == "Misty Terrain" and not (pokemon1.Type1.typeName == "Flying" or pokemon1.Type2.typeName == "Flying" or pokemon1.ability.abilityName == "Levitate"):
                        self.drawCurrentText("Misty Terrain prevents Pokemon from being statused!")
                    # Electric Terrain prevents grounded pokemon from being put to sleep
                    elif self.terrain[0] == "Electric Terrain" and secondaryList[1] in ["Rest", "Sleep"] and not (pokemon1.Type1.typeName == "Flying" or pokemon1.Type2.typeName == "Flying" or pokemon1.ability.abilityName == "Levitate"):
                        self.drawCurrentText("Electric Terrain prevents Pokemon from being put to sleep!")
                    else:
                        if secondaryList[2] == "Self":
                            # Cures user's status condition
                            if (pokemon1.status == "Healthy" or pokemon1.Moves[moveNumber - 1].moveName in ["Refresh", "Rest"]) and not (pokemon1.ability.abilityName == "Leaf Guard" and self.weather[0] == "Sunny Day"):
                                pokemon1.changeStatus(secondaryList[1])
                        else:
                            if not pokemon2.intangibility and not (pokemon2.volatile["Substitute"] > 0  and not (pokemon1.Moves[moveNumber - 1].sound or pokemon1.ability.abilityName == "Infiltrator")) or bounce:
                                if typeEffect > 0 or pokemon1.Moves[moveNumber - 1].power == 0:
                                    if pokemon2.status == "Healthy" and not (pokemon2.ability.abilityName == "Leaf Guard" and self.weather[0] == "Sunny Day"):
                                        if pokemon1.ability.abilityName == "Corrosion":
                                            pokemon2.changeStatus(secondaryList[1], True)
                                            if pokemon2.ability.abilityName == "Synchronize" and pokemon1.status == "Healthy" and secondaryList[1] in ["Burn", "Paralyze", "Poison"]:
                                                pokemon1.changeStatus(secondaryList[1], True)
                                        else:
                                            pokemon2.changeStatus(secondaryList[1])
                                            if pokemon2.ability.abilityName == "Synchronize" and pokemon1.status == "Healthy" and secondaryList[1] in ["Burn", "Paralyze", "Poison"]:
                                                pokemon1.changeStatus(secondaryList[1], True)
                # Sparkling Aria cures the opponent's burn
                elif pokemon1.Moves[moveNumber - 1].moveName == "Sparkling Aria" and pokemon2.status == "Burn":
                    pokemon2.changeStatus("Healthy")
                # Volatile conditions
                elif secondaryList[0] == "Volatile":
                    # Misty terrain prevents pokemon from being confused
                    if self.terrain[0] == "Misty Terrain" and secondaryList[1] == "Confuse" and not (pokemon1.Type1.typeName == "Flying" or pokemon1.Type2.typeName == "Flying" or pokemon1.ability.abilityName == "Levitate"):
                        self.drawCurrentText("Misty Terrain prevents Pokemon from being statused!")
                    elif bounce and not pokemon1.Moves[moveNumber - 1].power > 0:
                        pass     
                    else:
                        # Gives the user a volatile condition
                        if secondaryList[2] == "Self":
                            if secondaryList[1] in ["Mean Look", "Ingrain"]:
                                if not pokemon1.volatile["Block Condition"] == secondaryList[1]:
                                    pokemon1.changeStatus(secondaryList[1])
                            elif pokemon1.volatile[secondaryList[1]] == 0:
                                pokemon1.changeStatus(secondaryList[1])
                        else:
                            if not pokemon2.intangibility and not (pokemon2.volatile["Substitute"] > 0  and not (pokemon1.Moves[moveNumber - 1].sound or pokemon1.ability.abilityName == "Infiltrator")):
                                if typeEffect > 0 or pokemon1.Moves[moveNumber - 1].power == 0:
                                    statusEffect = secondaryList[1]
                                    # Traps the opponent
                                    if statusEffect in ["Mean Look", "Octolock"]:
                                        pokemon2.changeStatus(statusEffect)
                                    elif pokemon2.volatile[statusEffect] == 0:
                                        # Infatuates pokemon of the opposite gender
                                        if statusEffect == "Infatuation":
                                            if (pokemon1.gender == "Male" and pokemon2.gender == "Female") or (pokemon2.gender == "Male" and pokemon1.gender == "Female"):
                                                pokemon2.changeStatus(statusEffect)
                                        # Both pokemon will faint in 3 turns unless switched
                                        elif statusEffect == "Perish":
                                            if pokemon1.volatile["Perish"] == 0:
                                                pokemon1.changeStatus(statusEffect)
                                            if pokemon2.volatile["Perish"] == 0:
                                                pokemon2.changeStatus(statusEffect)
                                        else:
                                            pokemon2.changeStatus(statusEffect)
                # Sets up a substitute
                elif pokemon1.Moves[moveNumber - 1].moveName == "Substitute" and pokemon1.volatile["Substitute"] >= 0:
                    pokemon1.volatile["Substitute"] = floor(pokemon1.Stats["HP"] * 0.25)
                # Sets up screens
                elif pokemon1.Moves[moveNumber - 1].moveName in ["Reflect", "Baddy Bad"] and attackingTeam.reflect == 0:
                    if pokemon1.item.itemName == "Light Clay":
                        attackingTeam.reflect = 8
                    else:
                        attackingTeam.reflect = 5
                elif pokemon1.Moves[moveNumber - 1].moveName in ["Light Screen", "Glitzy Glow"] and attackingTeam.lightScreen == 0:
                    if pokemon1.item.itemName == "Light Clay":
                        attackingTeam.reflect = 8
                    else:
                        attackingTeam.lightScreen = 5
                # Sets up weather if possible
                elif pokemon1.Moves[moveNumber - 1].stat == "Weather":
                    if not self.weather[0] == pokemon1.Moves[moveNumber - 1].moveName and self.weather[1] < 9:
                        if pokemon1.Moves[moveNumber - 1].moveName in pokemon1.item.effect and not pokemon1.item.consumed:
                            self.weather = [pokemon1.Moves[moveNumber - 1].moveName, 8]
                        else:
                            self.weather = [pokemon1.Moves[moveNumber - 1].moveName, 5]
                        if self.weather[0] == "Rain Dance":
                            self.drawCurrentText("It started to rain!")
                        elif self.weather[0] == "Sunny Day":
                            self.drawCurrentText("The sunlight turned harsh!")
                        elif self.weather[0] == "Hail":
                            self.drawCurrentText("It started to hail!")
                        elif self.weather[0] == "Sandstorm":
                            self.drawCurrentText("A sandstorm kicked up!")
                        if not self.cloudNine:
                            pokemon1.changeForm(self.weather[0])
                            pokemon2.changeForm(self.weather[0])
                # Sets up terrain
                elif pokemon1.Moves[moveNumber - 1].stat == "Terrain":
                    if self.terrain[0] != pokemon1.Moves[moveNumber - 1].moveName:
                        if pokemon1.item.itemName == "Terrain Extender":
                            self.terrain = [pokemon1.Moves[moveNumber - 1].moveName, 8]
                        else:
                            self.terrain = [pokemon1.Moves[moveNumber - 1].moveName, 5]
                        self.drawCurrentText(pokemon1.pokemonName + " created a " + pokemon1.Moves[moveNumber - 1].moveName + "!")
                        if pokemon1.ability.abilityName == "Mimicry":
                            if self.terrain[0] == "Grassy Terrain":
                                newType = "Grass"
                            elif self.terrain[0] == "Misty Terrain":
                                newType = "Fairy"
                            elif self.terrain[0] == "Electric Terrain":
                                newType = "Electric"
                            elif self.terrain[0] == "Psychic Terrain":
                                newType = "Psychic"
                            pokemon1.changeType(newType, "None", False)
                        if pokemon2.ability.abilityName == "Mimicry":
                            if self.terrain[0] == "Grassy Terrain":
                                newType = "Grass"
                            elif self.terrain[0] == "Misty Terrain":
                                newType = "Fairy"
                            elif self.terrain[0] == "Electric Terrain":
                                newType = "Electric"
                            elif self.terrain[0] == "Psychic Terrain":
                                newType = "Psychic"
                            pokemon2.changeType(newType, "None", False)
                # Haze resets stats
                elif pokemon1.Moves[moveNumber - 1].moveName == "Haze":
                    pokemon1.statModifier = {"Attack" : 1, "Defense" : 1,
                                  "Special Attack": 1, "Special Defense": 1, 
                                  "Speed" : 1, "Accuracy": 1, "Evasion": 1}
                    pokemon2.statModifier = {"Attack" : 1, "Defense" : 1,
                                  "Special Attack": 1, "Special Defense": 1, 
                                  "Speed" : 1, "Accuracy": 1, "Evasion": 1}
                    self.drawCurrentText("All stats have been reset!")
                # Sets HP to heal or damage depending on weather
                if pokemon1.Moves[moveNumber - 1].power == 0:
                    if pokemon1.Moves[moveNumber - 1].moveName in ["Moonlight", "Synthesis", "Morning Sun"] and not self.cloudNine:
                        if self.weather[0] in ["Hail", "Rain Dance", "Sandstorm"]:
                            weatherShift = .5
                        elif self.weather[0] == "Sunny Day":
                            weatherShift = 4/3
                        else:
                            weatherShift = 1
                    elif pokemon1.Moves[moveNumber - 1].moveName == "Shore Up" and self.weather == "Sandstorm" and not self.cloudNine:
                        weatherShift = 4/3
                    else:
                        weatherShift = 1
                    healDamage = floor(pokemon1.Moves[moveNumber - 1].healing * pokemon1.Stats["HP"] * weatherShift)
                # Struggle will always damage user for 1/4 full HP on hit
                elif pokemon1.Moves[moveNumber - 1].moveName == "Struggle":
                    if pokemon2.intangibility:
                        self.drawCurrentText(pokemon2.pokemonName + " is in an intangible state!")
                        healDamage = 0
                        if oppLastMove in ["King's Shield", "Spiky Shield", "Baneful Bunker", "Silk Trap", "Obstruct"]:
                            if oppLastMove == "King's Shield":
                                pokemon1.modifyStat("Attack", "-1", False)
                            elif oppLastMove == "Silk Trap":
                                pokemon1.modifyStat("Speed", "-1", False)
                            elif oppLastMove == "Obstruct":
                                pokemon1.modifyStat("Defense", "-2", False)
                            elif oppLastMove == "Spiky Shield":
                                healDamage = ceil(pokemon1.Stats["HP"] / -8)
                            elif oppLastMove == "Baneful Bunker" and not (pokemon1.ability.abilityName == "Leaf Guard" and self.weather[0] == "Sunny Day"):
                                pokemon1.changeStatus("Poison")
                    else:
                        healDamage = (-1) * floor(pokemon1.Stats["HP"] / 4)
                else:
                    # Certain moves hit through intangibility
                    if pokemon2.intangibility and not (pokemon1.Moves[moveNumber - 1].moveName in ["Earthquake", "Magnitude", "Surf", "Whirlpool", "Twister", "Gust", "Thunder", "Hurricane", "Sky Uppercut"] or pokemon1.Moves[moveNumber - 1].feint or (pokemon1.ability.abilityName == "Unseen Fist" and pokemon1.Moves[moveNumber - 1].contact) or (pokemon1.Moves[moveNumber - 1].target == "Self" and pokemon1.Moves[moveNumber - 1].phySpe == "Status")):
                        self.drawCurrentText(pokemon2.pokemonName + " is in an intangible state!")
                        healDamage = 0
                        if oppLastMove in ["King's Shield", "Spiky Shield", "Baneful Bunker", "Silk Trap", "Obstruct"] and pokemon1.Moves[moveNumber - 1].contact and not (pokemon1.ability.abilityName == "Long Reach" or pokemon1.item.itemName in ["Punching Glove", "Protective Pads"]):
                            if oppLastMove == "King's Shield":
                                pokemon1.modifyStat("Attack", "-1", False)
                            elif oppLastMove == "Silk Trap":
                                pokemon1.modifyStat("Speed", "-1", False)
                            elif oppLastMove == "Obstruct":
                                pokemon1.modifyStat("Defense", "-2", False)
                            elif oppLastMove == "Spiky Shield":
                                healDamage = ceil(pokemon1.Stats["HP"] / -8)
                            elif oppLastMove == "Baneful Bunker" and not (pokemon1.ability.abilityName == "Leaf Guard" and self.weather[0] == "Sunny Day"):
                                pokemon1.changeStatus("Poison")
                    elif typeEffect > 0:
                        if (pokemon1.Moves[moveNumber - 1].moveName in ["Earthquake", "Magnitude", "Surf", "Whirlpool", "Twister", "Gust", "Thunder", "Hurricane", "Sky Uppercut"] or pokemon1.Moves[moveNumber - 1].feint or (pokemon1.ability.abilityName == "Unseen Fist" and pokemon1.Moves[moveNumber - 1].contact)) and pokemon2.intangibility:
                            # Dig is hit by Earthquake and Magnitude for double damahe
                            if pokemon1.Moves[moveNumber - 1].moveName in ["Earthquake", "Magnitude"] and pokemon2.volatile["Intangible"] == "Dig":
                                damage *= 2
                            # Dive is hit by Surf and Whirlpool for double damage
                            elif pokemon1.Moves[moveNumber - 1].moveName in ["Surf", "Whirlpool"] and pokemon2.volatile["Intangible"] == "Dive":
                                damage *= 2
                            # Fly is hit by Twister and Gust for double damage
                            elif pokemon1.Moves[moveNumber - 1].moveName in ["Twister", "Gust"] and pokemon2.volatile["Intangible"] == "Fly":
                                damage *= 2
                            # Fly is hit by Thunder, Hurricane, and Sky Uppercut
                            elif pokemon1.Moves[moveNumber - 1].moveName in ["Thunder", "Hurricane", "Sky Uppercut"] and pokemon2.volatile["Intangible"] == "Fly":
                                damage *= 1
                            # Feint moves and Unseen Fist hit through protect
                            elif (pokemon1.Moves[moveNumber - 1].feint or (pokemon1.ability.abilityName == "Unseen Fist" and pokemon1.Moves[moveNumber - 1].contact)) and pokemon2.volatile["Intangible"] == "Protect":
                                self.drawCurrentText(pokemon2.pokemonName + " couldn't protect itself!")
                            else:
                                self.drawCurrentText(pokemon2.pokemonName + " is in an intangible state!")
                                healDamage = 0
                                damage = 0
                                if oppLastMove in ["King's Shield", "Spiky Shield", "Baneful Bunker", "Silk Trap"] and pokemon1.Moves[moveNumber - 1].contact and not (pokemon1.ability.abilityName == "Long Reach" and not pokemon1.item.itemName in ["Punching Glove", "Protective Pads"]):
                                   if oppLastMove == "King's Shield":
                                       pokemon1.modifyStat("Attack", "-1", False)
                                   elif oppLastMove == "Silk Trap":
                                       pokemon1.modifyStat("Speed", "-1", False)
                                   elif oppLastMove == "Obstruct":
                                       pokemon1.modifyStat("Defense", "-2", False)
                                   elif oppLastMove == "Spiky Shield":
                                       healDamage = ceil(pokemon1.Stats["HP"] / -8)
                                   elif oppLastMove == "Baneful Bunker" and not (pokemon1.ability.abilityName == "Leaf Guard" and self.weather[0] == "Sunny Day"):
                                       pokemon1.changeStatus("Poison")
                        # OHKO instantly faint the target
                        elif pokemon1.Moves[moveNumber - 1].stat == "OHKO":
                            damage = pokemon2.Stats["HP"]
                        # Super Fang, Nature's Madness, and Ruination cut 
                        # remaining HP in half
                        elif pokemon1.Moves[moveNumber - 1].stat == "Super Fang":
                            damage = floor(pokemon2.currentHp/2)
                            if damage < 1:
                                damage == 1
                        # Guardian of Alola cuts remaining HP in fourth
                        elif pokemon1.Moves[moveNumber - 1].moveName == "Guardian of Alola":
                            damage = floor(3*pokemon2.currentHp/4)
                            if damage < 1:
                                damage == 1
                        # Screens reduce the corresponding damage by half
                        if defendingTeam.reflect > 0 and pokemon1.Moves[moveNumber - 1].phySpe == "Physical" and pokemon1.Moves[moveNumber - 1].moveName not in ["Brick Break", "Psychic Fangs", "Raging Bull", "Seismic Toss"] and not pokemon1.ability.abilityName == "Infiltrator":
                            damage *= .5
                        elif defendingTeam.lightScreen > 0 and pokemon1.Moves[moveNumber - 1].phySpe == "Special" and pokemon1.Moves[moveNumber - 1].moveName not in ["Dragon Rage", "Night Shade", "Sonic Boom"] and not pokemon1.ability.abilityName == "Infiltrator":
                            damage *= .5
                        # Pursuit does double damage to switching opponents
                        if priority1 == 7:
                            damage *= 2
                        # Stakeout does double damage to switched in opponent
                        if stakeout and pokemon1.ability == "Stakeout":
                            damage *= 2
                        # Fishious Rend and Bolt Beak do double damage if first or opponent
                        # switched in
                        if (stakeout or not analytic) and pokemon1.Moves[moveNumber - 1].moveName in ["Bolt Beak", "Fishious Rend"]:
                            damage *= 2
                        # Skill Link hits the maximum amount of times
                        if pokemon1.ability.abilityName == "Skill Link":
                            hits = int(pokemon1.Moves[moveNumber - 1].hitTimes[1])
                        # Triple Kick and Triple Axel have a check for each hit
                        elif pokemon1.Moves[moveNumber - 1].moveName in ["Triple Kick", "Triple Axel"]:
                            tripleHit = randint(0, 900)
                            if tripleHit < 90:
                                hits = 1
                            elif tripleHit < 171:
                                hits = 2
                            else:
                                hits = 3
                        # Parental Bond hits twice
                        elif pokemon1.ability.abilityName == "Parental Bond" and pokemon1.Moves[moveNumber - 1].hitTimes[1] == "1":
                            hits = 2
                        # Ash Greninja hits 3 times with Water Shuriken
                        elif pokemon1.pokemonName == "Greninja (Ash)" and pokemon1.Moves[moveNumber - 1].moveName == "Water Shuriken":
                            hits = 3
                        # Population Bomb has a check for each hit
                        elif pokemon1.Moves[moveNumber - 1].moveName == "Population Bomb":
                            hits = 1
                            for hitAttempt in range(9):
                                hitRoll = randint(0, 10)
                                if hitRoll == 5:
                                    break
                                else:
                                    hits += 1
                        else:
                            hits = randint(int(pokemon1.Moves[moveNumber - 1].hitTimes[0]), int(pokemon1.Moves[moveNumber - 1].hitTimes[1]))
                        for attackHits in range(hits):
                            # Redraws HP bar before each hit
                            self.healthBar()
                            if attackHits > 0:
                                self.drawCurrentText("Hit number " + str(attackHits) + "!")
                            # Ice Face protects against the first physical attack
                            if pokemon2.ability.abilityName == "Ice Face" and pokemon2.currentForm == "Base" and pokemon1.Moves[moveNumber - 1].phySpe == "Physical" and not pokemon1.ability.effect[0] == "Mold Breaker":
                                damage = 0
                                pokemon2.changeForm(self.weather[0], True)
                            # Disguise protects against the first attack
                            elif pokemon2.ability.abilityName == "Disguise" and pokemon2.currentForm == "Base" and not pokemon1.ability.effect[0] == "Mold Breaker":
                                damage = 0
                                pokemon2.changeForm(self.weather[0], True)
                            # Illusion reveals that the pokemon was Zorua or Zoroark
                            elif pokemon2.ability.abilityName == "Illusion" and pokemon2.illusion:
                                pokemon2.illusion = False
                                self.drawCurrentText(pokemon2.pokemonName + "'s illusion wore off!")
                            # Type reducing berries weaken super effective attacks
                            if pokemon1.Moves[moveNumber - 1].moveType.typeName in pokemon2.item.effect and pokemon2.item.secondEffect == "Defend" and typeEffect > 1 and not pokemon2.item.consumed and not (pokemon1.ability.abilityName == "Unnerve" or "As One" in pokemon1.ability.abilityName):
                                pokemon2.item.Consume()
                                itemMult = pokemon2.item.multiplier
                                self.drawCurrentText(pokemon2.pokemonName + " lessened the damage with its " + pokemon2.item.itemName + "!")
                                # Cheek Pouch heals after eating a berry
                                if pokemon2.ability.abilityName == "Cheek Pouch":
                                    pokemon2.currentHp += ceil(pokemon2.Stats["HP"] * (1/3))
                                    if pokemon2.currentHp > pokemon2.Stats["HP"]:
                                        pokemon2.currentHp = pokemon2.Stats["HP"]
                            else:
                                itemMult = 1
                            # Brick Break, Psychic Fangs, and Raging Bull removes screens
                            if pokemon1.Moves[moveNumber - 1].moveName in ["Brick Break", "Psychic Fangs", "Raging Bull"] and typeEffect > 0:
                                defendingTeam.lightScreen = 0
                                defendingTeam.reflect = 0
                            # Ice Spinner and Steel Roller remove terrain
                            if pokemon1.Moves[moveNumber - 1].moveName in ["Ice Spinner", "Steel Roller"]:
                                self.terrain = ["Clear", 0]
                                if pokemon1.ability.abilityName == "Mimicry":
                                    pokemon1.changeType(pokemon1.tempType1, pokemon1.tempType2, True)
                                if pokemon2.ability.abilityName == "Mimicry":
                                    pokemon2.changeType(pokemon2.tempType1, pokemon2.tempType2, True)
                            # The second hit of parental bond is weaker
                            if pokemon1.ability.abilityName == "Parental Bond" and pokemon1.Moves[moveNumber - 1].hitTimes[1] == "1" and attackHits == 1 and not pokemon1.Moves[moveNumber - 1].stat in ["Set Damage", "Level Damage"]:
                                multiHit = .25
                            # Triple Kick and Triple Axel do more for each successful hit
                            elif pokemon1.Moves[moveNumber - 1].moveName in ["Triple Kick", "Triple Axel"]:
                                multiHit = attackHits + 1
                            else:
                                multiHit = 1
                            critChance = pokemon1.Moves[moveNumber - 1].crit
                            if pokemon2.ability.effect[0] == "Critical":
                                # Shell Armor and Battle Armor cannot be crit
                                if pokemon2.ability.effect[1] == "Immunity" and not pokemon1.ability.effect[0] == "Mold Breaker":
                                    crit = 25
                                    sniperBoost = 1
                                # Sniper increases the damage of critical hits
                                elif pokemon1.ability.effect[1] == "Boost":
                                    crit = randint(1, 24)
                                    sniperBoost = 2
                                else:
                                    crit = randint(1, 24)
                                    sniperBoost = 1.5
                                # Super Luck increases crit chance
                                if pokemon1.ability.effect[1] == "Lucky":
                                    if critChance == 1:
                                        critChance = 3
                                    elif critChance == 3:
                                        critChance = 12
                                    elif critChance == 12:
                                        critChance = 24
                                # Merciless always critial hits poisoned targets
                                elif pokemon1.ability == "Merciless" and pokemon2.status in ["Poison", "Badly Poison"] and critChance < 25:
                                    critChance = 24
                            else:
                                crit = randint(1, 24)
                                sniperBoost = 1.5
                            # Pumped pokemon crit more often
                            if pokemon1.volatile["Pumped"] == 1:
                                if critChance == 1:
                                    critChance = 12
                                elif critChance == 3 or critChance == 12:
                                    critChance = 24
                            # Critical hit items increase crit chance
                            if pokemon1.item.effect == "Critical":
                                if pokemon1.item.secondEffect == "Signature":
                                    if critChance == 1:
                                        critChance = 12
                                    elif critChance == 3 or critChance == 12:
                                        critChance = 24
                                else:
                                    if critChance == 1:
                                        critChance = 3
                                    elif critChance == 3:
                                        critChance = 12
                                    elif critChance == 12:
                                        critChance = 24
                            if pokemon2.volatile["Substitute"] <= 0 or pokemon1.Moves[moveNumber - 1].sound or pokemon1.ability.AbilityName == "Infiltrator":
                                # Critical hits ignore user's lowered stats and
                                # targets raised stats
                                if crit <= critChance:
                                    if pokemon1.Moves[moveNumber - 1].phySpe == "Physical" or pokemon1.Moves[moveNumber - 1].moveName in ["Secret Sword", "Psyshock", "Psystrike"]:
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
                                    pokemon2.currentHp -= int(damage * multiHit * sniperBoost * itemMult * defMod / attMod)
                                    self.drawCurrentText("Critical hit!")
                                    if pokemon2.currentHp < 0:
                                        healDamage = ceil((damage * multiHit + pokemon2.currentHp) * sniperBoost * pokemon1.Moves[moveNumber - 1].healing)
                                    else:
                                        healDamage = ceil(damage * multiHit * sniperBoost * pokemon1.Moves[moveNumber - 1].healing)
                                        # Anger Point maximizes attack after being crit
                                        if pokemon2.ability.abilityName == "Anger Point":
                                            pokemon2.modifyStat("Attack", "12", True)
                                else:
                                    pokemon2.currentHp -= int(damage * multiHit)
                                    if pokemon2.currentHp < 0:
                                        healDamage = ceil((damage * multiHit + pokemon2.currentHp) * pokemon1.Moves[moveNumber - 1].healing)
                                    else:
                                        healDamage = ceil(damage * multiHit * pokemon1.Moves[moveNumber - 1].healing)
                                # Weak Armor lowers defense and raises speed after each physical hit
                                if pokemon1.Moves[moveNumber - 1].phySpe == "Physical" and pokemon2.ability.abilityName == "Weak Armor":
                                    pokemon2.modifyStat("Defense/Speed", "-1/2", True)
                                # Stamina raises defense after each hit
                                elif pokemon2.ability.abilityName == "Stamina":
                                    pokemon2.modifyStat("Defense", "1", True)
                                # Cotton Down, Tangling Hair, and Gooey lower speed
                                elif pokemon2.ability.effect[0] == "Gooey":
                                    if pokemon2.ability.effect[1] == "Contact" and not (pokemon1.Moves[moveNumber - 1].contact and not (pokemon1.ability.abilityName == "Long Reach" or pokemon1.item.itemName in ["Punching Glove", "Protective Pads"])):
                                        pass
                                    else:
                                        pokemon1.modifyStat("Speed", "-1", False)
                                # Justiifed and Rattled raise a stat if hit by certain types
                                elif pokemon2.ability.effect[0] == "Justified":
                                    if pokemon1.Moves[moveNumber - 1].moveType.typeName in pokemon2.ability.effect[2]:
                                        pokemon2.modifyStat(pokemon2.ability.effect[1], "1", True)
                                # Opponent's contact abilities have a chance to trigger
                                elif pokemon1.Moves[moveNumber - 1].contact and not (pokemon1.ability.abilityName == "Long Reach" or pokemon1.item.itemName in ["Punching Glove", "Protective Pads"]) and pokemon2.ability.effect[0] == "Contact" and pokemon2.ability.target == "Opponent":
                                    if (pokemon1.Type1.typeName == "Grass" or pokemon1.Type2.typeName == "Grass" or pokemon1.ability.abilityName == "Overcoat") and pokemon2.ability.abilityName == "Effect Spore":
                                        success = 11
                                    else:
                                        success = randint(1,10)
                                    if success <= pokemon2.ability.success:
                                        if (pokemon1.status == "Healthy" and not (pokemon1.ability.abilityName == "Leaf Guard" and self.weather[0] == "Sunny Day")) or pokemon2.ability.effect[1] in ["Perish", "Infatuation"]:
                                            pokemon1.changeStatus(pokemon2.ability.effect[1])
                                        if pokemon2.ability.effect[1] == "Perish":
                                            pokemon2.changeStatus(pokemon2.ability.effect[1])
                                # Poison Touch has a chance to poison on contact
                                elif pokemon1.Moves[moveNumber - 1].contact and not pokemon1.item.itemName in ["Punching Glove", "Protective Pads"] and pokemon1.ability.abilityName == "Poison Touch":
                                    success = randint(1,10)
                                    if success <= pokemon1.ability.success and pokemon1.status == "Healthy" and not (pokemon1.ability.abilityName == "Leaf Guard" and self.weather[0] == "Sunny Day"):
                                        pokemon2.changeStatus("Poison")
                                        if pokemon2.ability.abilityName == "Synchronize" and pokemon1.status == "Healthy":
                                            pokemon1.changeStatus("Poison", True)
                                # Each hit increases the power of Rage Fist
                                if pokemon2.rageFist < 7:
                                    pokemon2.rageFist += 1
                                # Rage builds if it was the opponent's last move
                                if oppLastMove == "Rage":
                                    self.drawCurrentText(pokemon2.pokemonName + "'s rage is building!")
                                    pokemon2.modifyStat("Attack", "1", True)
                            else:
                                if pokemon2.ability.effect[0] == "Critical":
                                    if pokemon2.ability.effect[1] == "Immunity" and not pokemon1.ability.effect[0] == "Mold Breaker":
                                        crit = 25
                                else:
                                    crit = randint(1, 24)
                                if crit <= critChance:
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
                                    pokemon2.volatile["Substitute"] -= int(damage * multiHit * 1.5 * defMod / attMod * multiHit)
                                    self.drawCurrentText("Critical hit!")
                                    if pokemon2.volatile["Substitute"] < 0:
                                        healDamage = ceil((damage * multiHit + pokemon2.volatile["Substitute"]) * sniperBoost * pokemon1.Moves[moveNumber - 1].healing)
                                        if pokemon2.ability.abilityName == "Anger Point":
                                            pokemon2.modifyStat("Attack", "12", True)
                                    else:
                                        healDamage = ceil(damage * multiHit * sniperBoost * pokemon1.Moves[moveNumber - 1].healing)
                                else:
                                    pokemon2.volatile["Substitute"] -= int(damage * multiHit)
                                    healDamage = ceil(damage * pokemon1.Moves[moveNumber - 1].healing)
                                if floor(pokemon2.volatile["Substitute"]) <= 0:
                                    pokemon2.volatile["Substitute"] = 0
                                    self.drawCurrentText(pokemon2.pokemonName + "'s substitute broke!")
                        if hits > 1:
                            self.drawCurrentText("Hit " + str(hits) + " times!")
                
                if pokemon1.Moves[moveNumber - 1].power > 0:
                    # No effect ability text
                    if typeEffect == 0 or (pokemon2.ability.abilityName == "Wonder Guard" and typeEffect <= 1):
                        if pokemon2.ability.effect[0] == "Type Immunity" and pokemon1.Moves[moveNumber - 1].moveType.typeName == pokemon2.ability.effect[1]:
                            if pokemon2.ability.effect[2] == "None":
                                self.drawCurrentText(pokemon2.pokemonName + " levitated over the attack!")
                            elif pokemon2.ability.effect[2] == "Heal":
                                pokemon2.currentHp += pokemon2.Stats["HP"] * .25
                                self.drawCurrentText(pokemon2.pokemonName + " restored some health!")
                                if pokemon2.currentHp > pokemon2.Stats["HP"]:
                                    pokemon2.currentHp = pokemon2.Stats["HP"]
                            elif pokemon2.ability.success == 1:
                                pokemon2.modifyStat(pokemon2.ability.effect[2], "1", True)
                        else:
                            self.drawCurrentText("It had no effect...")
                        healDamage = 0
                    else:
                        # Gukp Missile hits the opponent
                        if pokemon2.ability.abilityName == "Gulp Missile" and not pokemon2.currentForm == "Base":
                            if pokemon2.currentForm == "Gulping":
                                pokemon1.modifyStat("Defense", "-1")
                            elif pokemon2.currentForm == "Gorging" and not (pokemon1.ability.abilityName == "Leaf Guard" and self.weather[0] == "Sunny Day"):
                                pokemon1.changeStatus("Paralyze")
                                if pokemon2.ability.abilityName == "Synchronize" and pokemon1.status == "Healthy":
                                    pokemon1.changeStatus("Paralyze", True)
                            healDamage -= ceil(pokemon2.Stats["HP"] * .25)
                            pokemon2.changeForm(self.weather[0], True)
                        # Surf and Dive changes Cramorant's form
                        if pokemon1.ability.abilityName == "Gulp Missile" and pokemon1.currentForm == "Base" and pokemon1.Moves[moveNumber - 1].moveName in ["Surf", "Dive"]:
                            pokemon1.changeForm(self.weather[0], True)
                        # Relic Song changes Meloetta's form
                        elif pokemon1.pokemonName == "Meloetta (Aria)" and pokemon1.Moves[moveNumber - 1].moveName == "Relic Song":
                            pokemon1.changeForm(self.weather[0], True)
                        # User recharges next turn
                        if pokemon1.Moves[moveNumber - 1].charge == "Recharge":
                            pokemon1.recharge = 1
                        if typeEffect < 1:
                            self.drawCurrentText("It was not very effective.")
                        elif typeEffect > 1:
                            self.drawCurrentText("It was super effective!")
                        # Thermal Exchange increases attack after being hit by a fire move
                        if pokemon2.ability.abilityName == "Thermal Exchange" and pokemon1.Moves[moveNumber - 1].moveType.typeName == "Fire":
                            pokemon2.modifyStat("Attack", "1", False)
                        # Water Compaction increases defense after being hit by a water move
                        elif pokemon2.ability.abilityName == "Water Compaction" and pokemon1.Moves[moveNumber - 1].moveType.typeName == "Water":
                            pokemon2.modifyStat("Defense", "2", False)
                        # Steam Engine increases speed after being hit by a fire or water move
                        elif pokemon2.ability.abilityName == "Steam Engine" and pokemon1.Moves[moveNumber - 1].moveType.typeName in ["Fire", "Water"]:
                            pokemon2.modifyStat("Speed", "6", False)
                        # Flings item if possible
                        if pokemon1.Moves[moveNumber - 1].moveName == "Fling":       
                            if not (pokemon1.item.consumed or pokemon1.item.fling == 0):
                                self.drawCurrentText(pokemon1.pokemonName + " flung its " + pokemon1.item.itemName + "!")
                                pokemon1.item.Consume()
                            else:
                                self.drawCurrentText(pokemon1.pokemonName + " failed to fling a thing!")
                            
                            itemDamage = False
                            if "Damage" in pokemon2.item.effect:
                                if pokemon2.item.consumable:
                                    if pokemon2.item.secondEffect == pokemon1.Moves[moveNumber - 1].phySpe and not pokemon2.item.consumed and not (pokemon1.ability.abilityName == "Unnerve" or "As One" in pokemon1.ability.abilityName):
                                        pokemon2.item.Consume()
                                        itemDamage = True
                                        # Cheek Pouch heals after eating a berry
                                        if pokemon2.ability.abilityName == "Cheek Pouch":
                                            pokemon2.currentHp += ceil(pokemon2.Stats["HP"] * (1/3))
                                            if pokemon2.currentHp > pokemon2.Stats["HP"]:
                                                pokemon2.currentHp = pokemon2.Stats["HP"]
                                else:
                                    if pokemon1.Moves[moveNumber - 1].contact and not (pokemon1.ability.abilityName == "Long Reach" or pokemon1.item.itemName in ["Punching Glove", "Protective Pads"]):
                                        itemDamage = True
                            if itemDamage:
                                pokemon1.currentHp -= round(pokemon1.Stats["HP"] * pokemon2.item.multiplier)
                                self.drawCurrentText(pokemon1.pokemonName + " was hurt by " + pokemon2.item.itemName + "!")
                        # Volt Switch, U-Turn, and Flip Turn switches with a party member    
                        elif (pokemon1.Moves[moveNumber - 1].moveName in ["Volt Switch", "U-turn", "Flip Turn"] or pokemon1.currentHp < 1) and attackingTeam.alivePokemon > 1:
                            if not computer:
                                position = int(self.team1.switchMenu())
                            else:
                                position = randint(1, 6)
                                while attackingTeam.pokemonList[position - 1].currentHp <= 0 or attackingTeam.pokemonList[position - 1] == pokemon1:
                                    position = randint(1, 6)
                            attackingTeam.Switch(position)
                            self.switchIn(attackingTeam.activePokemon, defendingTeam.activePokemon)
                        # Knock Off removes held item
                        elif pokemon1.Moves[moveNumber - 1].moveName == "Knock Off":
                            pokemon2.item.Consume()
                            (pokemon2.pokemonName + " had its " + pokemon2.item.itemName + " removed!")
                        # Rapid Spin and Mortal Spin remove entry hazards    
                        elif pokemon1.Moves[moveNumber - 1].moveName in ["Rapid Spin", "Mortal Spin"]:
                            attackingTeam.entryHazards = {"Spikes" : 0, "Toxic Spikes" : 0, 
                                                          "Stealth Rock" : 0, "Sticky Web" : 0}
                        # Jaw Lock traps the opponent
                        elif pokemon1.Moves[moveNumber - 1].moveName == "Jaw Lock":
                            pokemon2.changeStatus("Mean Look")
                        # Clear Smog resets the oppponent's stats
                        elif pokemon1.Moves[moveNumber - 1].moveName == "Clear Smog":
                            pokemon2.statModifier = {"Attack" : 1, "Defense" : 1,
                                          "Special Attack": 1, "Special Defense": 1, 
                                          "Speed" : 1, "Accuracy": 1, "Evasion": 1}
                            self.drawCurrentText(pokemon2.pokemonName + "'s stats have been reset!")
                # Heals the user        
                if healDamage > 0:
                    # Liquid Ooze hurts the user instead of heal
                    if pokemon2.ability.abilityName == "Liquid Ooze" and pokemon1.Moves[moveNumber - 1].power > 0:
                        self.drawCurrentText(pokemon1.pokemonName + " sucked in liquid ooze!")
                        pokemon1.currentHp -= healDamage
                    else:
                        self.drawCurrentText(pokemon1.pokemonName + " had its health restored!")
                        pokemon1.currentHp += healDamage
                        # Roost removes flying type until next turn
                        if pokemon1.Moves[moveNumber - 1].moveName == "Roost":
                            if pokemon1.Type1.typeName == "Flying":
                                pokemon1.changeType(pokemon1.Type2.typeName, "None", False)
                            elif pokemon1.Type2.typeName == "Flying":
                                pokemon1.changeType(pokemon1.Type1.typeName, "None", False)
                            pokemon1.roosted = True
                # Recoil damage
                elif healDamage < 0 and not (pokemon1.ability.abilityName == "Rock Head" and not (pokemon1.Moves[moveNumber - 1].moveName == "Struggle" or pokemon1.Moves[moveNumber - 1].phySpe == "Status")):
                    self.drawCurrentText(pokemon1.pokemonName + " was hit in recoil!")
                    pokemon1.currentHp += healDamage
                # Color Change changes type to opponent's move
                if pokemon2.ability.abilityName == "Color Change":
                    self.drawCurrentText(pokemon2.pokemonName + " color changed to the " + pokemon1.Moves[moveNumber - 1].moveType.typeName + " type!")
                    pokemon2.changeType(pokemon1.Moves[moveNumber - 1].moveType.typeName, "None", False)
        
        elif hit == 142:
            pass
        else:
            # Bounce back text
            if bounce:
                self.drawCurrentText(pokemon2.pokemonName + " used " + pokemon1.Moves[moveNumber - 1].moveName + "!")
                self.drawCurrentText("The attack was bounced back!")      
            # Lowers PP by 1 normally or 2 if opponent's ability is pressure
            elif not pokemon1.chargeMove is None:
                if pokemon2.ability.abilityName == "Pressure":
                    pokemon1.Moves[pokemon1.chargeMove].currentPP -= 2
                else:
                    pokemon1.Moves[pokemon1.chargeMove].currentPP -= 1
                self.drawCurrentText(pokemon1.pokemonName + " used " + pokemon1.Moves[pokemon1.chargeMove].moveName + "!")
                pokemon1.chargeMove = None
                pokemon1.recharge = 0
            else:
                if pokemon2.ability.abilityName == "Pressure":
                    pokemon1.Moves[moveNumber - 1].currentPP -= 2
                else:
                    pokemon1.Moves[moveNumber - 1].currentPP -= 1
                self.drawCurrentText(pokemon1.pokemonName + " used " + pokemon1.Moves[moveNumber - 1].moveName + "!")
            self.drawCurrentText("The attack missed!")
        # Leppa Berry heals PP by at most 10   
        if pokemon1.Moves[moveNumber - 1].currentPP <= 0 and str(pokemon1.item) == "Leppa Berry" and not pokemon1.item.consumed and not (pokemon2.ability.abilityName == "Unnerve" or "As One" in pokemon2.ability.abilityName):
            pokemon1.item.Consume()
            self.drawCurrentText(pokemon1.pokemonName + " restored PP with its Leppa Berry!")
            if 10 <= pokemon1.Moves[moveNumber - 1].pp:
                pokemon1.Moves[moveNumber - 1].currentPP = 10
            else:
                pokemon1.Moves[moveNumber - 1].currentPP = pokemon1.Moves[moveNumber - 1].pp
            # Cheek Pouch heals after eating a berry
            if pokemon1.ability.abilityName == "Cheek Pouch":
                pokemon1.currentHp += ceil(pokemon1.Stats["HP"] * (1/3))
                if pokemon1.currentHp > pokemon1.Stats["HP"]:
                    pokemon1.currentHp = pokemon1.Stats["HP"]
        # Explosion, Self-Destruct, and Misty Explosion faints the user
        if pokemon1.Moves[moveNumber - 1].moveName in ["Explosion", "Self-Destruct", "Misty Explosion"] and beatStatus and not pokemon1.ability.abilityName == "Damp" and not pokemon2.ability.abilityName == "Damp":
            pokemon1.currentHp = 0
        # Sets the user's HP to max if above  
        if pokemon1.currentHp > pokemon1.Stats["HP"]:
            pokemon1.currentHp = pokemon1.Stats["HP"]
            moxie = True
        # Attacker faints from own attack
        elif pokemon1.currentHp <= 0:
            pokemon1.currentHp = 0
            pokemon2.volatile["Trap"] = 0
            self.drawCurrentText(pokemon1.pokemonName + " fainted!")
            attackingTeam.alivePokemon -= 1
            if attackingTeam.alivePokemon > 0:
                 while attackingTeam.activePokemon.currentHp <= 0:
                     if not computer:
                        position = int(self.team1.switchMenu())
                     else:
                        position = randint(1, 6)
                        while attackingTeam.pokemonList[position - 1].currentHp <= 0 or attackingTeam.pokemonList[position - 1] == pokemon1:
                            position = randint(1, 6)
                     attackingTeam.Switch(position)
                 self.switchIn(attackingTeam.activePokemon, defendingTeam.activePokemon)
            moxie = False
        else:
            moxie = True
        # Damage does at least the opponent's remaining HP
        if pokemon2.currentHp <= 0:
            # If sturdy, lives the attack on 1 HP
            if pokemon2.ability.abilityName == "Sturdy" and fullHP and not hits>1:
                pokemon2.currentHp = 1
                sturdy = True
            elif pokemon2.item.itemName == "Focus Sash" and fullHP and not hits>1 and not pokemon2.item.consumed:
                pokemon2.currentHP = 1
                sturdy = True
                pokemon2.item.consume()
            elif pokemon2.item.itemName == "Focus Band" and not pokemon2.item.consumed:
                focusBand = randint(1,10)
                if focusBand == 1:
                    pokemon2.currentHp = 1
                    sturdy = True
                else:
                    sturdy = False
            else:
                sturdy = False
            if not sturdy:
                pokemon2.currentHp = 0
                pokemon1.volatile["Trap"] = 0
                self.drawCurrentText(pokemon2.pokemonName + " fainted!")
                if moxie:
                    # Boosts related stat if Moxie
                    if pokemon1.ability.effect[0] == "Moxie":
                        if pokemon1.ability.effect[1] == "Best":
                            bestStatValue = 0
                            for statValue in pokemon1.Stats:
                                if not statValue == "HP":
                                    if bestStatValue < pokemon1.Stats[statValue]:
                                        bestStatValue = pokemon1.Stats[statValue]
                                        statName = statValue
                            pokemon1.modifyStat(statName, "1", True)
                        else:
                            pokemon1.modifyStat(pokemon1.ability.effect[1], "1", True)
                    # Greninja changes to Ash Greninja
                    elif pokemon1.ability.abilityName == "Battle Bond":
                        pokemon1.changeForm(self.weather[0], True)
                    # Fell Stinger boosts attack
                    if pokemon1.Moves[moveNumber - 1].moveName == "Fell Stinger":
                        pokemon1.modifyStat("Attack", "3", True)
                defendingTeam.alivePokemon -= 1
                if defendingTeam.alivePokemon > 0:
                     while defendingTeam.activePokemon.currentHp <= 0:
                         if not computer2:
                             position = int(self.team1.switchMenu())
                         else:
                            player2SwitchList = []
                            currentPokemon = self.team2.activePokemon
                            for pokemonSlot in range(6):
                                leastDamage = 999
                                for pokemonSlot2 in range(6):
                                    self.team2.activePokemon = self.team2.pokemonList[pokemonSlot2]
                                    damage1, unimportant = self.damageCalc(1, 1, False)
                                    damage2, unimportant = self.damageCalc(2, 1, False)
                                    damage = max(damage1, damage2)
                                    if damage < leastDamage and (pokemonSlot2 + 1) not in player2SwitchList:
                                        leastDamage = self.team2.pokemonList[pokemonSlot2].currentHp
                                        healthiest = pokemonSlot2 + 1
                                player2SwitchList.append(healthiest)
                            count = 0
                            position = player2SwitchList[0]
                            self.team2.activePokemon = currentPokemon
                            while self.team2.pokemonList[player2SwitchList[count] - 1] == self.team2.activePokemon or self.team2.pokemonList[player2SwitchList[count] - 1].currentHp <= 0:
                                position = player2SwitchList[count + 1]
                                count += 1
                         defendingTeam.Switch(position)
                     self.switchIn(defendingTeam.activePokemon, attackingTeam.activePokemon)
        # Boosts stat if Berserk or Anger Shell at half or less HP            
        if pokemon2.currentHp > 0 and pokemon2.currentHp <= .5 * pokemon2.Stats["HP"] and pokemon2.ability.effect[0] == "Berserk":
            if pokemon2.ability.abilityName == "Anger Shell":
                pokemon2.modifyStat(pokemon2.ability.effect[1], "1/1/1", True)
                pokemon2.modifyStat(pokemon2.ability.effect[2], "-1/-1", True)
            else:
                pokemon2.modifyStat(pokemon2.ability.effect[1], "1", True)
        # Berry cures status
        if pokemon2.status in pokemon2.item.effect and not pokemon2.item.consumed and "Berry" in pokemon2.item.itemName and not (pokemon1.ability.abilityName == "Unnerve" or "As One" in pokemon1.ability.abilityName):
            self.drawCurrentText(pokemon2.pokemonName + " status was cured by a "+ pokemon2.item.itemName + "!")
            pokemon2.changeStatus("Healthy")
            pokemon2.item.Consume()
            # Cheek Pouch heals after eating a berry
            if pokemon2.ability.abilityName == "Cheek Pouch":
                pokemon2.currentHp += ceil(pokemon2.Stats["HP"] * (1/3))
                if pokemon2.currentHp > pokemon2.Stats["HP"]:
                    pokemon2.currentHp = pokemon2.Stats["HP"]
        # Berry cures confusion
        elif pokemon2.volatile["Confuse"] == 1 and "Confuse" in pokemon2.item.effect and not pokemon2.item.consumed and not (pokemon1.ability.abilityName == "Unnerve" or "As One" in pokemon1.ability.abilityName):
            self.drawCurrentText(pokemon2.pokemonName + " status was cured by a berry!")
            pokemon2.volatile["Confuse"] = 0
            pokemon2.item.Consume()
            # Cheek Pouch heals after eating a berry
            if pokemon2.ability.abilityName == "Cheek Pouch":
                pokemon2.currentHp += ceil(pokemon2.Stats["HP"] * (1/3))
                if pokemon2.currentHp > pokemon2.Stats["HP"]:
                    pokemon2.currentHp = pokemon2.Stats["HP"]
        # Shed Shell prevents trapping
        elif (pokemon2.volatile["Trap"] > 0 or not pokemon2.volatile["Block Condition"] == "None") and "Trap" in pokemon2.item.effect and not pokemon2.item.consumed:
            pokemon2.volatile["Trap"] = 0
            pokemon2.volatile["Block Condition"] = "None"
        # Certain moves will thaw out a frozen pokemon
        elif pokemon2.status == "Freeze":
            if pokemon1.Moves[moveNumber - 1].moveName in ["Flame Wheel",
                                 "Sacred Fire", "Flare Blitz", "Scald",
                                 "Steam Eruption", "Burn Up", "Pyro Ball",
                                 "Scorching Sands"]:
                    pokemon2.changeStatus("Healthy")
                    self.drawCurrentText(pokemon1.pokemonName + " used " + pokemon1.Moves[moveNumber -1].moveName +
                          " and thawed " + pokemon2.pokemonName + " out!")
        # Wake-Up Slap wakes up sleeping pokemon
        elif pokemon2.status in ["Rest", "Sleep"]:
            if pokemon1.Moves[moveNumber - 1].moveName == "Wake-Up Slap":
                pokemon2.changeStatus("Healthy")
                self.drawCurrentText(pokemon2.pokemonName + " was woken up with Wake-Up Slap!")
        # Smelling Salts cures paralyzed pokemon
        elif pokemon2.status == "Paralyze":
            if pokemon1.Moves[moveNumber - 1].moveName == "Smelling Salts":
                pokemon2.changeStatus("Healthy")
                self.drawCurrentText(pokemon2.pokemonName + " was unparalyzed by Smelling Salts!")
        # Misty Terrain cures statused and confused pokemon        
        if self.terrain == "Misty Terrain":
            if not pokemon1.status == "Healthy" and not (pokemon1.Type1.typeName == "Flying" or pokemon1.Type2.typeName == "Flying" or pokemon1.ability.abilityName == "Levitate"):
                pokemon1.changeStatus("Healthy")
            if not pokemon2.status == "Healthy" and not (pokemon2.Type1.typeName == "Flying" or pokemon2.Type2.typeName == "Flying" or pokemon2.ability.abilityName == "Levitate"):
                pokemon2.changeStatus("Healthy")
            if pokemon1.volatile["Confuse"] >= 1 and not (pokemon1.Type1.typeName == "Flying" or pokemon1.Type2.typeName == "Flying" or pokemon1.ability.abilityName == "Levitate"):
                pokemon1.volatile["Confuse"] = 0
            if pokemon2.volatile["Confuse"] >= 1 and not (pokemon2.Type1.typeName == "Flying" or pokemon2.Type2.typeName == "Flying" or pokemon2.ability.abilityName == "Levitate"):
                pokemon2.volatile["Confuse"] = 0
        # Electric terrain wakes up sleeping pokemon
        elif self.terrain == "Electric Terrain":
            if pokemon1.status in ["Rest", "Sleep"] and not (pokemon1.Type1.typeName == "Flying" or pokemon1.Type2.typeName == "Flying" or pokemon1.ability.abilityName == "Levitate"):
                pokemon1.changeStatus("Healthy")
            if pokemon2.status in ["Rest", "Sleep"] and not (pokemon2.Type1.typeName == "Flying" or pokemon2.Type2.typeName == "Flying" or pokemon2.ability.abilityName == "Levitate"):
                pokemon2.changeStatus("Healthy")
        # Refreshes the HP bar
        self.healthBar()
    
    # Turn takes a turn for both teams                 
    def Turn(self, moveList, moveDict, megaDict, megaList, zMoveDict, itemDict, computer = False):
        # Sends in both pokemon on turn one
        if self.team1.activePokemon.turnOut == 0 and self.team2.activePokemon.turnOut == 0:
            self.switchIn(self.team1.activePokemon, self.team2.activePokemon)
            self.switchIn(self.team2.activePokemon, self.team1.activePokemon)
        # Cloud Nine changes forms of weather pokemon
        if self.cloudNine:
            self.team1.activePokemon.changeForm("Clear")
            self.team2.activePokemon.changeForm("Clear")
        # Weather changes form of weather pokemon
        else:
            self.team1.activePokemon.changeForm(self.weather[0], True)
            self.team2.activePokemon.changeForm(self.weather[0], True)
        # Draws the HP bar
        self.healthBar()
        # Keeps track of number of non-fainted pokemon
        alive1 = int(self.team1.alivePokemon)
        alive2 = int(self.team2.alivePokemon)
        # Choice of attack, switch, or forfeit
        player1Choice = "nothing"
        player2Choice = "nothing"
        # Increases number of turns out
        self.team1.activePokemon.turnOut += 1
        self.team2.activePokemon.turnOut += 1
        # Choice Scarf boosts speed by 1.5 times
        if self.team1.activePokemon.turnOut == 1 and self.team1.activePokemon.item.itemName == "Choice Scarf":
            scarfSpeed = 1.5
        else:
            scarfSpeed = 1
        if self.team2.activePokemon.turnOut == 1 and self.team2.activePokemon.item.itemName == "Choice Scarf":
            scarfSpeed /= 1.5
        # Team 1 can choose a move if not charging or recharging
        if self.team1.activePokemon.recharge == 0:
            # Blocked pokemon must attack or forfeit
            if self.team1.activePokemon.volatile["Trap"] > 0 or not self.team1.activePokemon.volatile["Block Condition"] == "None":
                choiceList = self.attackMenu(True)
                player1Choice = choiceList[0]
                team1Move = choiceList[1]
                willStruggle = True
                # Checks if there are any legal moves or forces pokemon to struggle
                for moveNum in range(5):
                    if self.team1.activePokemon.Moves[moveNum].currentPP > 0 and (moveNum + 1) not in self.team1.activePokemon.volatile["Blocked Moves"]:
                        willStruggle = False
                # Player 1 attacks
                if player1Choice == "attack":
                     if willStruggle:
                        self.drawCurrentText(self.team1.activePokemon.pokemonName + " has run out of moves!")
                        team1Move = 5
                        priority1 = 0
                     else:
                        # Attacks with a signature Z Move
                        if len(choiceList) > 3 and not self.team1.zMove and not self.team1.activePokemon.Moves[6] == None:
                            if choiceList[3] and self.team1.activePokemon.Moves[choiceList[1] - 1].moveName == self.team1.activePokemon.Moves[6].base:
                                team1Move = 7
                                # Necrozma changes form to Ultra Necrozma
                                if self.team1.activePokemon.Moves[6].moveName == "Light That Burns the Sky":
                                    self.team1.activePokemon.changeForm(self.weather, True)
                            else:
                                team1Move = choiceList[1]
                        # Attacks with non-status Z Move
                        elif len(choiceList) > 3 and not self.team1.zMove and self.team1.activePokemon.Moves[choiceList[1] - 1].moveType.typeName == self.team1.activePokemon.item.secondEffect and not self.team1.activePokemon.Moves[choiceList[1] - 1].phySpe == "Status":                        
                            if choiceList[3]:
                                team1Move = 7
                                for zMove in zMoveDict:
                                    if zMoveDict[zMove].crystal == self.team1.activePokemon.item.itemName:
                                        self.team1.activePokemon.Moves[6] = zMoveDict[zMove]
                                        # Decides the power of Z Move using base power
                                        # of regular move or exceptions
                                        zPowerDict = {140:200, 130:195, 120:190,
                                                      110:185, 100:180, 90:170,
                                                      80:160, 70:140, 60:120, 1:100}
                                        zSpecialDict = {"Mega Drain":120, "Weather Ball":160,
                                                        "Hex": 160,"Gear Grind":180,
                                                        "V-create":220, "Flying Press":170,
                                                        "Core Enforcer":140}
                                        if self.team1.activePokemon.Moves[choiceList[1] - 1].moveName not in zSpecialDict:
                                            for zPower in zPowerDict:
                                                if self.team1.activePokemon.Moves[choiceList[1] - 1].power >= zPower:
                                                    self.team1.activePokemon.Moves[6].power = zPowerDict[zPower]
                                                    self.team1.activePokemon.Moves[6].phySpe = self.team1.activePokemon.Moves[choiceList[1] - 1].phySpe
                                                    break
                                        else:
                                            self.team1.activePokemon.Moves[6].power = zSpecialDict[self.team1.activePokemon.Moves[choiceList[1] - 1].moveName]
                            else:
                                team1Move = choiceList[1]
                        # Attacks with status Z Move
                        elif len(choiceList) > 3 and not self.team1.zMove and self.team1.activePokemon.Moves[choiceList[1] - 1].moveType.typeName == self.team1.activePokemon.item.secondEffect and self.team1.activePokemon.Moves[choiceList[1] - 1].phySpe == "Status":
                            if choiceList[3]:
                                self.team1.activePokemon.Moves[6] = self.team1.activePokemon.Moves[choiceList[1] - 1]
                                team1Move = 7
                            else:
                                team1Move = choiceList[1]
                        else:
                            team1Move = choiceList[1]
                        priority1 = self.team1.activePokemon.Moves[team1Move - 1].priority
                # Player 1 forfeits, closing the graphics window
                else:
                    priority1 = 7
                    self.drawCurrentText("Player 1 has forfeitted")
                    return True
            else:
                # Forced to attack, switch, or forfeit
                while not player1Choice in ["attack", "switch", "forfeit"]:
                    choiceList = self.mainMenu()
                    player1Choice = choiceList[0]
                    if player1Choice == "switch":
                        priority1 = 6
                    elif player1Choice == "attack":
                        willStruggle = True
                        for moveNum in range(5):
                            if self.team1.activePokemon.Moves[moveNum].currentPP > 0 and (moveNum + 1) not in self.team1.activePokemon.volatile["Blocked Moves"]:
                                willStruggle = False
                        if willStruggle:
                            self.drawCurrentText(self.team1.activePokemon.pokemonName + " has run out of moves!")
                            team1Move = 5
                            priority1 = 0
                        else:
                            if len(choiceList) > 3 and not self.team1.zMove and not self.team1.activePokemon.Moves[6] == None:
                                if choiceList[3] and self.team1.activePokemon.Moves[choiceList[1] - 1].moveName == self.team1.activePokemon.Moves[6].base:
                                    team1Move = 7
                                    if self.team1.activePokemon.Moves[6].moveName == "Light That Burns the Sky":
                                        self.team1.activePokemon.changeForm(self.weather, True)
                                else:
                                    team1Move = choiceList[1]
                            elif len(choiceList) > 3 and not self.team1.zMove and self.team1.activePokemon.Moves[choiceList[1] - 1].moveType.typeName == self.team1.activePokemon.item.secondEffect and not self.team1.activePokemon.Moves[choiceList[1] - 1].phySpe == "Status":                        
                                if choiceList[3]:
                                    team1Move = 7
                                    for zMove in zMoveDict:
                                        if zMoveDict[zMove].crystal == self.team1.activePokemon.item.itemName:
                                            self.team1.activePokemon.Moves[6] = zMoveDict[zMove]
                                            zPowerDict = {140:200, 130:195, 120:190,
                                                          110:185, 100:180, 90:170,
                                                          80:160, 70:140, 60:120, 1:100}
                                            zSpecialDict = {"Mega Drain":120, "Weather Ball":160,
                                                            "Hex": 160,"Gear Grind":180,
                                                            "V-create":220, "Flying Press":170,
                                                            "Core Enforcer":140}
                                            if self.team1.activePokemon.Moves[choiceList[1] - 1].moveName not in zSpecialDict:
                                                for zPower in zPowerDict:
                                                    if self.team1.activePokemon.Moves[choiceList[1] - 1].power >= zPower:
                                                        self.team1.activePokemon.Moves[6].power = zPowerDict[zPower]
                                                        self.team1.activePokemon.Moves[6].phySpe = self.team1.activePokemon.Moves[choiceList[1] - 1].phySpe
                                                        break
                                            else:
                                                self.team1.activePokemon.Moves[6].power = zSpecialDict[self.team1.activePokemon.Moves[choiceList[1] - 1].moveName]
                                else:
                                    team1Move = choiceList[1]
                            elif len(choiceList) > 3 and not self.team1.zMove and self.team1.activePokemon.Moves[choiceList[1] - 1].moveType.typeName == self.team1.activePokemon.item.secondEffect and self.team1.activePokemon.Moves[choiceList[1] - 1].phySpe == "Status":
                                if choiceList[3]:
                                    self.team1.activePokemon.Moves[6] = self.team1.activePokemon.Moves[choiceList[1] - 1]
                                    team1Move = 7
                                else:
                                    team1Move = choiceList[1]
                            else:
                                team1Move = choiceList[1]

                        priority1 = self.team1.activePokemon.Moves[team1Move - 1].priority
                    elif player1Choice == "forfeit":
                        priority1 = 7
                        self.drawCurrentText("Player 1 has forfeitted")
                        return True
        # Uses a charged move
        elif self.team1.activePokemon.recharge == -1:
            player1Choice = "attack"
            team1Move =  self.team1.activePokemon.chargeMove + 1
            priority1 = 0
            choiceList = ["attack"]
        # Recharges a move
        else:
            player1Choice = "attack"
            team1Move = 1
            priority1 = 0
            choiceList = ["attack"]
        # Team 2 can choose a move if not charging or recharging   
        if self.team2.activePokemon.recharge == 0:
            # Human player chooses a move
            if not computer:
                self.drawCurrentText("\n" + self.team2.activePokemon.pokemonName + "\n")
                if self.team2.activePokemon.volatile["Trap"] > 0 or not self.team2.activePokemon.volatile["Block Condition"] == "None":
                    player2Choice == "attack"
                    team2Move = int(input("Choose a move "))
                    while self.team2.activePokemon.Moves[team2Move - 1].currentPP <= 0 or team2Move in self.team2.activePokemon.volatile["Blocked Moves"]:
                        team2Move = int(input("The move has no PP!\nChoose a Move "))
                    priority2 = self.team2.activePokemon.Moves[team2Move - 1].priority
                else:
                    while not player2Choice in ["attack", "switch", "forfeit"]:
                        player2Choice = self.mainMenu()
                        if player2Choice == "switch":
                            priority2 = 6
                            player2Switch = int(self.team2.switchMenu())
                        elif player2Choice == "attack":
                            willStruggle = True
                            for moveNum in range(5):
                                if self.team2.activePokemon.Moves[moveNum].currentPP > 0 and (moveNum + 1) not in self.team2.activePokemon.volatile["Blocked Moves"]:
                                    willStruggle = False
                            if willStruggle:
                                self.drawCurrentText(self.team2.activePokemon.pokemonName + " has run out of moves!")
                                team2Move = 5
                                priority2 = 0
                            else:
                                team2Move = int(input("Choose a move "))
                                while self.team2.activePokemon.Moves[team2Move - 1].currentPP <= 0 or team2Move in self.team2.activePokemon.volatile["Blocked Moves"]:
                                    team2Move = int(input("The move has no PP!\nChoose a Move"))
                                priority2 = self.team2.activePokemon.Moves[team2Move - 1].priority
            # Computer player chooses a move
            else:
                strongestAttack = {5 : -2}
                for attack in range(4):
                    if self.team2.activePokemon.Moves[attack].currentPP > 0 and (attack + 1) not in self.team2.activePokemon.volatile["Blocked Moves"]:
                        aveDamage = 0
                        # Calculates damage 64 times and finds the average
                        for i in range(64):
                            damage, unimportant = self.damageCalc(attack + 1, 2, False)
                            aveDamage += damage
                        aveDamage /= 64
                        # Multihit moves damage calculation
                        if int(self.team2.activePokemon.Moves[attack].hitTimes[1]) > 1:
                            if self.team2.activePokemon.ability.abilityName == "Skill Link":
                                aveDamage *= int(self.team2.activePokemon.Moves[attack].hitTimes[1])
                            else:
                                aveDamage *= (int(self.team2.activePokemon.Moves[attack].hitTimes[0]) + int(self.team2.activePokemon.Moves[attack].hitTimes[1]))/2
                        # Prevents computer from exploding at 1/6 or more HP
                        if (self.team2.activePokemon.currentHp >= int(self.team2.activePokemon.Stats["HP"] * .166) or self.team2.activePokemon.currentHp <= int(self.team2.activePokemon.Stats["HP"] * .333)) and self.team2.activePokemon.Moves[attack].moveName in ["Explosion", "Self-Destruct", "Misty Explosion"]:
                            aveDamage = 0
                        strongestAttack[attack + 1] = ceil(aveDamage/self.team1.activePokemon.Stats["HP"] * 64)
                        # Prioritizes moves that will knock out the opponent,
                        # especially if it has positive priority
                        if aveDamage > self.team1.activePokemon.currentHp:
                            strongestAttack[attack + 1] *= 3 
                            if self.team2.activePokemon.Moves[attack].priority >= 1:
                                strongestAttack[attack + 1] *= 5
                        # Prioritizes switch moves
                        if self.team2.activePokemon.Moves[attack].moveName in ["U-turn", "Volt Switch", "Flip Turn"] and self.team2.alivePokemon > 1:
                            strongestAttack[attack + 1] *= 1.5
                        # Prevents computer from using a charge or recharge move on a substitute
                        elif self.team2.activePokemon.Moves[attack].charge in ["Charge", "Recharge"] and (self.team1.activePokemon.currentHp < .25 * self.team1.activePokemon.Stats["HP"] or self.team1.activePokemon.volatile["Substitute"] > 0 or not self.team2.activePokemon.status == "Healthy"):
                            strongestAttack[attack + 1] = 0
                        # Disincentivizes using a charge or recharge move at half or more HP
                        elif self.team2.activePokemon.Moves[attack].charge in ["Charge", "Recharge"] and self.team2.activePokemon.currentHp > .5 * self.team2.activePokemon.Stats["HP"]:
                            strongestAttack[attack + 1] *= .5
                        # Gives relative value to status moves
                        elif self.team2.activePokemon.Moves[attack].phySpe == "Status":
                            if self.team2.activePokemon.Moves[attack].target == "Opponent" and self.team1.activePokemon.ability.abilityName in ["Good as Gold", "Magic Guard", "Magic Bounce", "Purified Salt"]:
                                strongestAttack[attack + 1] = -1
                            elif self.team2.activePokemon.Moves[attack].healing > 0:
                                strongestAttack[attack + 1] = ceil((self.team2.activePokemon.Stats["HP"] - self.team2.activePokemon.currentHp) / self.team2.activePokemon.Stats["HP"] * 128)
                            elif self.team2.activePokemon.Moves[attack].stat in ["Sleep", "Burn", "Poison", "Badly Poison", "Paralyze"] and self.team1.activePokemon.status == "Healthy" and not (self.team1.activePokemon.Type1.typeName in ["Fire", "Poison", "Electric", "Steel"] or self.team1.activePokemon.Type2.typeName in ["Fire", "Poison", "Electric", "Steel"]) and self.team2.activePokemon.turnOut <= 2:
                                strongestAttack[attack + 1] = (self.team2.activePokemon.Moves[attack].accuracy * self.team2.activePokemon.currentHp / self.team2.activePokemon.Stats["HP"]) / 2
                            elif self.team2.activePokemon.Moves[attack].stat in ["Sleep", "Burn", "Poison", "Badly Poison", "Paralyze"] and not self.team1.activePokemon.status == "Healthy":
                                strongestAttack[attack + 1] = -1
                mostDamage = -2
                # Finds the move with the highest damage
                for powers in strongestAttack:
                    if strongestAttack[powers] >= mostDamage:
                        mostDamage = strongestAttack[powers]
                        mostPowerfulMove = powers
                team2Move = mostPowerfulMove
                switchChance = randint(1, 4)
                # Tries to switch if the best move is weak
                if ((strongestAttack[powers] < 8 and self.team2.alivePokemon > 1 and switchChance == 1 and mostDamage < self.team1.activePokemon.currentHp * .85) or self.team2.activePokemon.volatile["Perish"] == 4 or self.team2.activePokemon.volatile["Drowsy"] == 1) and self.team2.activePokemon.volatile["Trap"] == 0 and self.team2.activePokemon.volatile["Block Condition"] == "None":
                    player2Choice = "switch"
                    player2SwitchList = []
                    currentPokemon = self.team2.activePokemon
                    for pokemonSlot in range(6):
                        leastDamage = 999
                        for pokemonSlot2 in range(6):
                            self.team2.activePokemon = self.team2.pokemonList[pokemonSlot2]
                            if player1Choice == "attack":
                                damage, unimportant = self.damageCalc(team1Move, 1, False)
                            else:
                                damage1, unimportant = self.damageCalc(1, 1, False)
                                damage2, unimportant = self.damageCalc(2, 1, False)
                                damage = max(damage1, damage2)
                            if damage < leastDamage and (pokemonSlot2 + 1) not in player2SwitchList:
                                leastDamage = self.team2.pokemonList[pokemonSlot2].currentHp
                                healthiest = pokemonSlot2 + 1
                        player2SwitchList.append(healthiest)
                    count = 0
                    player2Switch = player2SwitchList[0]
                    self.team2.activePokemon = currentPokemon
                    while self.team2.pokemonList[player2SwitchList[count] - 1] == self.team2.activePokemon or self.team2.pokemonList[player2SwitchList[count] - 1].currentHp <= 0:
                        player2Switch = player2SwitchList[count + 1]
                        count += 1
                    priority2 = 6
                else:
                    player2Choice = "attack"
                    if self.team2.activePokemon.Moves[team2Move - 1].moveType.typeName == self.team2.activePokemon.item.secondEffect and "Z-Move" in self.team2.activePokemon.item.effect and not self.team2.zMove:
                        for zMove in zMoveDict:
                            if zMoveDict[zMove].crystal == self.team2.activePokemon.item.itemName:
                                self.team2.activePokemon.Moves[6] = zMoveDict[zMove]
                                zPowerDict = {140:200, 130:195, 120:190,
                                              110:185, 100:180, 90:170,
                                              80:160, 70:140, 60:120, 1:100}
                                zSpecialDict = {"Mega Drain":120, "Weather Ball":160,
                                                "Hex": 160,"Gear Grind":180,
                                                "V-create":220, "Flying Press":170,
                                                "Core Enforcer":140}
                                if self.team2.activePokemon.Moves[team2Move - 1].moveName not in zSpecialDict:
                                    for zPower in zPowerDict:
                                        if self.team2.activePokemon.Moves[team2Move - 1].power >= zPower:
                                            self.team2.activePokemon.Moves[6].power = zPowerDict[zPower]
                                            self.team2.activePokemon.Moves[6].phySpe = self.team2.activePokemon.Moves[team2Move - 1].phySpe
                                            break
                                else:
                                    self.team2.activePokemon.Moves[6].power = zSpecialDict[self.team2.activePokemon.Moves[team2Move - 1].moveName]
                        team2Move = 7
                    priority2 = self.team2.activePokemon.Moves[team2Move - 1].priority
        elif self.team2.activePokemon.recharge == -1:
            player2Choice = "attack"
            team2Move =  self.team2.activePokemon.chargeMove + 1
            priority2 = 0
        else:
            player2Choice = "attack"
            team2Move = 1
            priority2 = 0
        # Pursuit does double damage to a switching out pokemon
        try:
            if player1Choice == "switch" and self.team2.activePokemon.Moves[team2Move - 1].moveName == "Pursuit":
                priority2 = 7
            if player2Choice == "switch" and self.team1.activePokemon.Moves[team1Move - 1].moveName == "Pursuit":
                priority1 = 7
        except:
            pass
        # Paralyzed pokemon have half speed
        if self.team1.activePokemon.status == "Paralyze":
            pokemon1Para = .5
        else:
            pokemon1Para = 1
        if self.team2.activePokemon.status == "Paralyze":
            pokemon2Para = .5
        else:
            pokemon2Para = 1
        # Boosts priority if the ability boosts it for the chosen move
        if self.team1.activePokemon.ability.effect[0] == "Priority" and player1Choice == "attack":
            if self.team1.activePokemon.Moves[team1Move - 1].phySpe == self.team1.activePokemon.ability.effect[1]:
                priority1 += 1
            elif self.team1.activePokemon.Moves[team1Move - 1].moveType.typeName == self.team1.activePokemon.ability.effect[1]:
                priority1 += 1
            elif self.team1.activePokemon.Moves[team1Move - 1].healing > 0 and self.team1.activePokemon.ability.effect[1] == "Heal":
                priority1 += 3
                
        if self.team2.activePokemon.ability.effect[0] == "Priority" and player2Choice == "attack":
            if self.team2.activePokemon.Moves[team2Move - 1].phySpe == self.team2.activePokemon.ability.effect[1]:
                priority2 += 1
            elif self.team2.activePokemon.Moves[team2Move - 1].moveType.typeName == self.team2.activePokemon.ability.effect[1]:
                priority2 += 1
            elif self.team2.activePokemon.Moves[team2Move - 1].healing > 0 and self.team2.activePokemon.ability.effect[1] == "Heal":
                priority1 += 3
        # Players switch before an attack is used
        if player1Choice == "switch":
            if self.team2.activePokemon.Moves[team2Move - 1].moveName == "Pursuit":
                self.Attack(moveList, moveDict, team2Move, 5, priority2, priority1, False, False, 2, computer)
            stakeout1 = True
            stakeout2 = False
            self.team1.Switch(choiceList[1])
            self.switchIn(self.team1.activePokemon, self.team2.activePokemon)
            self.healthBar()
        if player2Choice == "switch":
            if not player1Choice == "switch":
                if self.team1.activePokemon.Moves[team1Move - 1].moveName == "Pursuit":
                    self.Attack(moveList, moveDict, team1Move, 5, priority1, priority2, False, False, 1, False, computer)
            stakeout1 = False
            stakeout2 = True
            self.team2.Switch(player2Switch)
            self.switchIn(self.team2.activePokemon, self.team1.activePokemon)
            self.healthBar()
        if not player1Choice == "switch" and not player2Choice == "switch":
            stakeout1 = False
            stakeout2 = False
        # Mega evolves active pokemon
        if len(choiceList) > 1:
            if not self.team1.mega and not player1Choice == "switch" and choiceList[-2]:
                self.team1.megaEvolve(megaDict, megaList)
        if not self.team2.mega and not player2Choice == "switch":
            self.team2.megaEvolve(megaDict, megaList)
        weatherSpeed = 1
        terrainSpeed = 1
        abilitySpeed = 1
        # Boosts speed for weather
        if not self.weather[0] == "None" and not self.cloudNine:
            if self.weather[0] == self.team1.activePokemon.ability.effect[1] and self.team1.activePokemon.ability.effect[0] == "Speed":
                weatherSpeed *= self.team1.activePokemon.ability.success
            elif self.weather[0] == self.team1.activePokemon.ability.effect[1] and self.team1.activePokemon.boosterEnergy[2] and self.team1.activePokemon.boosterEnergy[1] == "Speed":
                weatherSpeed *= self.team1.activePokemon.boosterEnergy[0]
            if self.weather[0] == self.team2.activePokemon.ability.effect[1] and self.team2.activePokemon.ability.effect[0] == "Speed":
                weatherSpeed /= self.team2.activePokemon.ability.success
            elif self.weather[0] == self.team2.activePokemon.ability.effect[1] and self.team2.activePokemon.boosterEnergy[2] and self.team2.activePokemon.boosterEnergy[1] == "Speed":
                weatherSpeed /= self.team1.activePokemon.boosterEnergy[0]
        # Boosts speed for terrain        
        if not self.terrain[0] == "None":
            if self.terrain[0] == self.team1.activePokemon.ability.effect[1] and self.team1.activePokemon.ability.effect[0] == "Speed":
                terrainSpeed *= self.team1.activePokemon.ability.success
            elif self.terrain[0] == self.team1.activePokemon.ability.effect[1] and self.team1.activePokemon.boosterEnergy[2] and self.team1.activePokemon.boosterEnergy[1] == "Speed":
                terrainSpeed *= self.team1.activePokemon.boosterEnergy[0]
            if self.terrain[0] == self.team2.activePokemon.ability.effect[1] and self.team2.activePokemon.ability.effect[0] == "Speed":
                terrainSpeed /= self.team2.activePokemon.ability.success
            elif self.terrain[0] == self.team2.activePokemon.ability.effect[1] and self.team2.activePokemon.boosterEnergy[2] and self.team2.activePokemon.boosterEnergy[1] == "Speed":
                terrainSpeed /= self.team1.activePokemon.boosterEnergy[0]
        # Lowers speed for Slow Start
        if self.team1.activePokemon.ability.abilityName == "Slow Start" and self.team1.activePokemon.turnOut < 6:
            abilitySpeed /= 2
        if self.team2.activePokemon.ability.abilityName == "Slow Start" and self.team2.activePokemon.turnOut < 6:
            abilitySpeed *= 2
        # Raises speed for Quick Feet
        if self.team1.activePokemon.ability.abilityName == "Quick Feet" and not self.team1.activePokemon.status == "Healthy":
            abilitySpeed *= 3/2
        if self.team2.activePokemon.ability.abilityName == "Quick Feet" and not self.team2.activePokemon.status == "Healthy":
            abilitySpeed *= 2/3
        # Team 1 is faster and attacks first        
        if self.team1.activePokemon.Stats["Speed"] * self.team1.activePokemon.statModifier["Speed"] * pokemon1Para * weatherSpeed * terrainSpeed * abilitySpeed * scarfSpeed> self.team2.activePokemon.Stats["Speed"] * self.team2.activePokemon.statModifier["Speed"] * pokemon2Para and priority1 >= priority2:
            if player1Choice == "attack" and not (player2Choice == "switch" and self.team1.activePokemon.Moves[team1Move - 1].moveName == "Pursuit"):
                self.Attack(moveList, moveDict, team1Move, team2Move, priority1, priority2, False, stakeout1, 1, False, computer)
            if player2Choice == "attack" and alive1 == self.team1.alivePokemon and alive2 == self.team2.alivePokemon:
                if player1Choice == "attack":
                    self.Attack(moveList, moveDict, team2Move, team1Move, priority2, priority1, True, stakeout2, 2, computer)
                else:
                    self.Attack(moveList, moveDict, team2Move, 5, priority2, priority1, True, stakeout2, 2, computer)
        # Team 2 is faster and attacks first
        elif self.team1.activePokemon.Stats["Speed"] * self.team1.activePokemon.statModifier["Speed"] * pokemon1Para * weatherSpeed * terrainSpeed * abilitySpeed * scarfSpeed < self.team2.activePokemon.Stats["Speed"] * self.team2.activePokemon.statModifier["Speed"] * pokemon2Para and priority1 <= priority2:
            if player2Choice == "attack" and not (player1Choice == "switch" and self.team2.activePokemon.Moves[team2Move - 1].moveName == "Pursuit"):
                self.Attack(moveList, moveDict, team2Move, team1Move, priority2, priority1, False, stakeout2, 2, computer)
            if player1Choice == "attack" and alive1 == self.team1.alivePokemon and alive2 == self.team2.alivePokemon:
                self.Attack(moveList, moveDict, team1Move, team2Move, priority1, priority2, True, stakeout1, 1, False, computer)
        else:
            if priority1 > priority2:
                speedTie = 1
            elif priority1 < priority2:
                speedTie = 0
            else:
                speedTie = randint(0, 1)
            if speedTie == 0:
                # Player 2 wins the speed tie and attacks first
                if player2Choice == "attack" and not (player1Choice == "switch" and self.team2.activePokemon.Moves[team2Move - 1].moveName == "Pursuit"):
                    self.Attack(moveList, moveDict, team2Move, team1Move, priority2, priority1, False, stakeout2, 2, computer)
                if player1Choice == "attack" and alive1 == self.team1.alivePokemon and alive2 == self.team2.alivePokemon:
                    self.Attack(moveList, moveDict, team1Move, team2Move, priority1, priority2, True, stakeout1, 1, False, computer)
            else:
                # Player 1 wins the speed tie and attack first
                if player1Choice == "attack" and not (player2Choice == "switch" and self.team1.activePokemon.Moves[team1Move - 1].moveName == "Pursuit"):
                    self.Attack(moveList, moveDict, team1Move, team2Move, priority1, priority2, False, stakeout1, 1, False, computer)
                if player2Choice == "attack" and alive1 == self.team1.alivePokemon and alive2 == self.team2.alivePokemon:
                    self.Attack(moveList, moveDict, team2Move, 5, priority2, priority1, True, stakeout2, 2, computer)
        # Uses Z Move
        if len(choiceList) > 3:
            if team1Move == 7:
                if alive1 == self.team1.alivePokemon and not (priority1 < priority2 and self.team1.activePokemon.Stats["Speed"] * self.team1.activePokemon.statModifier["Speed"] * pokemon1Para * weatherSpeed * terrainSpeed * abilitySpeed * scarfSpeed < self.team2.activePokemon.Stats["Speed"] * self.team2.activePokemon.statModifier["Speed"] * pokemon2Para):  
                    self.team1.zMove = True
                elif not alive1 == self.team1.alivePokemon and (priority1 > priority2 or (priority1 == priority2 and self.team1.activePokemon.Stats["Speed"] * self.team1.activePokemon.statModifier["Speed"] * pokemon1Para * weatherSpeed * terrainSpeed * abilitySpeed * scarfSpeed > self.team2.activePokemon.Stats["Speed"] * self.team2.activePokemon.statModifier["Speed"] * pokemon2Para)):
                    self.team1.zMove = True
        # Stops being protected at the end of the turn
        if player1Choice == "attack" and self.team1.activePokemon.intangibility:
            if self.team1.activePokemon.Moves[team1Move - 1].moveName in ["Protect", "Detect"]:
                self.team1.activePokemon.intangibility = False
        if player2Choice == "attack" and self.team2.activePokemon.intangibility:
            if self.team2.activePokemon.Moves[team2Move - 1].moveName in ["Protect", "Detect"]:
                self.team2.activePokemon.intangibility = False
        # Team 1 uses item at the end of turn
        if self.team1.activePokemon.item.effect[0] in ["Heal", "Boost"] and not self.team1.activePokemon.item.consumed and not ("Berry" in self.team1.activePokemon.item.itemName and (self.team2.activePokemon.ability.abilityName == "Unnerve" or "As One" in self.team2.activePokemon.ability.abilityName)):
            # Boosts stat using a berry
            if self.team1.activePokemon.item.multiplier == 1.5:
                if self.team1.activePokemon.currentHp < .25 * self.team1.activePokemon.Stats["HP"]:
                    self.team1.activePokemon.modifyStat(self.team1.activePokemon.item.secondEffect, "1", True)
                    if self.team1.activePokemon.item.consumable:
                        self.team1.activePokemon.item.Consume()
                        # Cheek Pouch heals after eating a berry
                        if self.team1.activePokemon.ability.abilityName == "Cheek Pouch":
                            self.team1.activePokemon.currentHp += ceil(self.team1.activePokemon.Stats["HP"] * (1/3))
                            if self.team1.activePokemon.currentHp > self.team1.activePokemon.Stats["HP"]:
                                self.team1.activePokemon.currentHp = self.team1.activePokemon.Stats["HP"]
                    self.drawCurrentText(self.team1.activePokemon.pokemonName + " boosted its " + self.team1.activePokemon.item.secondEffect + " with its berry!")
            # Heals using Oran Berry or Berry Juice
            elif self.team1.activePokemon.item.multiplier > 1:
                if self.team1.activePokemon.currentHp < .5 * self.team1.activePokemon.Stats["HP"]:
                    self.team1.activePokemon.currentHp += int(self.team1.activePokemon.item.multiplier)
                    if self.team1.activePokemon.item.consumable:
                        self.team1.activePokemon.item.Consume()
                        if self.team1.activePokemon.ability.abilityName == "Cheek Pouch":
                            self.team1.activePokemon.currentHp += ceil(self.team1.activePokemon.Stats["HP"] * (1/3))
                            if self.team1.activePokemon.currentHp > self.team1.activePokemon.Stats["HP"]:
                                self.team1.activePokemon.currentHp = self.team1.activePokemon.Stats["HP"]
                    self.drawCurrentText(self.team1.activePokemon.pokemonName + " restored health with its " + self.team1.activePokemon.item.itemName + "!")
            # Heals using pinch berries
            elif self.team1.activePokemon.item.multiplier > .25:
                if self.team1.activePokemon.currentHp < .25 * self.team1.activePokemon.Stats["HP"] or (self.team1.activePokemon.currentHp < .5 * self.team1.activePokemon.Stats["HP"] and self.team1.activePokemon.ability.abilityName == "Gluttony"):
                    self.team1.activePokemon.currentHp += floor(self.team1.activePokemon.item.multiplier * self.team1.activePokemon.Stats["HP"])
                    if self.team1.activePokemon.item.consumable:
                        self.team1.activePokemon.item.Consume()
                        if self.team1.activePokemon.ability.abilityName == "Cheek Pouch":
                            self.team1.activePokemon.currentHp += ceil(self.team1.activePokemon.Stats["HP"] * (1/3))
                            if self.team1.activePokemon.currentHp > self.team1.activePokemon.Stats["HP"]:
                                self.team1.activePokemon.currentHp = self.team1.activePokemon.Stats["HP"]
                    self.drawCurrentText(self.team1.activePokemon.pokemonName + " restored health with its " + self.team1.activePokemon.item.itemName + "!")
                    # Confuses if nature dislikes berry
                    if self.team1.activePokemon.item.secondEffect == self.team1.activePokemon.minusNature:
                        self.team1.activePokemon.changeStatus("Confuse")
            else:
                # Heals using Sitrus Berry
                if self.team1.activePokemon.currentHp < .5 * self.team1.activePokemon.Stats["HP"] or not self.team1.activePokemon.item.consumable:
                    self.team1.activePokemon.currentHp += floor(self.team1.activePokemon.item.multiplier * self.team1.activePokemon.Stats["HP"])
                    if self.team1.activePokemon.item.consumable:
                        self.team1.activePokemon.item.Consume()
                        if self.team1.activePokemon.ability.abilityName == "Cheek Pouch":
                            self.team1.activePokemon.currentHp += ceil(self.team1.activePokemon.Stats["HP"] * (1/3))
                            if self.team1.activePokemon.currentHp > self.team1.activePokemon.Stats["HP"]:
                                self.team1.activePokemon.currentHp = self.team1.activePokemon.Stats["HP"]
                    self.drawCurrentText(self.team1.activePokemon.pokemonName + " restored health with its " + self.team1.activePokemon.item.itemName + "!")
            if self.team1.activePokemon.currentHp > self.team1.activePokemon.Stats["HP"]:
                self.team1.activePokemon.currentHp = self.team1.activePokemon.Stats["HP"]
        # Team 2 uses item at the end of turn
        if self.team2.activePokemon.item.effect[0] in ["Heal", "Boost"] and not self.team2.activePokemon.item.consumed and not ("Berry" in self.team2.activePokemon.item.itemName and (self.team1.activePokemon.ability.abilityName == "Unnerve" or "As One" in self.team1.activePokemon.ability.abilityName)):
            if self.team2.activePokemon.item.multiplier == 1.5:
                if self.team2.activePokemon.currentHp < .25 * self.team2.activePokemon.Stats["HP"]:
                    self.team2.activePokemon.modifyStat(self.team2.activePokemon.item.secondEffect, "1", True)
                    if self.team2.activePokemon.item.consumable:
                        self.team2.activePokemon.item.Consume()
                        if self.team2.activePokemon.ability.abilityName == "Cheek Pouch":
                            self.team2.activePokemon.currentHp += ceil(self.team2.activePokemon.Stats["HP"] * (1/3))
                            if self.team2.activePokemon.currentHp > self.team2.activePokemon.Stats["HP"]:
                                self.team2.activePokemon.currentHp = self.team2.activePokemon.Stats["HP"]
                    self.drawCurrentText(self.team2.activePokemon.pokemonName + " boosted its " + self.team2.activePokemon.item.secondEffect + " with its berry!")
            elif self.team2.activePokemon.item.multiplier > 1:
                if self.team2.activePokemon.currentHp < .5 * self.team2.activePokemon.Stats["HP"]:
                    self.team2.activePokemon.currentHp += int(self.team2.activePokemon.item.multiplier)
                    if self.team2.activePokemon.item.consumable:
                        self.team2.activePokemon.item.Consume()
                        if self.team2.activePokemon.ability.abilityName == "Cheek Pouch":
                            self.team2.activePokemon.currentHp += ceil(self.team2.activePokemon.Stats["HP"] * (1/3))
                            if self.team2.activePokemon.currentHp > self.team2.activePokemon.Stats["HP"]:
                                self.team2.activePokemon.currentHp = self.team2.activePokemon.Stats["HP"]
                    self.drawCurrentText(self.team2.activePokemon.pokemonName + " restored health with its " + self.team2.activePokemon.item.itemName + "!")
            elif self.team2.activePokemon.item.multiplier > .25:
                if self.team2.activePokemon.currentHp < .25 * self.team2.activePokemon.Stats["HP"] or (self.team1.activePokemon.currentHp < .5 * self.team1.activePokemon.Stats["HP"] and self.team1.activePokemon.ability.abilityName == "Gluttony"):
                    self.team2.activePokemon.currentHp += floor(self.team2.activePokemon.item.multiplier * self.team2.activePokemon.Stats["HP"])
                    if self.team2.activePokemon.item.consumable:
                        self.team2.activePokemon.item.Consume()
                        if self.team1.activePokemon.ability.abilityName == "Cheek Pouch":
                            self.team1.activePokemon.currentHp += ceil(self.team1.activePokemon.Stats["HP"] * (1/3))
                            if self.team1.activePokemon.currentHp > self.team1.activePokemon.Stats["HP"]:
                                self.team1.activePokemon.currentHp = self.team1.activePokemon.Stats["HP"]
                    self.drawCurrentText(self.team2.activePokemon.pokemonName + " restored health with its " + self.team2.activePokemon.item.itemName + "!")
                    if self.team2.activePokemon.item.secondEffect == self.team2.activePokemon.minusNature:
                        self.team2.activePokemon.changeStatus("Confuse")
            else:
                if self.team2.activePokemon.currentHp < .5 * self.team2.activePokemon.Stats["HP"] or not self.team2.activePokemon.item.consumable:
                    self.team2.activePokemon.currentHp += floor(self.team2.activePokemon.item.multiplier * self.team2.activePokemon.Stats["HP"])
                    if self.team2.activePokemon.item.consumable:
                        self.team2.activePokemon.item.Consume()
                        if self.team2.activePokemon.ability.abilityName == "Cheek Pouch":
                            self.team2.activePokemon.currentHp += ceil(self.team1.activePokemon.Stats["HP"] * (1/3))
                            if self.team2.activePokemon.currentHp > self.team2.activePokemon.Stats["HP"]:
                                self.team2.activePokemon.currentHp = self.team2.activePokemon.Stats["HP"]
                    self.drawCurrentText(self.team2.activePokemon.pokemonName + " restored health with its " + self.team2.activePokemon.item.itemName + "!")
            if self.team2.activePokemon.currentHp > self.team2.activePokemon.Stats["HP"]:
                self.team2.activePokemon.currentHp = self.team2.activePokemon.Stats["HP"]
        if not self.team1.activePokemon.status == "Healthy":
            # Sked Skin has a chance to heal status conditions
            if self.team1.activePokemon.ability.abilityName == "Shed Skin":
                shedSkin = randint(1,3)
                if shedSkin == 2:
                    self.team1.activePokemon.changeStatus("Healthy")
            # Hydration heals status conditions in the rain
            elif self.team1.activePokemon.ability.abilityName == "Hydration" and self.weather[0] == "Rain Dance" and self.weather[1] > 1:
                self.team1.activePokemon.changeStatus("Healthy")
        # Takes poison damage    
        if self.team1.activePokemon.status == "Poison":
            if self.team1.activePokemon.volatile["Badly Poison"] > 0:
                self.team1.activePokemon.currentHp -= ceil(self.team1.activePokemon.Stats["HP"] * (1/16) *
                                           self.team1.activePokemon.volatile["Badly Poison"])
                self.team1.activePokemon.volatile["Badly Poison"] += 1
            else:
                self.team1.activePokemon.currentHp -= ceil(self.team1.activePokemon.Stats["HP"] * (1/8))
            self.drawCurrentText(self.team1.activePokemon.pokemonName + " was hurt by poison!")
        # Takes burn damage
        elif self.team1.activePokemon.status == "Burn":
            self.team1.activePokemon.currentHp -= ceil(self.team1.activePokemon.Stats["HP"] * (1/16))
            self.drawCurrentText(self.team1.activePokemon.pokemonName + " was hurt by its burn!")
        # Takes Bad Dreams damage if sleeping
        elif self.team1.activePokemon.status in ["Sleep", "Rest"] and self.team2.activePokemon.ability.abilityName == "Bad Dreams":
            self.team1.activePokemon.currentHp -= ceil(self.team1.activePokemon.Stats["HP"] * (1/8))
            self.drawCurrentText(self.team1.activePokemon.pokemonName + " was hurt by a bad dream!")
        # Takes trap damage
        if self.team1.activePokemon.volatile["Trap"] != 0:
            self.team1.activePokemon.currentHp -= floor(self.team1.activePokemon.Stats["HP"] * (1/8))
            self.team1.activePokemon.volatile["Trap"] -= 1
            self.drawCurrentText(self.team1.activePokemon.pokemonName + " was hurt by the opponent's trap!")
        # Ingrain heals
        if self.team1.activePokemon.volatile["Block Condition"] == "Ingrain":
            self.team1.activePokemon.currentHp += int(self.team1.activePokemon.Stats["HP"] / 16)
            self.drawCurrentText(self.team1.activePokemon.pokemonName + " healed from its roots!")
            if self.team1.activePokemon.currentHp > self.team1.activePokemon.Stats["HP"]:
                self.team1.activePokemon.currentHp = self.team1.activePokemon.Stats["HP"]
        # Octolock lowers stats
        elif self.team1.activePokemon.volatile["Block Condition"] == "Octolock":
            if not self.team1.activePokemon.ability.effect[0] == "Clear Body":
                self.team1.activePokemon.modifyStat("Defense/Special Defense", "-1/-1", False)
            elif self.team1.activePokemon.ability.effect[1] == "Defense":
                self.team1.activePokemon.modifyStat("Special Defense", "-1", False)
            elif self.team1.activePokemon.ability.effect[1] == "All":
                pass
            else:
                self.team1.activePokemon.modifyStat("Defense/Special Defense", "-1/-1", False)
        # Perish count decreases
        if self.team1.activePokemon.volatile["Perish"] != 0:
            self.team1.activePokemon.volatile["Perish"] += 1
            self.drawCurrentText(self.team1.activePokemon.pokemonName + " perish count is " + str(5 - self.team1.activePokemon.volatile["Perish"]) + "!")
            if self.team1.activePokemon.volatile["Perish"] == 5:
                self.team1.activePokemon.currentHp = 0
        # Drowsy count decreases
        if self.team1.activePokemon.volatile["Drowsy"] != 0:
            self.team1.activePokemon.volatilw["Drowsy"] -= 1
            if self.team1.activePokemon.volatile["Drowsy"] == 0:
                self.team1.activePokemon.changeStatus("Sleep")
        if not self.team2.activePokemon.status == "Healthy":
            if self.team2.activePokemon.ability.abilityName == "Shed Skin":
                shedSkin = randint(1,3)
                if shedSkin == 2:
                    self.team2.activePokemon.changeStatus("Healthy")
            elif self.team2.activePokemon.ability.abilityName == "Hydration" and self.weather[0] == "Rain Dance" and self.weather[1] > 1:
                self.team2.activePokemon.changeStatus("Healthy")
        if self.team2.activePokemon.status == "Poison":
            if self.team2.activePokemon.volatile["Badly Poison"] > 0:
                self.team2.activePokemon.currentHp -= ceil(self.team2.activePokemon.Stats["HP"] * (1/16) *
                                           self.team2.activePokemon.volatile["Badly Poison"])
                self.team2.activePokemon.volatile["Badly Poison"] += 1
            else:
                self.team2.activePokemon.currentHp -= ceil(self.team2.activePokemon.Stats["HP"] * (1/8))
            self.drawCurrentText(self.team2.activePokemon.pokemonName + " was hurt by poison!")
        elif self.team2.activePokemon.status == "Burn":
            self.team2.activePokemon.currentHp -= ceil(self.team2.activePokemon.Stats["HP"] * (1/16))
            self.drawCurrentText(self.team2.activePokemon.pokemonName + " was hurt by its burn!")
        elif self.team2.activePokemon.status in ["Sleep", "Rest"] and self.team1.activePokemon.ability.abilityName == "Bad Dreams":
            self.team2.activePokemon.currentHp -= ceil(self.team2.activePokemon.Stats["HP"] * (1/8))
            self.drawCurrentText(self.team2.activePokemon.pokemonName + " was hurt by a bad dream!")
        if self.team2.activePokemon.volatile["Trap"] != 0:
            self.team2.activePokemon.currentHp -= floor(self.team2.activePokemon.Stats["HP"] * (1/8))
            self.team2.activePokemon.volatile["Trap"] -= 1
            self.drawCurrentText(self.team2.activePokemon.pokemonName + " was hurt by the opponent's trap!")
        if self.team2.activePokemon.volatile["Block Condition"] == "Ingrain":
            self.team2.activePokemon.currentHp += int(self.team2.activePokemon.Stats["HP"] / 16)
            self.drawCurrentText(self.team2.activePokemon.pokemonName + " healed from its roots!")
            if self.team2.activePokemon.currentHp > self.team2.activePokemon.Stats["HP"]:
                self.team2.activePokemon.currentHp = self.team2.activePokemon.Stats["HP"]
        elif self.team2.activePokemon.volatile["Block Condition"] == "Octolock":
            if not self.team2.activePokemon.ability.effect[0] == "Clear Body":
                self.team2.activePokemon.modifyStat("Defense/Special Defense", "-1/-1", False)
            elif self.team2.activePokemon.ability.effect[1] == "Defense":
                self.team2.activePokemon.modifyStat("Special Defense", "-1", False)
            elif self.team2.activePokemon.ability.effect[1] == "All":
                pass
            else:
                self.team2.activePokemon.modifyStat("Defense/Special Defense", "-1/-1", False)
        if self.team2.activePokemon.volatile["Perish"] != 0:
            self.team2.activePokemon.volatile["Perish"] += 1
            self.drawCurrentText(self.team2.activePokemon.pokemonName + " perish count is " + str(5 - self.team2.activePokemon.volatile["Perish"]) + "!")
            if self.team2.activePokemon.volatile["Perish"] == 5:
                self.team2.activePokemon.currentHp = 0
        if self.team1.activePokemon.volatile["Drowsy"] != 0:
            self.team1.activePokemon.volatilw["Drowsy"] -= 1
            if self.team1.activePokemon.volatile["Drowsy"] == 0:
                self.team1.activePokemon.changeStatus("Sleep")
        # Harvest tries to recover an eaten berry
        if self.team1.activePokemon.ability.abilityName == "Harvest" and "Berry" in self.team1.activePokemon.item.itemName and self.team1.activePokemon.item.consumed:
            if self.weather[0] == "Sunny Day" and not self.cloudNine:
                harvested = 1
            else:
                harvested = randint(0, 1)
            
            if harvested == 1:
                self.drawCurrentText(self.team1.activePokemon.pokemonName + "'s berry was harvested!")
                self.team1.activePokemon.item.consumed = False
        # Honey Gather tries to pickup Honey
        elif self.team1.activePokemon.ability.abilityName == "Honey Gather" and self.team1.activePokemon.item.consumed:
            self.team1.activePokemon.newItem(copy.deepcopy(itemDict["Honey"]))
            self.drawCurrentText(self.team1.activePokemon.pokemonName + " gathered some honey!")
        if self.team2.activePokemon.ability.abilityName == "Harvest" and "Berry" in self.team2.activePokemon.item.itemName and self.team2.activePokemon.item.consumed:
            if self.weather[0] == "Sunny Day" and not self.cloudNine:
                harvested = 1
            else:
                harvested = randint(0, 1)
            
            if harvested == 1:
                self.drawCurrentText(self.team2.activePokemon.pokemonName + "'s berry was harvested!")
                self.team2.activePokemon.item.consumed = False
        elif self.team2.activePokemon.ability.abilityName == "Honey Gather" and self.team2.activePokemon.item.consumed:
            self.team2.activePokemon.newItem(copy.deepcopy(itemDict["Honey"]))
            self.drawCurrentText(self.team2.activePokemon.pokemonName + " gathered some honey!")
        # Weahther takes effect
        if self.weather[0] != "Clear":
            self.weather[1] -= 1
            if self.weather[1] > 0 and not self.cloudNine:
                # Hail hurts non-ice pokemon
                if self.weather[0] == "Hail" and not (self.team1.activePokemon.Type1.typeName == "Ice" or self.team1.activePokemon.Type2.typeName == "Ice" or self.team1.activePokemon.ability.abilityName in ["Ice Body", "Snow Cloak", "Magic Guard", "Overcoat"] or self.team1.activePokemon.item.itemName == "Safety Goggles"):
                    self.team1.activePokemon.currentHp -= int(self.team1.activePokemon.Stats["HP"] / 16)
                    self.drawCurrentText(self.team1.activePokemon.pokemonName + " was buffeted by Hail!")
                elif self.weather[0] == "Hail" and self.team1.activePokemon.ability.abilityName == "Ice Body":
                    self.team1.activePokemon.currentHp += int(self.team1.activePokemon.Stats["HP"] / 16)
                    self.drawCurrentText(self.team1.activePokemon.pokemonName + " icy body was healed by the hail!")
                # Hail heals Ice Body pokemon
                if self.weather[0] == "Hail" and not (self.team1.activePokemon.Type2.typeName == "Ice" or self.team2.activePokemon.Type2.typeName == "Ice" or self.team2.activePokemon.ability.abilityName in ["Ice Body", "Snow Cloak", "Magic Guard", "Overcoat"] or self.team2.activePokemon.item.itemName == "Safety Goggles"):
                    self.team2.activePokemon.currentHp -= int(self.team2.activePokemon.Stats["HP"] / 16)
                    self.drawCurrentText(self.team2.activePokemon.pokemonName + " was buffeted by Hail!")
                elif self.weather[0] == "Hail" and self.team2.activePokemon.ability.abilityName == "Ice Body":
                    self.team2.activePokemon.currentHp += int(self.team2.activePokemon.Stats["HP"] / 16)
                    self.drawCurrentText(self.team2.activePokemon.pokemonName + " icy body was healed by the hail!")
                # Sandstorm hurts non-rock, non-steel, and non-ground pokemon
                if self.weather[0] == "Sandstorm" and not (self.team1.activePokemon.Type1.typeName in ["Rock", "Steel", "Ground"] or self.team1.activePokemon.Type2.typeName in ["Rock", "Steel", "Ground"] or self.team1.activePokemon.ability.abilityName in ["Sand Force", "Sand Rush", "Sand Veil", "Magic Guard", "Overcoat"] or self.team1.activePokemon.item.itemName == "Safety Goggles"):
                    self.team1.activePokemon.currentHp -= int(self.team1.activePokemon.Stats["HP"] / 16)
                    self.drawCurrentText(self.team1.activePokemon.pokemonName + " was buffeted by Sandstorm!")
                if self.weather[0] == "Sandstorm" and not (self.team2.activePokemon.Type2.typeName in ["Rock", "Steel", "Ground"] or self.team2.activePokemon.Type2.typeName in ["Rock", "Steel", "Ground"] or self.team2.activePokemon.ability.abilityName in ["Sand Force", "Sand Rush", "Sand Veil", "Magic Guard", "Overcoat"] or self.team2.activePokemon.item.itemName == "Safety Goggles"):
                    self.team2.activePokemon.currentHp -= int(self.team2.activePokemon.Stats["HP"] / 16)
                    self.drawCurrentText(self.team2.activePokemon.pokemonName + " was buffeted by Sandstorm!")
                # Sun hurts Solar Power pokemon
                if self.weather[0] == "Sunny Day" and self.team1.activePokemon.ability.abilityName in ["Solar Power"]:
                    self.team1.activePokemon.currentHp -= int(self.team1.activePokemon.Stats["HP"] / 8)
                    self.drawCurrentText(self.team1.activePokemon.pokemonName + " was hurt by the sun!")
                if self.weather[0] == "Sunny Day" and self.team2.activePokemon.ability.abilityName in ["Solar Power"]:
                    self.team2.activePokemon.currentHp -= int(self.team2.activePokemon.Stats["HP"] / 8)
                    self.drawCurrentText(self.team2.activePokemon.pokemonName + " was hurt by the sun!")
                # Booster Energy boosts
                if not self.team1.activePokemon.item.itemName == "Booster Energy":
                    self.team1.activePokemon.energyBoost(self.weather[0], self.terrain[0])
                if not self.team2.activePokemon.item.itemName == "Booster Energy":
                    self.team2.activePokemon.energyBoost(self.weather[0], self.terrain[0])
            else:
                self.weather[0] = "Clear"
                self.drawCurrentText("The weather cleared up!")
        # Terrain takes effect
        if self.terrain[0] != "Clear":
            self.terrain[1] -= 1
            if self.terrain[1] == 0:
                self.terrain[0] = "Clear"
                self.drawCurrentText("The terrain vanished!")
                if self.team1.activePokemon.ability.abilityName == "Mimicry":
                    self.team1.activePokemon.changeType(self.team1.activePokemon.tempType1, self.team1.activePokemon.tempType2, True)
                if self.team2.activePokemon.ability.abilityName == "Mimicry":
                    self.team2.activePokemon.changeType(self.team2.activePokemon.tempType1, self.team2.activePokemon.tempType2, True)
            if not self.team1.activePokemon.item.itemName == "Booster Energy":
                self.team1.activePokemon.energyBoost(self.weather[0], self.terrain[0])
            if not self.team2.activePokemon.item.itemName == "Booster Energy":
                self.team2.activePokemon.energyBoost(self.weather[0], self.terrain[0])
        # Grassy Terrain heals grounded pokemon
        if self.terrain[0] == "Grassy Terrain":
            if self.team1.activePokemon.Type1.typeName == "Flying" or self.team1.activePokemon.Type2.typeName == "Flying" or self.team1.activePokemon.ability.abilityName == "Levitate":
                pass
            else:
                self.team1.activePokemon.currentHp += int(self.team1.activePokemon.Stats["HP"] / 16)
                self.drawCurrentText(self.team1.activePokemon.pokemonName + " healed from the Grassy Terrain!")
                if self.team1.activePokemon.currentHp > self.team1.activePokemon.Stats["HP"]:
                    self.team1.activePokemon.currentHp = self.team1.activePokemon.Stats["HP"]
            if self.team2.activePokemon.Type1.typeName == "Flying" or self.team2.activePokemon.Type2.typeName == "Flying" or self.team2.activePokemon.ability.abilityName == "Levitate":
                pass
            else:
                self.team2.activePokemon.currentHp += int(self.team2.activePokemon.Stats["HP"] / 16)
                self.drawCurrentText(self.team2.activePokemon.pokemonName + " healed from the Grassy Terrain!")
                if self.team2.activePokemon.currentHp > self.team2.activePokemon.Stats["HP"]:
                    self.team2.activePokemon.currentHp = self.team2.activePokemon.Stats["HP"]
        # Team 1 switches a fainted pokemon
        if self.team1.activePokemon.currentHp <= 0:
            if self.team1.alivePokemon > 0:
                self.team1.activePokemon.currentHp = 0
                self.drawCurrentText(self.team1.activePokemon.pokemonName + " fainted!")
                self.team1.alivePokemon -= 1
                if self.team1.alivePokemon > 0:
                    while self.team1.activePokemon.currentHp <= 0:
                        position = int(self.team1.switchMenu())
                        self.team1.Switch(position)
                    self.switchIn(self.team1.activePokemon, self.team2.activePokemon)
        # Team 2 switches a fainted pokemon
        if self.team2.activePokemon.currentHp <= 0:
            if self.team2.alivePokemon > 0:
                self.team2.activePokemon.currentHp = 0
                self.drawCurrentText(self.team2.activePokemon.pokemonName + " fainted!") 
                self.team2.alivePokemon -= 1
                if self.team2.alivePokemon > 0:
                    while self.team2.activePokemon.currentHp <= 0:
                         if not computer:
                             position = int(self.team2.switchMenu())
                         else:
                            player2SwitchList = []
                            currentPokemon = self.team2.activePokemon
                            for pokemonSlot in range(6):
                                leastDamage = 999
                                for pokemonSlot2 in range(6):
                                    self.team2.activePokemon = self.team2.pokemonList[pokemonSlot2]
                                    damage1, unimportant = self.damageCalc(1, 1, False)
                                    damage2, unimportant = self.damageCalc(1, 1, False)
                                    damage3, unimportant = self.damageCalc(team1Move, 1, False)
                                    damage = max(damage1, damage2, damage3)
                                    if damage < leastDamage and (pokemonSlot2 + 1) not in player2SwitchList:
                                        leastDamage = self.team2.pokemonList[pokemonSlot2].currentHp
                                        healthiest = pokemonSlot2 + 1
                                player2SwitchList.append(healthiest)
                            count = 0
                            player2Switch = player2SwitchList[0]
                            self.team2.activePokemon = currentPokemon
                            while self.team2.pokemonList[player2SwitchList[count] - 1] == self.team2.activePokemon or self.team2.pokemonList[player2SwitchList[count] - 1].currentHp <= 0:
                                player2Switch = player2SwitchList[count + 1]
                                count += 1
                         self.team2.Switch(player2Switch)
                    self.switchIn(self.team2.activePokemon, self.team1.activePokemon)
        # Speed Boost raises speed by 1
        if self.team1.activePokemon.ability.abilityName == "Speed Boost":
            self.team1.activePokemon.modifyStat("Speed", "1", True)
        if self.team2.activePokemon.ability.abilityName == "Speed Boost":
            self.team2.activePokemon.modifyStat("Speed", "1", True)
        # Moody raises a random stat by 2 and lowers another by 1
        if self.team1.activePokemon.ability.abilityName == "Moody":
            stat1 = choice(["Attack", "Defense", "Special Attack", "Special Defense", "Speed"])
            stat2 = choice(["Attack", "Defense", "Special Attack", "Special Defense", "Speed"])
            while stat1 == stat2:
                stat1 = choice(["Attack", "Defense", "Special Attack", "Special Defense", "Speed"])
                stat2 = choice(["Attack", "Defense", "Special Attack", "Special Defense", "Speed"])
            self.team1.activePokemon.modifyStat(stat1, "2", True)
            self.team1.activePokemon.modifyStat(stat2, "-1", True)
        if self.team2.activePokemon.ability.abilityName == "Moody":
            stat1 = choice(["Attack", "Defense", "Special Attack", "Special Defense", "Speed"])
            stat2 = choice(["Attack", "Defense", "Special Attack", "Special Defense", "Speed"])
            while stat1 == stat2:
                stat1 = choice(["Attack", "Defense", "Special Attack", "Special Defense", "Speed"])
                stat2 = choice(["Attack", "Defense", "Special Attack", "Special Defense", "Speed"])
            self.team2.activePokemon.modifyStat(stat1, "2", True)
            self.team2.activePokemon.modifyStat(stat2, "-1", True)
        # Hunger Switch changes Aura Wheel from dark to electric every turn
        if self.team1.activePokemon.ability.abilityName == "Hunger Switch":
            self.team1.activePokemon.changeForm(self.weather[0], True)
        if self.team2.activePokemon.ability.abilityName == "Hunger Switch":
            self.team2.activePokemon.changeForm(self.weather[0], True)
        # Screens wear off after 5 or 8 turns depending on if Light Clay was the held item         
        if self.team1.reflect > 0:
            self.team1.reflect -= 1
            if self.team1.reflect == 0:
                self.drawCurrentText("Your Reflect wore off!")
        if self.team2.reflect > 0:
            self.team2.reflect -= 1
            if self.team2.reflect == 0:
                self.drawCurrentText("The opponent's Reflect wore off!")
        if self.team1.lightScreen > 0:
            self.team1.lightScreen -= 1
            if self.team1.lightScreen == 0:
                self.drawCurrentText("Your Light Screen wore off!")
        if self.team2.lightScreen > 0:
            self.team2.lightScreen -= 1
            if self.team2.lightScreen == 0:
                self.drawCurrentText("The opponent's Light Screen wore off!")
        # Protect stops making the user intangible
        if self.team1.activePokemon.volatile["Intangible"] == "Protect":
            self.team1.activePokemon.volatile["Intangible"] == " "
            self.team1.activePokemon.intangibility = False
        if self.team2.activePokemon.volatile["Intangible"] == "Protect":
            self.team2.activePokemon.volatile["Intangible"] == " "
            self.team2.activePokemon.intangibility = False
        # Roosted pokemon become airborn again
        if self.team1.activePokemon.roosted:
            self.team1.activePokemon.changeType(self.team1.activePokemon.tempType1.typeName, self.team1.activePokemon.tempType2.typeName, False)
            self.team1.activePokemon.roosted = False
        if self.team2.activePokemon.roosted:
            self.team2.activePokemon.changeType(self.team2.activePokemon.tempType1.typeName, self.team2.activePokemon.tempType2.typeName, False)
            self.team2.activePokemon.roosted = False
        # Slow Start pokemon have attack and speed returned to normal
        if self.team1.activePokemon.ability.abilityName == "Slow Start" and self.team1.activePokemon.turnOut == 5:
            self.drawCurrentText(self.team1.activePokemon.pokemonName + " got its act together!")
        if self.team2.activePokemon.ability.abilityName == "Slow Start" and self.team2.activePokemon.turnOut == 5:
            self.drawCurrentText(self.team2.activePokemon.pokemonName + " got its act together!")
        # If no Cloud Nine, changes weather form
        if not self.cloudNine:
            self.team1.activePokemon.changeForm(self.weather[0], True)
            self.team2.activePokemon.changeForm(self.weather[0], True)
        self.healthBar()
    
    # Z Moves are imported to by used by pokemon    
    def importZMoves(self, zMoveDict, zMoveSignatureDict, zMoveCrystalList):
        self.zMoveDict = zMoveDict
        self.zMoveSignatureDict = zMoveSignatureDict
        self.zMoveCrystalList = zMoveCrystalList

# Selects pokemon to use in battle
def selectPokemon(sheet, number, chosen = []):
    pokemonList = []
    pokemonName = []
    
    infile = pd.read_excel('Pokemon Simulator Stats.xlsx', sheet)
    for strName in infile["Name"]:
        pokemonName.append(strName)
    
    # Gurantees the chosen pokemon will be used in the battle
    for pokemon in chosen:
        pokemonList.append(pokemon)
        number -= 1
    
    for pokemon in range(number):
        pokemonList.insert(0, choice(pokemonName))
        
    return pokemonList

# Imports pokemon from the Excel spreadsheet Pokemon Simulator Stats        
def Pokedex(pokemonList, megaDict, abilityDict, abilitySpecialtyDict, abilityList, sheet):
    infile = pd.read_excel('Pokemon Simulator Stats.xlsx', sheet)
    
    pokedexDict = {}
    pokemonName = []
    pokemonPosition = []
    pokemonType1 = []
    pokemonType2 = []
    pokemonAbilityI = []
    pokemonAbilityII = []
    pokemonAbilityH = []
    pokemonMove = []
    pokemonHp = []
    pokemonAt = []
    pokemonDe = []
    pokemonSa = []
    pokemonSd = []
    pokemonSp = []
    pokemonGender = []
    pokemonEvolve = []
    pokemonMass = []
    pokemonCrunch = []
    
    counter = 0
    # All of the information is put into lists temporarily
    for strName in infile["Name"]:
        if strName in pokemonList or sheet == "Fakemon":
            pokemonName.append(strName)
            pokemonPosition.append(counter)
        counter += 1
    
    counter = 0
    for strType1 in infile["Type 1"]:
        if counter in pokemonPosition:
            pokemonType1.append(strType1)
        counter += 1
    
    counter = 0
    for strType2 in infile["Type 2"]:
        if counter in pokemonPosition:    
            if str(strType2) == "nan":
                strType2 = "None"
            pokemonType2.append(strType2)
        counter += 1
    
    counter = 0
    for strAbility in infile["Ability I"]:
        if counter in pokemonPosition:
            if str(strAbility) == "nan":
                strAbility = "None"
            pokemonAbilityI.append(strAbility)
        counter += 1
    
    counter = 0
    for strAbility in infile["Ability II"]:
        if counter in pokemonPosition:
            if str(strAbility) == "nan":
                strAbility = "None"
            pokemonAbilityII.append(strAbility)
        counter += 1
    
    counter = 0
    for strAbility in infile["Hidden Ability"]:
        if counter in pokemonPosition:
            if str(strAbility) == "nan":
                strAbility = "None"
            pokemonAbilityH.append(strAbility)
        counter += 1
    
    counter = 0
    for strMove in infile["Guaranteed Move"]:
        if counter in pokemonPosition:
            pokemonMove.append(strMove)
        counter += 1
    
    counter = 0
    for intHP in infile["HP"]:
        if counter in pokemonPosition:
            pokemonHp.append(int(intHP))
        counter += 1
    
    counter = 0
    for intAt in infile["Attack"]:
        if counter in pokemonPosition:
            pokemonAt.append(int(intAt))
        counter += 1
    
    counter = 0
    for intDe in infile["Defense"]:
        if counter in pokemonPosition:
            pokemonDe.append(int(intDe))
        counter += 1
        
    counter = 0
    for intSa in infile["Special Attack"]:
        if counter in pokemonPosition:
            pokemonSa.append(int(intSa))
        counter += 1
    
    counter = 0
    for intSd in infile["Special Defense"]:
        if counter in pokemonPosition:
            pokemonSd.append(int(intSd))
        counter += 1
    
    counter = 0
    for intSp in infile["Speed"]:
        if counter in pokemonPosition:
            pokemonSp.append(int(intSp))
        counter += 1
        
    counter = 0
    for gender in infile["Gender"]:
        if counter in pokemonPosition:
            genderRatio = str(gender).split("/")
            genderList = []
            if len(genderRatio) == 1:
                genderList.append("None")
            else:
                for i in range(int(genderRatio[0])):
                    genderList.append("Male")
                for i in range(int(genderRatio[1])):
                    genderList.append("Female")
            pokemonGender.append(genderList)
        counter += 1
    
    counter = 0
    for evolve in infile["Evolve"]:
        if counter in pokemonPosition:
            pokemonEvolve.append(evolve)
        counter += 1
    
    counter = 0
    for massList in infile["Mass"]:
        if counter in pokemonPosition:
            currentMass = massList.split(" ")
            if currentMass[0] == "???":
                currentMass.append(False)
            else:
                currentMass[0] = float(currentMass[0])
                currentMass.append(True)
            pokemonMass.append(currentMass)
        counter += 1
    
    counter = 0
    if sheet == "Fakemon":
        if counter in pokemonPosition:
            for strCrunch in infile["Crunch Name"]:
                pokemonCrunch.append(strCrunch)
        counter += 1
    # Creates the pokemon objects
    for pokemonNum in range(len(pokemonName)):
        specialty = False
        # Checks if the pokemon has a special ability
        for pokemonAbility in abilitySpecialtyDict:
            if abilitySpecialtyDict[pokemonAbility].effect[1] in pokemonName[pokemonNum]:
                pokemonObj = Pokemon(pokemonName[pokemonNum], abilitySpecialtyDict[pokemonAbility],
                             pokemonEvolve[pokemonNum], pokemonMass[pokemonNum],
                             pokemonType1[pokemonNum], pokemonType2[pokemonNum], 
                             pokemonGender[pokemonNum])
                specialty = True
        if not specialty:
            # Checks if pokemon has any abilities in the current abilityList
            possibleAbilities = []
            if pokemonAbilityI[pokemonNum] in abilityList:
                possibleAbilities.append(pokemonAbilityI[pokemonNum])
            if pokemonAbilityII[pokemonNum] in abilityList:
                possibleAbilities.append(pokemonAbilityII[pokemonNum])
            if pokemonAbilityH[pokemonNum] in abilityList:
                possibleAbilities.append(pokemonAbilityH[pokemonNum])
            if len(possibleAbilities) == 0:
                pokemonObj = Pokemon(pokemonName[pokemonNum], abilityDict[choice(abilityList)], 
                                 pokemonEvolve[pokemonNum], pokemonMass[pokemonNum],
                                 pokemonType1[pokemonNum], pokemonType2[pokemonNum], 
                                 pokemonGender[pokemonNum])
            else:
                pokemonObj = Pokemon(pokemonName[pokemonNum], abilityDict[choice(possibleAbilities)], 
                             pokemonEvolve[pokemonNum], pokemonMass[pokemonNum],
                             pokemonType1[pokemonNum], pokemonType2[pokemonNum], 
                             pokemonGender[pokemonNum])
        # Sets the base stats of a pokemon
        pokemonObj.setBaseStat("HP", pokemonHp[pokemonNum])
        if pokemonName[pokemonNum] in megaDict:
            megaDict[pokemonName[pokemonNum]][0].setBaseStat("HP", pokemonHp[pokemonNum])
        pokemonObj.setBaseStat("Attack", pokemonAt[pokemonNum])
        pokemonObj.setBaseStat("Defense", pokemonDe[pokemonNum])
        pokemonObj.setBaseStat("Special Attack", pokemonSa[pokemonNum])
        pokemonObj.setBaseStat("Special Defense", pokemonSd[pokemonNum])
        pokemonObj.setBaseStat("Speed", pokemonSp[pokemonNum])   
        # Gives the pokemon a guaranteed move
        pokemonObj.guaranteedMove = pokemonMove[pokemonNum]
        if len(pokemonCrunch) > 0:
            pokemonObj.crunchName = pokemonCrunch[pokemonNum]
        pokedexDict[pokemonName[pokemonNum]] = pokemonObj
    
    if sheet == "Fakemon":
        return pokedexDict, pokemonName
    else:
        return pokedexDict, megaDict

# Imports moves from the Excel spreadsheet Pokemon Simulator Stats
def MoveList():
    infile = pd.read_excel('Pokemon Simulator Stats.xlsx', 'Moves')
    
    moveDict = {}
    moveAttacking = {}
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
    moveContact = []
    movePunching = []
    moveSlicing = []
    moveZEffect = []
    moveZTarget = []
    moveZStages = []
    
    for strName in infile["Move"]:
        moveName.append(strName)
        
    for strType in infile["Type"]:
        if str(strType) == "nan":
            strType = "None"
        moveType.append(strType)
        if strType not in moveAttacking:
            moveAttacking[strType] = []
    
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
        if str(strStat) == "nan":
            strStat = "None"
        moveStat.append(strStat)
    
    for strTarget in infile["Target"]:
        if str(strTarget) == "nan":
            strTarget = "None"
        moveTarget.append(strTarget)
        
    for strStages in infile["Stages"]:
        moveStages.append(str(strStages))
        
    for strHits in infile["Hit Times"]:
        moveHitTimes.append(str(strHits))
    
    for intPriority in infile["Priority"]:
        movePriority.append(int(intPriority))
        
    for strCharge in infile["Charge"]:
        if str(strCharge) == "nan":
            strCharge = "None"
        moveCharge.append(strCharge)
        
    for strCrit in infile["Crit"]:
        moveCrit.append(strCrit)
        
    for boolSound in infile["Sound"]:
        moveSound.append(bool(boolSound))
        
    for boolFeint in infile["Feint"]:
        moveFeint.append(bool(boolFeint))
        
    for boolContact in infile["Contact"]:
        moveContact.append(bool(boolContact))
    
    for boolPunching in infile["Punching"]:
        movePunching.append(bool(boolPunching))    
    
    for boolSlicing in infile["Slicing"]:
        moveSlicing.append(bool(boolSlicing))
        
    for strEffect in infile["Z Effect"]:
        if str(strEffect) == "nan":
            strEffect = "None"
        moveZEffect.append(strEffect)
        
    for strTarget in infile["Z Target"]:
        if str(strTarget) == "nan":
            strTarget = "None"
        moveZTarget.append(strTarget)
        
    for strStages in infile["Z Stages"]:
        if str(strStages) == "nan":
            strStages = "None"
        moveZStages.append(str(strStages))
    
    struggleRemoved = False
    
    for move in range(len(moveName)):
        # Checks if Struggle has been created
        if struggleRemoved:
            moveDict[moveName[move - 1]] = Move(moveName[move - 1], moveType[move - 1], 
                    movePower[move - 1], moveAccuracy[move - 1], movePP[move - 1], 
                    movePhySpe[move - 1], moveHealing[move - 1], moveChance[move - 1], 
                    moveStat[move - 1], moveTarget[move - 1], moveStages[move - 1], 
                    moveHitTimes[move - 1], movePriority[move - 1], 
                    moveCharge[move - 1], moveCrit[move - 1], moveSound[move - 1], 
                    moveFeint[move - 1], moveContact[move - 1], movePunching[move - 1],
                    moveSlicing[move - 1], moveZEffect[move - 1],moveZTarget[move - 1], 
                    moveZStages[move - 1])
            if movePower[move - 1] >= 1:
                moveAttacking[moveType[move - 1]].append(moveName[move - 1])
        # Struggle is not a regular move, so it is seperated to prevent adding to a movepool
        elif moveName[move] == "Struggle":
            struggle = Move(moveName[move], moveType[move], movePower[move],
                moveAccuracy[move], movePP[move], movePhySpe[move], 
                moveHealing[move], moveChance[move], moveStat[move], 
                moveTarget[move], moveStages[move], moveHitTimes[move], 
                movePriority[move], moveCharge[move], moveCrit[move], 
                moveSound[move], moveFeint[move], moveContact[move],
                movePunching[move], moveSlicing[move], moveZEffect[move], 
                moveZTarget[move], moveZStages[move])
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
            moveContact.pop(move)
            movePunching.pop(move)
            moveSlicing.pop(move)
            struggleRemoved = True
        else:
            moveDict[moveName[move]] = Move(moveName[move], moveType[move], 
                    movePower[move], moveAccuracy[move], movePP[move], 
                    movePhySpe[move], moveHealing[move], moveChance[move], 
                    moveStat[move], moveTarget[move], moveStages[move], 
                    moveHitTimes[move], movePriority[move], moveCharge[move], 
                    moveCrit[move], moveSound[move], moveFeint[move], moveContact[move],
                    movePunching[move], moveSlicing[move], moveZEffect[move], 
                    moveZTarget[move], moveZStages[move])
            if movePower[move] >= 1:
                moveAttacking[moveType[move]].append(moveName[move])
    
    # Clears up space after not needing lists
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
    moveContact = []
    movePunching = []
    moveSlicing = []
    moveZEffect = []
    moveZTarget = []
    moveZStages = []
    return moveDict, moveName, moveAttacking, struggle

# Imports items from the Excel spreadsheet Pokemon Simulator Stats
def ItemList():
    infile = pd.read_excel('Pokemon Simulator Stats.xlsx', 'Items')
    
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
        
    for listEffect in infile["Effect"]:
        if str(listEffect) == "nan":
            listEffect = "None"
        itemEffect.append(str(listEffect).split("/"))
        
    for strSecondEffect in infile["Second Effect"]:
        if str(strSecondEffect) == "nan":
            strSecondEffect = "None"
        itemsecondEffect.append(str(strSecondEffect))
    
    for floatMultiplier in infile["Multiplier"]:
        itemMultiplier.append(round(floatMultiplier, 4))
        
    for boolConsume in infile["Consumable"]:
        itemConsumable.append(bool(boolConsume))
        
    for strSpecialty in infile["Signature"]:
        if str(strSpecialty) == "nan":
            strSpecialty = "None"
        itemSpecialty.append(strSpecialty)
        
    for intFling in infile["Fling"]:
        itemFling.append(int(intFling))
    
    for item in range(len(itemName)):
        # Specialty items are put into a seperate dictionary
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

# Imports mega pokemon from the Excel spreadsheet Pokemon Simulator Stats
def Megas(abilityDict):
    infile = pd.read_excel('Pokemon Simulator Stats.xlsx', 'Mega Pokemon')
    
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
    pokemonAbility = []
    pokemonMass = []
    
    for strName in infile["Pokemon"]:
        pokemonName.append(strName)
        
    for strLabel in infile["Label"]:
        if str(strLabel) == "nan":
            pokemonLabel.append("")
        else:
            pokemonLabel.append(" " + str(strLabel))
            
    for strItem in infile["Item"]:
        pokemonItem.append(strItem)
    
    for strType1 in infile["Type 1"]:
        pokemonType1.append(strType1)
        
    for strType2 in infile["Type 2"]:
        if str(strType2) == "nan":
            strType2 = "None"
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
        
    for strAbility in infile["Ability"]:
        pokemonAbility.append(strAbility)
        
    for massList in infile["Mass"]:
        currentMass = massList.split(" ")
        currentMass[0] = float(currentMass[0])
        currentMass.append(True)
        pokemonMass.append(currentMass)
    
    for pokemonNum in range(len(pokemonName)):
        pokemonObj = Pokemon("Mega " + pokemonName[pokemonNum] + pokemonLabel[pokemonNum], 
                             abilityDict[pokemonAbility[pokemonNum]], "No", 
                             pokemonMass[pokemonNum], pokemonType1[pokemonNum], 
                             pokemonType2[pokemonNum])
        pokemonObj.setBaseStat("Attack", pokemonAt[pokemonNum])
        pokemonObj.setBaseStat("Defense", pokemonDe[pokemonNum])
        pokemonObj.setBaseStat("Special Attack", pokemonSa[pokemonNum])
        pokemonObj.setBaseStat("Special Defense", pokemonSd[pokemonNum])
        pokemonObj.setBaseStat("Speed", pokemonSp[pokemonNum])
        pokedexDict[pokemonName[pokemonNum] + pokemonLabel[pokemonNum]] = [pokemonObj, pokemonItem[pokemonNum]]
        
    return pokedexDict, pokemonName

# Imports abilities from the Excel spreadsheet Pokemon Simulator Stats
def Abilities():
    infile = pd.read_excel('Pokemon Simulator Stats.xlsx', 'Abilities')
    
    abilitySpecialtyDict = {}
    specialtyNumbers = []
    abilityDict = {}
    abilityName = []
    target = []
    effect1 = []
    effect2 = []
    effect3 = []
    success = []
    
    for strName in infile["Name"]:
        abilityName.append(strName)
        
    for strTarget in infile["Target"]:
        target.append(strTarget)
        
    for strEffect in infile["Effect 1"]:
        if str(strEffect) == "nan":
            strEffect = "None"
        effect1.append(strEffect)
        
    for strEffect in infile["Effect 2"]:
        if str(strEffect) == "nan":
            strEffect = "None"
        effect2.append(strEffect)
        
    for strEffect in infile["Effect 3"]:
        if str(strEffect) == "nan":
            strEffect = "None"
        effect3.append(strEffect)
        
    for floatSuccess in infile["Success"]:
        success.append(floatSuccess)
        
    for abilityNum in range(len(abilityName)):
        if effect1[abilityNum] == "Specialty":
            abilitySpecialtyDict[abilityName[abilityNum]] = Ability(abilityName[abilityNum], 
                   target[abilityNum], effect1[abilityNum], effect2[abilityNum],
                   effect3[abilityNum], success[abilityNum])
            specialtyNumbers.append(abilityNum)
        else:
            abilityDict[abilityName[abilityNum]] = Ability(abilityName[abilityNum],
                   target[abilityNum], effect1[abilityNum], effect2[abilityNum],
                   effect3[abilityNum], success[abilityNum])
    
    specialtyCounter = 0        
    for specialtyAbilityNum in specialtyNumbers:
        abilityName.pop(specialtyAbilityNum - specialtyCounter)
        specialtyCounter += 1

    return abilityDict, abilitySpecialtyDict, abilityName

# Imports Z moves from the Excel spreadsheet Pokemon Simulator Stats
def ZMoveList():
    infile = pd.read_excel('Pokemon Simulator Stats.xlsx', 'Z Moves')
    
    moveDict = {}
    signatureDict = {}
    moveName = []
    moveType = []
    movePower = []
    movePhySpe = [] 
    moveStat = [] 
    moveTarget = []
    moveStages = []
    moveCrit = [] 
    moveContact = []
    moveSound = []
    moveCrystal = []
    moveUniqueCrystal = []
    moveMethod = []
    moveBase = []
    movePokemon = []
    
    for strName in infile["Name"]:
        moveName.append(strName)
        
    for strType in infile["Type"]:
        moveType.append(strType)
    
    for intPower in infile["Power"]:
        movePower.append(int(intPower))
        
    for strPhySpec in infile["Physical"]:
        movePhySpe.append(strPhySpec)
        
    for strStat in infile["Secondary"]:
        if str(strStat) == "nan":
            strStat = "None"
        moveStat.append(strStat)
    
    for strTarget in infile["Target"]:
        moveTarget.append(str(strTarget))
        
    for strStages in infile["Stages"]:
        moveStages.append(str(strStages))
        
    for strCrit in infile["Crit"]:
        moveCrit.append(strCrit)
        
    for boolContact in infile["Contact"]:
        moveContact.append(bool(boolContact))
        
    for boolSound in infile["Sound"]:
        moveSound.append(bool(boolSound))
        
    for strBase in infile["Base Move"]:
        moveBase.append(strBase)
    
    for strCrystal in infile["Crystal"]:
        moveCrystal.append(strCrystal)
        if not strCrystal in moveUniqueCrystal:
            moveUniqueCrystal.append(strCrystal)
        
    for strMethod in infile["Method"]:
        moveMethod.append(strMethod)
        
    for strSignature in infile["Signature"]:
        if str(strSignature) == "nan":
            strSignature = "None"
        movePokemon.append(strSignature)
        
    for zMove in range(len(moveName)):    
        newZMove = ZMove(moveName[zMove], moveType[zMove], movePower[zMove], movePhySpe[zMove], 
                         moveStat[zMove], moveTarget[zMove], moveStages[zMove], moveCrit[zMove], 
                         moveContact[zMove], moveSound[zMove], moveBase[zMove], moveCrystal[zMove], 
                         moveMethod[zMove], movePokemon[zMove])
        if not newZMove.signature == "None":
            signatureDict[moveCrystal[zMove]] = [newZMove, newZMove.signature]
            
        moveDict[moveName[zMove]] = newZMove
        
    return moveDict, signatureDict, moveUniqueCrystal

# Simulates the game against a computer
def battleSimulator():
    battleWindow = GraphWin("Battle Simulator", 500, 400)
    battleWindow.setCoords(0, 0, 500, 400)
    # Imports the data from the Excel sheet and stores
    abilityDict, abilitySpecialtyDict, abilityList = Abilities()
    megaDict, megaList = Megas(abilityDict)
    megaUsed = [choice(megaList), choice(megaList)]
    pokemonName = selectPokemon("Pokemon", 10, megaUsed)
    pokemonDict, megaDict = Pokedex(pokemonName, megaDict, abilityDict, abilitySpecialtyDict, abilityList, 'Pokemon')
    fakemonDict, fakemonList = Pokedex(pokemonName, megaDict, abilityDict, abilitySpecialtyDict, abilityList, 'Fakemon')
    moveDict, moveList, moveAttacking, struggle = MoveList()
    itemDict, itemSpecialtyDict, itemNormalName, itemSpecialtyName = ItemList()
    megaDict, megaList = Megas(abilityDict)
    zMoveDict, zMoveSignatureDict, zMoveCrystalList = ZMoveList()
    
    simTeam = Team()
    simTeam2 = Team()
    # Generates 12 pokemon
    for newPokemon in range(12):
        move2 = False
        # Pokemon created by suggestions of people Brian knows
        if newPokemon in [10, 11]:
            pokemon1 = copy.deepcopy(fakemonDict[choice(fakemonList)]) 
            # Pokemon that cannot evolve get a penalty
            if pokemon1.evolve:
                evolveDebuff = 0
            else:
                evolveDebuff = 5
            pokemon1Total = pokemon1.BaseStats["HP"] + pokemon1.BaseStats["Attack"] + pokemon1.BaseStats["Defense"] + pokemon1.BaseStats["Special Attack"] + pokemon1.BaseStats["Special Defense"] + pokemon1.BaseStats["Speed"]
            pokemon1.Gender()
            # First two moves are the same type as the pokemon, if applicable
            pokemon1.newMove(copy.deepcopy(moveDict[choice(moveAttacking[pokemon1.Type1.typeName])]))
            if not pokemon1.Type2.typeName == "None":
                pokemon1.newMove(copy.deepcopy(moveDict[choice(moveAttacking[pokemon1.Type2.typeName])]))
            else:
                while not move2:
                    move2Choice = copy.deepcopy(moveDict[choice(moveList)])
                    if not move2Choice.moveType.typeName == pokemon1.Type1.typeName:
                        move2 = True
                pokemon1.newMove(move2Choice)
            # Third move is guaranteed if in the move list
            if pokemon1.guaranteedMove in moveList and not pokemon1.guaranteedMove == pokemon1.Moves[0].moveName and not pokemon1.guaranteedMove == pokemon1.Moves[1].moveName:  
                pokemon1.newMove(copy.deepcopy(moveDict[pokemon1.guaranteedMove]))
            else:
                moveName = choice(moveList)
                while moveName == pokemon1.Moves[0].moveName or moveName == pokemon1.Moves[1].moveName:
                    moveName = choice(moveList)
                pokemon1.newMove(copy.deepcopy(moveDict[moveName]))
            # Last move is random
            moveName = choice(moveList)
            while moveName == pokemon1.Moves[0].moveName or moveName == pokemon1.Moves[1].moveName or moveName == pokemon1.Moves[2].moveName:
                moveName = choice(moveList)
            pokemon1.newMove(copy.deepcopy(moveDict[moveName]))
            # Pokemon with signature items are given one
            if pokemon1.pokemonName in itemSpecialtyDict:
                signatureItem = choice(itemSpecialtyName)
                while signatureItem not in itemSpecialtyDict[pokemon1.pokemonName]:
                    signatureItem = choice(itemSpecialtyName)
                pokemon1.newItem(copy.deepcopy(itemSpecialtyDict[pokemon1.pokemonName][signatureItem]))
            else:
                pokemon1.newItem(copy.deepcopy(itemDict[choice(itemNormalName)]))
            pokemon1.replaceMove(struggle, 5)
            # Base stats and natures are decided randomly
            pokemon1.setStats((100 - ceil(pokemon1Total/20)), choice(["Attack", "Defense", "Special Attack", 
                                         "Special Defense", "Speed"]), 
                    choice(["Attack", "Defense", "Special Attack", "Special Defense", 
                           "Speed"]), [randint(0,31), randint(0,31), randint(0,31),
                                  randint(0,31), randint(0,31), randint(0,31)], 
                           [randint(0, 252), randint(0, 252), randint(0, 252), randint(0, 252),
                            randint(0, 252), randint(0, 252)])
        # Pokemon will hold a Z Crystal
        elif newPokemon in [6, 7]:
            pokemon1 = copy.deepcopy(pokemonDict[pokemonName[newPokemon]])
            if pokemon1.evolve:
                evolveDebuff = 0
            else:
                evolveDebuff = 5
            pokemon1Total = pokemon1.BaseStats["HP"] + pokemon1.BaseStats["Attack"] + pokemon1.BaseStats["Defense"] + pokemon1.BaseStats["Special Attack"] + pokemon1.BaseStats["Special Defense"] + pokemon1.BaseStats["Speed"]
            pokemon1.Gender()
            pokemon1.newMove(copy.deepcopy(moveDict[choice(moveAttacking[pokemon1.Type1.typeName])]))
            #move1Choice = copy.deepcopy(moveDict["Splash"])
            #pokemon1.newMove(move1Choice)
            if not pokemon1.Type2.typeName == "None":
                pokemon1.newMove(copy.deepcopy(moveDict[choice(moveAttacking[pokemon1.Type2.typeName])]))
            else:
                while not move2:
                    move2Choice = copy.deepcopy(moveDict[choice(moveList)])
                    if not move2Choice.moveType.typeName == pokemon1.Type1.typeName:
                        move2 = True
                pokemon1.newMove(move2Choice)
            if pokemon1.guaranteedMove in moveList and not pokemon1.guaranteedMove == pokemon1.Moves[0].moveName and not pokemon1.guaranteedMove == pokemon1.Moves[1].moveName:  
                pokemon1.newMove(copy.deepcopy(moveDict[pokemon1.guaranteedMove]))
            else:
                moveName = choice(moveList)
                while moveName == pokemon1.Moves[0].moveName or moveName == pokemon1.Moves[1].moveName:
                    moveName = choice(moveList)
                pokemon1.newMove(copy.deepcopy(moveDict[moveName]))
            moveName = choice(moveList)
            while moveName == pokemon1.Moves[0].moveName or moveName == pokemon1.Moves[1].moveName or moveName == pokemon1.Moves[2].moveName:
                moveName = choice(moveList)
            pokemon1.newMove(copy.deepcopy(moveDict[moveName]))
            if pokemon1.pokemonName in itemSpecialtyDict:
                signatureItem = choice(itemSpecialtyName)
                while signatureItem not in itemSpecialtyDict[pokemon1.pokemonName]:
                    signatureItem = choice(itemSpecialtyName)
                pokemon1.newItem(copy.deepcopy(itemSpecialtyDict[pokemon1.pokemonName][signatureItem]))
            else:
                legalItem = False
                while not legalItem:
                    legalItem = True
                    item = choice(zMoveCrystalList)
                    for zMove in zMoveSignatureDict:
                        if item == zMoveSignatureDict[zMove][0].crystal:
                            legalItem = False
                    if legalItem:
                        legalItem = False
                        for move in pokemon1.Moves:
                            if move == None:
                                break
                            elif move.moveType.typeName == itemDict[item].secondEffect:
                                legalItem = True
                pokemon1.newItem(copy.deepcopy(itemDict[item]))
            pokemon1.replaceMove(struggle, 5)
            pokemon1.setStats((110 - evolveDebuff - ceil(pokemon1Total/20)), choice(["Attack", "Defense", "Special Attack", 
                                         "Special Defense", "Speed"]), 
                    choice(["Attack", "Defense", "Special Attack", "Special Defense", 
                           "Speed"]), [randint(0,31), randint(0,31), randint(0,31),
                                  randint(0,31), randint(0,31), randint(0,31)], 
                           [randint(0, 252), randint(0, 252), randint(0, 252), randint(0, 252),
                            randint(0, 252), randint(0, 252)])
        # The non special pokemon
        else:
            #pokemon1 = copy.deepcopy(pokemonDict["Dracovish"])
            pokemon1 = copy.deepcopy(pokemonDict[pokemonName[newPokemon]])
            if pokemon1.evolve:
                evolveDebuff = 0
            else:
                evolveDebuff = 5
            pokemon1Total = pokemon1.BaseStats["HP"] + pokemon1.BaseStats["Attack"] + pokemon1.BaseStats["Defense"] + pokemon1.BaseStats["Special Attack"] + pokemon1.BaseStats["Special Defense"] + pokemon1.BaseStats["Speed"]
            pokemon1.Gender()
            
            pokemon1.newMove(copy.deepcopy(moveDict[choice(moveAttacking[pokemon1.Type1.typeName])]))
            if not pokemon1.Type2.typeName == "None":
                pokemon1.newMove(copy.deepcopy(moveDict[choice(moveAttacking[pokemon1.Type2.typeName])]))
            else:
                while not move2:
                    move2Choice = copy.deepcopy(moveDict[choice(moveList)])
                    if not move2Choice.moveType.typeName == pokemon1.Type1.typeName:
                        move2 = True
                pokemon1.newMove(move2Choice)
            if pokemon1.guaranteedMove in moveList and not pokemon1.guaranteedMove == pokemon1.Moves[0].moveName and not pokemon1.guaranteedMove == pokemon1.Moves[1].moveName:  
                pokemon1.newMove(copy.deepcopy(moveDict[pokemon1.guaranteedMove]))
            else:
                moveName = choice(moveList)
                while moveName == pokemon1.Moves[0].moveName or moveName == pokemon1.Moves[1].moveName:
                    moveName = choice(moveList)
                pokemon1.newMove(copy.deepcopy(moveDict[moveName]))
            moveName = choice(moveList)
            while moveName == pokemon1.Moves[0].moveName or moveName == pokemon1.Moves[1].moveName or moveName == pokemon1.Moves[2].moveName:
                moveName = choice(moveList)
            pokemon1.newMove(copy.deepcopy(moveDict[moveName]))
            #move1Choice = copy.deepcopy(moveDict["Twister"])
            #pokemon1.newMove(move1Choice)
            #move1Choice = copy.deepcopy(moveDict["Nuzzle"])
            #pokemon1.newMove(move1Choice)
            if pokemon1.pokemonName in itemSpecialtyDict:
                signatureItem = choice(itemSpecialtyName)
                while signatureItem not in itemSpecialtyDict[pokemon1.pokemonName]:
                    signatureItem = choice(itemSpecialtyName)
                pokemon1.newItem(copy.deepcopy(itemSpecialtyDict[pokemon1.pokemonName][signatureItem]))
            else:
                #pokemon1.newItem(copy.deepcopy(itemDict["Darkinium Z"]))
                pokemon1.newItem(copy.deepcopy(itemDict[choice(itemNormalName)]))
            pokemon1.replaceMove(struggle, 5)
            pokemon1.setStats((110 - evolveDebuff - ceil(pokemon1Total/20)), choice(["Attack", "Defense", "Special Attack", 
                                         "Special Defense", "Speed"]), 
                    choice(["Attack", "Defense", "Special Attack", "Special Defense", 
                           "Speed"]), [randint(0,31), randint(0,31), randint(0,31),
                                  randint(0,31), randint(0,31), randint(0,31)], 
                           [randint(0, 252), randint(0, 252), randint(0, 252), randint(0, 252),
                            randint(0, 252), randint(0, 252)]) 
        # Adds pokemon to either team 1 or team 2
        if newPokemon%2 == 0:
            simTeam.addPokemon(pokemon1)
        else:
            simTeam2.addPokemon(pokemon1)
    # Creates a battle
    testBattle = Battle(simTeam, simTeam2, battleWindow)
    testBattle.typeMatchup()
    testBattle.importZMoves(zMoveDict, zMoveSignatureDict, zMoveCrystalList)
    testBattle.fixType()
    # Checks if a winner has been found
    while simTeam.alivePokemon > 0 and simTeam2.alivePokemon > 0:
        testBattle.Turn(moveList, moveDict, megaDict, megaList, zMoveDict, itemDict, True)
        if simTeam.alivePokemon == 0:
            testBattle.drawCurrentText("Team 2 wins!")
        elif simTeam2.alivePokemon == 0:
            testBattle.drawCurrentText("Team 1 wins!")
    # Closes window
    testBattle.win.close()

battleSimulator()
