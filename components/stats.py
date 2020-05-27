class Stats:
	def __init__(self, ST=10, DX=10, IQ=10, HT=10):
		self.ST = ST
		self.DX = DX
		self.IQ = IQ
		self.HT = HT
		self.base_max_hp = HT
		self.hp = self.base_max_hp
		self.move = int((DX + HT) / 4)

	@property
	def max_hp(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.max_hp_bonus
		else:
			bonus = 0
		return self.base_max_hp + bonus

	def get_strength_in_range(self):
		if self.ST < 5:
			return 5
		if self.ST > 19:
			return 19
		else:
			return self.ST
