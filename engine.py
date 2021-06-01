import tcod as libtcod
from input_handlers import handle_keys, handle_mouse, handle_main_menu
from loader_functions.initialize_new_game import get_game_variables
from loader_functions.constants import get_constants
from loader_functions.data_loaders import load_game, save_game
from entity import Entity
from render_functions import clear_all, render_all
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from death_functions import kill_monster, kill_player, handle_death
from game_messages import Message
from menus import main_menu, message_box
from dlevel import Dlevel
from spells import Spell
from components.equippable import make_dropped_missile
from components.consumable import get_carried_potions
import components.inventory
from systems import move_system
from systems import time_system
from systems import spell_system
from systems.pickup_system import pickup_item
from systems import input_process_system
from systems import results_process_system
from targeting import Targeting
from game_state import GameState
from character import get_character_class
from race import get_character_race

def main():
	constants = get_constants()
	#libtcod.console_set_custom_font('dejavu10x10_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
	libtcod.console_set_custom_font('res/tiles.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_CP437, 16, 24)
	libtcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], True, vsync=True)

	con = libtcod.console_new(constants['screen_width'], constants['screen_height'])
	panel = libtcod.console_new(constants['screen_width'], constants['panel_height'])

	show_main_menu = True
	show_load_error_message = False
	main_menu_background_image = libtcod.image_load('menu_bg.png')

	key = libtcod.Key()
	mouse = libtcod.Mouse()

	while not libtcod.console_is_window_closed():
		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

		if show_main_menu:
			main_menu(con, main_menu_background_image, constants['screen_width'], constants['screen_height'])
			if show_load_error_message:
				message_box(con, 'No save game to load', 50, constants['screen_width'], constants['screen_height'])

			libtcod.console_flush()
			action = handle_main_menu(key)
			new_game = action.get('new_game')
			load_saved_game = action.get('load_game')
			exit_game = action.get('exit')

			if show_load_error_message and (new_game or load_saved_game or exit_game):
				show_load_error_message = False
			elif new_game:
				character_race = get_character_race(con, constants)
				character_class = get_character_class(con, constants)
				player_class = character_class.get('player_class')
				player, entities, game_map, message_log, game_state, dlevels = get_game_variables(constants, player_class)
				game_state = GameStates.PLAYERS_TURN
				show_main_menu = False
			elif load_saved_game:
				try:
					player, entities, game_map, message_log, game_state, dlevels = load_game()
					show_main_menu = False
				except FileNotFoundError:
					show_load_error_message = True
			elif exit_game:
				break
		else:
			con.clear()
			play_game(player, entities, game_map, message_log, game_state, con, panel, constants, dlevels)
			show_main_menu = True

def play_game(player, entities, game_map, message_log, game_state, con, panel, constants, dlevels):
	fov_recompute = True
	fov_map = initialize_fov(game_map)
	key = libtcod.Key()
	mouse = libtcod.Mouse()
	game_state = GameState()
	action_free = True
	targets = Targeting()
	game_state.game_turn = 1
	while not libtcod.console_is_window_closed():
		while action_free:
			
			libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

			if fov_recompute:
				recompute_fov(fov_map, player.x, player.y, constants['fov_radius'], constants['fov_light_walls'], constants['fov_algorithm'])
			
			render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, constants['screen_width'], constants['screen_height'], constants['bar_width'], constants['panel_height'], constants['panel_y'], mouse, constants['colors'], game_state)
			fov_recompute = False

			libtcod.console_flush()
			clear_all(con, entities)
			
			action = handle_keys(key, game_state)
			mouse_action = handle_mouse(mouse)

			# It all happens here - start off by process the action / mouse action, to get player_turn_results list, plus update some game state, e.g. as a result of combat
			player_turn_results, fov_recompute, game_state, entities, game_map, fov_map, dlevels, targets = input_process_system.process_input(action, mouse_action, player, entities, game_state, message_log, game_map, dlevels, fov_recompute, fov_map, constants, con, targets)

			#now pass the player turn results along to be processed
			game_state, entities, player, targets, action_free = results_process_system.process_results(player_turn_results, game_state, entities, player, message_log, targets, action_free)

		player_turn_results = []
		player_turn_results.extend(time_system.process_entity_turn(player))
		game_state, entities, player, targets, action_free = results_process_system.process_results(player_turn_results, game_state, entities, player, message_log, targets, action_free)

		#now enemy chooses an action, process the results
		for entity in entities:
			if entity.ai:
				enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)
				entities, game_state, message_log = results_process_system.process_ai_results(enemy_turn_results, entity, entities, player, message_log, game_state)
		game_state.game_turn += 1
		# reset action_free to True to player gets a turn again
		action_free = True
		if game_state.current_game_state != GameStates.PLAYER_DEAD:
			game_state.current_game_state = GameStates.PLAYERS_TURN

if __name__ == "__main__":
	main()