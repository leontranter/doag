from enum import Enum

class Consumable:
	def __init__(self, consumable_type, use_function=None, targeting=False, targeting_message=None, **kwargs):
		self.consumable_type = consumable_type
		self.use_function = use_function
		self.targeting = targeting
		self.targeting_message = targeting_message
		self.function_kwargs = kwargs

def get_carried_potions(carrying_entity):
	potions = []
	for item in carrying_entity.inventory.items:
		if item.consumable:
			if item.consumable.consumable_type == ConsumableTypes.POTION:
				potions.append(item)
	return potions

class ConsumableTypes(Enum):
	POTION = 1
	SCROLL = 2
	SPELLBOOK = 3