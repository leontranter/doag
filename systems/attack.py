from loader_functions.constants import WeaponTypes, WeaponCategories
from systems.skill_manager import SkillNames

def get_hit_modifier_from_status_effects(entity):
	modifier = 0
	for effect in entity.fighter.effect_list:
		modifier += effect.get("hit_modifier") or 0
	return modifier

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

def get_weapon_skill_for_attack(attacker, weapon):
	if attacker.skills:
		weapon_skill = weapon_skill_lookup(weapon)
		weapon_skill_num = attacker.skills.get_skill_check(weapon_skill)
		return weapon_skill_num
	elif attacker.stats:
		return attacker.stats.DX - 5
	else:
		return 5

def weapon_skill_lookup(weapon):
	return weapon_skill_matches.get(weapon.melee_weapon.weapon_category)

weapon_skill_matches = {WeaponCategories.SWORD: SkillNames.SWORD, WeaponCategories.BOW: SkillNames.BOW, WeaponCategories.CROSSBOW: SkillNames.CROSSBOW, WeaponCategories.STAFF: SkillNames.STAFF,
WeaponCategories.DAGGER: SkillNames.DAGGER, WeaponCategories.AXE: SkillNames.AXE}