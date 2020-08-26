from loader_functions.constants import WeaponTypes, WeaponCategories
from systems.skill_manager import SkillNames
from systems.damage import get_current_melee_damage, get_current_missile_damage, calculate_damage, damage_messages
from attack_types import AttackTypes
from random_utils import d6_dice_roll
from game_messages import Message
from attack_types import AttackTypes

def attack(attacker, target, attack_type):
	results = []
	if check_hit(attacker, target):
		defense_result, defense_choice = target.defender.defend_melee_attack() if attack_type == AttackTypes.MELEE else target.defender.defend_missile_attack()
		if not defense_result:
			results.append(hit_message(attacker, target, defense_choice))
			dice_number, dice_type, modifier, damage_type = get_current_melee_damage(attacker)
			results = resolve_hit(attacker, results, dice_number, dice_type, modifier, damage_type, target)
		else:
			verb = "hit" if attacker.name.true_name == "Player" else "hits"
			results.append({'message': Message(f'{attacker.name.subject_name} {verb}, but {target.name.object_name} {defense_choice}s the attack.')})
	else:
		results.append(miss_message(attacker, target, attack_type))
		if attack_type == AttackTypes.MISSILE:
			if d6_dice_roll(1, 0) > 2:
				results.append({'missile_dropped': attacker.equipment.ammunition.ammunition.ammunition_type, 'dropped_location': (target.x, target.y)})
	return results

def resolve_hit(attacker, results, dice_number, dice_type, modifier, damage_type, target):
	base_damage, penetrated_damage, final_damage = calculate_damage(dice_number, dice_type, modifier, damage_type, target)
	return damage_messages(results, attacker, target, base_damage, final_damage, damage_type)

def hit_message(attacker, target, defense_choice):
	verb = "hit" if attacker.name.true_name == "Player" else "hits"
	verb2 = "try" if target.name.true_name == "Player" else "tries"
	verb3 = "fail" if target.name.true_name == "Player" else "fails"
	return {'message':  Message(f"{attacker.name.subject_name} {verb}! {target.name.subject_name} {verb2} to {defense_choice} the attack but {verb3}.")}

def miss_message(attacker, target, attack_type):
	if attack_type == AttackTypes.MELEE:
		verb = "miss" if attacker.name.true_name == "Player" else "misses"
		return {'message': Message(f'{attacker.name.subject_name} {verb} {target.name.object_name}.')}
	elif attack_type == AttackTypes.MISSILE:
		verb1 = "fire" if attacker.name.true_name == "Player" else "fires"
		pronoun = "your" if attacker.name.true_name == "Player" else "their"
		verb2 = "miss" if attacker.name.true_name == "Player" else "misses"
		return {'message': Message(f'{attacker.name.subject_name} {verb1} {pronoun} {attacker.equipment.main_hand.name.true_name} but {verb2} {target.name.object_name}.')}

def get_hit_modifier_from_status_effects(entity):
	modifier = 0
	for effect in entity.fighter.effect_list:
		modifier += effect.hit_modifier or 0
	return modifier

def check_hit(attacker, target):
	base_skill_target = get_weapon_skill_for_attack(attacker)
	base_skill_target += apply_hit_modifiers(attacker)
	if d6_dice_roll(3, 0) <= base_skill_target:
		return True
	else:
		return False

def get_hit_modifier_from_equipment(entity):
	modifier = 0
	if entity.equipment.main_hand:
		modifier += entity.equipment.main_hand.equippable.hit_modifier or 0	
	if entity.equipment.off_hand:
		modifier += entity.equipment.off_hand.equippable.hit_modifier or 0
	if entity.equipment.body:
		modifier += entity.equipment.body.equippable.hit_modifier or 0
	if entity.equipment.ammunition:
		modifier += entity.equipment.ammunition.equippable.hit_modifier or 0
	return modifier	

def apply_hit_modifiers(entity):
	return get_hit_modifier_from_status_effects(entity) + get_hit_modifier_from_equipment(entity)

def get_weapon_skill_for_attack(attacker):
	if attacker.skills:
		if attacker.equipment.main_hand:
			weapon_skill = weapon_skill_lookup(attacker.equipment.main_hand)
			return attacker.skills.get_skill_check(weapon_skill)
		else:
			return attacker.skills.get_skill_check(SkillNames.UNARMED)
	elif attacker.stats:
		return attacker.stats.DX - 5
	else:
		return 5

def weapon_skill_lookup(weapon):
	if weapon.melee_weapon:
		return weapon_skill_matches.get(weapon.melee_weapon.weapon_category)
	elif weapon.missile_weapon:
		return weapon_skill_matches.get(weapon.missile_weapon.weapon_category)

weapon_skill_matches = {WeaponCategories.SWORD: SkillNames.SWORD, WeaponCategories.BOW: SkillNames.BOW, WeaponCategories.CROSSBOW: SkillNames.CROSSBOW, WeaponCategories.STAFF: SkillNames.STAFF,
WeaponCategories.DAGGER: SkillNames.DAGGER, WeaponCategories.AXE: SkillNames.AXE}