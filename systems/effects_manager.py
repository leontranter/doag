def add_effect(effect, entity):
	try:
		# If there is already the same effect on the target, don't add a new one, just increase the duration on the current one - makes life much easier
		for current_effect in entity.effects.effect_list:
			if current_effect.get("name") == effect.get("name"):
				if current_effect.get("turns_left") and effect.get("turns_left"):
					current_effect["turns_left"] += effect["turns_left"]
			else:
				entity.effects.effect_list.append(effect)
		return True
	except:
		return False