class Stats:
	def __init__(self, Strength=10, Precision=10, Agility=10, Intellect=10, Willpower=10, Stamina=10, Endurance=10):
		self.Strength = Strength
		self.Precision = Precision
		self.Agility = Agility
		self.Intellect = Intellect
		self.Willpower = Willpower
		self.Stamina = Stamina
		self.Endurance = Endurance
		self.max_hp = self.Stamina + self.Endurance
		self.hp = self.max_hp
		self.evade = int((self.Agility + self.Precision) / 4)
		self.max_sp = Stamina * 2
		self.sp = self.max_sp
		self.hp_regen_counter = 0
		self.sp_regen_counter = 0

	@property
	def total_max_hp(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.max_hp_bonus
		else:
			bonus = 0
		return self.max_hp + bonus

	@property
	def hp_regen_amount(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.hp_regen_bonus
		else:
			bonus = 0
		return self.Endurance / 100 + bonus

	@property
	def sp_regen_amount(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.sp_regen_bonus
		else:
			bonus = 0
		return self.Stamina / 100 + bonus

	@property
	def mana_regen_amount(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.mana_regen_bonus
		else:
			bonus = 0
		return self.Willpower / 100 + bonus

	def restore_stamina(self, amount):
		self.sp += amount
		if self.sp > self.max_sp:
			self.sp = self.max_sp