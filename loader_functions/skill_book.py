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