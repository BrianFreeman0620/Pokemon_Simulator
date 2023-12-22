from graphics import Point, Rectangle, Text
from math import floor
import copy

from Helper_Pokemon import Clicked

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