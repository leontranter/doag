import tcod as libtcod
from game_messages import Message
from spells import Spell
from item_functions import cast_fireball, heal

class Caster:
	def __init__(self, spells=[], max_mana=0):
		self.spells = spells
		self.max_mana = max_mana
		self.mana = max_mana

	def learnFireballSpell(self):
		spell = SpellFactory("Fireball", 10, cast_fireball, targeting=True, targeting_message=Message('Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan), damage=30, radius=3)
		self.spells.append(spell)

	def learnHealSpell(self):
		spell = SpellFactory("Heal", 5, heal, amount=10)
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

class SpellFactory:
	def __init__(self, spell_name, mana_cost, use_function=None, targeting=False, targeting_message=None, **kwargs):
		self.name = spell_name
		self.use_function = use_function
		self.mana_cost = mana_cost
		self.targeting = targeting
		self.targeting_message = targeting_message
		self.function_kwargs = kwargs
