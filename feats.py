class Feat:
	def __init__(self, name, display_name, parent_skill, minimum_rank, stamina_cost, use_function, targeting, targeting_message, feat_range, **kwargs):
		self.name = name
		self.display_name = display_name
		self.parent_skill = parent_skill
		self.minimum_rank = minimum_rank
		self.stamina_cost = stamina_cost
		self.use_function = use_function
		self.targeting = targeting
		self.targeting_message = targeting_message
		self.feat_range = feat_range
		self.function_kwargs = kwargs