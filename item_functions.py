import tcod as libtcod
from game_messages import Message
from components.ai import ConfusedMonster
from systems.effects_manager import add_effect
from systems.move_system import distance
from spells import Spell

def make_fireball_spell():
	spell = Spell("Fireball", 10, cast_fireball, targeting=True, targeting_message=Message('Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan), damage=30, radius=3)
	return spell

def make_heal_spell():
	spell = Spell("Heal", 5, heal, amount=10)
	return spell

def make_bless_spell():
	spell = Spell("Bless", 4, bless, targeting=True, targeting_message=Message('Left-click a target to cast Bless on, or right-click to cancel.', libtcod.light_cyan), bonus=1)
	return spell

def heal(*args, **kwargs):
	entity = args[0]
	amount = kwargs.get('amount')

	results = []

	if entity.stats and entity.fighter:
		if entity.stats.hp == entity.stats.max_hp:
			results.append({'consumed': False, 'message': Message('You are already at full health.', libtcod.yellow)})
		else:
			entity.fighter.heal(amount)
			results.append({'consumed': True, 'message': Message('Your wounds start to feel better!', libtcod.green)})	
	else:
		results.append({'message': Message('The potion does nothing...')})
	return results

#TODO: needs to be completely reworked
def poison(*args, **kwargs):
	entity = args[0]
	amount = kwargs.get('amount')

	results = []
	poison_effect = {'name': "Poison", "turns_left": 5, "damage_per_turn": 3}
	add_effect(poison_effect, entity)
	results.append({'consumed': True, 'message': Message('You drink a potion of poison! You feel terrible!', libtcod.green)})
	return results

def bless(*args, **kwargs):
	entities = kwargs.get('entities')
	fov_map = kwargs.get('fov_map')
	target_x = kwargs.get('target_x')
	target_y = kwargs.get('target_y')
	target_self = kwargs.get('target_self')
	bonus = kwargs.get('bonus')
	
	results = []
	bless_effect = {'name': "Bless", "turns_left": 7, "hit_modifier": bonus, "physical_damage_modifier": bonus}
	for entity in entities:
		if entity.x == target_x and entity.y == target_y and entity.fighter:
			add_effect(bless_effect, entity)
			results.append({'consumed': True, 'message': Message('You cast bless on the target.', libtcod.green)})
			break
	else:
		results.append({'message': Message("There is no target there to cast that spell on.", libtcod.red)})
	return results

def cast_lightning(*args, **kwargs):
	caster = args[0]
	entities = kwargs.get('entities')
	fov_map = kwargs.get('fov_map')
	damage = kwargs.get('damage')
	maximum_range = kwargs.get('maximum_range')

	results = []

	target = None
	closest_distance = maximum_range + 1

	for entity in entities:
		if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
			distance = caster.distance_to(entity)
		
			if distance < closest_distance:
				target = entity
				closest_distance = distance

	if target:
		results.append({'consumed': True, 'target': target, 'message': Message('A lightning strikes the {0} with a loud thunder! The damage is {1}'.format(target.name, damage))})
		results.extend(target.fighter.take_damage(damage))
	else:
		results.append({'consumed': False, 'target': None, 'message': Message('No enemy is close enough to strike.', libtcod.red)})
	return results

def cast_fireball(*args, **kwargs):
	entities = kwargs.get('entities')
	fov_map = kwargs.get('fov_map')
	damage = kwargs.get('damage')
	radius = kwargs.get('radius')
	target_x = kwargs.get('target_x')
	target_y = kwargs.get('target_y')

	results = []

	if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
		results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
		return results
	results.append({'consumed': True, 'message': Message('The fireball explodes, burning everything within {0} tiles!'.format(radius), libtcod.orange)})

	for entity in entities:
		if distance(entity, target_x, target_y) <= radius and entity.fighter:
			results.append({'message': Message('The {0} gets burned for {1} points.'.format(entity.name.true_name, damage), libtcod.orange)})
			results.extend(entity.fighter.take_damage(damage))
	return results

# TODO: needs to be completely reworked
def cast_confuse(*args, **kwargs):
	entities = kwargs.get('entities')
	fov_map = kwargs.get('fov_map')
	target_x = kwargs.get('target_x')
	target_y = kwargs.get('target_y')
	target_self = kwargs.get('target_self')
	results = []

	# TODO: Fix this! probably need to split out into cast confuse and resolve confuse functions
	if target_self:
		results.append({'consumed': True, 'message': Message("You are confused!", libtcod.yellow)})
		return results

	if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
		results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
		return results

	for entity in entities:
		if entity.x == target_x and entity.y == target_y and entity.ai:
			confused_ai = ConfusedMonster(entity.ai, 10)
			confused_ai.owner = entity
			entity.ai = confused_ai

			results.append({'consumed': True, 'message': Message('The {} becomes confused!'.format(entity.name.true_name), libtcod.light_green)})

			break
	else:
		results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.', libtcod.yellow)})

	return results

def learn_spell_from_book(*args, **kwargs):
	results = []
	entity = args[0]
	spell_name = kwargs.get('spell_name')
	spell = spell_function_lookup[spell_name]()
	entity.caster.spells.append(spell)
	results.append({'message': Message(f"You learned the {spell_name} spell.")})
	results.append({'consumed': True})
	return results

spell_function_lookup = {
	'fireball': make_fireball_spell,
	'bless': make_bless_spell,
	'heal': make_heal_spell
}

