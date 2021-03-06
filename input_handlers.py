import tcod as libtcod
from game_states import GameStates

def handle_keys(key, game_state):
	if game_state.current_game_state == GameStates.PLAYERS_TURN:
		return handle_player_turn_keys(key)
	elif game_state.current_game_state == GameStates.PLAYER_DEAD:
		return handle_player_dead_keys(key)
	elif game_state.current_game_state == GameStates.TARGETING:
		return handle_targeting_keys(key)
	elif game_state.current_game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
		return handle_inventory_keys(key)
	elif game_state.current_game_state == GameStates.LEVEL_UP:
		return handle_level_up_menu(key)
	elif game_state.current_game_state == GameStates.CHARACTER_SCREEN:
		return handle_character_screen(key)
	elif game_state.current_game_state == GameStates.SPELLS_SCREEN:
		return handle_spells_screen(key)
	elif game_state.current_game_state == GameStates.POTION_SCREEN:
		return handle_potions_menu(key)
	elif game_state.current_game_state == GameStates.EQUIPMENT_SCREEN:
		return handle_equipment_menu(key)
	elif game_state.current_game_state == GameStates.FEATS_SCREEN:
		return handle_feats_screen(key)
	elif game_state.current_game_state == GameStates.SKILLS_SCREEN:
		return handle_skills_screen(key)
	return {}

def handle_player_turn_keys(key):
	key_char = chr(key.c)
	# Movement keys
	if key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
		return {'move': (0, -1)}
	elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
		return {'move': (0, 1)}
	elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP4:
		return {'move': (-1, 0)}
	elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP6:
		return {'move': (1, 0)}
	elif key.vk == libtcod.KEY_KP7:
		return {'move': (-1,-1)}
	elif key.vk == libtcod.KEY_KP9:
		return {'move': (1, -1)}
	elif key.vk == libtcod.KEY_KP1:
		return {'move': (-1, 1)}
	elif key.vk == libtcod.KEY_KP3:
		return {'move': (1, 1)}
	elif key_char == 'z':
		return {'wait': True}
	if key_char == 'g':
		return {'pickup': True}
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		return {'fullscreen': True}
	elif key_char == 'i':
		return {'show_inventory': True}
	elif key_char == 'd':
		return {'drop_inventory': True}
	elif key_char == 'x':
		return {'take_stairs': True}
	elif key_char == 'u':
		return {'take_stairs_up': True}
	elif key_char == 'c':
		return {'show_character_screen': True}
	elif key_char == 'e':
		return {'show_equipment_screen': True}
	elif key_char == 'k':
		return {'show_spells_screen': True}
	elif key_char == 'f':
		return {'fire_weapon': True}
	elif key_char == 'l':
		return {'load_weapon': True}
	elif key_char == 'q':
		return {'quaff_potion': True}
	elif key_char == 'p':
		return {'perform_feat': True}
	elif key_char == 's':
		return {'show_skills_screen': True}
	elif key.vk == libtcod.KEY_ESCAPE:
		#exit the game
		return {'exit': True}
	return {}

def handle_inventory_keys(key):
	index = key.c - ord('a')
	if index >= 0:
		return {'inventory_index': index}
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		return {'fullscreen': True}
	elif key.vk == libtcod.KEY_ESCAPE:
		return {'exit': True}
	return {}

def handle_player_dead_keys(key):
	key_char = chr(key.c)
	if key_char == 'i':
		return {'show_inventory': True}
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		# Alt Enter is toggle full screen
		return {'fullscreen': True}
	elif key.vk == libtcod.KEY_ESCAPE:
		return {'exit': True}
	return {}

def handle_targeting_keys(key):
	if key.vk == libtcod.KEY_ESCAPE:
		return {'exit': True}
	return {}

def handle_mouse(mouse):
	(x, y) = (mouse.cx, mouse.cy)
	if mouse.lbutton_pressed:
		return {'left_click': (x, y)}
	elif mouse.rbutton_pressed:
		return {'right_click': (x, y)}
	return {}

def handle_main_menu(key):
	key_char = chr(key.c)
	if key_char == 'a':
		return {'new_game': True}
	elif key_char == 'b':
		return {'load_game': True}
	elif key_char == 'c' or key.vk == libtcod.KEY_ESCAPE:
		return {'exit': True}
	return {}

def handle_level_up_menu(key):
	if key:
		key_char = chr(key.c)
		if key_char == 'a':
			return {'level_up': 'hp'}
		elif key_char == 'b':
			return {'level_up': 'str'}
		elif key_char == 'c':
			return {'level_up': 'def'}
	return {}

def handle_character_screen(key):
	if key.vk == libtcod.KEY_ESCAPE:
		return {'exit': True}
	return {}

def handle_skills_screen(key):
	if key.vk == libtcod.KEY_ESCAPE:
		return {'exit': True}
	return {}

def handle_spells_screen(key):
	index = key.c - ord('a')
	if index >= 0:
		return {'spells_index': index}
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		return {'fullscreen': True}
	elif key.vk == libtcod.KEY_ESCAPE:
		return {'exit': True}
	return {}

def handle_potions_menu(key):
	index = key.c - ord('a')
	if index >= 0:
		return {'potion_index': index}
	elif key.vk == libtcod.KEY_ENTER and key.lalt:
		return {'fullscreen': True}
	elif key.vk == libtcod.KEY_ESCAPE:
		return {'exit': True}
	return {}

def handle_equipment_menu(key):
	index = key.c - ord('a')
	if index >= 0:
		return {'equipment_index': index}
	elif key.vk == libtcod.KEY_ENTER and key.lalt:
		return {'fullscreen': True}
	elif key.vk == libtcod.KEY_ESCAPE:
		return {'exit': True}
	return {}

def handle_feats_screen(key):
	index = key.c - ord('a')
	if index >= 0:
		return {'feat_index': index}
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		return {'fullscreen': True}
	elif key.vk == libtcod.KEY_ESCAPE:
		return {'exit': True}
	return {}

def handle_character_class_menu(key):
	index = key.c - ord('a')
	if index >= 0:
		return {'player_class': index}
	elif key.vk == libtcod.KEY_ENTER and key.lalt:
		return {'fullscreen': True}
	elif key.vk == libtcod.KEY_ESCAPE:
		return {'exit': True}
	return {}

def handle_character_race_menu(key):
	index = key.c - ord('a')
	if index >= 0:
		return {'player_class': index}
	elif key.vk == libtcod.KEY_ENTER and key.lalt:
		return {'fullscreen': True}
	elif key.vk == libtcod.KEY_ESCAPE:
		return {'exit': True}
	return {}