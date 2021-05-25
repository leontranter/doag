from systems import effects_manager

def process_entity_turn(entity):
	results = []
	results.extend(effects_manager.process_damage_over_time(entity))
	effects_manager.tick_down_effects(entity)	
	# TODO: move this somewhere else? Maybe in engine?? e.g. we shouldn't do this if time effects have just killed someone... 
	# TODO: change the regen from hardcoded to something else, probably based on stamina?
	regen_hp(entity, 0.2)
	regen_mana(entity, 0.2)
	return results

def regen_hp(entity, amount):
	if entity.fighter:
		entity.fighter.hp_regen_counter += amount
		if entity.fighter.hp_regen_counter >= 1:
			entity.fighter.hp_regen_counter -= 1
			entity.fighter.heal(1)

def regen_mana(entity, amount):
	if entity.caster:
		entity.caster.mana_regen_counter += amount
		if entity.caster.mana_regen_counter >= 1:
			entity.caster.mana_regen_counter -= 1
			entity.caster.restore_mana(1)		