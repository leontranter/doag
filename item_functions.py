import tcod as libtcod
from game_messages import Message
from components.ai import ConfusedMonster

def heal(*args, **kwargs):
	entity = args[0]
	amount = kwargs.get('amount')

	results = []

	if entity.stats.hp == entity.stats.max_hp:
		results.append({'consumed': False, 'message': Message('You are already at full health.', libtcod.yellow)})
	else:
		entity.fighter.heal(amount)
		results.append({'consumed': True, 'message': Message('Your wounds start to feel better!', libtcod.green)})
	
	return results

def poison(*args, **kwargs):
	entity = args[0]
	amount = kwargs.get('amount')

	results = []
	entity.fighter.take_damage(amount)
	results.append({'consumed': True, 'message': Message('You drink a potion of poison! You feel terrible!', libtcod.green)})
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
		if entity.distance(target_x, target_y) <= radius and entity.fighter:
			results.append({'message': Message('The {0} gets burned for {1} points.'.format(entity.name, damage), libtcod.orange)})
			results.extend(entity.fighter.take_damage(damage))
	return results
def cast_confuse(*args, **kwargs):
	entities = kwargs.get('entities')
	fov_map = kwargs.get('fov_map')
	target_x = kwargs.get('target_x')
	target_y = kwargs.get('target_y')

	results = []

	if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
		results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
		return results

	for entity in entities:
		if entity.x == target_x and entity.y == target_y and entity.ai:
			confused_ai = ConfusedMonster(entity.ai, 10)
			confused_ai.owner = entity
			entity.ai = confused_ai

			results.append({'consumed': True, 'message': Message('The {} becomes confused!'.format(entity.name), libtcod.light_green)})

			break
	else:
		results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.', libtcod.yellow)})

	return results

def learn_fireball(*args, **kwargs):
	entity = args[0]
	results = []
	for spell in entity.caster.spells:
		if spell.name == "Fireball":
			results.append({'consumed': False, 'message': Message("You already know that spell.", libtcod.light_green)})
			break
	else:
		entity.caster.learnFireballSpell()
		results.append({'consumed': True, 'message': Message('You learned the Fireball spell!', libtcod.light_green)})
	return results

def learn_heal(*args, **kwargs):
	entity = args[0]
	results = []
	for spell in entity.caster.spells:
		if spell.name == "Heal":
			results.append({'consumed': False, 'message': Message("You already know that spell.", libtcod.light_green)})
			break
	else:
		entity.caster.learnHealSpell()
		results.append({'consumed': True, 'message': Message('You learned the Heal spell!', libtcod.light_green)})
	return results