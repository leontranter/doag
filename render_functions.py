import tcod as libtcod
from enum import Enum
from game_states import GameStates
from menus import inventory_menu, level_up_menu, character_screen, spells_menu, potion_menu, equipment_menu, feats_menu
from systems.name_system import get_display_name
from loader_functions.tile_codes import *
from game_states import GameStates

class RenderOrder(Enum):
	STAIRS = 1
	CORPSE = 2
	ITEM = 3
	ACTOR = 4

def get_names_under_mouse(mouse, entities, fov_map, player):
	(x, y) = (mouse.cx, mouse.cy)	
	names = [get_display_name(player, entity) for entity in entities if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
	names = ', '.join(names)
	return names.capitalize()

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
	bar_width = int(float(value) / maximum * total_width)
	
	libtcod.console_set_default_background(panel, back_color)
	libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

	libtcod.console_set_default_background(panel, bar_color)
	if bar_width > 0:
		libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

	libtcod.console_set_default_foreground(panel, libtcod.white)
	libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER, '{0}: {1}/{2}'.format(name, value, maximum))


def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, bar_width, panel_height, panel_y, mouse, colors, game_state):
	if True:
		for y in range(game_map.height):
			for x in range(game_map.width):
				visible = libtcod.map_is_in_fov(fov_map, x, y)
				wall = game_map.tiles[x][y].block_sight

				if visible:
					if wall:
						#libtcod.console_set_char_background(con, x, y, colors.get('light_wall'), libtcod.BKGND_SET)
						libtcod.console_put_char(con, x, y, WALL_LIGHT, libtcod.BKGND_NONE)
					else:
						#libtcod.console_set_char_background(con, x, y, colors.get('light_ground'), libtcod.BKGND_SET)
						libtcod.console_put_char(con, x, y, FLOOR_LIGHT, libtcod.BKGND_NONE)
					game_map.tiles[x][y].explored = True
				elif game_map.tiles[x][y].explored:
					if wall:
						#libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
						libtcod.console_put_char(con, x, y, WALL_DARK, libtcod.BKGND_NONE)
					else:
						#libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)
						libtcod.console_put_char(con, x, y, FLOOR_DARK, libtcod.BKGND_NONE)
	#draw all entities in the list
	entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)
	for entity in entities_in_render_order:
		draw_entity(con, entity, fov_map, game_map)

	libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

	libtcod.console_set_default_background(panel, libtcod.black)
	libtcod.console_clear(panel)

	# print the game messages, one line at a time
	y = 1
	for message in message_log.messages:
		libtcod.console_set_default_foreground(panel, message.color)
		libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
		y += 1

	render_bar(panel, 1, 1, bar_width, 'HP', player.stats.hp, player.stats.max_hp, libtcod.light_red, libtcod.darker_red)
	render_bar(panel, 1, 5, bar_width, 'Mana', player.caster.mana, player.caster.max_mana, libtcod.blue, libtcod.darker_blue)
	libtcod.console_print_ex(panel, 1, 8, libtcod.BKGND_NONE, libtcod.LEFT, 'Dungeon level: {0}'.format(game_map.dungeon_level))
	libtcod.console_print_ex(panel, 1, 8, libtcod.BKGND_NONE, libtcod.LEFT, f'GS: {game_state}')
	libtcod.console_print_ex(panel, 1, 10, libtcod.BKGND_NONE, libtcod.LEFT, 'Effects:')
	append_effects(panel, player, 11)
	libtcod.console_set_default_foreground(panel, libtcod.light_gray)
	libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse(mouse, entities, fov_map, player))

	libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)
	if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
		if game_state == GameStates.SHOW_INVENTORY:
			inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
		else:
			inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'
	
		inventory_menu(con, inventory_title, 50, screen_width, screen_height, player)

	elif game_state == GameStates.LEVEL_UP:
		level_up_menu(con, 'Level up! Choose a stat to raise:', player, 40, screen_width, screen_height)

	elif game_state == GameStates.CHARACTER_SCREEN:
		character_screen(player, 50, 10, screen_width, screen_height)

	elif game_state == GameStates.SPELLS_SCREEN:
		spells_menu(con, "Choose a spell to cast...", 50, screen_width, screen_height, player)

	elif game_state == GameStates.POTION_SCREEN:
		menu_title = "Choose a potion to quaff."
		potion_menu(con, menu_title, 50, screen_width, screen_height, player)

	elif game_state == GameStates.EQUIPMENT_SCREEN:
		menu_title = "Your currently equipped items."
		equipment_menu(con, menu_title, 50, screen_width, screen_height, player)

	elif game_state == GameStates.FEATS_SCREEN:
		menu_title = "Choose a feat to perform..."
		feats_menu(con, menu_title, 50, screen_width, screen_height, player)

def clear_all(con, entities):
	for entity in entities:
		clear_entity(con, entity)

def draw_entity(con, entity, fov_map, game_map):
	if libtcod.map_is_in_fov(fov_map, entity.x, entity.y) or (entity.stairs and game_map.tiles[entity.x][entity.y].explored):
		libtcod.console_set_default_foreground(con, entity.color)
		libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)
		libtcod.console_set_default_foreground(con, libtcod.white)

def clear_entity(con, entity):
	libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)

def append_effects(panel, player, starting_y):
	current_y = starting_y
	for effect in player.fighter.effect_list:
		libtcod.console_print_ex(panel, 1, current_y, libtcod.BKGND_NONE, libtcod.LEFT, effect.description)
		current_y += 1
		if current_y - starting_y == 5:
			break