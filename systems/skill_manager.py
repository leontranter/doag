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

from systems import skill_manager

# a list of all the skills in the game
# the key is the skill name, value is a tuple containing the base skill lookup function, and the default penalty if you don't have the skill at rank 1

skill_check_lookups = {
	'sword': (skill_manager.get_agility, 4),
	'shield': (skill_manager.get_agility, 3),
	'dagger': (skill_manager.get_agility, 2),
	'bow': (skill_manager.get_precision, 4),
	'alchemy': (skill_manager.get_intellect, 8)
}