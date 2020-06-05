import tcod as libtcod
from item_functions import heal, cast_fireball, cast_lightning, cast_confuse, learn_fireball, learn_heal
from game_messages import Message

class Item:
	def __init__(self, use_function=None, targeting=False, targeting_message=None, **kwargs):
		self.use_function = use_function
		self.targeting = targeting
		self.targeting_message = targeting_message
		self.function_kwargs = kwargs