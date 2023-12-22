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