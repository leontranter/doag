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
		spell = SpellFactory("Fireball", 10, cast_fireball, targeting=True, targeting_message="Choose a target for your fireball...", damage=30, radius=3)
		self.spells.append(spell)

	def learnHealSpell(self):
		spell = SpellFactory("Heal", 5, heal, amount=10)
		self.spells.append(spell)
	# TODO: do we need this?
	#def removeSpell(self, spell):
		#pass

	def cast(self, spell_entity, **kwargs):
		results = []
		
		spell_component = spell_entity

		print(spell_component.__dict__)
		if spell_component.mana_cost > self.mana:
			print("cost: {}, self mana: {}".format(spell_component.mana_cost, self.mana))
			results.append({'not_cast': spell_component.name})
			return results

		if spell_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
			results.append({'spell_targeting': spell_entity})
		else:
			kwargs = {**spell_component.function_kwargs, **kwargs}
			self.mana -= spell_component.mana_cost
			spell_cast_results = spell_component.use_function(self.owner, **kwargs)

			results.extend(spell_cast_results)
		results.append({'cast': spell_component.name})
		return results

class SpellFactory:
	def __init__(self, spell_name, mana_cost, use_function=None, targeting=False, targeting_message=None, **kwargs):
		self.name = spell_name
		self.use_function = use_function
		self.mana_cost = mana_cost
		self.targeting = targeting
		self.targeting_message = targeting_message
		self.function_kwargs = kwargs
