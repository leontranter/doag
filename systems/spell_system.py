from item_functions import make_fireball_spell, make_bless_spell, make_heal_spell
from game_messages import Message

def learn_spell(entity, spell_name):
	results = []
	spell = spell_function_lookup[spell_name]()
	entity.caster.spells.append(spell)
	results.append({'message': Message("You learned the {spell_name} spell.")})
	results.append({'consumed': True})
	return results

spell_function_lookup = {
	'fireball': make_fireball_spell,
	'bless': make_bless_spell,
	'heal': make_heal_spell
}