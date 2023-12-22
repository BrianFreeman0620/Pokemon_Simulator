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