class Effect:
	def __init__(self, name, description, turns_left, damage_per_turn=0, hit_modifier=0, physical_damage_modifier=0):
		self.name = name
		self.description = description
		self.turns_left = turns_left
		self.damage_per_turn = damage_per_turn
		self.hit_modifier = hit_modifier
		self.physical_damage_modifier = physical_damage_modifier
