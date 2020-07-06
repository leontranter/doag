import tcod as libtcod
from item_functions import heal, cast_fireball, cast_lightning, cast_confuse, learn_fireball, learn_heal
from game_messages import Message

class Item:
	def __init__(self, weight=0, quantity=0):
		self.weight = weight
		self.quantity = 0