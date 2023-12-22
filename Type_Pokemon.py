# The Type class defines the type of pokemon and moves
class Type:
    
    def __init__(self, typeName):
        self.typeName = typeName
        self.effectDict = {}
    
    # Sets the type effectiveness when attacking
    def setEffectiveness(self, typeName, damageMult):
        self.effectDict[typeName] = damageMult