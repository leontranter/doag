from item_functions import make_fireball_spell, make_bless_spell, make_heal_spell
from game_messages import Message
from random_utils import d6_dice_roll

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
		entity.caster.mana -= spell.mana_cost
		return results

	if spell.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
		results.append({'spell_targeting': spell})
	else:
		kwargs = {**spell.function_kwargs, **kwargs}
		entity.caster.mana -= spell.mana_cost
		spell_cast_results = spell.use_function(entity, **kwargs)

		results.extend(spell_cast_results)
		results.append({'cast': spell.name})
	return results

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
	'heal': make_heal_spell
}