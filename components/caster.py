import tcod as libtcod
from game_messages import Message
from spells import SpellFactory
from item_functions import cast_fireball, heal

class Caster:
	def __init__(self, spells=[], max_mana=0):
		self.spells = spells
		self.max_mana = max_mana
		self.mana = max_mana

	def learn_fireball_spell(self):
		spell = SpellFactory.make_fireball_spell()
		self.spells.append(spell)

	def learn_heal_spell(self):
		spell = SpellFactory.make_heal_spell()
		self.spells.append(spell)

	def learn_bless_spell(self):
		spell = SpellFactory.make_bless_spell()
		self.spells.append(spell)

	# TODO: do we need this?
	#def removeSpell(self, spell):
		#pass

	def cast(self, spell, **kwargs):
		results = []

		if spell.mana_cost > self.mana:
			results.append({'not_cast': spell.name})
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
