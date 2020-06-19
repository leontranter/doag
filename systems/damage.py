import tcod as libtcod
from random_utils import dice_roll
from damage_types import DamageTypes, damage_type_modifiers
from game_messages import Message

def calculate_damage(dice, modifier, damage_type, target):
	base_damage = dice_roll(dice, modifier)
	penetrated_damage = max(base_damage - target.fighter.DR, 0)
	final_damage = int(penetrated_damage * damage_type_modifiers[damage_type])
	return base_damage, penetrated_damage, final_damage

def damage_messages(results, attacker, target, base_damage, final_damage, damage_type):
	if final_damage > 0:
		verb = "hit" if attacker.name.true_name == "Player" else "hits"
		results.append({
			'message': Message(f'{attacker.name.subject_name} {verb} {target.name.object_name} for {str(base_damage)} hit points.', libtcod.white)
			})
		verb = "takes" if attacker.name.true_name == "Player" else "take"
		results.append({'message': Message(f'After DR of {target.fighter.DR} is applied, {target.name.object_name} {verb} {str(final_damage)} {damage_type.name.lower()} damage.', libtcod.white)})
		results.extend(target.fighter.take_damage(final_damage))
		if target.stats.hp > 0:
			verb = "have" if target.name.true_name == "Player" else "has"
			results.append({'message': Message(f'{target.name.subject_name.capitalize()} {verb} {target.stats.hp} hp remaining.', libtcod.white)})
	else:
		verb = "don't" if attacker.name.true_name == "Player" else "doesn't"
		verb2 = "your" if target.name.true_name == "Player" else target.name.object_name
		results.append({'message': Message('{attacker.name.subject_name} {verb} do enough damage to penetrate {verb2} armour.', libtcod.white)})

	return results