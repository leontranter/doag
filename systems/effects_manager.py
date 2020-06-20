def add_effect(effect, entity):
		# If there is already the same effect on the target, don't add a new one, just increase the duration on the current one - makes life much easier
	for current_effect in entity.effects.effect_list:
		if current_effect.get("name") == effect.get("name"):
			if current_effect.get("turns_left") and effect.get("turns_left"):
				current_effect["turns_left"] += effect["turns_left"]
				return "extended"
	else:
		entity.effects.effect_list.append(effect)
		return "appended"

def get_effects_names(entity):
	list_of_effects = []
	for effect in entity.effects.effect_list:
		list_of_effects.append(effect.get("name"))

def process_damage_over_time(entity):
	for currect_effect in entity.effects.effect_list:
		if current_effect.get("damage_over_time") and entity.fighter:
			entity.fighter.take_damage(current_effect.get("damage_over_time"))

def tick_down_effects(entity):
	for i in range(len(entity.effects.effect_list)-1, -1, -1):
		entity.effects.effect_list[i]["turns_left"] -= 1
		if entity.effects.effect_list[i].get("turns_left") < 1:
			del(entity.effects.effect_list[i])