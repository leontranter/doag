from components.fighter import Fighter
from systems.attack import weapon_skill_lookup

class Defender:
	def __init__(self):
		self.default_defense = 3

	def defend_melee_attack():
		defense_num = get_best_melee_defense()
		defense_roll = diceRoll(3, 0)
		if defense_roll <= defense_num:
			return True
		else:
			return False

	def defend_missile_attack():
		defense_num = get_best_missile_defense()
		defense_roll = diceRoll(3, 0)
		if defense_roll <= defense_num:
			return True
		else:
			return False


	def get_parry(self):
		bonus = self.PD_bonus
		if self.owner.equipment.main_hand and self.owner.skills:
			weapon_skill = weapon_skill_lookup(self.owner.equipment.main_hand.equippable)
			weapon_skill_num = self.owner.skills.getSkill(weapon_skill)
			return int(weapon_skill_num / 2) + bonus
		else:
			return self.default_defense + bonus

	def get_block(self):
		if self.owner.equipment.off_hand.equippable.isShield:
			if self.owner.skills:
				bonus = self.owner.fighter.PD_bonus
				shield_skill_num = self.owner.skills.getSkill("shield")
				return int(shield_skill_num / 2) + bonus
			else:
				return None
		else:
			return None

	def getDodge(self):
		bonus = self.owner.fighter.PD_bonus
		dodge = self.move + bonus
		return dodge

	def get_best_melee_defense(self):
		if self.getBlock():	
			best_mele_defense = max(self.getParry(), self.getBlock(), self.getDodge())
		else:
			best_melee_defense = max(self.getParry(), self.getDodge()) 
		return best_melee_defense

	def get_best_missile_defense(self):
		if getBlock():
			best_missile_defense = max(self.getBlock(), self.getDodge())
		else:
			best_missile_defense = getDodge()
		return best_missile_defensp