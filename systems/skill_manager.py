def get_strength(entity):
	if entity.stats:
		return entity.stats.Strength
	else:
		return 0

def get_precision(entity):
	if entity.stats:
		return entity.stats.Precision
	else:
		return 0

def get_agility(entity):
	if entity.stats:
		return entity.stats.Agility
	else:
		return 0

def get_intellect(entity):
	if entity.stats:
		return entity.stats.Intellect
	else:
		return 0

def get_willpower(entity):
	if entity.stats:
		return entity.stats.Willpower
	else:
		return 0

def get_stamina(entity):
	if entity.stats:
		return entity.stats.Stamina
	else:
		return 0

def get_endurance(entity):
	if entity.stats:
		return entity.stats.Endurance
	else:
		return 0