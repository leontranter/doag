from loader_functions.constants import WeaponTypes

def get_weapon_skill_for_attack(attacker, weapon):
	if attacker.skills:
		weapon_skill = weapon_skill_lookup(weapon)
		weapon_skill_num = attacker.skills.getSkill(weapon_skill)
		return weapon_skill_num
	elif attacker.stats:
		return attacker.stats.DX - 5
	else:
		return 5

def weapon_skill_lookup(weapon):
	return weapon_skill_matches.get(weapon.weapon_type)

weapon_skill_matches = {WeaponTypes.SWORD: "sword", WeaponTypes.BOW: "bow", WeaponTypes.CROSSBOW: "crossbow", WeaponTypes.STAFF: "staff", WeaponTypes.DAGGER: "dagger", WeaponTypes.POLEARM: "polearm", WeaponTypes.AXE: "axe"}
#weapon_skill_matches = {WeaponTypes.SWORD: "sword"}