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
from game_state import GameState
from magic_functions import make_firebolt_spell
from item_factory import make_healing_potion, make_poison_potion, make_fireball_book, make_confusion_scroll, make_bless_book, make_fireball_scroll, make_confusion_potion
from systems.skill_manager import SkillNames

def get_game_variables(constants, player_class=None):
	if not player_class:
		player_class = 0
	player = create_player(constants, player_class)
		
	entities = [player]
	
	game_map = GameMap(constants['map_width'], constants['map_height'])
	game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'], constants['map_height'], player, entities)
	
	# create the entities and map, save them to a Dlevel object
	max_dlevels = constants['max_dlevels']
	dlevels = populate_dlevels(entities, game_map, max_dlevels)

	message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

	game_state = GameState()
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
	performer_component = set_feats(player_class)
	stats_component = set_stats(player_class)
	skills_component = set_skills(player_class)
	caster_component = set_spells(player_class, stats_component)
	potion_description_links = assign_potion_descriptions(constants['potion_descriptions'], constants['potion_types'])
	scroll_description_links = assign_scroll_descriptions(constants['scroll_descriptions'], constants['scroll_types'])
	identified_component = Identified(potion_description_links, scroll_description_links)
	player_name = Name("Player")
	player = Entity(0, 0, '@', libtcod.white, blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, inventory=inventory_component, level=level_component,
		equipment=equipment_component, caster=caster_component, stats=stats_component, skills=skills_component, defender=defender_component, name=player_name,
		identified=identified_component, performer=performer_component)
	player = equip_player(player, player_class)
	return player

def set_stats(player_class):
	stats_mapping = {0: [16, 14, 14, 10, 10, 16, 16], 1: [15, 14, 14, 15, 15, 15, 14], 2: [12, 14, 12, 18, 16, 9, 11], 3: [13, 12, 13, 13, 16, 14, 12]}
	p_str, p_pre, p_agi, p_int, p_wil, p_sta, p_end = stats_mapping[player_class]
	player_stats = Stats(Strength=p_str, Precision=p_pre, Agility=p_agi, Intellect=p_int, Willpower=p_wil, Stamina=p_sta, Endurance=p_end)
	return player_stats

def set_spells(player_class, stats_component):
	# TODO: Fix this!!!
	caster_component = Caster(max_mana=stats_component.Willpower)
	spell_mapping = {0: [], 1: [], 2: [make_firebolt_spell], 3: []}
	for starting_spell in spell_mapping[player_class]:
		spell = starting_spell()
		caster_component.spells.append(spell)
	return caster_component

def set_skills(player_class):
	skills_component = Skills()
	skills_mapping = {0: [(SkillNames.SWORD, 2), (SkillNames.SURVIVAL, 1), (SkillNames.ATHLETICS, 1)],
						1: [(SkillNames.SWORD, 1), (SkillNames.HOLY, 1), (SkillNames.SHIELD, 1)],
						2: [(SkillNames.MATTER, 1), (SkillNames.STORM, 1), (SkillNames.FIRE, 1)],
						3: [(SkillNames.HOLY, 2), (SkillNames.MACE, 1), (SkillNames.LIGHT, 1)]}
	for character_skill in skills_mapping[player_class]:
		skill_name, skill_level = character_skill
		skills_component.set_skill_rank(skill_name, skill_level)
	return skills_component

def set_feats(player_class):
	# TODO: This could probably be reworked to dictionary lookup - not sure if it is worth it
	player_performer = Performer()
	if player_class == 0:
		feat1 = make_savage_strike()
		player_performer.feat_list.append(feat1)
		feat2 = make_standing_jump()
		player_performer.feat_list.append(feat2)
	elif player_class == 1:
		feat1 = make_standing_jump()
		player_performer.feat_list.append(feat1)
	elif player_class == 2:
		feat1 = make_savage_strike()
		player_performer.feat_list.append(feat1)
	return player_performer

def equip_player(player, player_class):
	x, y = 1, 1
	if player_class == 0:
		item = EquippableFactory.make_greatsword()
		player.inventory.items.append(item)
		player.equipment.main_hand = item
		item2 = EquippableFactory.make_dagger()
		player.inventory.items.append(item2)
		item = EquippableFactory.make_leather_armor()
		player.inventory.items.append(item)
		player.equipment.body = item
	elif player_class == 1:
		item = EquippableFactory.make_longsword()
		player.inventory.items.append(item)
		player.equipment.main_hand = item
		item = EquippableFactory.make_shield()
		player.inventory.items.append(item)
		player.equipment.off_hand = item
		item = EquippableFactory.make_chain_armor()
		player.inventory.items.append(item)
		player.equipment.body = item
	elif player_class == 2:
		item = EquippableFactory.make_dagger()
		player.inventory.items.append(item)
		player.equipment.main_hand = item
		item = EquippableFactory.make_small_shield()
		player.inventory.items.append(item)
		item = EquippableFactory.make_padded_armor()
		player.inventory.items.append(item)
		player.equipment.body = item
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