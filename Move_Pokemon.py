from random import randint

from Type_Pokemon import Type

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
            if self.stat in ["Flinch", "Confuse", "Trap", "Mean Look", "Octolock", "Ingrain", "Infatuation", "Pumped", "Perish", "Drowsy", "Aqua Ring"]:
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