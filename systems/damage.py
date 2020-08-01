import tcod as libtcod
from random_utils import d6_dice_roll, dn_dice_roll
from damage_types import DamageTypes, damage_type_modifiers
from game_messages import Message

def get_current_melee_damage(entity):
	# TODO: Fix this! Implement punching and kicking properly
	# nothing in main hand
	if not entity.equipment.main_hand:
		dice_number, dice_type, modifier = (1,3,0)
		damage_type = DamageTypes.CRUSHING
	# something in main hand but it's not a melee weapon, e.g. a bow - TODO: make this better
	elif entity.equipment.main_hand and not entity.equipment.main_hand.melee_weapon:
		dice_number, dice_type, modifier = (1,3,0)
		damage_type = DamageTypes.CRUSHING
	elif entity.equipment.main_hand.melee_weapon:
		dice_number, dice_type, modifier = entity.equipment.main_hand.melee_weapon.melee_damage
		damage_type = entity.equipment.main_hand.melee_weapon.melee_damage_type
	else:
		# something very weird has happened
		dice_number, dice_type, modifier = (1,2,0)
		damage_type = DamageTypes.CRUSHING
	modifier += apply_physical_damage_modifiers(modifier, entity)
	return (dice_number, dice_type, modifier, damage_type)

def get_current_missile_damage(entity):
	if not entity.equipment or not entity.equipment.main_hand or not entity.equipment.main_hand.missile_weapon:
		return (0, 0, DamageTypes.CRUSHING)
	else:
		dice_number, dice_type, modifier = entity.equipment.main_hand.missile_weapon.missile_damage
		# TODO: Sort this missile damage stuff out once and for all
		#modifier += self.owner.equipment.missile_damage_bonus
		damage_type = entity.equipment.main_hand.missile_weapon.missile_damage_type
		return (dice_number, dice_type, modifier, damage_type)

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

def calculate_damage(dice_number, dice_type, modifier, damage_type, target):
	base_damage = dn_dice_roll(dice_number, dice_type, modifier)
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
		dice_number, dice_type, modifier, damage_type = get_current_melee_damage(entity)
		damage_type = damage_type.name.capitalize()
		if modifier < 0:
			damage_string = "{}d{} {} {}".format(dice_number, dice_type, modifier, damage_type)
		elif modifier == 0:
			damage_string = "{}d{} {}".format(dice_number, dice_type, damage_type)
		else:
			damage_string = "{}d{} +{} {}".format(dice_number, dice_type, modifier, damage_type)
	else:
		damage_string = ""
	return damage_string