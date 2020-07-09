class MeleeWeapon:
	def __init__(self, weapon_type, weapon_category, melee_attack_type, melee_damage_bonus, melee_damage_type, min_strength=8):
		self.weapon_type = weapon_type
		self.weapon_category = weapon_category
		self.melee_attack_type = melee_attack_type
		self.melee_damage_bonus = melee_damage_bonus
		self.melee_damage_type = melee_damage_type
		self.min_strength = min_strength