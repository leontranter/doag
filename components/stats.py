class Stats:
	def __init__(self, Strength=10, Precision=10, Agility=10, Intellect=10, Willpower=10, Stamina=10, Endurance=10):
		self.Strength = Strength
		self.Precision = Precision
		self.Agility = Agility
		self.Intellect = Intellect
		self.Willpower = Willpower
		self.Stamina = Stamina
		self.Endurance = Endurance
		self.base_max_hp = self.Stamina + self.Endurance
		self.hp = self.base_max_hp
		self.evade = int((self.Agility + self.Precision) / 4)
		self.base_sp = Stamina * 2
		self.sp = self.base_sp

	@property
	def max_hp(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.max_hp_bonus
		else:
			bonus = 0
		return self.base_max_hp + bonus

	def get_strength_in_range(self):
		if self.Strength < 5:
			return 5
		if self.Strength > 19:
			return 19
		else:
			return self.Strength
