import tcod as libtcod
from random_utils import diceRoll
from damage_types import DamageTypes, damage_type_modifiers
from game_messages import Message

def calculate_damage(dice, modifier, damage_type, target):
	base_damage = diceRoll(dice, modifier)
	penetrated_damage = max(base_damage - target.fighter.DR, 0)
	final_damage = int(penetrated_damage * damage_type_modifiers[damage_type])
	return base_damage, penetrated_damage, final_damage

def damage_messages(results, attacker, target, base_damage, final_damage, damage_type):
	if final_damage > 0:
		results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(attacker.name.capitalize(), target.name, str(base_damage)), libtcod.white)})
		results.append({'message': Message('After DR of {0} is applied, {1} takes {2} {3} damage.'.format(target.fighter.DR, target.name, str(final_damage), damage_type.name.lower()), libtcod.white)})
		results.extend(target.fighter.take_damage(final_damage))
		if target.stats.hp > 0:
			results.append({'message': Message('The {} has {} hp remaining.'.format(target.name, target.stats.hp), libtcod.white)})
	else:
		results.append({'message': Message('{0} attacks {1} but does no damage.'.format(attacker.name.capitalize(), target.name), libtcod.white)})

	return results