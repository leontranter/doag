import tcod as libtcod
class Caster:
	def __init__(self, spells=[], max_mana=0):
		self.spells = spells
		self.max_mana = max_mana
		self.mana = max_mana