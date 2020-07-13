from enum import Enum, auto

class SkillNames(Enum):
	SWORD = auto()
	SHIELD = auto()
	DAGGER = auto()
	AXE = auto()
	MACE = auto()
	STAFF = auto()
	BOW = auto()
	CROSSBOW = auto()
	ALCHEMY = auto()
	HOLY = auto()

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
	SkillNames.SWORD: (get_agility, 4),
	SkillNames.SHIELD: (get_agility, 3),
	SkillNames.DAGGER: (get_agility, 2),
	SkillNames.BOW: (get_precision, 4),
	SkillNames.CROSSBOW: (get_precision, 3),
	SkillNames.AXE: (get_precision, 4),
	SkillNames.STAFF: (get_agility, 4),
	SkillNames.ALCHEMY: (get_intellect, 8),
	SkillNames.HOLY: (get_willpower, 8)
}

