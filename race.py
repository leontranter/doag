from menus import character_race_menu, main_menu
from input_handlers import handle_character_race_menu
import tcod as libtcod

def get_character_race(con, constants):
	key = libtcod.Key()
	mouse = libtcod.Mouse()
	character_race = None
	while not character_race:
		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
		character_race_menu(con, constants['screen_width'], constants['screen_height'])
		libtcod.console_flush()
		character_race = handle_character_race_menu(key)
	return character_race