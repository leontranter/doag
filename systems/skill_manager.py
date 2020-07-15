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
	FIRE = auto()

def get_strength(entity):
	if entity.stats:
		return entity.stats.Strength or 0

def get_precision(entity):
	if entity.stats:
		return entity.stats.Precision or 0

def get_agility(entity):
	if entity.stats:
		return entity.stats.Agility or 0

def get_intellect(entity):
	if entity.stats:
		return entity.stats.Intellect or 0

def get_willpower(entity):
	if entity.stats:
		return entity.stats.Willpower or 0

def get_stamina(entity):
	if entity.stats:
		return entity.stats.Stamina or 0

def get_endurance(entity):
	if entity.stats:
		return entity.stats.Endurance or 0


# how to find a skill check number
# the key is the skill name, value is a tuple containing the two lookup functions (which you then take the average of), and the default penalty if you don't have the skill at rank 1

skill_check_lookups = {
	SkillNames.SWORD: (get_strength, get_precision, 4),
	SkillNames.SHIELD: (get_agility, get_strength, 3),
	SkillNames.DAGGER: (get_precision, get_agility, 2),
	SkillNames.BOW: (get_precision, get_precision, 4),
	SkillNames.CROSSBOW: (get_precision, get_precision, 3),
	SkillNames.AXE: (get_strength, get_agility, 4),
	SkillNames.MACE: (get_agility, get_strength, 4),
	SkillNames.STAFF: (get_agility, get_agility, 4),
	SkillNames.ALCHEMY: (get_intellect, get_intellect, 7),
	SkillNames.HOLY: (get_willpower, get_intellect, 8),
	SkillNames.FIRE: (get_intellect, get_willpower, 8)
}