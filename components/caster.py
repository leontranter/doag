import tcod as libtcod

class Caster:
	def __init__(self, spells=[], max_mana=0):
		self.spells = spells
		self.max_mana = max_mana
		self.mana = max_mana
		self.mana_regen_counter = 0

	def restore_mana(self, amount):
		self.mana += amount
		if self.mana >= self.max_mana:
			self.mana = self.max_mana