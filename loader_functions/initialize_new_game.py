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
from components.performer import Performer
from systems.feat_system import make_savage_strike, make_standing_jump
from entity import Entity
from game_messages import MessageLog
from game_states import GameStates
from map_objects.game_map import GameMap
from render_functions import RenderOrder
from dlevel import Dlevel
from components.name import Name
from components.identified import Identified
from random import shuffle
from magic_functions import make_firebolt_spell
from item_factory import make_healing_potion, make_poison_potion, make_fireball_book, make_confusion_scroll, make_bless_book, make_fireball_scroll, make_confusion_potion
from systems.skill_manager import SkillNames

def get_game_variables(constants, player_class, start_equipped=False):
	player = create_player(constants, player_class)
	if start_equipped:
		player = equip_player(player)
	
	entities = [player]
	
	game_map = GameMap(constants['map_width'], constants['map_height'])
	game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'], constants['map_height'], player, entities)
	
	# create the entities and map, save them to a Dlevel object
	max_dlevels = constants['max_dlevels']
	dlevels = populate_dlevels(entities, game_map, max_dlevels)

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

def create_player(constants, player_class):
	fighter_component = Fighter()
	inventory_component = Inventory(26)
	level_component = Level()
	equipment_component = Equipment()
	defender_component = Defender()
	performer_component = Performer()
	stats_component = set_stats(player_class)
	skills_component = Skills()
	skills_component.set_skill_rank(SkillNames.SWORD, 1)
	skills_component.set_skill_rank(SkillNames.DAGGER, 1)
	skills_component.set_skill_rank(SkillNames.BOW, 1)
	skills_component.set_skill_rank(SkillNames.HOLY, 1)
	feat = make_savage_strike()
	feat2 = make_standing_jump()
	spell = make_firebolt_spell()
	caster_component = Caster(max_mana=stats_component.Willpower)
	potion_description_links = assign_potion_descriptions(constants['potion_descriptions'], constants['potion_types'])
	scroll_description_links = assign_scroll_descriptions(constants['scroll_descriptions'], constants['scroll_types'])
	identified_component = Identified(potion_description_links, scroll_description_links)
	player_name = Name("Player")
	player = Entity(0, 0, '@', libtcod.white, blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, inventory=inventory_component, level=level_component,
		equipment=equipment_component, caster=caster_component, stats=stats_component, skills=skills_component, defender=defender_component, name=player_name,
		identified=identified_component, performer=performer_component)
	player.performer.feat_list.extend([feat, feat2])
	player.caster.spells.append(spell)
	return player

def set_stats(player_class):
	if player_class['character_class'] == 0: #barbarian
		player_stats = Stats(Strength=16, Precision=14, Agility=14, Intellect=10, Willpower=10, Stamina=16, Endurance=16)
	elif player_class['character_class'] == 1: # paladin
		player_stats = Stats(Strength=15, Precision=14, Agility=14, Intellect=15, Willpower=15, Stamina=15, Endurance=14)
	else: #wizard
		player_stats = Stats(Strength=12, Precision=14, Agility=14, Intellect=18, Willpower=16, Stamina=9, Endurance=11)
	return player_stats


def equip_player(player):
	x, y = 1, 1
	item = EquippableFactory.make_shortbow()
	player.inventory.items.append(item)
	item = EquippableFactory.make_arrows(x, y, 10)
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
	scroll = make_fireball_scroll()
	player.inventory.items.append(scroll)
	potion = make_confusion_potion()
	player.inventory.items.append(potion)
	return player

def populate_dlevels(entities, game_map, max_dlevel):
	dlevels = {}
	dlevel_1 = Dlevel(entities, game_map.tiles, game_map.dungeon_level, True)
	dlevels[1] = dlevel_1
	for i in range(2, max_dlevel+1):
		dlevels[i] = Dlevel([], [], i)
	
	return dlevels