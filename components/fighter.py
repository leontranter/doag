import tcod as libtcod
from game_messages import Message
from loader_functions.constants import get_basic_damage
from random_utils import dice_roll
from damage_types import DamageTypes, damage_type_modifiers
from systems.damage import calculate_damage, damage_messages, apply_physical_damage_modifiers
from systems.attack import get_weapon_skill_for_attack
from systems.damage import get_basic_swing_damage, get_basic_thrust_damage

class Fighter:
	def __init__(self, base_DR=0, xp=0):
		self.base_DR = base_DR
		self.xp = xp
		self.effects_list = []

	@property
	def DR(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.DR_bonus
		else:
			bonus = 0
		return self.base_DR + bonus	

	def get_current_melee_damage(self):
		# TODO: Fix this! Implement punching and kicking properly
		# nothing in main hand
		if not self.owner.equipment.main_hand:
			dice, modifier = get_basic_thrust_damage(self.owner)
			damage_type = DamageTypes.CRUSHING
		# something in main hand but it's not a melee weapon, e.g. a bow
		elif self.owner.equipment.main_hand and not self.owner.equipment.main_hand.melee_weapon:
			dice, modifier = self.get_basic_thrust_damage(self.owner)
			modifier += 1
			damage_type = DamageTypes.CRUSHING
		elif self.owner.equipment.main_hand.melee_weapon.melee_attack_type == "swing":
			dice, modifier = get_basic_swing_damage(self.owner)
			damage_type = self.owner.equipment.main_hand.melee_weapon.melee_damage_type
		else:
			dice, modifier = get_basic_thrust_damage(self.owner)
			damage_type = self.owner.equipment.main_hand.melee_weapon.melee_damage_type
		modifier += apply_physical_damage_modifiers(modifier, self.owner)
		return (dice, modifier, damage_type)

	def get_current_missile_damage(self):
		if not self.owner.equipment.main_hand.missile_weapon:
			return 0, 0, "crushing"
		else:
			dice, modifier = self.owner.equipment.main_hand.missile_weapon.missile_damage
			# TODO: Sort this missile damage stuff out once and for all
			#modifier += self.owner.equipment.missile_damage_bonus
			damage_type = self.owner.equipment.main_hand.missile_weapon.missile_damage_type
			return (dice, modifier, damage_type)
	
	def resolve_hit(self, results, dice, modifier, damage_type, target):
		base_damage, penetrated_damage, final_damage = calculate_damage(dice, modifier, damage_type, target)
		results = damage_messages(results, self.owner, target, base_damage, final_damage, damage_type)
		return results

	def take_damage(self, amount):
		results = []

		self.owner.stats.hp -= amount

		if self.owner.stats.hp <= 0:
			results.append({'dead': self.owner, 'xp': self.xp})
		return results

	# TODO: clean this up - most of these two functions can be merged
	def melee_attack(self, target):
		results = []
		if self.check_hit(target):
			defense_result, defense_choice = target.defender.defend_melee_attack()
			if not defense_result:
				results.append(self.hit_message(target, defense_choice))
				dice, modifier, damage_type = self.get_current_melee_damage()
				results = self.resolve_hit(results, dice, modifier, damage_type, target)
			else:
				verb = "hit" if self.owner.name.true_name == "Player" else "hits"
				results.append({'attack_defended': True, 'message': Message(f'{self.owner.name.subject_name} {verb}, but {target.name.object_name} {defense_choice}s the attack.')})
		else:
			verb = "miss" if self.owner.name.true_name == "Player" else "misses"
			results.append({'attack_miss': True, 'message': Message(f'{self.owner.name.subject_name} {verb} {target.name.object_name}.')})
		return results

	def missile_attack(self, target):
		results = []
		if self.check_hit(target):
			defense_result, defense_choice = target.defender.defend_missile_attack()
			if not defense_result:
				results.append(self.hit_message(target, defense_choice))
				dice, modifier, damage_type = self.get_current_missile_damage()
				results = self.resolve_hit(results, dice, modifier, damage_type, target)
			else:
				verb = "hit" if self.owner.name.true_name == "Player" else "hits"
				results.append({'attack_defended': True, 'message': Message(f'{self.owner.name.subject_name} {verb}, but the {target.name.object_name} {defense_choice}s the attack.')})	
		else:
			verb1 = "fire" if self.owner.name.true_name == "Player" else "fires"
			pronoun = "your" if self.owner.name.true_name == "Player" else "their"
			verb2 = "miss" if self.owner.name.true_name == "Player" else "misses"
			results.append({'attack_miss': True, 'message': Message(f'{self.owner.name.subject_name} {verb1} {pronoun} {self.owner.equipment.main_hand.name.true_name} but {verb2} {target.name.object_name}.')})
		if dice_roll(1, 0) > 2:
			results.append({'missile_dropped': True, 'missile_type': self.owner.equipment.ammunition.name.true_name, 'dropped_location': (target.x, target.y)})
		results.append({'fired_weapon': True})
		return results

	def check_hit(self, target):
		# TODO: Fix this!
		if self.owner.equipment.main_hand and self.owner.equipment.main_hand.melee_weapon:
			skill_target = get_weapon_skill_for_attack(self.owner, self.owner.equipment.main_hand.melee_weapon)
		elif self.owner.equipment.main_hand and self.owner.equipment.main_hand.missile_weapon:
			skill_target = get_weapon_skill_for_attack(self.owner, self.owner.equipment.main_hand.missile_weapon)
		numberRolled = dice_roll(3, 0)
		if numberRolled <= skill_target:
			return True
		else:
			return False

	def hit_message(self, target, defense_choice):
		verb = "hit" if self.owner.name.true_name == "Player" else "hits"
		verb2 = "try" if target.name.true_name == "Player" else "tries"
		verb3 = "fail" if target.name.true_name == "Player" else "fails"
		message = {'message':  Message(f"{self.owner.name.subject_name} {verb}! {target.name.subject_name} {verb2} to {defense_choice} the attack but {verb3}.")} 
		return message

	def heal(self, amount):
		self.owner.stats.hp += amount
		if self.owner.stats.hp > self.owner.stats.max_hp:
			self.owner.stats.hp = self.owner.stats.max_hp

	def load_missile_weapon(self):
		results = []
		# TODO : needs to check you have the right type of ammunition!!
		if self.owner.equipment.has_missile_weapon():
			if self.owner.equipment.has_ammunition():
				self.owner.equipment.main_hand.missile_weapon.loaded = True
				results.append({"loaded": True, "message": Message("You load your missile weapon.")})
			else:
				results.append({'message': Message("You don't have any ammunition for that weapon!")})
		else:
			results.append({'message': Message("You don't have a missile weapon equipped!")})
		return results

	def fire_weapon(self, **kwargs):
		results = []
		if not self.owner.equipment.main_hand.missile_weapon:
			results.append({'message': Message("You have no missile weapon equipped.")})
		elif not self.owner.equipment.main_hand.missile_weapon.loaded:
			results.append({'message': Message("You don't have any ammunition loaded.")})
			return results
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
						self.owner.equipment.main_hand.missile_weapon.loaded = False
						results.extend(self.missile_attack(entity))					
		return results
