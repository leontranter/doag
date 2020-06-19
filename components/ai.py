import tcod as libtcod
from random import randint
from game_messages import Message

class BasicMonster():
	def take_turn(self, target, fov_map, game_map, entities):
		results = []

		monster = self.owner
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			results = self.attack_player(monster, target, fov_map, game_map, entities)
		return results

	def attack_player(self, monster, target, fov_map, game_map, entities):
		# missile attack
		results = []
		target_x, target_y = target.x, target.y
		# TODO: Monster should switch weapons - or maybe run away! - if it has run out of ammunition!
		if self.owner.equipment.has_missile_weapon():
			if self.owner.equipment.has_ammunition():
				if monster.equipment.main_hand.missile_weapon.loaded:
					results.extend(monster.fighter.fire_weapon(weapon=monster.equipment.main_hand.equippable, entities=entities, fov_map=fov_map, target_x=target_x, target_y=target_y))
				else:
					# TODO: This doesn't belong here - should move it to Fighter, but the load weapon function needs to be reworked to work for monsters!!
					self.owner.equipment.main_hand.missile_weapon.loaded = True
					results.append({"message": Message(f"The {self.owner.name.true_name} loads its {self.owner.equipment.main_hand.name.true_name}.")})
			else:
				#no ammunition
				for item in self.owner.inventory.items:
					if item.melee_weapon:
						results.append({"message": Message(f"The {self.owner.name.true_name} equips a {item.name.true_name}."), "equips": item})
		else:
			# melee action (attack or move towards)
			results = self.make_melee_action(results, target, entities, game_map)
		return results

	def make_melee_action(self, results, target, entities, game_map):
		monster = self.owner
		if monster.distance_to(target) >= 2:
			monster.move_astar(target, entities, game_map)
		elif target.stats.hp > 0:
			attack_results = monster.fighter.melee_attack(target)
			results.extend(attack_results)
		return results


class ConfusedMonster:
	def __init__(self, previous_ai, number_of_turns=10):
		self.previous_ai = previous_ai
		self.number_of_turns = number_of_turns

	def take_turn(self, target, fov_map, game_map, entities):
		results = []

		if self.number_of_turns > 0:
			random_x = self.owner.x + randint(0, 2) - 1
			random_y = self.owner.y + randint(0, 2) - 1

			if random_x != self.owner.x and random_y != self.owner.y:
				self.owner.move_towards(random_x, random_y, game_map, entities)

			self.number_of_turns -= 1
		else:
			self.owner.ai = self.previous_ai
			results.append({'message': Message('The {0} is no longer confused!'.format(self.owner.name.true_name), libtcod.red)})

		return results