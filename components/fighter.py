import tcod as libtcod
from game_messages import Message
from random_utils import d6_dice_roll
from damage_types import DamageTypes, damage_type_modifiers
from systems.damage import calculate_damage, damage_messages, apply_physical_damage_modifiers, get_current_melee_damage, get_current_missile_damage
from systems.attack import get_weapon_skill_for_attack, apply_hit_modifiers, attack
from systems.damage import get_current_melee_damage
from attack_types import AttackTypes

class Fighter:
	def __init__(self, base_DR=0, xp_reward=0):
		self.base_DR = base_DR
		self.xp_reward = xp_reward
		self.effect_list = []
		# TODO: fix this up
		self.current_targeting_weapon = None
		self.current_targeting_spell = None
		self.current_targeting_consumable = None

	@property
	def DR(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.DR_bonus
		else:
			bonus = 0
		return self.base_DR + bonus	

	def take_damage(self, amount):
		results = []
		self.owner.stats.hp -= amount
		if self.owner.stats.hp <= 0:
			results.append({'dead': self.owner})
		return results

	def heal(self, amount):
		self.owner.stats.hp += amount
		if self.owner.stats.hp >= self.owner.stats.base_max_hp:
			self.owner.stats.hp = self.owner.stats.base_max_hp
		
	def load_missile_weapon(self):
		results = []
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
			if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
				results.append({'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
				return results
			else:
				for entity in entities:
					if entity.x == target_x and entity.y == target_y and entity.fighter:
						self.owner.equipment.ammunition.item.quantity -= 1
						self.owner.equipment.main_hand.missile_weapon.loaded = False
						results.extend(attack(self.owner, entity, AttackTypes.MISSILE))					
		return results
