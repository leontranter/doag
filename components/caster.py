import tcod as libtcod
from game_messages import Message
from spells import SpellFactory
from item_functions import cast_fireball, heal


class Caster:
	def __init__(self, spells=[], max_mana=0):
		self.spells = spells
		self.max_mana = max_mana
		self.mana = max_mana

	def cast(self, spell, **kwargs):
		results = []

		if spell.mana_cost > self.mana:
			results.append({'message': Message("You don't have enough mana to cast that spell.")})
			return results

		if spell.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
			results.append({'spell_targeting': spell})
		else:
			kwargs = {**spell.function_kwargs, **kwargs}
			self.mana -= spell.mana_cost
			spell_cast_results = spell.use_function(self.owner, **kwargs)

			results.extend(spell_cast_results)
			results.append({'cast': spell.name})
		return results

def learn_fireball_spell(entity, **kwargs):
	results = []
	spell = SpellFactory.make_fireball_spell()
	entity.caster.spells.append(spell)
	results.append({'message': Message("You learned the Fireball spell.")})
	results.append({'consumed': True})
	return results

def learn_heal_spell(entity, **kwargs):
	results = []
	spell = SpellFactory.make_heal_spell()
	entity.caster.spells.append(spell)
	results.append({'message': Message("You learned the Heal spell.")})
	results.append({'consumed': True})
	return results

def learn_bless_spell(entity, **kwargs):
	results = []
	spell = SpellFactory.make_bless_spell()
	entity.caster.spells.append(spell)
	results.append({'message': Message("You learned the Bless spell.")})
	results.append({'consumed': True})
	return results

def learn_spell(entity, spell_name):
	results = []
	spell = spell_function_lookup[spell_name]()
	entity.caster.spells.append(spell)
	results.append({'message': Message("You learned the {spell_name} spell.")})
	results.append({'consumed': True})
	return results

spell_function_lookup = {
	'fireball': SpellFactory.make_fireball_spell,
	'bless': SpellFactory.make_bless_spell,
	'heal': SpellFactory.make_heal_spell
}