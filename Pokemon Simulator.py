from random import choice, randint
from math import ceil
from graphics import GraphWin
import copy

from Battle_Pokemon import Battle
from Helper_Pokemon import Abilities, ItemList, Megas, MoveList, Pokedex, selectPokemon, ZMoveList
from Team_Pokemon import Team

# Simulates the game against a computer
def battleSimulator():
    battleWindow = GraphWin("Battle Simulator", 500, 400)
    battleWindow.setCoords(0, 0, 500, 400)
    # Imports the data from the Excel sheet and stores
    abilityDict, abilitySpecialtyDict, abilityList = Abilities()
    megaDict, megaList = Megas(abilityDict)
    megaUsed = [choice(megaList), choice(megaList)]
    # Add pokemon to test code
    #megaUsed.append("Smeargle")
    #megaUsed.append("Smeargle")
    pokemonName = selectPokemon("Pokemon", 10, megaUsed)
    pokemonDict, megaDict = Pokedex(pokemonName, megaDict, abilityDict, abilitySpecialtyDict, abilityList, 'Pokemon')
    fakemonDict, fakemonList = Pokedex(pokemonName, megaDict, abilityDict, abilitySpecialtyDict, abilityList, 'Fakemon')
    moveDict, moveList, moveAttacking, struggle = MoveList()
    itemDict, itemSpecialtyDict, itemNormalName, itemSpecialtyName = ItemList()
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
