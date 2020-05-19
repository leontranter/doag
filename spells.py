from item_functions import heal, cast_fireball, cast_lightning, cast_confuse

class Spell:

	def __init__(self, name, use_function=None, targeting=None, targeting_message=None, **kwargs):
		self.name = name
		self.use_function = use_function
		self.targeting = targeting
		self.targeting_message = targeting_message
		self.function_kwargs = kwargs