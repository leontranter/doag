class Spell:
	def __init__(self, name, mana_cost, use_function=None, targeting=None, targeting_message=None, **kwargs):
		self.name = name
		self.mana_cost = mana_cost
		self.use_function = use_function
		self.targeting = targeting
		self.targeting_message = targeting_message
		self.function_kwargs = kwargs

