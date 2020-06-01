import tcod as libtcod
from item_functions import heal, cast_fireball, cast_lightning, cast_confuse, learn_fireball, learn_heal
from game_messages import Message

class Item:
	def __init__(self, use_function=None, targeting=False, targeting_message=None, **kwargs):
		self.use_function = use_function
		self.targeting = targeting
		self.targeting_message = targeting_message
		self.function_kwargs = kwargs

class ItemFactory:
	
	def makeHealingPotion():
		tempItem = Item(use_function=heal, amount=40)
		return tempItem

	def makeLightningScroll():
		tempItem = Item(use_function=cast_lightning, damage=40, maximum_range=5)
		return tempItem

	def makeFireballScroll():
		tempItem = Item(use_function=cast_fireball, targeting=True, targeting_message=Message('Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan), damage=25, radius=3)
		return tempItem

	def makeConfusionScroll():
		tempItem = Item(use_function=cast_confuse, targeting=True, targeting_message=Message('Left-click on an enemy to confuse it or right-click to cancel.', libtcod.light_cyan))
		return tempItem

	def makeFireballBook():
		tempItem = Item(use_function=learn_fireball, spell="Fireball")
		return tempItem

	def makeHealBook():
		tempItem = Item(use_function=learn_heal, spell="Heal")
		return tempItem