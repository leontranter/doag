class Level:
	def __init__(self, current_level=1, current_xp=0, level_up_base=1, level_up_factor=2):
		self.current_level = current_level
		self.current_xp = current_xp
		self.level_up_base = level_up_base
		self.level_up_factor = level_up_factor

	@property
	def experience_to_next_level(self):
		return self.level_up_base + self.current_level * self.level_up_factor

	def add_xp(self, xp):
		self.current_xp += xp

		if self.current_xp > self.experience_to_next_level:
			self.current_xp -= self.experience_to_next_level
			self.current_level += 1
			return True
		else:
			return False

	def level_up(self):
		if self.owner.stats and self.owner.fighter:
			self.owner.stats.max_hp += 1
			self.owner.stats.Endurance += 1
			self.owner.fighter.heal(2)
			self.owner.stats.max_sp += 2
			self.owner.stats.sp += 2
			if self.owner.caster:
				self.owner.caster.max_mana += 1