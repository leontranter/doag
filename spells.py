import tcod as libtcod
from item_functions import heal, cast_fireball, cast_lightning, cast_confuse
from game_messages import Message

class Spell:
	def __init__(self, name, mana_cost, use_function=None, targeting=None, targeting_message=None, **kwargs):
		self.name = name
		self.mana_cost = mana_cost
		self.use_function = use_function
		self.targeting = targeting
		self.targeting_message = targeting_message
		self.function_kwargs = kwargs

class SpellFactory:
	def make_fireball_spell():
		spell = Spell("Fireball", 10, cast_fireball, targeting=True, targeting_message=Message('Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan), damage=30, radius=3)
		return spell

	def make_heal_spell():
		spell = Spell("Heal", 5, heal, amount=10)
		return spell

	def make_bless_spell():
		spell = Spell("Bless", 4, bless, targeting=True, targeting_message=Message('Left-click a target to cast Bless on, or right-click to cancel.', libtcod.light_cyan), bonus=1)