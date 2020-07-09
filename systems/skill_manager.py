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

# a list of all the skills in the game
# the key is the skill name, value is a tuple containing the base skill lookup function, and the default penalty if you don't have the skill at rank 1

skill_check_lookups = {
	'sword': (get_agility, 4),
	'shield': (get_agility, 3),
	'dagger': (get_agility, 2),
	'bow': (get_precision, 4),
	'alchemy': (get_intellect, 8),
	'holy': (get_willpower, 8)
}