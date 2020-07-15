class Spell:
	def __init__(self, name, mana_cost, spell_skill, use_function, targeting=None, targeting_message=None, **kwargs):
		self.name = name
		self.mana_cost = mana_cost
		self.spell_skill = spell_skill
		self.use_function = use_function
		self.targeting = targeting
		self.targeting_message = targeting_message
		self.function_kwargs = kwargs