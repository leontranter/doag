import tcod as libtcod
from game_messages import Message
from components.ai import ConfusedMonster
from systems.effects_manager import add_effect, EffectNames
from systems.move_system import distance
from systems.skill_manager import SkillNames
from spells import Spell
from components.effects import Effect
from random_utils import dn_dice_roll

def make_fireball_spell():
	spell = Spell("Fireball", 10, SkillNames.FIRE, cast_fireball, targeting=True, targeting_message=Message('Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan), damage=30, radius=3)
	return spell

def make_heal_spell():
	spell = Spell("Heal", 5, SkillNames.HOLY, heal, targeting=None, targeting_message=None, amount=10)
	return spell

def make_bless_spell():
	spell = Spell("Bless", 4, SkillNames.HOLY, bless, targeting=True, targeting_message=Message('Left-click a target to cast Bless on, or right-click to cancel.', libtcod.light_cyan), bonus=1)
	return spell

def make_lightning_bolt_spell():
	spell = Spell("Lightning Bolt", 5, SkillNames.STORM, bolt_spell, targeting=True, targeting_message=Message('Left-click a target to cast Lightning Bolt on, or right-click to cancel.', libtcod.light_cyan), damage_dice=(3,6))
	return spell

def make_firebolt_spell():
	spell = Spell("Fire Bolt", 3, SkillNames.FIRE, bolt_spell, targeting=True, targeting_message=Message('Left-click a target to cast Fire Bolt on, or right-click to cancel.', libtcod.light_cyan), damage_dice=(3,8))
	return spell	

def heal(*args, **kwargs):
	entity = args[0]
	amount = kwargs.get('amount')

	results = []
	# TODO: this needs work - healing someone else will incorrectly show a message about you
	if entity.stats and entity.fighter:
		if entity.stats.hp == entity.stats.max_hp:
			results.append({'consumed': False, 'message': Message('You are already at full health.', libtcod.yellow)})
		else:
			entity.fighter.heal(amount)
			results.append({'consumed': True, 'message': Message('Your wounds start to feel better!', libtcod.green)})	
	else:
		results.append({'message': Message('The potion does nothing...')})
	return results

def poison(*args, **kwargs):
	entity = args[0]
	amount = kwargs.get('amount')

	results = []
	poison_effect = Effect(name=EffectNames.POISON, description="Poisoned", turns_left=5, damage_per_turn=amount)
	add_effect(poison_effect, entity)
	results.append({'consumed': True, 'message': Message('You drink a potion of poison! You feel terrible!', libtcod.green)})
	return results

def bolt_spell(*args, **kwargs):
	entities = kwargs.get('entities')
	fov_map = kwargs.get('fov_map')
	damage = kwargs.get('damage')
	target_x, target_y = kwargs.get('target_x'), kwargs.get('target_y')
	damage_dice_num, damage_dice_type = kwargs.get('damage_dice')
	results = []

	if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
		results.append({'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
		return results

	for entity in entities:
		if entity.x == target_x and entity.y == target_y and entity.fighter:
			damage = dn_dice_roll(damage_dice_num, damage_dice_type)
			results.append({'message': Message(f'{entity.name.subject_name} is hit for {damage}.')})
			results.extend(entity.fighter.take_damage(damage))
	return results

def bless(*args, **kwargs):
	caster, target = args[0], args[1]
	bonus = kwargs.get('bonus')
	duration = (caster.skills.get_skill_rank(SkillNames.HOLY) * 3) + 1
	results = []
	bless_effect = Effect(name=EffectNames.BLESS, description="Blessed", turns_left=duration, hit_modifier=bonus, physical_damage_modifier=bonus)
	add_effect(bless_effect, target)
	results.append({'consumed': True, 'message': Message('You cast bless on the target.', libtcod.green)})
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
			quantity = "point" if damage == 1 else "points"
			verb = "get" if entity.name.true_name == "Player" else "gets"
			results.append({'message': Message(f'{entity.name.subject_name} {verb} burned for {damage} {quantity}.', libtcod.orange)})
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
		if entity.x == target_x and entity.y == target_y and entity.fighter:
			effect = Effect(name=EffectNames.CONFUSION, description="Confused", turns_left=5)
			add_effect(effect, entity)
			results.append({'consumed': True, 'message': Message('The {} becomes confused!'.format(entity.name.true_name), libtcod.light_green)})
			break
	else:
		results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.', libtcod.yellow)})
	return results

def apply_confuse(*args, **kwargs):
	results = []
	entity=args[0]
	effect = Effect(name=EffectNames.CONFUSION, description="Confused", turns_left=15)
	add_effect(effect, entity)
	results.append({'consumed': True, 'message': Message('You drink a potion of confusion! You feel confused!', libtcod.green)})
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
	'heal': make_heal_spell,
	'firebolt': make_firebolt_spell
}