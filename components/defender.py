from components.fighter import Fighter
from systems.attack import weapon_skill_lookup
from random_utils import dice_roll
from systems.skill_manager import SkillNames

class Defender:
	def __init__(self):
		self.default_defense = 3

	def defend_melee_attack(self):
		defense_choice, defense_num = self.get_best_melee_defense()
		if dice_roll(3, 0) <= defense_num:
			return True, defense_choice
		else:
			return False, defense_choice

	def defend_missile_attack(self):
		defense_choice, defense_num = self.get_best_missile_defense()
		if dice_roll(3, 0) <= defense_num:
			return True, defense_choice
		else:
			return False, defense_choice

	def get_parry(self):
		if self.owner.equipment.main_hand and self.owner.equipment.main_hand.melee_weapon:
			weapon_skill = weapon_skill_lookup(self.owner.equipment.main_hand.melee_weapon)
			weapon_skill_num = self.owner.skills.get_skill_check(weapon_skill)
			parry_num = int(weapon_skill_num /2)
			return parry_num
		else:
			return self.default_defense

	def get_block(self):
		if self.owner.equipment.off_hand and self.owner.equipment.off_hand.equippable.isShield:
			shield_skill_num = self.owner.skills.get_skill_check(SkillNames.SHIELD)
			return int(shield_skill_num / 2)
		else:
			return 0

	def get_evade(self):
		evade = self.owner.stats.evade
		return evade

	def get_best_melee_defense(self):
		if not (self.owner.equipment or self.owner.skills):
			# This should never happen - something has gone wrong - but better to just return a evade of 3 rather than blow up
			return ("evade", 3)
		defenses = {"block": self.get_block(), "parry": self.get_parry(), "evade": self.get_evade()}
		# whats our best defense score?
		max_defense = max([value for key, value in defenses.items()])
		# find the corresponding defense name in the dictionary
		for key, value in defenses.items():
			if value == max_defense:
				defense_choice = key
				# no point looking further, just grab the first one that has the highest score
				# there may be reasons why you would want to prioritise one over another if they have the same score
				# TODO: maybe a better way to break ties? i.e. favour evade over block or parry, if I implement parrying weapons or shields breaking?
				break
		return (defense_choice, max_defense)

	def get_best_missile_defense(self):
		if self.get_block() > self.get_evade():
			return ("block", self.get_block())
		else:
			return ("evade", self.get_evade())