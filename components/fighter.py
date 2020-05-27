import tcod as libtcod
from game_messages import Message
from loader_functions.constants import get_basic_damage
from random_utils import diceRoll
from damage_types import DamageTypes, damage_type_modifiers
from systems.damage import calculate_damage, damage_messages
from systems.attack import get_weapon_skill_for_attack

class Fighter:
	def __init__(self, base_DR=0, xp=0):
		self.base_DR = base_DR
		self.xp = xp

	@property
	def DR(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.DR_bonus
		else:
			bonus = 0
		return self.base_DR + bonus

	@property
	def PD(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.PD_bonus
		else:
			bonus = 0
		return bonus	

	def get_basic_swing_damage(self):
		# TODO: Fix this up!! No magic numbers!
		ST = self.owner.stats.get_strength_in_range()
		swing_damage, thrust_damage = get_basic_damage()
		dice, modifier = swing_damage[ST][0], swing_damage[ST][1]
		return (dice, modifier)

	def get_basic_thrust_damage(self):
		ST = self.owner.stats.get_strength_in_range()
		swing_damage, thrust_damage = get_basic_damage()
		dice, modifier = thrust_damage[ST][0], thrust_damage[ST][1]
		return (dice, modifier)

	def get_current_melee_damage(self):
		if self.owner.equipment.main_hand.equippable.melee_attack_type == "swing":
			dice, modifier = self.get_basic_swing_damage()
		else:
			dice, modifier = self.get_basic_thrust_damage()
		modifier += self.owner.equipment.melee_damage_bonus
		damage_type = self.owner.equipment.main_hand.equippable.melee_damage_type
		return (dice, modifier, damage_type)

	def get_current_missile_damage(self):
		if not self.owner.equipment.main_hand.equippable.missile_damage_type:
			return 0, 0, "crushing"
		else:
			dice, modifier = self.owner.equipment.main_hand.equippable.missile_damage
			modifier += self.owner.equipment.missile_damage_bonus
			damage_type = self.owner.equipment.main_hand.equippable.missile_damage_type
			return (dice, modifier, damage_type)
		
	def take_damage(self, amount):
		results = []

		self.owner.stats.hp -= amount

		if self.owner.stats.hp <= 0:
			results.append({'dead': self.owner, 'xp': self.xp})
		return results

	def melee_attack(self, target):
		results = []
		if self.check_hit(target):
			if target.defender.defend_attack(attack_type="melee"):
				dice, modifier, damage_type = self.get_current_melee_damage()
				results = self.resolve_hit(results, dice, modifier, damage_type, target)
			else:
				results.append({'attack_defended': True, 'message': Message(f'The {target.name} defends against your attack.')})
		else:
			print("miss!")
			results.append({'melee_attack_miss': True, 'message': Message(f'{self.owner.name} misses the {target.name}.')})
		return results

	def resolve_hit(self, results, dice, modifier, damage_type, target, missile_attack=False):
		base_damage, penetrated_damage, final_damage = calculate_damage(dice, modifier, damage_type, target)
		results = damage_messages(results, self.owner, target, base_damage, final_damage, damage_type)
		return results

	def missile_attack(self, target):
		results = []
		if self.check_hit(target):
			dice, modifier, damage_type = self.get_current_missile_damage()
			results.append({'fired_weapon': True})
			results = self.resolve_hit(results, dice, modifier, damage_type, target, missile_attack=True)
		else:
			results.append({'missile_attack_miss': True, 'message': Message(f'{self.owner.name} misses the {target.name}.')})
		return results

	def check_hit(self, target):
		# TODO: Fix this!
		skill_target = get_weapon_skill_for_attack(self.owner, self.owner.equipment.main_hand.equippable)
		numberRolled = diceRoll(3, 0)
		if numberRolled <= skill_target:		
			print(f"diceRoll was {numberRolled}, target was {skill_target}")
			return True
		else:
			return False

	def heal(self, amount):
		self.owner.stats.hp += amount
		if self.owner.stats.hp > self.owner.stats.max_hp:
			self.owner.stats.hp = self.owner.stats.max_hp

	def fire_weapon(self, **kwargs):
		results = []
		if not self.owner.equipment.main_hand.equippable.missile_damage:
			results.append({"no_missile_attack_weapon": True})
		if not (kwargs.get("target_x") or kwargs.get("target_y")):
			results.append({'missile_targeting': True})
			return results
		else:
			entities = kwargs.get('entities')
			fov_map = kwargs.get('fov_map')
			target_x = kwargs.get('target_x')
			target_y = kwargs.get('target_y')
			weapon = kwargs.get('weapon')
			if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
				results.append({'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
				return results
			else:
				for entity in entities:
					if entity.x == target_x and entity.y == target_y and entity.fighter:
						self.owner.equipment.ammunition.equippable.quantity -= 1
						print("lost an arrow")
						results.extend(self.missile_attack(entity))					
		return results
