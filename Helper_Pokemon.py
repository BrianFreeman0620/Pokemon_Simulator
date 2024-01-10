from random import choice
from math import sqrt
from graphics import Circle, color_rgb, Line, Oval, Point, Polygon, Rectangle
import pandas as pd

from Ability_Pokemon import Ability
from Item_Pokemon import Item
from Move_Pokemon import Move, ZMove
from Class_Pokemon import Pokemon

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

# Creates a picture using the pokemon's types and shiny value                
def pokemonPicture(teamNumber, type1, type2, shiny):
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

# Imports pokemon from the Excel spreadsheet Pokemon Simulator Stats        
def Pokedex(pokemonList, megaDict, abilityDict, abilitySpecialtyDict, abilityList, sheet):
    infile = pd.read_excel('Pokemon Simulator Stats.xlsx', sheet)
    
    pokedexDict = {}
    pokemonDict = {}
    pokemonName = []
    pokemonPosition = []
    
    counter = 0
    # All of the information is put into lists temporarily
    # PokemonDict position 0 for name
    for strName in infile["Name"]:
        if strName in pokemonList or sheet == "Fakemon":
            pokemonName.append(strName)
            pokemonPosition.append(counter)
            pokemonDict[counter] = [strName]
        counter += 1
    
    # PokemonDict position 1 for Type 1
    counter = 0
    for strType1 in infile["Type 1"]:
        if counter in pokemonPosition:
            pokemonDict[counter].append(strType1)
        counter += 1
    
    # PokemonDict position 2 for Type 2
    counter = 0
    for strType2 in infile["Type 2"]:
        if counter in pokemonPosition:    
            if str(strType2) == "nan":
                strType2 = "None"
            pokemonDict[counter].append(strType2)
        counter += 1
    
    # PokemonDict position 3 for Ability 1
    counter = 0
    for strAbility in infile["Ability I"]:
        if counter in pokemonPosition:
            if str(strAbility) == "nan":
                strAbility = "None"
            pokemonDict[counter].append(strAbility)
        counter += 1
    
    # PokemonDict position 4 for Ability 2
    counter = 0
    for strAbility in infile["Ability II"]:
        if counter in pokemonPosition:
            if str(strAbility) == "nan":
                strAbility = "None"
            pokemonDict[counter].append(strAbility)
        counter += 1
    
    # PokemonDict position 5 for Hidden Ability
    counter = 0
    for strAbility in infile["Hidden Ability"]:
        if counter in pokemonPosition:
            if str(strAbility) == "nan":
                strAbility = "None"
            pokemonDict[counter].append(strAbility)
        counter += 1
    
    # PokemonDict position 6 for Guaranteed Move
    counter = 0
    for strMove in infile["Guaranteed Move"]:
        if counter in pokemonPosition:
            pokemonDict[counter].append(strMove)
        counter += 1
    
    # PokemonDict position 7 for HP
    counter = 0
    for intHP in infile["HP"]:
        if counter in pokemonPosition:
            pokemonDict[counter].append(int(intHP))
        counter += 1
    
    # PokemonDict position 8 for Attack
    counter = 0
    for intAt in infile["Attack"]:
        if counter in pokemonPosition:
            pokemonDict[counter].append(int(intAt))
        counter += 1
    
    # PokemonDict position 9 for Defense
    counter = 0
    for intDe in infile["Defense"]:
        if counter in pokemonPosition:
            pokemonDict[counter].append(int(intDe))
        counter += 1
    
    # PokemonDict position 10 for Special Attack
    counter = 0
    for intSa in infile["Special Attack"]:
        if counter in pokemonPosition:
            pokemonDict[counter].append(int(intSa))
        counter += 1
    
    # PokemonDict position 11 for Special Defense
    counter = 0
    for intSd in infile["Special Defense"]:
        if counter in pokemonPosition:
            pokemonDict[counter].append(int(intSd))
        counter += 1
    
    # PokemonDict position 12 for Speed
    counter = 0
    for intSp in infile["Speed"]:
        if counter in pokemonPosition:
            pokemonDict[counter].append(int(intSp))
        counter += 1
     
    # PokemonDict position 13 for Gender ratio
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
            pokemonDict[counter].append(genderList)
        counter += 1
    
    # PokemonDict position 14 for Evolve
    counter = 0
    for evolve in infile["Evolve"]:
        if counter in pokemonPosition:
            pokemonDict[counter].append(evolve)
        counter += 1
    
    # PokemonDict position 15 for Mass
    counter = 0
    for massList in infile["Mass"]:
        if counter in pokemonPosition:
            currentMass = [massList]
            if currentMass[0] == "???":
                currentMass.append(False)
            else:
                currentMass[0] = float(currentMass[0])
                currentMass.append(True)
            pokemonDict[counter].append(currentMass)
        counter += 1
    
    # PokemonDict position 16 for Crunch Name
    counter = 0
    if sheet == "Fakemon":
        for strCrunch in infile["Crunch Name"]:
            pokemonDict[counter].append(strCrunch)
            counter += 1
    # Creates the pokemon objects
    for pokemonNum in pokemonPosition:
        specialty = False
        # Checks if the pokemon has a special ability
        for pokemonAbility in abilitySpecialtyDict:
            if abilitySpecialtyDict[pokemonAbility].effect[1] in pokemonDict[pokemonNum][0]:
                pokemonObj = Pokemon(pokemonDict[pokemonNum][0], abilitySpecialtyDict[pokemonAbility],
                             pokemonDict[pokemonNum][14], pokemonDict[pokemonNum][15],
                             pokemonDict[pokemonNum][1], pokemonDict[pokemonNum][2], 
                             pokemonDict[pokemonNum][13])
                specialty = True
        if not specialty:
            # Checks if pokemon has any abilities in the current abilityList
            possibleAbilities = []
            if pokemonDict[pokemonNum][3] in abilityList:
                possibleAbilities.append(pokemonDict[pokemonNum][3])
            if pokemonDict[pokemonNum][4] in abilityList:
                possibleAbilities.append(pokemonDict[pokemonNum][4])
            if pokemonDict[pokemonNum][5] in abilityList:
                possibleAbilities.append(pokemonDict[pokemonNum][5])
            if len(possibleAbilities) == 0:
                pokemonObj = Pokemon(pokemonDict[pokemonNum][0], abilityDict[choice(abilityList)], 
                                 pokemonDict[pokemonNum][14], pokemonDict[pokemonNum][15],
                                 pokemonDict[pokemonNum][1], pokemonDict[pokemonNum][2], 
                                 pokemonDict[pokemonNum][13])
            else:
                pokemonObj = Pokemon(pokemonDict[pokemonNum][0], abilityDict[choice(possibleAbilities)], 
                pokemonDict[pokemonNum][14], pokemonDict[pokemonNum][15],
                pokemonDict[pokemonNum][1], pokemonDict[pokemonNum][2], 
                pokemonDict[pokemonNum][13])
        # Sets the base stats of a pokemon
        pokemonObj.setBaseStat("HP", pokemonDict[pokemonNum][7])
        if pokemonDict[pokemonNum][0] in megaDict:
            megaDict[pokemonDict[pokemonNum][0]][0].setBaseStat("HP", pokemonDict[pokemonNum][7])
        pokemonObj.setBaseStat("Attack", pokemonDict[pokemonNum][8])
        pokemonObj.setBaseStat("Defense", pokemonDict[pokemonNum][9])
        pokemonObj.setBaseStat("Special Attack", pokemonDict[pokemonNum][10])
        pokemonObj.setBaseStat("Special Defense", pokemonDict[pokemonNum][11])
        pokemonObj.setBaseStat("Speed", pokemonDict[pokemonNum][12])   
        # Gives the pokemon a guaranteed move
        pokemonObj.guaranteedMove = pokemonDict[pokemonNum][6]
        if len(pokemonDict[pokemonNum]) == 17:
            pokemonObj.crunchName = pokemonDict[pokemonNum][16]
        pokedexDict[pokemonDict[pokemonNum][0]] = pokemonObj
    
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
        currentMass = [float(massList)]
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
