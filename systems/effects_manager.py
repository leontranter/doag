def add_effect(effect, entity):
		# If there is already the same effect on the target, don't add a new one, just increase the duration on the current one - makes life much easier
	if entity.fighter:
		for current_effect in entity.fighter.effect_list:
			if current_effect.get("name") == effect.get("name"):
				if current_effect.get("turns_left") and effect.get("turns_left"):
					current_effect["turns_left"] += effect["turns_left"]
					return "extended"
		else:
			entity.fighter.effect_list.append(effect)
			return "appended"

def get_effects_names(entity):
	list_of_effects = []
	for effect in entity.fighter.effect_list:
		list_of_effects.append(effect.get("name"))
	return list_of_effects

def process_damage_over_time(entity):
	results = []
	for effect in entity.fighter.effect_list:
		if effect.get("damage_per_turn") and entity.fighter:
			results.extend(entity.fighter.take_damage(effect.get("damage_per_turn")))
	return results

def tick_down_effects(entity):
	for i in range(len(entity.fighter.effect_list)-1, -1, -1):
		entity.fighter.effect_list[i]["turns_left"] -= 1
		if entity.fighter.effect_list[i].get("turns_left") < 1:
			del(entity.fighter.effect_list[i])