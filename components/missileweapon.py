class MissileWeapon:
	def __init__(self, weapon_type, weapon_category, missile_damage_type, missile_damage=(0, 0, 0), min_strength=8, loaded=False):
		self.weapon_type = weapon_type
		self.weapon_category = weapon_category
		self.missile_damage_type = missile_damage_type
		self.missile_damage = missile_damage
		self.min_strength = min_strength
		self.loaded = loaded