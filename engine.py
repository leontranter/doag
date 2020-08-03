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

def main():
	constants = get_constants()
	#libtcod.console_set_custom_font('dejavu10x10_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
	libtcod.console_set_custom_font('res/tiles.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_CP437, 16, 24)
	libtcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False)

	con = libtcod.console_new(constants['screen_width'], constants['screen_height'])
	panel = libtcod.console_new(constants['screen_width'], constants['panel_height'])

	#idx = 256
	#for y in range(16, 24):
#		libtcod.console_map_ascii_codes_to_font(idx, 16, 0, y)
#		idx += 16

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
				message_box(con, 'No save gam to load', 50, constants['screen_width'], constants['screen_height'])

			libtcod.console_flush()
			action = handle_main_menu(key)
			new_game = action.get('new_game')
			load_saved_game = action.get('load_game')
			exit_game = action.get('exit')

			if show_load_error_message and (new_game or load_saved_game or exit_game):
				show_load_error_message = False
			elif new_game:
				player, entities, game_map, message_log, game_state, dlevels = get_game_variables(constants, start_equipped=True)
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
			libtcod.console_clear(con)
			play_game(player, entities, game_map, message_log, game_state, con, panel, constants, dlevels)
			show_main_menu = True

def play_game(player, entities, game_map, message_log, game_state, con, panel, constants, dlevels):
	fov_recompute = True
	fov_map = initialize_fov(game_map)

	key = libtcod.Key()
	mouse = libtcod.Mouse()

	game_state = GameStates.PLAYERS_TURN
	previous_game_state = game_state
	action_free = True
	targets = Targeting()

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
			player_turn_results, fov_recompute, game_state, previous_game_state, entities, game_map, fov_map, dlevels, targets, action_free = input_process_system.process_input(action, mouse_action, player, entities, game_state, previous_game_state, message_log, game_map, dlevels, fov_recompute, fov_map, constants, con, action_free, targets)

			#now pass the player turn results along to be processed
			game_state, previous_game_state, entities, player, targets = results_process_system.process_results(player_turn_results, game_state, previous_game_state, entities, player, message_log, targets)

		player_turn_results = []
		player_turn_results.extend(time_system.process_entity_turn(player))
		game_state, previous_game_state, entities, player, targets = results_process_system.process_results(player_turn_results, game_state, previous_game_state, entities, player, message_log, targets)

		#now enemy chooses an action, process the results
		for entity in entities:
			if entity.ai:
				enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)
				entities, game_state, message_log = results_process_system.process_ai_results(enemy_turn_results, entity, entities, player, message_log, game_state)
		
		# reset action_free to True to player gets a turn again
		action_free = True
		print("resetting game state")
		game_state = GameStates.PLAYERS_TURN

if __name__ == "__main__":
	main()