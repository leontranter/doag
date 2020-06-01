from components.fighter import Fighter
from systems.attack import weapon_skill_lookup
from random_utils import dice_roll

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
		defense_num = self.get_best_missile_defense()
		if dice_roll(3, 0) <= defense_num:
			return True
		else:
			return False

	def get_parry(self):
		bonus = self.owner.equipment.PD_bonus
		if self.owner.skills and self.owner.equipment.main_hand:
			weapon_skill = weapon_skill_lookup(self.owner.equipment.main_hand.equippable)
			weapon_skill_num = self.owner.skills.getSkill(weapon_skill)
			parry_num = int(weapon_skill_num /2) + bonus
			return parry_num
		else:
			return self.default_defense + bonus

	def get_block(self):
		if self.owner.equipment and self.owner.equipment.off_hand and self.owner.equipment.off_hand.equippable.isShield:
			bonus = self.owner.equipment.PD_bonus
			shield_skill_num = self.owner.skills.getSkill("shield")
			return int(shield_skill_num / 2) + bonus
		else:
			return 0

	def get_dodge(self):
		bonus = self.owner.equipment.PD_bonus
		dodge = self.owner.stats.move + bonus
		return dodge

	def get_best_melee_defense(self):
		if not (self.owner.equipment or self.owner.skills):
			# This should never happen - something has gone wrong - but better to just return a dodge of 3 rather than blow up
			return ("dodge", 3)
		defenses = {"block": self.get_block(), "parry": self.get_parry(), "dodge": self.get_dodge()}
		# whats our best defense score?
		max_defense = max([value for key, value in defenses.items()])
		# find the corresponding defense name in the dictionary
		for key, value in defenses.items():
			if value == max_defense:
				defense_choice = key
				# no point looking further, just grab the first one that has the highest score
				# there may be reasons why you would want to prioritise one over another if they have the same score
				# TODO: maybe a better way to break ties? i.e. favour dodge over block or parry, if I implement parrying weapons or shields breaking?
				break
		return (defense_choice, max_defense)

	def get_best_missile_defense(self):
		if self.get_block() > self.get_dodge():
			return ("block", self.get_block())
		else:
			return ("dodge", self.get_dodge())