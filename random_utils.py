from random import randint

def random_choice_index(chances):
	random_chance = randint(1, sum(chances))

	running_sum = 0
	choice = 0
	for w in chances:
		running_sum += w

		if random_chance <= running_sum:
			return choice
		choice += 1

def random_choice_from_dict(choice_dict):
	choices = list(choice_dict.keys())
	chances = list(choice_dict.values())

	return choices[random_choice_index(chances)]

def from_dungeon_level(table, dungeon_level):
	for (value, level) in reversed(table):
		if dungeon_level >= level:
			return value

	return 0

def d6_dice_roll(number_of_dice, modifier=0):
	roll = 0
	for _ in range(number_of_dice):
		this_roll = randint(1, 6)
		roll += this_roll
	roll += modifier
	return roll

def dn_dice_roll(number_of_dice, dice_type, modifier=0):
	roll = 0
	for _ in range(number_of_dice):
		this_roll = randint(1, dice_type)
		roll += this_roll
	roll += modifier
	return roll
