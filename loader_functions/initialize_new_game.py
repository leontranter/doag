import tcod as libtcod

from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.equipment import Equipment
from components.caster import Caster
from components.equippable import Equippable, EquippableFactory
from components.stats import Stats
from components.skills import Skills
from components.defender import Defender
from entity import Entity
from game_messages import MessageLog
from game_states import GameStates
from map_objects.game_map import GameMap
from render_functions import RenderOrder
from dlevel import Dlevel
from components.name import Name
from components.effects import Effects
from components.identified import Identified
from random import shuffle
from item_factory import make_healing_potion, make_poison_potion, make_fireball_book, make_confusion_scroll, make_bless_book
from systems.skill_manager import SkillNames

def get_game_variables(constants, start_equipped=False):
	# create the player character
	fighter_component = Fighter()
	inventory_component = Inventory(26)
	level_component = Level()
	equipment_component = Equipment()
	defender_component = Defender()
	stats_component = Stats(Strength=12, Precision=11, Agility=12, Intellect=11, Willpower=11, Stamina=12, Endurance=12)
	skills_component = Skills()
	skills_component.set_skill_rank(SkillNames.SWORD, 1)
	skills_component.set_skill_rank(SkillNames.DAGGER, 1)
	skills_component.set_skill_rank(SkillNames.BOW, 1)
	skills_component.set_skill_rank(SkillNames.HOLY, 1)
	# TODO: fix this max mana!
	caster_component = Caster(max_mana=20)
	potion_description_links = assign_potion_descriptions(constants['potion_descriptions'], constants['potion_types'])
	scroll_description_links = assign_scroll_descriptions(constants['scroll_descriptions'], constants['scroll_types'])
	identified_component = Identified(potion_description_links, scroll_description_links)
	player_name = Name("Player")
	player = Entity(0, 0, '@', libtcod.white, blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, inventory=inventory_component, level=level_component, equipment=equipment_component, caster=caster_component, stats=stats_component, skills=skills_component, defender=defender_component, name=player_name, identified=identified_component)
	entities = [player]
	
	# TODO: Refactor this to a function!!! No excuses!!!
	if start_equipped:
		x, y = 1, 1
		item = EquippableFactory.make_shortbow()
		player.inventory.items.append(item)
		#player.equipment.main_hand = item
		item = EquippableFactory.make_arrows(1, 1, 10)
		player.inventory.items.append(item)
		item2 = EquippableFactory.make_dagger()
		player.inventory.items.append(item2)
		player.equipment.main_hand = item2
		item = EquippableFactory.make_leather_armor()
		player.inventory.items.append(item)
		player.equipment.body = item
		item = EquippableFactory.make_greatsword()
		player.inventory.items.append(item)
		item = EquippableFactory.make_shield()
		player.inventory.items.append(item)
		potion1 = make_poison_potion()
		player.inventory.items.append(potion1)
		potion2 = make_poison_potion()
		player.inventory.items.append(potion2)
		book = make_bless_book()
		player.inventory.items.append(book)
		scroll = make_confusion_scroll()
		player.inventory.items.append(scroll)
		scroll2 = make_confusion_scroll()
		player.inventory.items.append(scroll2)

	
	game_map = GameMap(constants['map_width'], constants['map_height'])
	game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'], constants['map_height'], player, entities)
	
	#set the game difficulty - TODO: bring in this from a menu etc
	game_difficulty = 1
	difficulty_modifiers = {1: 2.0, 2: 1.75, 3: 1.5, 4: 1, 5: 1}
	player.stats.base_max_hp = int(player.stats.base_max_hp * difficulty_modifiers[game_difficulty])
	player.stats.hp = player.stats.base_max_hp

	# create the entities and map, save them to a Dlevel object
	dlevel_1 = Dlevel(entities, game_map.tiles, game_map.dungeon_level, True)
	dlevel_2 = Dlevel([], [], 2)
	dlevel_3 = Dlevel([], [], 3)
	dlevel_4 = Dlevel([], [], 4)
	dlevel_5 = Dlevel([], [], 5)
	dlevel_6 = Dlevel([], [], 6)
	dlevels = {1: dlevel_1, 2: dlevel_2, 3: dlevel_3, 4: dlevel_4, 5: dlevel_5, 6: dlevel_6}

	message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

	game_state = GameStates.PLAYERS_TURN
	return player, entities, game_map, message_log, game_state, dlevels

def assign_potion_descriptions(potion_descriptions, potion_types):	
	potion_description_links = {}
	
	# Shuffle the descriptions, so we can then randomly assign a description to a type and then return the dictionary that maps them
	shuffle(potion_descriptions)
	
	for i in range(len(potion_descriptions)):
		potion_description_links[potion_types[i]] = potion_descriptions[i]

	return potion_description_links

def assign_scroll_descriptions(scroll_descriptions, scroll_types):	
	scroll_description_links = {}
	
	# Shuffle the descriptions, so we can then randomly assign a description to a type and then return the dictionary that maps them
	shuffle(scroll_descriptions)
	
	for i in range(len(scroll_descriptions)):
		scroll_description_links[scroll_types[i]] = scroll_descriptions[i]

	return scroll_description_links