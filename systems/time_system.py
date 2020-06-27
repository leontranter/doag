from systems import effects_manager

def process_entity_turn(entity):
	results = []
	results.extend(effects_manager.process_damage_over_time(entity))
	effects_manager.tick_down_effects(entity)
	return results