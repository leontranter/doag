class Feat:
	def __init__(self, name, display_name, parent_skill, minimum_rank, stamina_cost, use_function, targeting,
		tile_targeting, targeting_message, feat_range, cannot_target_entity=False, can_pass_entities=False, **kwargs):
		self.name = name
		self.display_name = display_name
		self.parent_skill = parent_skill
		self.minimum_rank = minimum_rank
		self.stamina_cost = stamina_cost
		self.use_function = use_function
		self.targeting = targeting
		self.tile_targeting = tile_targeting
		self.targeting_message = targeting_message
		self.feat_range = feat_range
		self.cannot_target_entity = cannot_target_entity
		self.can_pass_entities = can_pass_entities
		self.function_kwargs = kwargs