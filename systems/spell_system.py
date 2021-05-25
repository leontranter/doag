from magic_functions import make_fireball_spell, make_bless_spell, make_heal_spell, make_firebolt_spell
from game_messages import Message
from random_utils import d6_dice_roll
from systems.move_system import distance

def learn_spell(entity, spell_name):
	results = []
	spell = spell_function_lookup[spell_name]()
	entity.caster.spells.append(spell)
	results.append({'message': Message("You learned the {spell_name} spell.")})
	results.append({'consumed': True})
	return results

def cast(entity, spell, **kwargs):
	results = []

	if spell.mana_cost > entity.caster.mana:
		results.append({'message': Message("You don't have enough mana to cast that spell.")})
		return results

	if not attempt_cast(entity, spell):
		results.append({'message': Message("You fail to cast the spell properly!")})
		results.append({'failed_cast': True})
		entity.caster.mana -= spell.mana_cost
		return results

	if not spell.targeting:
		target = None
	# so spell needs target coordinates - check if we already have one
	elif not (kwargs.get('target_x') or kwargs.get('target_y')):
		results.append({'spell_targeting': spell})
		return results
	else:
		# we have coordinates, so get a valid target entity in range - assume if it is a fighter, it is a target 
		spell_range = kwargs.get('spell_range') or 5 # TODO - pretty random... and should be a constant, not a magic number
		target_x, target_y = kwargs.get('target_x'), kwargs.get('target_y')
		if distance(entity, target_x, target_y) > spell_range:
			results.append({'message': Message("That target is out of range.")})
			return results
		entities = kwargs.get('entities')
		fov_map = kwargs.get('fov_map')
		target = get_spell_target(entity, target_x, target_y, entities, fov_map)
		if not target:
			results.append({'message': Message("There is no valid target there.")})
			return results
	kwargs = {**spell.function_kwargs, **kwargs}
	entity.caster.mana -= spell.mana_cost
	results.extend(spell.use_function(entity, target, **kwargs))
	results.append({'cast': spell.name})
	return results

def get_spell_target(caster, target_x, target_y, entities, fov_map):
	for entity in entities:
		if entity.x == target_x and entity.y == target_y and entity.fighter:
			return entity
	else:
		return None

def attempt_cast(entity, spell):
	if entity.skills:
		skill_check = entity.skills.get_skill_check(spell.spell_skill)
	else:
		skill_check = 3
	number_rolled = d6_dice_roll(3, 0)
	return number_rolled <= skill_check

spell_function_lookup = {
	'fireball': make_fireball_spell,
	'bless': make_bless_spell,
	'heal': make_heal_spell,
	'firebolt': make_firebolt_spell
}