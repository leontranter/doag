import tcod as libtcod
from random_utils import dice_roll
from damage_types import DamageTypes, damage_type_modifiers
from game_messages import Message
from loader_functions.constants import get_basic_damage

def get_current_melee_damage(entity):
	# TODO: Fix this! Implement punching and kicking properly
	# nothing in main hand
	if not entity.equipment.main_hand:
		dice, modifier = get_basic_thrust_damage(entity)
		damage_type = DamageTypes.CRUSHING
	# something in main hand but it's not a melee weapon, e.g. a bow
	elif entity.equipment.main_hand and not entity.equipment.main_hand.melee_weapon:
		dice, modifier = get_basic_thrust_damage(entity)
		modifier += 1
		damage_type = DamageTypes.CRUSHING
	elif entity.equipment.main_hand.melee_weapon.melee_attack_type == "swing":
		dice, modifier = get_basic_swing_damage(entity)
		damage_type = entity.equipment.main_hand.melee_weapon.melee_damage_type
	else:
		dice, modifier = get_basic_thrust_damage(entity)
		damage_type = entity.equipment.main_hand.melee_weapon.melee_damage_type
	modifier += apply_physical_damage_modifiers(modifier, entity)
	return (dice, modifier, damage_type)

def get_physical_damage_modifier_from_status_effects(entity):
	physical_damage_modifier = 0
	for effect in entity.fighter.effect_list:
		physical_damage_modifier += effect.get("physical_damage_modifier") or 0
	return physical_damage_modifier	

def get_physical_damage_modifier_from_equipment(entity):
	modifier = 0
	# TODO: could refactor this into iterating through a list??
	if entity.equipment.main_hand:
		modifier += entity.equipment.main_hand.equippable.physical_damage_modifier or 0	
	if entity.equipment.off_hand:
		modifier += entity.equipment.off_hand.equippable.physical_damage_modifier or 0
	if entity.equipment.body:
		modifier += entity.equipment.body.equippable.physical_damage_modifier or 0
	if entity.equipment.ammunition:
		modifier += entity.equipment.ammunition.equippable.physical_damage_modifier or 0
	return modifier	

def get_basic_swing_damage(entity):
	ST = entity.stats.get_strength_in_range()
	swing_damage, thrust_damage = get_basic_damage()
	dice, modifier = swing_damage[ST][0], swing_damage[ST][1]
	return (dice, modifier)

def get_basic_thrust_damage(entity):
	ST = entity.stats.get_strength_in_range()
	swing_damage, thrust_damage = get_basic_damage()
	dice, modifier = thrust_damage[ST][0], thrust_damage[ST][1]	
	return (dice, modifier)

def calculate_damage(dice, modifier, damage_type, target):
	base_damage = dice_roll(dice, modifier)
	penetrated_damage = max(base_damage - target.fighter.DR, 0)
	final_damage = int(penetrated_damage * damage_type_modifiers[damage_type])
	return base_damage, penetrated_damage, final_damage

def damage_messages(results, attacker, target, base_damage, final_damage, damage_type):
	if final_damage > 0:
		verb = "hit" if attacker.name.true_name == "Player" else "hits"
		results.append({
			'message': Message(f'{attacker.name.subject_name} {verb} {target.name.object_name} for {str(base_damage)} hit points.', libtcod.red)
			})
		verb = "takes" if attacker.name.true_name == "Player" else "take"
		results.append({'message': Message(f'After DR of {target.fighter.DR} is applied, {target.name.object_name} {verb} {str(final_damage)} {damage_type.name.lower()} damage.', libtcod.red)})
		results.extend(target.fighter.take_damage(final_damage))
	else:
		verb = "don't" if attacker.name.true_name == "Player" else "doesn't"
		verb2 = "your" if target.name.true_name == "Player" else target.name.object_name
		results.append({'message': Message(f'{attacker.name.subject_name} {verb} do enough damage to penetrate {verb2} armour.', libtcod.red)})

	return results

def apply_physical_damage_modifiers(modifier, entity):
	modifier += get_physical_damage_modifier_from_status_effects(entity)
	modifier += get_physical_damage_modifier_from_equipment(entity)
	return modifier

def get_damage_string(entity):
	if entity.fighter:
		dice, modifier, damage_type = get_current_melee_damage(entity)
		damage_type = damage_type.name.capitalize()
		if modifier < 0:
			damage_string = "{}d6 {} {}".format(dice, modifier, damage_type)
		elif modifier == 0:
			damage_string = "{}d6 {}".format(dice, damage_type)
		else:
			damage_string = "{}d6 +{} {}".format(dice, modifier, damage_type)
	else:
		damage_string = ""
	return damage_string