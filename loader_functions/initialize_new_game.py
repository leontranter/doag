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

def get_game_variables(constants, start_equipped=False):
	# create the player character
	fighter_component = Fighter()
	inventory_component = Inventory(26)
	level_component = Level()
	equipment_component = Equipment()
	defender_component = Defender()
	stats_component = Stats(ST=12, DX=12, IQ=12, HT=12)
	skills_component = Skills()
	skills_component.setSkill("sword", 14)
	skills_component.setSkill("dagger", 14)
	skills_component.setSkill("bow", 14)

	caster_component = Caster(max_mana=20)
	player = Entity(0, 0, '@', libtcod.white, "Player", blocks=True, render_order=RenderOrder.ACTOR, fighter = fighter_component, inventory=inventory_component, level=level_component, equipment=equipment_component, caster=caster_component, stats=stats_component, skills=skills_component, defender=defender_component)
	entities = [player]

	
	if start_equipped:
		x, y = 1, 1
		equippable_component = EquippableFactory.makeBow()
		item = Entity(x, y, '(', libtcod.red, 'Bow', equippable=equippable_component)
		player.inventory.items.append(item)
		equippable_component = EquippableFactory.makeArrows()
		item = Entity(x, y, '(', libtcod.red, 'Arrows', equippable=equippable_component)
		player.inventory.items.append(item)
		equippable_component = EquippableFactory.makeDagger()
		item = Entity(x, y, '(', libtcod.red, 'Dagger', equippable = equippable_component)
		player.inventory.items.append(item)
		player.equipment.main_hand = item
		equippable_component = EquippableFactory.makeLeatherArmor()
		item = Entity(x, y, '[', libtcod.red, 'Leather Armor', equippable = equippable_component)
		player.inventory.items.append(item)
		player.equipment.body = item
		equippable_component = EquippableFactory.makeZweihander()
		item = Entity(x, y, '(', libtcod.red, 'Zweihander', equippable = equippable_component)
		player.inventory.items.append(item)
		equippable_component = EquippableFactory.makeShield()
		item = Entity(x, y, '[', libtcod.darker_orange, 'Shield', equippable=equippable_component)
		player.inventory.items.append(item)

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
	dlevels = {'dlevel_1': dlevel_1, 'dlevel_2': dlevel_2, 'dlevel_3': dlevel_3, 'dlevel_4': dlevel_4, 'dlevel_5': dlevel_5, 'dlevel_6': dlevel_6}

	message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

	game_state = GameStates.PLAYERS_TURN
	return player, entities, game_map, message_log, game_state, dlevels

def assign_item_names():
	pass